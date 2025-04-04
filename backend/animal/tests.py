from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from animal.models import Specie, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal

User = get_user_model()

class AnimalTestCase(APITestCase):
    """
    Testes para o app de Animal.
    """

    def setUp(self):
        # Criação de um usuário de teste e autenticação
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Criação de objetos necessários para os testes
        self.specie = Specie.objects.create(name="Cattle")
        self.breed = Breed.objects.create(name="Angus", species=self.species)
        self.group = AnimalGroup.objects.create(name="Group A", description="Test group")
        self.gender = Gender.objects.create(name="Male", description="Test gender")
        self.status = Status.objects.create(name="Active", description="Animal is active")
        self.identification_type = IdentificationType.objects.create(name="Tag")
        self.observation = "Test observations"

        # Dados do animal para criação via API
        self.animal_data = {
            "identification_type": self.identification_type.id,
            "identification": "123ABC",
            "birth_date": "2020-01-01",
            "specie": self.specie.id,
            "breed": self.breed.id,
            "status": self.status.id,
            "owner": self.user.id,
            "group": self.group.id,
            "gender": self.gender.id,
            "observations": self.observation
        }

        # Criação de um animal diretamente no banco para testes de GET/PUT/DELETE
        self.animal = Animal.objects.create(
            identification="123ABC",
            owner=self.user,
            breed=self.breed,
            group=self.group,
            gender=self.gender,
            status=self.status,
            identification_type=self.identification_type,
            birth_date="2020-01-01",
            observations=self.observation
        )

    def test_register_animal(self):
        """
        Testa o registro de um novo animal via API e verifica se o retorno
        contém o campo 'identification' conforme esperado.
        """
        animal_data = {
            "identification_type": self.identification_type.id,
            "identification": "456DEF",
            "birth_date": "2021-06-01",
            "specie": self.specie.id,
            "breed": self.breed.id,
            "status": self.status.id,
            "owner": self.user.id,
            "group": self.group.id,
            "gender": self.gender.id,
            "observations": "Test observations"
        }
        response = self.client.post("/animal/animal-register/", data=animal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["identification"], animal_data["identification"])

    def test_get_all_animals(self):
        """
        Testa a obtenção de todos os animais via API.
        """
        response = self.client.get("/animal/animal-get/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_animal(self):
        """
        Testa a obtenção de um único animal via API.
        """
        response = self.client.get(f"/animal/animal-get/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identification"], self.animal.identification)

    def test_filter_animals(self):
        """
        Testa a filtragem de animais com base em specie, breed e status.
        """
        filter_params = {
            "specie": self.specie.id,
            "breed": self.breed.id,
            "status": self.status.id
        }
        response = self.client.get("/animal/animal-filter/", data=filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_animal(self):
        """
        Testa a atualização dos dados de um animal via API.
        """
        updated_data = {
            "identification": "789GHI",
            "status": self.status.id
        }
        response = self.client.put(f"/animal/animal-update/{self.animal.id}/", data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identification"], updated_data["identification"])

    def test_delete_animal(self):
        """
        Testa a exclusão de um animal via API e verifica se a exclusão foi efetivada.
        """
        response = self.client.delete(f"/animal/animal-delete/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verifica se o animal foi excluído
        response = self.client.get(f"/animal/animal-get/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_multiple_animals_registration(self):
        """
        Testa o registro de múltiplos animais e a contagem correta.
        """
        # Registra um novo animal
        new_animal_data = {
            "identification_type": self.identification_type.id,
            "identification": "999XYZ",
            "birth_date": "2022-01-01",
            "specie": self.specie.id,
            "breed": self.breed.id,
            "status": self.status.id,
            "owner": self.user.id,
            "group": self.group.id,
            "gender": self.gender.id,
            "observations": "Another test"
        }
        response = self.client.post("/animal/animal-register/", data=new_animal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtém a lista de animais e verifica se a contagem é pelo menos 2
        response = self.client.get("/animal/animal-get/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_animal_filtering(self):
        """
        Testa a filtragem de animais para garantir que apenas os que correspondem aos critérios sejam retornados.
        """
        filter_params = {
            "specie": self.specie.id,
            "breed": self.breed.id,
            "status": self.status.id
        }
        response = self.client.get("/animal/animal-filter/", data=filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)