from django.db import models
from user.models import User

class Specie(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Breed(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name="breeds")

    def __str__(self):
        return f"{self.name} ({self.specie.name})"

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
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description if self.description else self.name

class Animal(models.Model):
    identification = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animals")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="animals", blank=True, null=True)
    group = models.ForeignKey(AnimalGroup, on_delete=models.CASCADE, related_name="animals", blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="animals")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="animals")
    identification_type = models.ForeignKey(IdentificationType, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    observations = models.TextField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identification} - {self.status.name}"