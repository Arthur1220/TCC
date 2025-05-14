# contract/tests_integration.py

import time
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

class ContractIntegrationTestCase(APITestCase):
    """
    Testes end-to-end contra um nó Hardhat local.
    Pré-requisitos:
      1) npx hardhat node
      2) npx hardhat run scripts/deploy.js --network localhost
      3) .env já carregado em settings.py, com RPC_URL e CONTRACT_ADDRESS do proxy.
    """

    def setUp(self):
        # Cria e autentica um usuário Django
        self.user = User.objects.create_user("ituser", "itpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # Pequena pausa para o nó e o deploy estabilizarem
        time.sleep(1)

    def test_full_flow_register_and_query(self):
        # 1) Consulta status
        resp = self.client.get(reverse("contract-status"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.json().get("active"))

        # 2) Conta eventos antes de registrar
        r_before = self.client.get(reverse("get-number-events") + "?animal_id=7")
        self.assertEqual(r_before.status_code, status.HTTP_200_OK)
        initial_count = r_before.json().get("count")

        # 3) Registra um novo evento
        payload = {
            "event_id":   42,
            "animal_id":  7,
            "event_type": 3,
            "data_hash":  "0xdeadbeef",
            "user_hash":  "IntegrationTestUser"
        }
        r_reg = self.client.post(
            reverse("register-contract-event"),
            payload,
            format="json"
        )
        self.assertEqual(r_reg.status_code, status.HTTP_201_CREATED)
        tx_hash = r_reg.json().get("tx_hash")
        self.assertTrue(tx_hash.startswith("0x"))

        # 4) Verifica contagem de eventos aumentou em 1
        r_after = self.client.get(reverse("get-number-events") + "?animal_id=7")
        self.assertEqual(r_after.status_code, status.HTTP_200_OK)
        self.assertEqual(r_after.json().get("count"), initial_count + 1)

        # 5) Lê o evento recém-registrado no índice correspondente
        idx = initial_count  # novo evento ocupa este índice
        r_idx = self.client.get(reverse("get-contract-event", args=[7]) + f"?index={idx}")
        self.assertEqual(r_idx.status_code, status.HTTP_200_OK)
        data = r_idx.json()
        self.assertEqual(data["eventId"],   42)
        self.assertEqual(data["animalId"],  7)
        self.assertEqual(data["dataHash"], "0xdeadbeef")
        self.assertIn("IntegrationTestUser", data["userHash"])

        # 6) Lista todos os eventos e verifica o tamanho correto
        r_list = self.client.get(reverse("list-contract-events", args=[7]))
        self.assertEqual(r_list.status_code, status.HTTP_200_OK)
        events = r_list.json().get("events")
        self.assertIsInstance(events, list)
        self.assertEqual(len(events), initial_count + 1)
        # O último evento deve ser justamente o que registramos
        self.assertEqual(events[-1]["eventId"], 42)
