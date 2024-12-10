#!/bin/bash

# Aplica as migrações
echo "Aplicando migrações..."
python manage.py migrate

# Coleta os arquivos estáticos (se necessário)
# echo "Coletando arquivos estáticos..."
# python manage.py collectstatic --noinput

# Inicia o servidor
echo "Iniciando o servidor Django..."
exec "$@"