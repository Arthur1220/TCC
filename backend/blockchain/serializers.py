from rest_framework import serializers
from .models import Blockchain, BlockchainStatus
# Importar os serializers dos modelos relacionados
from user.serializers import UserSerializer # Supondo que UserSerializer está em user/serializers.py
from animal.serializers import AnimalSerializer # Você precisará criar ou ter este serializer
from event.serializers import EventSerializer # Você precisará criar ou ter este serializer

class BlockchainStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainStatus
        fields = '__all__'

# BlockchainSerializer com campos aninhados para os detalhes dos objetos relacionados
class BlockchainSerializer(serializers.ModelSerializer):
    # Campos SerializerMethodField para aninhar os detalhes
    # Usamos SerializerMethodField para ter controle total sobre o que é serializado
    # e para evitar recursão ou problemas de importação circular se os serializers forem complexos.
    animal_details = serializers.SerializerMethodField()
    event_details = serializers.SerializerMethodField()
    owner_details = serializers.SerializerMethodField()
    status_details = serializers.SerializerMethodField() # Para os detalhes do status

    class Meta:
        model = Blockchain
        fields = (
            'id', 'animal', 'event', 'transaction_hash', 'registration_date', 'owner', 'status', 'animal_details', 'event_details', 'owner_details', 'status_details', 'transaction_cost', 'cost_currency_symbol' 
        )
        read_only_fields = ('registration_date',) # A data de registro é automática

    # Métodos para obter os dados detalhados
    def get_animal_details(self, obj):
        if obj.animal:
            return AnimalSerializer(obj.animal).data
        return None

    def get_event_details(self, obj):
        if obj.event:
            return EventSerializer(obj.event).data
        return None

    def get_owner_details(self, obj):
        if obj.owner:
            # Você pode querer um serializer mais leve para o owner aqui
            # mas UserSerializer deve funcionar se não houver recursão infinita
            return UserSerializer(obj.owner).data
        return None

    def get_status_details(self, obj):
        if obj.status:
            return BlockchainStatusSerializer(obj.status).data
        return None