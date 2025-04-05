from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from animal.models import Animal, Specie, Breed, Status, IdentificationType, Gender
from event.models import EventType, Event, Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences
from property.models import Property

User = get_user_model()

class BaseEventTestCase(APITestCase):
    def setUp(self):
        # Criação do usuário e autenticação
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        
        # Criação de objetos do app animal
        self.specie = Specie.objects.create(name="Bovinos")
        self.breed = Breed.objects.create(name="Nelore", specie=self.specie)
        self.animal_status = Status.objects.create(name="Ativo", description="Animal ativo")
        self.gender = Gender.objects.create(name="Macho", description="Animal do sexo masculino")
        self.identification_type = IdentificationType.objects.create(name="Brinco")
        self.animal = Animal.objects.create(
            identification_type=self.identification_type,
            identification="123456",
            birth_date="2022-01-01",
            breed=self.breed,
            status=self.animal_status,
            owner=self.user,
            gender=self.gender
        )
        
        # Criação de objetos do app event
        self.event_type = EventType.objects.create(name="Vacinação", description="Evento de vacinação")
        
        # Criação de propriedades para testes de Movement
        self.property1 = Property.objects.create(
            name="Fazenda 1", address="Rua 1", city="Cidade", state="Estado", zip_code="00000", owner=self.user
        )
        self.property2 = Property.objects.create(
            name="Fazenda 2", address="Rua 2", city="Cidade", state="Estado", zip_code="11111", owner=self.user
        )

# Testes para EventType
class EventTypeTestCase(BaseEventTestCase):
    def test_create_event_type(self):
        url = '/event/event-type/'
        data = {"name": "Medicação", "description": "Evento de medicação"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_get_event_types(self):
        url = '/event/event-type/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

# Testes para Event
class EventTestCase(BaseEventTestCase):
    def test_create_event(self):
        url = '/event/event-register/'
        data = {
            "animal": self.animal.id,
            "event_type": self.event_type.id,
            "date": "2023-12-10T10:00:00Z",  # use "date" e não "event_date"
            "location": "Fazenda Modelo",
            "observations": "Aplicação de vacina antirrábica"
            # 'recorded_by' será setado automaticamente pelo view (via request.user)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["location"], data["location"])

    def test_get_events(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )
        url = '/event/event-get/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_event(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )
        url = f'/event/event-update/{event.id}/'
        update_data = {"location": "Nova Fazenda Modelo", "observations": "Vacina reforço aplicada"}
        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], update_data["location"])

    def test_delete_event(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Aplicação de vacina antirrábica",
            recorded_by=self.user
        )
        url = f'/event/event-delete/{event.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Event deleted")

# Testes para Movement
class MovementTestCase(BaseEventTestCase):
    def test_register_movement(self):
        # Crie um evento para o movimento
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Movement",
            recorded_by=self.user
        )
        url = '/event/movement-register/'
        data = {
            "event": event.id,
            "origin_property": self.property1.id,
            "destination_property": self.property2.id,
            "date": "2023-12-11T10:00:00Z",
            "reason": "Test movement"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reason"], data["reason"])

    def test_get_movement(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Movement",
            recorded_by=self.user
        )
        movement = Movement.objects.create(
            event=event,
            origin_property=self.property1,
            destination_property=self.property2,
            date="2023-12-11T10:00:00Z",
            reason="Test movement"
        )
        url = f'/event/movement-get/{movement.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["reason"], "Test movement")

# Testes para Weighing
class WeighingTestCase(BaseEventTestCase):
    def test_register_weighing(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Weighing",
            recorded_by=self.user
        )
        url = '/event/weighing-register/'
        data = {
            "event": event.id,
            "weight": "250.50",
            "date": "2023-12-10T12:00:00Z"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["weight"], "250.50")

    def test_get_weighing(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Weighing",
            recorded_by=self.user
        )
        weighing = Weighing.objects.create(
            event=event,
            weight="250.50",
            date="2023-12-10T12:00:00Z"
        )
        url = f'/event/weighing-get/{weighing.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weight"], "250.50")

# Testes para Vacine
class VacineTestCase(BaseEventTestCase):
    def test_register_vacine(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Vacine",
            recorded_by=self.user
        )
        url = '/event/vacine-register/'
        data = {
            "event": event.id,
            "name": "Vacina X",
            "manufacturer": "Fabricante Y",
            "batch": "Lote Z",
            "validity": "2024-12-31",
            "dose": "2.5",
            "next_dose_date": "2024-01-01T10:00:00Z"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Vacina X")

# Testes para Medicine
class MedicineTestCase(BaseEventTestCase):
    def test_register_medicine(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Medicine",
            recorded_by=self.user
        )
        url = '/event/medicine-register/'
        data = {
            "event": event.id,
            "name": "Medicine A",
            "manufacturer": "Manufacturer B",
            "batch": "Batch C",
            "validity": "2024-12-31",
            "dose": "1.5",
            "next_dose_date": "2024-01-01T10:00:00Z",
            "reason": "For treatment",
            "withdrawal_time": 5
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Medicine A")

# Testes para Reproduction
class ReproductionTestCase(BaseEventTestCase):
    def test_register_reproduction(self):
        # Criar dois animais para reprodução
        male_animal = Animal.objects.create(
            identification_type=self.identification_type,
            identification="MALE123",
            birth_date="2022-01-01",
            breed=self.breed,
            status=self.animal_status,
            owner=self.user,
            gender=self.gender
        )
        female_animal = Animal.objects.create(
            identification_type=self.identification_type,
            identification="FEMALE123",
            birth_date="2022-01-01",
            breed=self.breed,
            status=self.animal_status,
            owner=self.user,
            gender=self.gender
        )
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Reproduction",
            recorded_by=self.user
        )
        url = '/event/reproduction-register/'
        data = {
            "event": event.id,
            "reproduction_type": "natural",
            "male_id": male_animal.id,
            "female_id": female_animal.id,
            "date": "2023-12-11T10:00:00Z",
            "result": "positive"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["result"], "positive")

# Testes para Slaughter
class SlaughterTestCase(BaseEventTestCase):
    def test_register_slaughter(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Slaughter",
            recorded_by=self.user
        )
        url = '/event/slaughter-register/'
        data = {
            "event": event.id,
            "date": "2023-12-11T10:00:00Z",
            "location": "Local A",
            "final_weight": "300.00",
            "inspection_result": "passed"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["inspection_result"], "passed")

# Testes para SpecialOccurrences
class SpecialOccurrencesTestCase(BaseEventTestCase):
    def test_register_special_occurrence(self):
        event = Event.objects.create(
            animal=self.animal,
            event_type=self.event_type,
            date="2023-12-10T10:00:00Z",
            location="Fazenda Modelo",
            observations="Test Special Occurrence",
            recorded_by=self.user
        )
        url = '/event/special-occurrences-register/'
        data = {
            "event": event.id,
            "occurrence_type": "Accident",
            "description": "Test occurrence",
            "date": "2023-12-11T10:00:00Z",
            "actions_taken": "Action taken"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["occurrence_type"], "Accident")
