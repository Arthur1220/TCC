from django.db import models
from django.conf import settings # Para user model (settings.AUTH_USER_MODEL)
from simple_history.models import HistoricalRecords
# from animal.models import Animal # Se precisar de type hinting, senão string 'animal.Animal' é ok
from user.models import User

class OwnershipTransferRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING_APPROVAL', 'Pendente de Aprovação'),
        ('APPROVED', 'Aprovada pelo Destinatário'),
        ('REJECTED', 'Rejeitada pelo Destinatário'),
        ('PROCESSING', 'Processando Transferência On-chain'),
        ('COMPLETED', 'Concluída'),
        ('FAILED_BLOCKCHAIN', 'Falha na Blockchain'),
        ('CANCELLED_BY_INITIATOR', 'Cancelada pelo Solicitante'),
    ]

    animals = models.ManyToManyField(
        'animal.Animal', # Referencia o model Animal do app 'animal'
        related_name='transfer_requests_involved_in',
        verbose_name="Animais na Solicitação"
    )
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='initiated_transfer_requests',
        on_delete=models.CASCADE,
        verbose_name="Solicitante (Proprietário Atual)"
    )
    requested_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_transfer_requests',
        on_delete=models.CASCADE,
        verbose_name="Destinatário Solicitado"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='PENDING_APPROVAL',
        verbose_name="Status da Solicitação"
    )
    request_date = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação")
    action_date = models.DateTimeField(null=True, blank=True, verbose_name="Data da Ação do Destinatário")
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Conclusão Efetiva")

    initiator_notes = models.TextField(blank=True, null=True, verbose_name="Observações do Solicitante")
    recipient_notes = models.TextField(blank=True, null=True, verbose_name="Observações do Destinatário (ao aceitar/rejeitar)")
    history = HistoricalRecords()

    class Meta:
        ordering = ['-request_date']
        verbose_name = "Solicitação de Transferência de Titularidade"
        verbose_name_plural = "Solicitações de Transferência de Titularidade"

    def __str__(self):
        animal_count = self.animals.count()
        return f"Solicitação de {self.initiated_by.username} para {self.requested_to.username} ({animal_count} animal(is)) - {self.get_status_display()}"