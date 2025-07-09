#!/bin/bash
set -e

# --- WAIT SCRIPT START ---
# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is up!"

# Wait for the blockchain RPC to be ready
echo "Waiting for blockchain RPC..."
while ! nc -z blockchain 8545; do
  sleep 1
done
echo "Blockchain RPC is up!"
# --- WAIT SCRIPT END ---

echo "Executando makemigrations (caso haja alterações nos modelos)..."
python manage.py makemigrations

echo "Aplicando migrações..."
python manage.py migrate

echo "Aguardando 5 segundos para garantir que as migrações estejam finalizadas..."
sleep 5

echo "Recolhendo ficheiros estáticos..."
python manage.py collectstatic --no-input

echo "Carregando fixtures..."
/code/load_fixtures.sh

echo "Aguardando 5 segundos antes de criar o superusuário..."
sleep 5

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
#exec python manage.py runserver 0.0.0.0:8000

#echo "Iniciando o servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application