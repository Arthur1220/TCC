from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Specie, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal
from django.core.exceptions import ObjectDoesNotExist
from .serializers import SpecieSerializer, BreedSerializer, AnimalGroupSerializer, GenderSerializer, StatusSerializer, IdentificationTypeSerializer, AnimalSerializer

class SpecieViewSet(ModelViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    permission_classes = [AllowAny]

class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]

# animal/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action  # se precisar de ações customizadas
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import AnimalGroup
from .serializers import AnimalGroupSerializer

class AnimalGroupViewSet(ModelViewSet):
    queryset = AnimalGroup.objects.all()
    serializer_class = AnimalGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Para registrar (criar) um novo grupo
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'owner': request.user.id,
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Lista os grupos de animais do usuário logado
        animal_groups = AnimalGroup.objects.filter(owner=request.user.id)
        serializer = self.get_serializer(animal_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # Recupera um grupo específico, garantindo que o usuário é o dono
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            serializer = self.get_serializer(animal_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        # Atualiza um grupo específico
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            serializer = self.get_serializer(animal_group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        # Deleta um grupo específico
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            animal_group.delete()
            return Response({'message': 'Animal group deleted successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [AllowAny]

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]

class IdentificationTypeViewSet(ModelViewSet):
    queryset = IdentificationType.objects.all()
    serializer_class = IdentificationTypeSerializer
    permission_classes = [AllowAny]

class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'identification': request.data['identification'],
            'owner': request.user.id,
            'breed': request.data['breed'],
            'group': request.data['group'],
            'gender': request.data['gender'],
            'status': request.data['status'],
            'identification_type': request.data['identification_type'],
            'birth_date': request.data['birth_date'],
            'observations': request.data['observations'],
        }

        serializer = AnimalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                animal = Animal.objects.get(pk=id)
                serializer = AnimalSerializer(animal)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            animals = Animal.objects.all()
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_fields = [field.name for field in Animal._meta.fields]

        for key, value in query_params.items():
            if key in allowed_fields:
                filters[key] = value

        try:
            animals = Animal.objects.filter(**filters)
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            animal = Animal.objects.get(pk=id)
            serializer = AnimalSerializer(instance=animal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            animal = Animal.objects.get(pk=id)
            animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)