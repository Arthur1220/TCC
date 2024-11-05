from django.db import models
from user.models import User

class Sex(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=6, unique=True)
    description = models.CharField(max_length=50)

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=50)

class Species(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    identification = models.CharField(max_length=255)
    born_date = models.DateField()
    register_date = models.DateTimeField(auto_now_add=True)

    sex = models.ForeignKey(Sex, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, blank=True, null=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animais')