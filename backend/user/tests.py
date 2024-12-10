from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from user.models import Role, UserRole

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        # Configuração inicial
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone': '123456789'
        }
        self.user = User.objects.create_user(**self.user_data)

        self.role_data = {
            'name': 'Admin',
            'description': 'Administrador do sistema'
        }
        self.role = Role.objects.create(**self.role_data)

        self.user_role_data = {
            'user': self.user,
            'role': self.role
        }
        self.user_role = UserRole.objects.create(**self.user_role_data)

        # URLs
        self.register_url = '/user/register/'
        self.login_url = '/user/login/'
        self.profile_url = '/user/profile/'
        self.roles_url = '/user/getRoles/'
        self.role_detail_url = f'/user/getRole/{self.role.id}/'
        self.user_roles_url = '/user/getUserRoles/'
        self.user_role_create_url = '/user/createUserRole/'

    # Testes para User
    def test_register_user(self):
        new_user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'phone': '987654321'
        }
        response = self.client.post(self.register_url, data=new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)

    def test_login_user(self):
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': self.user_data['password']
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

    # Testes para Role
    def test_get_roles(self):
        response = self.client.get(self.roles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_role_by_id(self):
        response = self.client.get(self.role_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.role_data['name'])

    # Testes para UserRole
    def test_create_user_role(self):
        new_user = User.objects.create_user(
            username='newuserrole',
            email='newuserrole@example.com',
            password='test1234'
        )
        new_role = Role.objects.create(name='Editor', description='Pode editar conteúdos.')

        new_user_role_data = {
            'user': new_user.id,
            'role': new_role.id
        }
        response = self.client.post(self.user_role_create_url, data=new_user_role_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], new_user.id)
        self.assertEqual(response.data['role'], new_role.id)

    def test_get_user_roles(self):
        response = self.client.get(self.user_roles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
