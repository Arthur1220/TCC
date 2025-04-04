#!/bin/bash
set -e

echo "Aplicando migrações..."
python manage.py migrate

echo "Carregando fixtures..."
/code/load_fixtures.sh

# Cria o superusuário automaticamente se as variáveis de ambiente estiverem definidas
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "Criando superusuário..."
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
fi

echo "Iniciando o servidor Django..."
exec python manage.py runserver 0.0.0.0:8000