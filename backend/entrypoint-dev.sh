#!/bin/bash
set -e

echo "Aguardando 10 segundos para a blockchain iniciar..."
sleep 10

echo "Aplicando migrações (para o banco de dados SQLite)..."
python manage.py migrate

echo "Carregando fixtures..."
# Atenção: loaddata pode falhar se os dados já existirem. Remova se causar problemas.
python manage.py loaddata blockchain/fixtures/blockchain_status.json || echo "Fixtures já existem."
python manage.py loaddata event/fixtures/event_types.json || echo "Fixtures já existem."
# ... adicione os outros comandos loaddata com `|| echo "..."`

echo "Criando superusuário (se não existir)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF

echo "Iniciando o servidor de DESENVOLVIMENTO do Django em http://0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000