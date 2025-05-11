import json
from pathlib import Path
from web3 import Web3
from django.conf import settings

# Importa as variáveis de ambiente do settings
BLOCKCHAIN_PROVIDER = settings.BLOCKCHAIN_PROVIDER
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS
WALLET_PUBLIC = settings.WALLET_PUBLIC
WALLET_PRIVATE = settings.WALLET_PRIVATE

# Define o caminho para o ABI do contrato
ABI_PATH = Path(__file__).parent / "contract_abi.json"

# Carrega o ABI; se for um artifact, extrai a chave "abi"
with open(ABI_PATH, "r") as f:
    loaded = json.load(f)
    if isinstance(loaded, dict) and "abi" in loaded:
        contract_abi = loaded["abi"]
    else:
        contract_abi = loaded

# Conecta-se ao provider blockchain
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_PROVIDER, request_kwargs={"timeout": 10}))
if not w3.is_connected():
    raise Exception("Falha ao conectar ao provider blockchain.")

# Instancia o contrato inteligente
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def convert_to_bytes32(text: str) -> str:
    encoded = text.encode('utf-8')
    if len(encoded) > 32:
        raise Exception("O texto é muito longo para ser convertido em bytes32")
    padded = encoded.ljust(32, b'\0')
    return Web3.to_hex(padded)

def register_event(event_id: int, animal_id: int, event_type: int, data_hash: str, user_hash: str):
    # Converte o user_hash para bytes32 se necessário
    try:
        if not (user_hash.startswith("0x") and len(user_hash) == 66):
            user_hash = convert_to_bytes32(user_hash)
    except Exception as e:
        raise Exception("Erro convertendo user_hash para bytes32: " + str(e))
        
    account = w3.eth.account.from_key(WALLET_PRIVATE)
    
    try:
        # Obtém a função diretamente usando o atributo functions
        function_call = contract.functions.registerEvent(
            event_id, animal_id, event_type, data_hash, user_hash
        )
        # Constrói a transação
        txn = function_call.build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address, "pending"),
            'gas': 3000000,
            'gasPrice': w3.eth.gas_price,
        })
    except Exception as e:
        raise Exception("Erro ao construir a transação: " + str(e))
    
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def get_number_of_events(animal_id: int):
    return contract.functions.getNumberOfEvents(animal_id).call()

def get_event_by_index(animal_id: int, index: int):
    return contract.functions.getEventByIndex(animal_id, index).call()

def get_events_by_animal(animal_id: int):
    return contract.functions.getEventsByAnimal(animal_id).call()

def is_active() -> bool:
    return contract.functions.isActive().call()

def add_registrar(registrar_address: str):
    account = w3.eth.account.from_key(WALLET_PRIVATE)
    txn = contract.functions.addRegistrar(registrar_address).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address, "pending"),
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price,
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def remove_registrar(registrar_address: str):
    account = w3.eth.account.from_key(WALLET_PRIVATE)
    txn = contract.functions.removeRegistrar(registrar_address).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address, "pending"),
        'gas': 3000000,
        'gasPrice': w3.eth.gas_price,
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def pause_contract() -> str:
    acct = w3.eth.account.from_key(WALLET_PRIVATE)
    fn   = contract.functions.pause()
    txn  = fn.build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        "gas": 200_000,
        "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
        "maxFeePerGas": w3.to_wei(50, "gwei"),
    })
    signed = acct.sign_transaction(txn)
    txh    = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(txh)
    return receipt.transactionHash.hex()

def unpause_contract() -> str:
    acct = w3.eth.account.from_key(WALLET_PRIVATE)
    fn   = contract.functions.unpause()
    txn  = fn.build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        "gas": 200_000,
        "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
        "maxFeePerGas": w3.to_wei(50, "gwei"),
    })
    signed = acct.sign_transaction(txn)
    txh    = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(txh)
    return receipt.transactionHash.hex()
