# Sistema de Rastreabilidade Animal com Blockchain - AnimalTracking

Este projeto é um sistema de rastreabilidade para a cadeia produtiva animal, desenvolvido como um Trabalho de Conclusão de Curso (TCC). A solução utiliza uma arquitetura híbrida que combina uma aplicação web moderna com a segurança e imutabilidade da tecnologia blockchain para registrar eventos críticos na vida dos animais.

## 📜 Visão Geral

O sistema permite que produtores rurais, veterinários e outros agentes da cadeia produtiva registrem eventos como nascimento, vacinação, medicação e transferência de titularidade. Esses registros geram um *hash* que é ancorado em uma blockchain de segunda camada (simulada via **Hardhat**), garantindo um histórico à prova de fraudes e totalmente auditável.

A plataforma foi projetada para ser acessível, abstraindo toda a complexidade da Web3 do usuário final através de uma carteira custodial gerenciada pelo backend.

## ✨ Principais Funcionalidades

  * **Gestão de Ativos:** Cadastro de propriedades, lotes e animais.
  * **Registro de Eventos Críticos:** Lançamento de eventos (vacinação, medicação, etc.) com registro imutável na blockchain.
  * **Transferência de Titularidade:** Processo seguro para transferir a posse de animais entre usuários.
  * **Painel de Controle:** Dashboard com indicadores de gestão e resumo de custos on-chain.
  * **Auditoria Pública:** Interface para qualquer pessoa verificar a autenticidade de um registro usando o ID do animal ou o hash da transação.
  * **Governança:** Painel administrativo para gerenciamento de parâmetros do sistema e do contrato inteligente.

## 🛠️ Tecnologias Utilizadas

  * **Backend:** Django, Django REST Framework
  * **Frontend:** Vue.js, Vite
  * **Blockchain:** Solidity, Hardhat, Ethers.js, OpenZeppelin Upgrades
  * **Banco de Dados:** PostgreSQL (armazenamento off-chain)
  * **Infraestrutura:** Docker, Docker Compose

-----

## 🚀 Como Executar o Projeto Localmente

Este projeto é totalmente orquestrado com Docker. Para executá-lo, você precisa ter o **Docker** e o **Docker Compose** instalados.

### 1\. Preparação do Ambiente

Primeiro, clone o repositório e navegue até a pasta raiz:

```bash
git clone https://github.com/Arthur1220/TCC.git
cd TCC
```

Em seguida, crie o arquivo de variáveis de ambiente a partir do exemplo:

```bash
cp .env.example .env
```

O arquivo `.env` já vem pré-configurado para o ambiente de desenvolvimento local.

### 2\. Executando com um Único Comando

[cite\_start]O projeto inclui um `Makefile` e um script de automação (`deploy.sh`) que cuidam de todo o processo de inicialização. [cite: 104]

Para executar tudo, basta rodar o comando:

```bash
make deploy
```

Este comando irá automaticamente:

1.  Construir as imagens Docker.
2.  Iniciar um nó Hardhat (blockchain local).
3.  Implantar o contrato inteligente `AnimalTracking.sol`.
4.  Atualizar o arquivo `.env` com o endereço do contrato.
5.  Iniciar os serviços de backend (Django) e frontend (Vue).

Ao final do processo, a aplicação estará disponível nos seguintes endereços:

  * **Frontend (Vue.js):** `http://localhost:5173`
  * **Backend (API Django):** `http://localhost:8000/api/`
  * **Blockchain (Nó Hardhat):** `http://localhost:8545`

-----

## 👨‍💻 Comandos Úteis para Desenvolvimento

Enquanto `make deploy` automatiza o início, os comandos abaixo são úteis para um controle mais granular do ambiente.

### Gerenciamento do Ambiente Docker

  * **Parar e remover tudo (limpeza total):**

    ```bash
    docker-compose down --rmi all --volumes --remove-orphans
    ```

      * `down`: Para os contêineres.
      * `--rmi all`: Remove todas as imagens Docker usadas pelos serviços.
      * `--volumes`: **DELETA TODOS OS DADOS**, incluindo o banco de dados e o estado da blockchain local. Use quando quiser recomeçar do zero.
      * `--remove-orphans`: Remove contêineres de serviços que não existem mais no `docker-compose.yml`.

  * **Iniciar o ambiente (com build forçado):**

    ```bash
    docker-compose up --build -d
    ```

      * `--build`: Força a reconstrução das imagens antes de iniciar. Útil após fazer alterações no `Dockerfile` ou no código-fonte.
      * `-d`: Roda em modo "detached" (em segundo plano).

  * **Reconstruir imagens sem usar cache:**

    ```bash
    docker compose build --no-cache
    ```

      * `--no-cache`: Ignora o cache de build do Docker. É mais lento, mas útil para resolver problemas de cache inconsistente.

### Comandos Manuais da Blockchain

Estes comandos devem ser executados de dentro da pasta `blockchain/`. Eles são úteis para depuração e testes específicos do contrato.

```bash
cd blockchain
```

  * **Instalar dependências da blockchain:**

    ```bash
    npm install
    ```

  * **Compilar os contratos inteligentes:**

    ```bash
    npx hardhat compile
    ```

      * Verifica se há erros de sintaxe no seu código Solidity e gera os "artefatos" (ABI e bytecode) necessários para interagir com o contrato.

  * **Iniciar um nó de blockchain local:**

    ```bash
    npx hardhat node
    ```

      * Inicia uma blockchain de simulação na sua máquina, com várias contas de teste pré-financiadas com ETH.

  * **Fazer o deploy do contrato na rede local:**

    ```bash
    npx hardhat run scripts/deploy.js --network localhost
    ```

      * Executa o script `deploy.js` para publicar seu contrato na rede que está rodando (definida como `localhost` no `hardhat.config.js`).

-----

## CONTRIBUTORS

  * **Arthur Marques Azevedo** - *Desenvolvedor* - [Arthur1220](https://www.google.com/search?q=https://github.com/Arthur1220)