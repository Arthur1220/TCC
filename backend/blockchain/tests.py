from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User
from animal.models import Animal, IdentificationType, Specie, Breed, Status as AnimalStatus, Gender
from event.models import Event, EventType
from .models import BlockchainStatus, Blockchain

class BlockchainTestCase(APITestCase):
    def setUp(self):
        # Criar usuário
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Criar tipos relacionados a animais
        self.gender = Gender.objects.create(name="Macho", description="Animal do sexo masculino.")
        self.identification_type = IdentificationType.objects.create(name="Brinco")
        self.specie = Specie.objects.create(name="Bovino")
        self.breed = Breed.objects.create(name="Nelore", specie=self.specie)
        self.animal_status = AnimalStatus.objects.create(name="Ativo", description="Animal ativo no sistema.")

        # Criar animal
        self.animal = Animal.objects.create(
            identification_type=self.identification_type,
            identification="123456",
            birth_date="2022-01-01",
            breed=self.breed,
            status=self.animal_status,
            owner=self.user,
            gender=self.gender
        )

        # Criar tipo de evento
        self.event_type = EventType.objects.create(name="Vacinação", description="Evento de vacinação.")

        # Criar evento
        self.event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Vacina aplicada",
            recorded_by=self.user
        )

        # Criar status
        self.blockchain_status = BlockchainStatus.objects.create(name="Confirmada", description="Transação confirmada com sucesso na blockchain.")

        # URLs
        self.blockchain_register_url = '/blockchain/blockchain-register/'
        self.blockchain_get_url = '/blockchain/blockchain-get/'
        self.status_url = '/blockchain/status/'

    def test_create_status(self):
        data = {"name": "Pendente", "description": "Transação aguardando confirmação na blockchain."}
        response = self.client.post(self.status_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_get_status(self):
        response = self.client.get(f"{self.status_url}{self.blockchain_status.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.blockchain_status.name)

    def test_create_blockchain(self):
        data = {
            "animal": self.animal.id,
            "event": self.event.id,
            "transaction_hash": "abc123hash",
            "owner": self.user.id,
            "status": self.blockchain_status.id
        }
        response = self.client.post(self.blockchain_register_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction_hash'], data['transaction_hash'])

    def test_get_blockchains(self):
        blockchain = Blockchain.objects.create(
            animal=self.animal,
            event=self.event,
            transaction_hash="abc123hash",
            owner=self.user,
            status=self.blockchain_status
        )
        response = self.client.get(self.blockchain_get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_blockchain(self):
        blockchain = Blockchain.objects.create(
            animal=self.animal,
            event=self.event,
            transaction_hash="abc123hash",
            owner=self.user,
            status=self.blockchain_status
        )
        update_data = {"status": self.blockchain_status.id}
        response = self.client.put(f'/blockchain/blockchain-update/{blockchain.id}/', data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_blockchain(self):
        blockchain = Blockchain.objects.create(
            animal=self.animal,
            event=self.event,
            transaction_hash="abc123hash",
            owner=self.user,
            status=self.blockchain_status
        )
        response = self.client.delete(f'/blockchain/blockchain-delete/{blockchain.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Blockchain deleted")
