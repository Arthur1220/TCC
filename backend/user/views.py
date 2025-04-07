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
                response.set_cookie('access', access_token, httponly=True, secure=False, samesite='Lax')
                response.set_cookie('refresh', refresh_token, httponly=True, secure=False, samesite='Lax')
                return response
            else:
                return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def refresh(request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token is None:
            return Response({'error': 'Refresh token ausente.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response({'message': 'Token atualizado com sucesso.'}, status=status.HTTP_200_OK)
            response.set_cookie('access', new_access, httponly=True, secure=False, samesite='Lax')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def logout(request):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            try:
                # Tenta invalidar (blacklist) o refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Se houver erro (por exemplo, se o token já estiver na blacklist), logue o erro
                print(f"Erro ao invalidar token: {e}")
        response = Response({'message': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
        # Remove os cookies definindo-os com expiração no passado
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def profile(request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    permission_classes = [IsAuthenticated]

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
    @permission_classes([AllowAny])
    def get(request, pk=None):
        if pk:
            try:
                user_role = UserRole.objects.get(pk=pk)
                serializer = UserRoleSerializer(user_role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'UserRole not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_roles = UserRole.objects.all()
            serializer = UserRoleSerializer(user_roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def register(request):
        data = {
            'user': request.data['user'],
            'role': request.data['role']
        }
        serializer = UserRoleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer error:", serializer.errors)