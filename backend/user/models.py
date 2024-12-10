from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username