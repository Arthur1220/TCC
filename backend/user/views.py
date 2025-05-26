from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from django.utils import timezone
from .models import User, Role, UserRole
from .serializers import UserSerializer, LogoutSerializer, RoleSerializer, UserRoleSerializer
import uuid

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def register(request):
        def generate_unique_user_hash():
            while True:
                temp_hash = uuid.uuid4().hex
                if not User.objects.filter(user_hash=temp_hash).exists():
                    return temp_hash

        data = {
            'username': request.data['username'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'email': request.data['email'],
            'password': request.data['password'],
            'phone': request.data['phone'],
            'user_hash': generate_unique_user_hash(),
            'data_joined': timezone.now()
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuário criado com sucesso.', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def login(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response(
                    {'error': 'Username e password são necessários.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Se o username contém '@', assume que é email e busca o usuário correspondente
            if '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    username = user_obj.username
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Credenciais inválidas.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            user = authenticate(username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                response = Response({'message': 'Login realizado com sucesso.'}, status=status.HTTP_200_OK)
                # Configure os cookies:
                response.set_cookie('access', access_token, httponly=True, secure=False, samesite='Lax', path='/')
                response.set_cookie('refresh', refresh_token, httponly=True, secure=False, samesite='Lax', path='/')

                # Adicione os tokens ao payload da resposta
                response.data = {
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone': user.phone,
                        'user_hash': user.user_hash
                    }
                }
                # Adicione o ID do usuário ao payload da resposta
                response.data['user']['id'] = user.id
                # Adicione o hash do usuário ao payload da resposta
                response.data['user']['user_hash'] = user.user_hash

                return response
            else:
                return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def refresh(request):
        print("DEBUG - Refresh endpoint iniciado")
        # Verifica o refresh token nos cookies
        refresh_token = request.COOKIES.get('refresh')
        print("DEBUG - Refresh token recebido:", refresh_token)
        
        if refresh_token is None:
            print("DEBUG - Refresh token ausente nos cookies")
            response = Response({'error': 'Refresh token ausente.'}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('access', path='/')
            response.delete_cookie('refresh', path='/')
            print("DEBUG - Cookies 'access' e 'refresh' deletados")
            return response
        
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response({'message': 'Token atualizado com sucesso.'}, status=status.HTTP_200_OK)
            response.set_cookie('access', new_access, httponly=True, secure=False, samesite='Lax', path='/')
            print("DEBUG - Novo access token definido:", new_access)
            return response
        except Exception as e:
            print("ERROR in refresh endpoint:", e)
            response = Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('access', path='/')
            response.delete_cookie('refresh', path='/')
            print("DEBUG - Em caso de erro, cookies 'access' e 'refresh' deletados")
            return response

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def logout(request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            try:
                # Tenta invalidar (blacklist) o refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Se houver erro (por exemplo, se o token já estiver na blacklist), logue o erro
                print(f"Erro ao invalidar token, token atualmente invalido: {e}")
        response = Response({'message': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
        # Remove os cookies definindo-os com expiração no passado
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list_all_users(request):
        # Adiciona prefetch_related para otimizar o carregamento das roles
        users = User.objects.all().prefetch_related('roles__role') 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def profile(request):
        try:
            user_data = UserSerializer(request.user).data

            # Adicionar as roles do usuário
            user_roles = UserRole.objects.filter(user=request.user)
            roles_data = [UserRoleSerializer(ur).data for ur in user_roles]
            
            user_data['roles'] = roles_data

            return Response(user_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, pk=None):
        if pk:
            try:
                role = Role.objects.get(pk=pk)
                serializer = RoleSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            roles = Role.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserRoleViewSet(ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    @api_view(['GET'])
    @permission_classes([IsAuthenticated]) # Pode ser IsAdminUser
    def get(request, pk=None):
        if pk: # Get a specific UserRole by its ID
            try:
                user_role = UserRole.objects.get(pk=pk)
                serializer = UserRoleSerializer(user_role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'UserRole not found'}, status=status.HTTP_404_NOT_FOUND)
        elif 'user_id' in request.query_params: # Get UserRoles for a specific user
            user_id = request.query_params.get('user_id')
            try:
                user = User.objects.get(pk=user_id)
                user_roles = UserRole.objects.filter(user=user)
                serializer = UserRoleSerializer(user_roles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found for the given user_id'}, status=status.HTTP_404_NOT_FOUND)
        else: # Get all UserRoles
            user_roles = UserRole.objects.all()
            serializer = UserRoleSerializer(user_roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['POST'])
    @permission_classes([AllowAny]) # Apenas admins podem criar/atribuir roles
    def assign_role(request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        if not user_id or not role_id:
            return Response({'error': 'user_id and role_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            role = Role.objects.get(pk=role_id)
            
            user_role, created = UserRole.objects.get_or_create(user=user, role=role)
            
            if created:
                serializer = UserRoleSerializer(user_role)
                return Response({'status': 'Role assigned successfully.', 'user_role': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                serializer = UserRoleSerializer(user_role)
                return Response({'status': 'User already has this role.', 'user_role': serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated]) # Apenas admins podem remover roles
    def remove_role(request, user_id, role_id):
        try:
            user_role = UserRole.objects.get(user_id=user_id, role_id=role_id)
            user_role.delete()
            return Response({'status': 'Role removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except UserRole.DoesNotExist:
            return Response({'error': 'UserRole not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)