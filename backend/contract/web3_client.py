import os
import json
from pathlib import Path
from web3 import Web3
from django.conf import settings

print("=== Configurações do settings no web3_client ===")
bp = getattr(settings, "BLOCKCHAIN_PROVIDER", None)
ca = getattr(settings, "CONTRACT_ADDRESS", None)
wp = getattr(settings, "WALLET_PUBLIC", None)
wpr = getattr(settings, "WALLET_PRIVATE", None)
print("BLOCKCHAIN_PROVIDER:", repr(bp))
print("CONTRACT_ADDRESS:", repr(ca))
print("WALLET_PUBLIC:", repr(wp))
print("WALLET_PRIVATE:", repr(wpr))
print("===================================================")

# Obtenha as configurações do blockchain a partir do settings
BLOCKCHAIN_PROVIDER = bp
CONTRACT_ADDRESS = ca
WALLET_PRIVATE = wpr
WALLET_PUBLIC = wp

# Define o caminho para o ABI
ABI_PATH = Path(__file__).parent / "contract_abi.json"

with open(ABI_PATH, "r") as f:
    contract_abi = json.load(f)

# Obtenha as configurações do blockchain a partir do settings
BLOCKCHAIN_PROVIDER = getattr(settings, "BLOCKCHAIN_PROVIDER", None)
CONTRACT_ADDRESS = getattr(settings, "KYC_CONTRACT_ADDRESS", None)
WALLET_PRIVATE = getattr(settings, "WALLET_PRIVATE", None)
WALLET_PUBLIC = getattr(settings, "WALLET_PUBLIC", None)

if not BLOCKCHAIN_PROVIDER or not CONTRACT_ADDRESS:
    raise Exception("As configurações de blockchain não estão definidas no settings.")

# Conecte-se ao provider
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_PROVIDER))
if not w3.isConnected():
    raise Exception("Falha ao conectar ao provider blockchain.")

# Instancie o contrato
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def register_event(event_id: int, animal_id: int, event_type: int, data_hash: str, user_hash: str):
    """
    Chama a função registerEvent do contrato e retorna o hash da transação.
    """
    account = w3.eth.account.from_key(WALLET_PRIVATE)
    txn = contract.functions.registerEvent(event_id, animal_id, event_type, data_hash, user_hash).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price,
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash.hex()

def get_number_of_events(animal_id: int):
    """
    Retorna o número de eventos registrados para um animal.
    """
    return contract.functions.getNumberOfEvents(animal_id).call()

def get_event_by_index(animal_id: int, index: int):
    """
    Retorna os dados do evento pelo índice.
    """
    return contract.functions.getEventByIndex(animal_id, index).call()

def is_active():
    """
    Retorna se o contrato está ativo.
    """
    return contract.functions.isActive().call()
