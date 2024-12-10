from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Property

User = get_user_model()

class PropertyAPITestCase(APITestCase):

    def setUp(self):
        # Configuração inicial
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.property_data = {
            'name': 'Test Property',
            'address': '123 Test Street',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
        }

        self.property = Property.objects.create(owner=self.user, **self.property_data)

        # URLs para os testes
        self.register_url = '/property/register/'
        self.get_url = '/property/get/'
        self.get_single_url = f'/property/get/{self.property.id}/'
        self.update_url = f'/property/update/{self.property.id}/'
        self.delete_url = f'/property/delete/{self.property.id}/'

    def test_register_property(self):
        new_property_data = {
            'name': 'New Property',
            'address': '456 New Street',
            'city': 'New City',
            'state': 'New State',
            'zip_code': '67890',
        }

        response = self.client.post(self.register_url, data=new_property_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_property_data['name'])

    def test_get_properties(self):
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_property(self):
        response = self.client.get(self.get_single_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.property_data['name'])

    def test_update_property(self):
        updated_data = {
            'name': 'Updated Property',
            'address': '789 Updated Street',
        }

        response = self.client.put(self.update_url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['address'], updated_data['address'])

    def test_delete_property(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Property deleted successfully')

        # Verifique se a propriedade foi realmente excluída
        response = self.client.get(self.get_single_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
