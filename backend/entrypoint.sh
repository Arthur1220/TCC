#!/bin/bash

# Aplica as migrações
echo "Aplicando migrações..."
python manage.py migrate

# Carrega os dados das fixtures
echo "Carregando fixtures..."
/code/load_fixtures.sh

# Inicia o servidor
echo "Iniciando o servidor Django..."
exec python manage.py runserver 0.0.0.0:8000