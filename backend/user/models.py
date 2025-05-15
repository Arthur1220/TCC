from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.username
    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'