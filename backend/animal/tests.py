from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from animal.models import Species, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal

User = get_user_model()

class AnimalTestCase(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Create necessary objects
        self.species = Species.objects.create(name="Cattle")
        self.breed = Breed.objects.create(name="Angus", species=self.species)
        self.group = AnimalGroup.objects.create(name="Group A", description="Test group")
        self.gender = Gender.objects.create(name="Male", description="Test gender")
        self.status = Status.objects.create(name="Active", description="Animal is active")
        self.identification_type = IdentificationType.objects.create(name="Tag")

        # Animal data
        self.animal_data = {
            "identification_type": self.identification_type,
            "identification": "123ABC",
            "birth_date": "2020-01-01",
            "species": self.species,
            "breed": self.breed,
            "status": self.status,
            "owner": self.user,
            "group": self.group,
            "gender": self.gender
        }

        self.animal = Animal.objects.create(**self.animal_data)

    def test_register_animal(self):
        animal_data = {
            "identification_type": self.identification_type.id,
            "identification": "456DEF",
            "birth_date": "2021-06-01",
            "species": self.species.id,
            "breed": self.breed.id,
            "status": self.status.id,
            "owner": self.user.id,
            "group": self.group.id,
            "gender": self.gender.id
        }
        response = self.client.post("/animal/animal-register/", data=animal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["identification"], animal_data["identification"])

    def test_get_all_animals(self):
        response = self.client.get("/animal/animal-get/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_animal(self):
        response = self.client.get(f"/animal/animal-get/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identification"], self.animal.identification)

    def test_filter_animals(self):
        filter_params = {
            "species": self.species.id,
            "breed": self.breed.id,
            "status": self.status.id
        }
        response = self.client.get("/animal/animal-filter/", data=filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_animal(self):
        updated_data = {
            "identification": "789GHI",
            "status": self.status.id
        }
        response = self.client.put(f"/animal/animal-update/{self.animal.id}/", data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identification"], updated_data["identification"])

    def test_delete_animal(self):
        response = self.client.delete(f"/animal/animal-delete/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the animal is deleted
        response = self.client.get(f"/animal/animal-get/{self.animal.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
