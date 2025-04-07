# core/config.py
from pathlib import Path
from pydantic import BaseSettings, Field, ValidationError

# BASE_DIR: diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

class EnvSettings(BaseSettings):
    # Configurações do Contrato (blockchain)
    BLOCKCHAIN_PROVIDER: str = Field(..., description="URL do provider blockchain")
    CONTRACT_ADDRESS: str = Field(..., description="Endereço do contrato de KYC")
    WALLET_PUBLIC: str = Field(..., description="Chave pública da carteira")
    WALLET_PRIVATE: str = Field(..., description="Chave privada da carteira")

    class Config:
        # Agora o arquivo .env está dentro da pasta backend
        env_file = BASE_DIR / "backend" / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

try:
    env_settings = EnvSettings()
except ValidationError as e:
    raise Exception(f"Erro nas variáveis de ambiente: {e}")

# Exporta as variáveis validadas
BLOCKCHAIN_PROVIDER = env_settings.BLOCKCHAIN_PROVIDER
CONTRACT_ADDRESS = env_settings.CONTRACT_ADDRESS
WALLET_PUBLIC = env_settings.WALLET_PUBLIC
WALLET_PRIVATE = env_settings.WALLET_PRIVATE
