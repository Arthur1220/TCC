from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Species, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal
from django.core.exceptions import ObjectDoesNotExist
from .serializers import SpeciesSerializer, BreedSerializer, AnimalGroupSerializer, GenderSerializer, StatusSerializer, IdentificationTypeSerializer, AnimalSerializer

class SpeciesViewSet(ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = [AllowAny]

class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]

class AnimalGroupViewSet(ModelViewSet):
    queryset = AnimalGroup.objects.all()
    serializer_class = AnimalGroupSerializer
    permission_classes = [AllowAny]

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
            'identification_type': request.data['identification_type'],
            'identification': request.data['identification'],
            'birth_date': request.data['birth_date'],
            'species': request.data['species'],
            'breed': request.data['breed'],
            'status': request.data['status'],
            'owner': request.user.id,
            'group': request.data['group'],
            'gender': request.data['gender']
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