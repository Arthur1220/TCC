from django.db import models
from user.models import User
from event.models import Event
from animal.models import Animal

class Status(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.name

class Blockchain(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, blank=False, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    transaction_hash = models.CharField(max_length=100, unique=True, blank=False, null=False)
    registration_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.transaction_hash