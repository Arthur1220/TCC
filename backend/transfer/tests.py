from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from animal.models import Animal, Specie, Breed, Gender, Status as AnimalStatus, IdentificationType, AnimalGroup

# Obtenha o modelo User do seu projeto
User = get_user_model()

class OwnershipTransferRequestAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Criar Usuários
        cls.user_a = User.objects.create_user(username='usera', password='password123')
        cls.user_b = User.objects.create_user(username='userb', password='password123')
        cls.user_c = User.objects.create_user(username='userc', password='password123')

        # Criar dados de lookup para Animais (simplificado)
        cls.specie1 = Specie.objects.create(name='Bovino')
        cls.breed1 = Breed.objects.create(name='Nelore', specie=cls.specie1)
        cls.gender_male = Gender.objects.create(name='Macho')
        cls.id_type1 = IdentificationType.objects.create(name='Brinco')
        
        # Status dos Animais (importante para validação no serializer)
        cls.status_active = AnimalStatus.objects.create(name='Ativo') # Permite transferência
        cls.status_sold = AnimalStatus.objects.create(name='Vendido') # Não permite transferência (exemplo)

        # Animais para User A
        cls.animal1_a = Animal.objects.create(
            identification='A001', owner=cls.user_a, breed=cls.breed1,
            gender=cls.gender_male, status=cls.status_active, identification_type=cls.id_type1
        )
        cls.animal2_a = Animal.objects.create(
            identification='A002', owner=cls.user_a, breed=cls.breed1,
            gender=cls.gender_male, status=cls.status_active, identification_type=cls.id_type1
        )
        cls.animal3_a_sold = Animal.objects.create( # Animal que não pode ser transferido
            identification='A003', owner=cls.user_a, breed=cls.breed1,
            gender=cls.gender_male, status=cls.status_sold, identification_type=cls.id_type1
        )
        
        # Animal para User B (para testar que User A não pode transferi-lo)
        cls.animal1_b = Animal.objects.create(
            identification='B001', owner=cls.user_b, breed=cls.breed1,
            gender=cls.gender_male, status=cls.status_active, identification_type=cls.id_type1
        )

        # URLs (definidas aqui para fácil acesso)
        cls.create_request_url = reverse('transfer-request-create')
        cls.list_sent_url = reverse('transfer-request-list-sent')
        cls.list_received_url = reverse('transfer-request-list-received')
        # Para URLs com PK, usaremos args=[pk] em reverse() dentro dos testes

    def test_create_transfer_request_success(self):
        self.client.force_authenticate(user=self.user_a)
        data = {
            'animals': [self.animal1_a.pk, self.animal2_a.pk],
            'requested_to_id': self.user_b.pk,
            'initiator_notes': 'Por favor, aceite.'
        }
        response = self.client.post(self.create_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING_APPROVAL')
        self.assertEqual(response.data['initiated_by'], self.user_a.pk)
        self.assertEqual(response.data['requested_to'], self.user_b.pk)
        self.assertIn(self.animal1_a.pk, [animal['id'] for animal in response.data['animals_details']])
        self.assertIn(self.animal2_a.pk, [animal['id'] for animal in response.data['animals_details']])

    def test_create_transfer_request_unauthenticated(self):
        data = {
            'animals': [self.animal1_a.pk],
            'requested_to_id': self.user_b.pk,
        }
        response = self.client.post(self.create_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_transfer_request_animal_not_owned(self):
        self.client.force_authenticate(user=self.user_a)
        data = {
            'animals': [self.animal1_b.pk], # Animal de User B
            'requested_to_id': self.user_c.pk
        }
        response = self.client.post(self.create_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('não pertence a você', str(response.data['animals']))


    def test_create_transfer_request_animal_invalid_status(self):
        self.client.force_authenticate(user=self.user_a)
        data = {
            'animals': [self.animal3_a_sold.pk], # Animal com status 'Vendido'
            'requested_to_id': self.user_b.pk
        }
        response = self.client.post(self.create_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('não permite transferência', str(response.data['animals']))

    def test_create_transfer_request_to_self(self):
        self.client.force_authenticate(user=self.user_a)
        data = {
            'animals': [self.animal1_a.pk],
            'requested_to_id': self.user_a.pk # Transferindo para si mesmo
        }
        response = self.client.post(self.create_request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('não pode solicitar uma transferência para si mesmo', str(response.data['requested_to_id']))

    def test_list_sent_requests(self):
        self.client.force_authenticate(user=self.user_a)
        # User A cria uma requisição para User B
        self.client.post(self.create_request_url, {'animals': [self.animal1_a.pk], 'requested_to_id': self.user_b.pk}, format='json')
        
        response = self.client.get(self.list_sent_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['initiated_by'], self.user_a.pk)

    def test_list_received_requests_pending_approval(self):
        self.client.force_authenticate(user=self.user_a)
        # User A cria uma requisição para User B
        self.client.post(self.create_request_url, {'animals': [self.animal1_a.pk], 'requested_to_id': self.user_b.pk}, format='json')
        
        self.client.force_authenticate(user=self.user_b) # Agora como User B
        response = self.client.get(self.list_received_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['requested_to'], self.user_b.pk)
        self.assertEqual(response.data[0]['status'], 'PENDING_APPROVAL')

    def test_retrieve_request_by_initiator_and_recipient(self):
        self.client.force_authenticate(user=self.user_a)
        create_response = self.client.post(self.create_request_url, {'animals': [self.animal1_a.pk], 'requested_to_id': self.user_b.pk}, format='json')
        request_id = create_response.data['id']
        detail_url = reverse('transfer-request-retrieve', args=[request_id])

        # Teste pelo solicitante (User A)
        response_a = self.client.get(detail_url)
        self.assertEqual(response_a.status_code, status.HTTP_200_OK)
        self.assertEqual(response_a.data['id'], request_id)

        # Teste pelo destinatário (User B)
        self.client.force_authenticate(user=self.user_b)
        response_b = self.client.get(detail_url)
        self.assertEqual(response_b.status_code, status.HTTP_200_OK)
        self.assertEqual(response_b.data['id'], request_id)

        # Teste por outro usuário (User C) - deve falhar
        self.client.force_authenticate(user=self.user_c)
        response_c = self.client.get(detail_url)
        self.assertEqual(response_c.status_code, status.HTTP_403_FORBIDDEN)

    def _create_pending_request(self):
        """Helper para criar uma requisição pendente de User A para User B."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post(
            self.create_request_url,
            {'animals': [self.animal1_a.pk, self.animal2_a.pk], 'requested_to_id': self.user_b.pk},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def test_cancel_request_success_by_initiator(self):
        request_id = self._create_pending_request()
        cancel_url = reverse('transfer-request-cancel', args=[request_id])
        
        self.client.force_authenticate(user=self.user_a) # Solicitante
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Solicitação cancelada com sucesso.')
        
        # Verificar o status no BD
        detail_url = reverse('transfer-request-retrieve', args=[request_id])
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.data['status'], 'CANCELLED_BY_INITIATOR')

    def test_cancel_request_fail_by_recipient(self):
        request_id = self._create_pending_request()
        cancel_url = reverse('transfer-request-cancel', args=[request_id])

        self.client.force_authenticate(user=self.user_b) # Destinatário não pode cancelar
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_request_success_by_recipient(self):
        request_id = self._create_pending_request()
        reject_url = reverse('transfer-request-reject', args=[request_id])
        
        self.client.force_authenticate(user=self.user_b) # Destinatário
        data = {'recipient_notes': 'Não tenho interesse no momento.'}
        response = self.client.post(reject_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Solicitação rejeitada com sucesso.')

        # Verificar o status e notas no BD
        self.client.force_authenticate(user=self.user_a) # Voltar para User A para poder ver os detalhes
        detail_url = reverse('transfer-request-retrieve', args=[request_id])
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.data['status'], 'REJECTED')
        self.assertEqual(detail_response.data['recipient_notes'], 'Não tenho interesse no momento.')

    def test_reject_request_fail_by_initiator(self):
        request_id = self._create_pending_request()
        reject_url = reverse('transfer-request-reject', args=[request_id])

        self.client.force_authenticate(user=self.user_a) # Solicitante não pode rejeitar
        response = self.client.post(reject_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_and_process_request_success(self):
        request_id = self._create_pending_request() # animal1_a e animal2_a
        approve_url = reverse('transfer-request-approve', args=[request_id])

        # Checar proprietários antes
        self.assertEqual(Animal.objects.get(pk=self.animal1_a.pk).owner, self.user_a)
        self.assertEqual(Animal.objects.get(pk=self.animal2_a.pk).owner, self.user_a)
        # Criar grupo para user_a para animal1_a para testar se fica None
        group_a = AnimalGroup.objects.create(name="Grupo User A", owner=self.user_a)
        self.animal1_a.group = group_a
        self.animal1_a.save()

        self.client.force_authenticate(user=self.user_b) # Destinatário aprova
        data = {'recipient_notes': 'Aprovado!'}
        response = self.client.post(approve_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['recipient_notes'], 'Aprovado!')
        self.assertIsNotNone(response.data['action_date'])
        self.assertIsNotNone(response.data['completion_date'])

        # Verificar mudança de proprietário e grupo no BD
        animal1_updated = Animal.objects.get(pk=self.animal1_a.pk)
        animal2_updated = Animal.objects.get(pk=self.animal2_a.pk)
        self.assertEqual(animal1_updated.owner, self.user_b)
        self.assertEqual(animal2_updated.owner, self.user_b)
        self.assertIsNone(animal1_updated.group) # Deve ser None
        self.assertIsNone(animal2_updated.group) # Já era None, continua None

    def test_approve_request_fail_by_initiator(self):
        request_id = self._create_pending_request()
        approve_url = reverse('transfer-request-approve', args=[request_id])

        self.client.force_authenticate(user=self.user_a) # Solicitante não pode aprovar
        response = self.client.post(approve_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_request_fail_if_status_not_pending(self):
        request_id = self._create_pending_request()
        
        # Mudar status para REJECTED primeiro
        self.client.force_authenticate(user=self.user_b)
        reject_url = reverse('transfer-request-reject', args=[request_id])
        self.client.post(reject_url, {}, format='json')

        # Tentar aprovar
        approve_url = reverse('transfer-request-approve', args=[request_id])
        response = self.client.post(approve_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('não pode mais ser aprovada', response.data['error'])

    def test_approve_request_fail_if_animal_owner_changed_mid_process(self):
        request_id = self._create_pending_request() 
        
        animal_obj_1 = Animal.objects.get(pk=self.animal1_a.pk)
        original_owner_animal1 = animal_obj_1.owner
        
        animal_obj_1.owner = self.user_c 
        animal_obj_1.save()

        approve_url = reverse('transfer-request-approve', args=[request_id])
        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(approve_url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Esperar 400 em vez de 500
        self.assertIn('mudou. Proprietário esperado', str(response.data['error'])) # Verifica a mensagem de erro
        
        updated_request = self.get_object_model(request_id)
        self.assertEqual(updated_request.status, 'ERROR_PROCESSING')

        self.assertEqual(Animal.objects.get(pk=self.animal1_a.pk).owner, self.user_c)
        self.assertEqual(Animal.objects.get(pk=self.animal2_a.pk).owner, original_owner_animal1)

    @classmethod
    def get_object_model(cls, pk): # Helper para pegar o objeto do modelo diretamente
        from transfer.models import OwnershipTransferRequest as OTR_MODEL # Evitar import no topo da classe
        return OTR_MODEL.objects.get(pk=pk)