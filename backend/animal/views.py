from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .models import Sex, Status, Species, Breed, Animal
from .serializer import SexSerializer, StatusSerializer, SpeciesSerializer, BreedSerializer, AnimalSerializer

class SexViewSet(ModelViewSet):
    queryset = Sex.objects.all()
    serializer_class = SexSerializer

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