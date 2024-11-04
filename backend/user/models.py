from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class User(AbstractUser):
    username = None  # Remover o campo username
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class UserManager(BaseUserManager):
    def create_user(self, email, name, cpf, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be filled')
        if not name:
            raise ValueError('The name field must be filled')
        if not cpf:
            raise ValueError('The CPF field must be filled')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, cpf, password, **extra_fields)