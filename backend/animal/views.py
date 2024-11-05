from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import Sex, Status, Species, Breed, Animal
from .serializer import SexSerializer, StatusSerializer, SpeciesSerializer, BreedSerializer, AnimalSerializer

class SexViewSet(ModelViewSet):
    queryset = Sex.objects.all()
    serializer_class = SexSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def create(request):
        data = request.data.copy()
        serializer = SexSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list(request, pk=None):
        if pk:
            try:
                sex = Sex.objects.get(id=pk)
                serializer = SexSerializer(sex, many=False)
            except:
                return Response({'message': 'Sex not find'}, status=status.HTTP_404_NOT_FOUND)
        else:
            sex = Sex.objects.all()
            serializer = SexSerializer(sex, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['DELETE'])
    @permission_classes([AllowAny])
    def delete(request, pk):
        try:
            sex = Sex.objects.get(id=pk)
            sex.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Sex not find'}, status=status.HTTP_404_NOT_FOUND)
        
class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def create(request):
        data = request.data.copy()
        serializer = StatusSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list(request, pk=None):
        if pk:
            try:
                data = Status.objects.get(id=pk)
                serializer = StatusSerializer(data, many=False)
            except:
                return Response({'message': 'Status not find'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = Status.objects.all()
            serializer = StatusSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['DELETE'])
    @permission_classes([AllowAny])
    def delete(request, pk):
        try:
            data = Status.objects.get(id=pk)
            data.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Status not find'}, status=status.HTTP_404_NOT_FOUND)
        
class SpeciesViewSet(ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def create(request):
        data = request.data.copy()
        serializer = SpeciesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list(request, pk=None):
        if pk:
            try:
                species = Species.objects.get(id=pk)
                serializer = SpeciesSerializer(species, many=False)
            except:
                return Response({'message': 'Species not find'}, status=status.HTTP_404_NOT_FOUND)
        else:
            species = Species.objects.all()
            serializer = SpeciesSerializer(species, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['DELETE'])
    @permission_classes([AllowAny])
    def delete(request, pk):
        try:
            species = Species.objects.get(id=pk)
            species.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Species not find'}, status=status.HTTP_404_NOT_FOUND)
        
class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def create(request):
        data = request.data.copy()
        serializer = BreedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list(request, pk=None):
        if pk:
            try:
                breed = Breed.objects.get(id=pk)
                serializer = BreedSerializer(breed, many=False)
            except:
                return Response({'message': 'Breed not find'}, status=status.HTTP_404_NOT_FOUND)
        else:
            breed = Breed.objects.all()
            serializer = BreedSerializer(breed, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['DELETE'])
    @permission_classes([AllowAny])
    def delete(request, pk):
        try:
            breed = Breed.objects.get(id=pk)
            breed.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Breed not find'}, status=status.HTTP_404_NOT_FOUND)
        
class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create(request):
        data = request.data.copy()
        serializer = AnimalSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def list(request, pk=None):
        if pk:
            try:
                animal = Animal.objects.get(id=pk)
                serializer = AnimalSerializer(animal, many=False)
            except:
                return Response({'message': 'Animal not find'}, status=status.HTTP_404_NOT_FOUND)
        else:
            animal = Animal.objects.all()
            serializer = AnimalSerializer(animal, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @api_view(['DELETE'])
    @permission_classes([AllowAny])
    def delete(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            animal.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'message': 'Animal not find'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PATCH'])
    @permission_classes([AllowAny])
    def update(request, pk):
        try:
            animal = Animal.objects.get(id=pk)
            data = request.data.copy()
            serializer = AnimalSerializer(animal, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Animal not find'}, status=status.HTTP_404_NOT_FOUND)