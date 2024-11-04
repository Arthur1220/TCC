from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import User
from .serializer import UserSerializer, LogoutSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def register(request):
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'cpf': request.data.get('cpf'),
            'password': request.data.get('password'),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def login(request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            user = None
            
            user = authenticate(email=email, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                
                return Response(token, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)
    
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

        return Response({'message': 'Sucess logout'}, status=status.HTTP_204_NO_CONTENT)