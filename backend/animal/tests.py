# animal/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Sex, Status, Species, Breed, Animal
from user.models import User

class SexAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sex_url = reverse('register')
        self.get_sex_url = reverse('get')
        self.delete_sex_url = lambda pk: reverse('delete', args=[pk])
        self.sex_data = {
            'name': 'Male',
            'description': 'Macho',
        }

    def test_register_sex(self):
        response = self.client.post('/registerSex/', self.sex_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sex.objects.count(), 1)
        self.assertEqual(Sex.objects.get().name, 'Male')

    def test_get_sex_list(self):
        Sex.objects.create(**self.sex_data)
        response = self.client.get('/getSex/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Male')

    def test_get_single_sex(self):
        sex = Sex.objects.create(**self.sex_data)
        response = self.client.get(f'/getSex/{sex.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Male')

    def test_delete_sex(self):
        sex = Sex.objects.create(**self.sex_data)
        response = self.client.delete(f'/deleteSex/{sex.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sex.objects.count(), 0)

    def test_delete_nonexistent_sex(self):
        response = self.client.delete('/deleteSex/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

class StatusAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.status_url = reverse('register')
        self.get_status_url = reverse('get')
        self.delete_status_url = lambda pk: reverse('delete', args=[pk])
        self.status_data = {
            'name': 'active',
            'description': 'Ativo',
        }

    def test_register_status(self):
        response = self.client.post('/registerStatus/', self.status_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(Status.objects.get().name, 'active')

    def test_get_status_list(self):
        Status.objects.create(**self.status_data)
        response = self.client.get('/getStatus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'active')

    def test_get_single_status(self):
        status_obj = Status.objects.create(**self.status_data)
        response = self.client.get(f'/getStatus/{status_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'active')

    def test_delete_status(self):
        status_obj = Status.objects.create(**self.status_data)
        response = self.client.delete(f'/deleteStatus/{status_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 0)

    def test_delete_nonexistent_status(self):
        response = self.client.delete('/deleteStatus/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

class SpeciesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.species_url = reverse('register')
        self.get_species_url = reverse('get')
        self.delete_species_url = lambda pk: reverse('delete', args=[pk])
        self.species_data = {
            'name': 'cow',
            'description': 'Vaca',
        }

    def test_register_species(self):
        response = self.client.post('/registerSpecies/', self.species_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Species.objects.count(), 1)
        self.assertEqual(Species.objects.get().name, 'cow')

    def test_get_species_list(self):
        Species.objects.create(**self.species_data)
        response = self.client.get('/getSpecies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'cow')

    def test_get_single_species(self):
        species = Species.objects.create(**self.species_data)
        response = self.client.get(f'/getSpecies/{species.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'cow')

    def test_delete_species(self):
        species = Species.objects.create(**self.species_data)
        response = self.client.delete(f'/deleteSpecies/{species.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Species.objects.count(), 0)

    def test_delete_nonexistent_species(self):
        response = self.client.delete('/deleteSpecies/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

class BreedAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.breed_url = reverse('register')
        self.get_breed_url = reverse('get')
        self.delete_breed_url = lambda pk: reverse('delete', args=[pk])
        self.species = Species.objects.create(name='cow', description='Vaca')
        self.breed_data = {
            'name': 'nelore',
            'description': 'Nelore',
        }

    def test_register_breed(self):
        response = self.client.post('/registerBreed/', self.breed_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.count(), 1)
        self.assertEqual(Breed.objects.get().name, 'nelore')

    def test_get_breed_list(self):
        Breed.objects.create(**self.breed_data)
        response = self.client.get('/getBreed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'nelore')

    def test_get_single_breed(self):
        breed = Breed.objects.create(**self.breed_data)
        response = self.client.get(f'/getBreed/{breed.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'nelore')

    def test_delete_breed(self):
        breed = Breed.objects.create(**self.breed_data)
        response = self.client.delete(f'/deleteBreed/{breed.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.count(), 0)

    def test_delete_nonexistent_breed(self):
        response = self.client.delete('/deleteBreed/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

class AnimalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criação de um usuário para atribuir como owner
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            cpf='12345678901',
            password='testpassword'
        )
        
        # Criação das instâncias necessárias para Animal
        self.sex = Sex.objects.create(name='Male', description='Macho')
        self.status = Status.objects.create(name='active', description='Ativo')
        self.species = Species.objects.create(name='cow', description='Vaca')
        self.breed = Breed.objects.create(name='nelore', description='Nelore')
        
        # Dados para criação de Animal
        self.animal_data = {
            'name': 'Boi Bravo',
            'identification': 'BR12345',
            'born_date': '2020-01-01',
            'sex': self.sex.id,
            'status': self.status.id,
            'species': self.species.id,
            'breed': self.breed.id,
            # 'lote': None  # Opcional, pode ser adicionado conforme necessário
        }
        
        self.animal_url = reverse('register')

    def test_register_animal(self):
        response = self.client.post('/registerAnimal/', self.animal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.count(), 1)
        animal = Animal.objects.get()
        self.assertEqual(animal.name, 'Boi Bravo')
        self.assertEqual(animal.identification, 'BR12345')
        self.assertEqual(animal.owner, self.user)

    def test_get_animal_list(self):
        Animal.objects.create(
            name='Boi Bravo',
            identification='BR12345',
            born_date='2020-01-01',
            sex=self.sex,
            status=self.status,
            species=self.species,
            breed=self.breed,
            owner=self.user
        )
        response = self.client.get('/getAnimal/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Boi Bravo')

    def test_get_single_animal(self):
        animal = Animal.objects.create(
            name='Boi Bravo',
            identification='BR12345',
            born_date='2020-01-01',
            sex=self.sex,
            status=self.status,
            species=self.species,
            breed=self.breed,
            owner=self.user
        )
        response = self.client.get(f'/getAnimal/{animal.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Boi Bravo')

    def test_update_animal(self):
        animal = Animal.objects.create(
            name='Boi Bravo',
            identification='BR12345',
            born_date='2020-01-01',
            sex=self.sex,
            status=self.status,
            species=self.species,
            breed=self.breed,
            owner=self.user
        )
        updated_data = {
            'name': 'Boi Forte',
            'status': self.status.id,  # Mantendo o mesmo status
        }
        response = self.client.patch(f'/updateAnimal/{animal.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        animal.refresh_from_db()
        self.assertEqual(animal.name, 'Boi Forte')

    def test_delete_animal(self):
        animal = Animal.objects.create(
            name='Boi Bravo',
            identification='BR12345',
            born_date='2020-01-01',
            sex=self.sex,
            status=self.status,
            species=self.species,
            breed=self.breed,
            owner=self.user
        )
        response = self.client.delete(f'/deleteAnimal/{animal.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.count(), 0)

    def test_delete_nonexistent_animal(self):
        response = self.client.delete('/deleteAnimal/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

    def test_update_nonexistent_animal(self):
        updated_data = {
            'name': 'Boi Forte',
        }
        response = self.client.patch('/updateAnimal/999/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

    def test_register_animal_invalid_data(self):
        invalid_data = self.animal_data.copy()
        invalid_data['identification'] = ''  # Campo obrigatório vazio
        response = self.client.post('/registerAnimal/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('identification', response.data)
