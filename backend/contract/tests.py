from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

User = get_user_model()

class ContractAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=user)

    @patch('contract.web3_client.is_active')
    def test_contract_status_active(self, mock_is_active):
        mock_is_active.return_value = True
        url = reverse('contract-status')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"active": True})

    @patch('contract.web3_client.is_active')
    def test_contract_status_error(self, mock_is_active):
        mock_is_active.side_effect = Exception("boom")
        url = reverse('contract-status')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.get_number_of_events')
    def test_get_number_events_success(self, mock_get):
        mock_get.return_value = 3
        url = reverse('get-number-events') + '?animal_id=5'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"count": 3})

    def test_get_number_events_missing_param(self):
        url = reverse('get-number-events')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_number_events_invalid_param(self):
        url = reverse('get-number-events') + '?animal_id=abc'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('contract.web3_client.get_event_by_index')
    def test_get_event_by_index_success(self, mock_get):
        mock_get.return_value = (1, 10, 2, 'hash', '0xabc', '0xuser', 123)
        url = reverse('get-contract-event', args=[10]) + '?index=2'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = {
            "eventId": 1,
            "animalId": 10,
            "eventType": 2,
            "dataHash": 'hash',
            "registrant": '0xabc',
            "userHash": '0xuser',
            "timestamp": 123
        }
        self.assertEqual(resp.json(), expected)

    @patch('contract.web3_client.get_event_by_index')
    def test_get_event_by_index_error(self, mock_get):
        mock_get.side_effect = Exception("fail")
        url = reverse('get-contract-event', args=[1])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.get_events_by_animal')
    def test_list_events_success(self, mock_list):
        mock_list.return_value = [
            (1, 10, 2, 'h1', '0xr1', '0xu1', 101),
            (2, 10, 3, 'h2', '0xr2', '0xu2', 102),
        ]
        url = reverse('list-contract-events', args=[10])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = {
            "events": [
                {"eventId": 1, "animalId": 10, "eventType": 2, "dataHash": 'h1', "registrant": '0xr1', "userHash": '0xu1', "timestamp": 101},
                {"eventId": 2, "animalId": 10, "eventType": 3, "dataHash": 'h2', "registrant": '0xr2', "userHash": '0xu2', "timestamp": 102},
            ]
        }
        self.assertEqual(resp.json(), expected)

    @patch('contract.web3_client.get_events_by_animal')
    def test_list_events_error(self, mock_list):
        mock_list.side_effect = Exception("fail")
        url = reverse('list-contract-events', args=[1])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.register_event')
    def test_register_event_success(self, mock_reg):
        mock_reg.return_value = '0xtx'
        url = reverse('register-contract-event')
        data = {"event_id":1,"animal_id":2,"event_type":3,"data_hash":"h","user_hash":"u"}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json(), {"tx_hash": '0xtx'})

    def test_register_event_missing(self):
        url = reverse('register-contract-event')
        data = {"event_id":1}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('contract.web3_client.register_event')
    def test_register_event_error(self, mock_reg):
        mock_reg.side_effect = Exception("fail")
        url = reverse('register-contract-event')
        data = {"event_id":1,"animal_id":2,"event_type":3,"data_hash":"h","user_hash":"u"}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.add_registrar')
    def test_add_registrar_success(self, mock_add):
        mock_add.return_value = '0xareg'
        url = reverse('add-registrar')
        resp = self.client.post(url, {"registrar_address": '0x1'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json(), {"tx_hash": '0xareg'})

    def test_add_registrar_missing(self):
        url = reverse('add-registrar')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('contract.web3_client.add_registrar')
    def test_add_registrar_error(self, mock_add):
        mock_add.side_effect = Exception("fail")
        url = reverse('add-registrar')
        resp = self.client.post(url, {"registrar_address": '0x1'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.remove_registrar')
    def test_remove_registrar_success(self, mock_rem):
        mock_rem.return_value = '0xrem'
        url = reverse('remove-registrar')
        resp = self.client.post(url, {"registrar_address": '0x1'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"tx_hash": '0xrem'})

    def test_remove_registrar_missing(self):
        url = reverse('remove-registrar')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('contract.web3_client.remove_registrar')
    def test_remove_registrar_error(self, mock_rem):
        mock_rem.side_effect = Exception("fail")
        url = reverse('remove-registrar')
        resp = self.client.post(url, {"registrar_address": '0x1'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.pause_contract')
    def test_pause_contract_success(self, mock_pause):
        mock_pause.return_value = '0xphash'
        url = reverse('pause-contract')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"tx_hash": '0xphash'})

    @patch('contract.web3_client.pause_contract')
    def test_pause_contract_error(self, mock_pause):
        mock_pause.side_effect = Exception("fail")
        url = reverse('pause-contract')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())

    @patch('contract.web3_client.unpause_contract')
    def test_unpause_contract_success(self, mock_unpause):
        mock_unpause.return_value = '0xuhash'
        url = reverse('unpause-contract')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), {"tx_hash": '0xuhash'})

    @patch('contract.web3_client.unpause_contract')
    def test_unpause_contract_error(self, mock_unpause):
        mock_unpause.side_effect = Exception("fail")
        url = reverse('unpause-contract')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.json())
