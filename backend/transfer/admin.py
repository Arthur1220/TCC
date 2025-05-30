# transfer/admin.py
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import OwnershipTransferRequest

@admin.register(OwnershipTransferRequest)
class OwnershipTransferRequestAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 
        'initiated_by', 
        'requested_to', 
        'status', 
        'request_date', 
        'action_date', 
        'completion_date',
        'get_animal_count'
    )
    list_filter = ('status', 'request_date', 'initiated_by', 'requested_to')
    search_fields = (
        'initiated_by__username', 
        'requested_to__username', 
        'animals__identification', # Para buscar por identificação de animal
    )
    readonly_fields = ('request_date', 'action_date', 'completion_date')
    # Para mostrar animais M2M de forma mais amigável (opcional, pode ser pesado para muitos animais)
    # filter_horizontal = ('animals',) # Ou filter_vertical

    def get_animal_count(self, obj):
        return obj.animals.count()
    get_animal_count.short_description = 'Qtd. Animais'

    # Se você quiser ver os campos M2M na visualização de detalhes:
    # Descomente filter_horizontal ou filter_vertical, ou use um inline.
    # Exemplo de inline (mais complexo, mas útil para detalhes):
    # class AnimalInline(admin.TabularInline): # ou StackedInline
    #     model = OwnershipTransferRequest.animals.through # Acessa a tabela through do M2M
    #     extra = 0
    #     verbose_name = "Animal na Solicitação"
    #     verbose_name_plural = "Animais na Solicitação"
    #     # Você pode querer mostrar campos do Animal aqui, o que exigiria personalizar o inline.
    #     # Por padrão, mostrará apenas o ID do animal.

    # inlines = [AnimalInline] # Descomente se usar o inline