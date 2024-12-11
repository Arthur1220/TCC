from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from animal.models import Animal, Species, Breed, Status, IdentificationType, Gender
from .models import EventType, Event

User = get_user_model()

class EventTestCase(APITestCase):
    def setUp(self):
        # Criar usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Criar objetos relacionados
        self.species = Species.objects.create(name="Bovinos")
        self.breed = Breed.objects.create(name="Nelore", species=self.species)
        self.status = Status.objects.create(name="Ativo", description="Animal ativo")
        self.gender = Gender.objects.create(name="Macho", description="Animal do sexo masculino")
        self.identification_type = IdentificationType.objects.create(name="Brinco")

        # Criar animal para teste
        self.animal = Animal.objects.create(
            identification_type=self.identification_type,
            identification="123456",
            birth_date="2022-01-01",
            species=self.species,
            breed=self.breed,
            status=self.status,
            owner=self.user,
            gender=self.gender
        )

        # Criar tipo de evento
        self.event_type = EventType.objects.create(name="Vacinação", description="Evento de vacinação")

        # URLs
        self.event_type_url = '/event/event-type/'
        self.event_url = '/event/event-register/'

    def test_create_event_type(self):
        data = {
            "name": "Medicação",
            "description": "Evento de medicação"
        }
        response = self.client.post(self.event_type_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_get_event_types(self):
        response = self.client.get(self.event_type_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_event(self):
        data = {
            "animal": self.animal.id,
            "event_type": self.event_type.id,
            "event_date": "2023-12-10T10:00:00Z",
            "location": "Fazenda Modelo",
            "observations": "Aplicação de vacina antirrábica",
            "recorded_by": self.user.id
        }
        response = self.client.post(self.event_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['location'], data['location'])

    def test_get_events(self):
        # Criar um evento
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            event_date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )

        response = self.client.get('/event/event-get/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_event(self):
        # Criar um evento
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            event_date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )

        update_data = {
            "location": "Nova Fazenda Modelo",
            "observations": "Vacina reforço aplicada"
        }

        response = self.client.put(f'/event/event-update/{event.id}/', data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], update_data['location'])

    def test_delete_event(self):
        # Criar um evento
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            event_date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )

        response = self.client.delete(f'/event/event-delete/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Event deleted')
