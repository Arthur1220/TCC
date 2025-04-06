from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
import json

User = get_user_model()

class ContractAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_contract_status(self):
        url = reverse("contract-status")
        response = self.client.get(url)
        # Verifica se o endpoint retorna 200 e contém a chave "active"
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("active", response.json())

    def test_get_number_events_invalid(self):
        url = reverse("get-number-events") + "?animal_id=9999"
        response = self.client.get(url)
        # Pode retornar 0 ou erro, dependendo da implementação do contrato
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_register_contract_event_missing_data(self):
        url = reverse("register-contract-event")
        data = {
            "event_id": 1,
            "animal_id": 100,
            "event_type": 1
            # data_hash e user_hash estão faltando
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
