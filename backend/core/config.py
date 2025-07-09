# core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError

class EnvSettings(BaseSettings):
    BLOCKCHAIN_PROVIDER: str = Field(
        ...,
        description="URL do provider blockchain (lido de BLOCKCHAIN_PROVIDER no ambiente)"
    )
    CONTRACT_ADDRESS: str = Field(
        ...,
        description="Endereço do contrato (lido de DJANGO_CONTRACT_ADDRESS no ambiente)"
    )
    WALLET_PUBLIC: str = Field(
        ...,
        description="Chave pública da carteira (lido de WALLET_PUBLIC no ambiente)"
    )
    WALLET_PRIVATE: str = Field(
        ...,
        description="Chave privada da carteira (lido de PRIVATE_KEY no ambiente)"
    )

try:
    env_settings = EnvSettings()
except ValidationError as e:
    raise Exception(f"Erro nas variáveis de ambiente: {e}")

# Exporta as variáveis validadas
BLOCKCHAIN_PROVIDER = env_settings.BLOCKCHAIN_PROVIDER
CONTRACT_ADDRESS    = env_settings.CONTRACT_ADDRESS
WALLET_PUBLIC       = env_settings.WALLET_PUBLIC
WALLET_PRIVATE      = env_settings.WALLET_PRIVATE
