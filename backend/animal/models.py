from django.db import models
from user.models import User

class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Breed(models.Model):
    name = models.CharField(max_length=50, unique=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="breeds")

    def __str__(self):
        return f"{self.name} ({self.species.name})"

class AnimalGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class IdentificationType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.description

class Animal(models.Model):
    identification_type = models.ForeignKey(IdentificationType, on_delete=models.CASCADE)
    identification = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="animals")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="animals", blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="animals")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animals")
    group = models.ForeignKey(AnimalGroup, on_delete=models.CASCADE, related_name="animals", blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="animals")

    def __str__(self):
        return f"{self.identification} - {self.status.name}"