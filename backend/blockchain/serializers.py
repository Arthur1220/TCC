from rest_framework import serializers
from .models import Blockchain, BlockchainStatus

class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blockchain
        fields = '__all__'

class BlockchainStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainStatus
        fields = '__all__'