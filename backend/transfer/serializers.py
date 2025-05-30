from rest_framework import serializers
from .models import OwnershipTransferRequest
from animal.models import Animal # Para validação e representação
from animal.serializers import AnimalSerializer # Para representação aninhada de animais
from django.contrib.auth import get_user_model

User = get_user_model()

class OwnershipTransferRequestSerializer(serializers.ModelSerializer):
    # Campos para exibir informações legíveis (read-only)
    initiated_by_username = serializers.CharField(source='initiated_by.username', read_only=True)
    # requested_to_username será derivado do campo 'requested_to' do modelo
    requested_to_username = serializers.CharField(source='requested_to.username', read_only=True) 
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    animals_details = AnimalSerializer(source='animals', many=True, read_only=True)

    # Campo de escrita para 'animals'
    animals = serializers.PrimaryKeyRelatedField(
        queryset=Animal.objects.all(),
        many=True,
        write_only=True
    )
    
    # Campo de escrita para 'requested_to'. O nome do campo no serializer será 'requested_to'.
    # DRF é inteligente o suficiente para usar o valor fornecido (um ID) para popular o ForeignKey 'requested_to' no modelo.
    # Não precisamos de 'requested_to_id' como um nome de campo separado no serializer se o nome do campo do modelo é 'requested_to'.
    # Se quisermos que o payload JSON tenha 'requested_to_id', mantemos como estava, mas ajustamos 'fields'.
    # Vamos manter 'requested_to_id' no payload para consistência com os testes e ajustar 'fields'.

    requested_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='requested_to', # O valor deste campo irá para o atributo 'requested_to' do modelo.
        write_only=True,
        label="ID do Destinatário Solicitado" # Label opcional para forms do DRF
    )
    
    # Para leitura do 'requested_to' (PK), o DRF já faz isso por padrão se 'requested_to' estiver nos fields.
    # E o 'requested_to_username' já lida com a leitura do nome.

    class Meta:
        model = OwnershipTransferRequest
        fields = [
            'id',
            'animals', # write_only
            'animals_details', # read_only
            'initiated_by', # read_only (preenchido na view)
            'initiated_by_username', # read_only
            
            # Para escrita, o payload JSON usará 'requested_to_id'.
            # Para leitura, o objeto 'requested_to' (FK) no modelo será serializado como seu PK
            # se 'requested_to' estiver listado abaixo e não for write_only.
            'requested_to_id', # write_only
            'requested_to', # Este é o campo do modelo, será read_only por padrão se 'requested_to_id' com source existir.
                            # Ou, para ser explícito, defina-o como read_only.
            'requested_to_username', # read_only
            
            'status', # read_only (default no modelo)
            'status_display', # read_only
            'request_date', # read_only
            'action_date', # read_only
            'completion_date', # read_only
            'initiator_notes',
            'recipient_notes',
        ]
        read_only_fields = [
            'initiated_by', 'status', 'request_date', 
            'action_date', 'completion_date',
            'requested_to' # Torna 'requested_to' (o campo do modelo) explicitamente read_only no serializer
                           # já que estamos usando 'requested_to_id' para escrita.
        ]

    def validate_animals(self, animal_instances): # O valor já são instâncias de Animal
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Contexto da requisição não encontrado.")
        user = request.user
        for animal in animal_instances:
            if animal.owner != user:
                raise serializers.ValidationError(f"O animal com ID {animal.id} ({animal.identification}) não pertence a você ou não pode ser transferido.")
            if animal.status.name.lower() in ['vendido', 'morto']:
                 raise serializers.ValidationError(f"O animal {animal.identification} tem um status ({animal.status.name}) que não permite transferência.")
        if not animal_instances:
            raise serializers.ValidationError("Pelo menos um animal deve ser selecionado para a transferência.")
        return animal_instances

    def validate_requested_to_id(self, requested_to_user_instance): # O valor já é uma instância de User
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Contexto da requisição não encontrado.")
        if requested_to_user_instance == request.user:
            raise serializers.ValidationError("Você não pode solicitar uma transferência para si mesmo.")
        return requested_to_user_instance

    def create(self, validated_data):
        # 'animals' em validated_data já são as instâncias de Animal
        # 'requested_to' em validated_data já é a instância de User (devido ao source em requested_to_id)
        
        # Remove 'animals' para definir separadamente com .set()
        animals_instances = validated_data.pop('animals')
        
        # 'initiated_by' será passado pelo método save() da view.
        # 'requested_to' já está correto em validated_data devido ao source='requested_to' em requested_to_id.
        
        transfer_request = OwnershipTransferRequest.objects.create(**validated_data)
        transfer_request.animals.set(animals_instances)
        return transfer_request

class TransferActionSerializer(serializers.Serializer):
    """
    Serializer para ações de aceitar/rejeitar uma solicitação.
    """
    recipient_notes = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    # Não precisa de outros campos, pois a ação (aceitar/rejeitar) será definida pela URL/View.