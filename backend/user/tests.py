from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAPITestCase(APITestCase):

    def setUp(self):
        # Configuração de um usuário inicial para testes de login e perfil
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'strongpassword123',
            'telefone': '123456789'
        }
        self.user = User.objects.create_user(**self.user_data)

        # URLs do sistema
        self.login_url = '/login/'
        self.register_url = '/register/'
        self.profile_url = '/profile/'
        self.logout_url = '/logout/'
        self.refresh_url = '/token/refresh/'

    def test_register_user(self):
        # Criando um novo conjunto de dados exclusivos para o teste de registro
        unique_user_data = {
            'username': 'uniqueuser',
            'first_name': 'Unique',
            'last_name': 'User',
            'email': 'unique@example.com',
            'password': 'unique12345',
            'telefone': '987654321',
        }
        response = self.client.post(self.register_url, data=unique_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_login_user(self):
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_access_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        # Gerar token para logout
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.post(self.logout_url, data={'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_refresh_token(self):
        # Gerar token para refresh
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.refresh_url, data={'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
