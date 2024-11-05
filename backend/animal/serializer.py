from rest_framework import serializers
from .models import Sex, Status, Species, Breed, Animal

class SexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sex
        fields = ['id', 'name', 'description']
    
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description']

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'name', 'description']

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'identification', 'born_date', 'register_date', 'sex', 'status', 'species', 'breed', 'lote', 'owner']