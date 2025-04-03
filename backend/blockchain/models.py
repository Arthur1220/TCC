from django.db import models
from user.models import User
from event.models import Event
from animal.models import Animal

class BlockchainStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Blockchain(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=100, unique=True, blank=False, null=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    status = models.ForeignKey(BlockchainStatus, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.transaction_hash