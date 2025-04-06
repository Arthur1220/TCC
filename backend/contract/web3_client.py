import json
from pathlib import Path
from web3 import Web3
from django.conf import settings

# Assumindo que o módulo de configuração (core/config.py) já validou e exportou as variáveis,
# basta importá-las do settings:
BLOCKCHAIN_PROVIDER = settings.BLOCKCHAIN_PROVIDER
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS
WALLET_PUBLIC = settings.WALLET_PUBLIC
WALLET_PRIVATE = settings.WALLET_PRIVATE

# Define o caminho para o ABI do contrato
ABI_PATH = Path(__file__).parent / "contract_abi.json"

# Carrega o arquivo de ABI e, se for um artifact, extrai a chave "abi"
with open(ABI_PATH, "r") as f:
    loaded = json.load(f)
    if isinstance(loaded, dict) and "abi" in loaded:
        contract_abi = loaded["abi"]
    else:
        contract_abi = loaded

# Conecta-se ao provider blockchain
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_PROVIDER))
if not w3.is_connected():
    raise Exception("Falha ao conectar ao provider blockchain.")

# Instancia o contrato inteligente
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def register_event(event_id: int, animal_id: int, event_type: int, data_hash: str, user_hash: str):
    """
    Chama a função registerEvent do contrato e retorna o hash da transação.
    """
    account = w3.eth.account.from_key(WALLET_PRIVATE)
    txn = contract.functions.registerEvent(
        event_id, animal_id, event_type, data_hash, user_hash
    ).buildTransaction({
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