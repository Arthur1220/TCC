from django.db import models
from user.models import User
from event.models import Event
from animal.models import Animal
from simple_history.models import HistoricalRecords

class BlockchainStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Blockchain(models.Model):
    # Definindo related_name explícitos para facilitar a serialização e consultas
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='blockchain_entries')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='blockchain_entries')
    transaction_hash = models.CharField(max_length=100, unique=True, blank=False, null=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blockchain_entries_owned', blank=False, null=False)
    status = models.ForeignKey(BlockchainStatus, on_delete=models.CASCADE, related_name='blockchain_entries_by_status', blank=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.transaction_hash

    class Meta:
        # Adiciona uma ordenação padrão para facilitar a visualização no frontend
        ordering = ['-registration_date'] # Ordena pelos mais recentes primeiro