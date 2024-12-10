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

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def register(request):
        data = {
            'username': request.data['username'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'email': request.data['email'],
            'password': request.data['password'],
            'phone': request.data['phone'],
            'data_joined': timezone.now()
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer error:", serializer.errors)  # Log dos erros
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def login(request):
        try:
            username = request.data['username']
            password = request.data['password']

            if username and '@' in username:
                try:
                    user = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    pass
            
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }

                return Response(token, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def profile(request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
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