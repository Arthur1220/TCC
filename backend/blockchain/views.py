from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import BlockchainStatus, Blockchain
from .serializers import BlockchainStatusSerializer, BlockchainSerializer # Importe os serializers
# Importar os modelos Animal, Event e User para usar no select_related se necessário
# from animal.models import Animal
# from event.models import Event
# from user.models import User

class BlockchainStatusViewSet(ModelViewSet):
    queryset = BlockchainStatus.objects.all()
    serializer_class = BlockchainStatusSerializer
    permission_classes = [AllowAny] # Permissões para o status, ajuste conforme necessário

class BlockchainViewSet(ModelViewSet):
    # Adicione select_related aqui para otimizar todas as operações de listagem/recuperação
    # que usam este queryset base (como list, retrieve, etc., se você os habilitasse)
    queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')
    serializer_class = BlockchainSerializer
    # permission_classes = [IsAuthenticated] # Defina uma permissão padrão para o ViewSet se usar seus métodos padrão (list, retrieve, etc.)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'animal': request.data.get('animal'), # Use .get() para evitar KeyError se o campo não existir
            'event': request.data.get('event'),
            'transaction_hash': request.data.get('transaction_hash'),
            'owner': request.user.id, # O owner é o usuário logado
            'status': request.data.get('status'),
        }

        serializer = BlockchainSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id=None):
        # Otimiza a consulta para carregar os objetos relacionados
        queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')

        if id:
            try:
                blockchain = queryset.get(pk=id)
                serializer = BlockchainSerializer(blockchain)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            blockchains = queryset.all() # Usar o queryset otimizado
            serializer = BlockchainSerializer(blockchains, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def filter_get(request):
        query_params = request.query_params
        
        # Otimiza a consulta para carregar os objetos relacionados
        queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')

        # Filtros para campos diretos (transaction_hash, registration_date, etc.)
        for field_name in ['transaction_hash', 'registration_date']: # Adicione outros campos diretos se necessário
            if field_name in query_params:
                queryset = queryset.filter(**{f'{field_name}__icontains': query_params[field_name]}) # Use icontains para busca parcial de strings

        # Filtros para chaves estrangeiras (pelo ID ou pelo nome do campo relacionado)
        if 'animal_id' in query_params:
            queryset = queryset.filter(animal__id=query_params['animal_id'])
        if 'event_id' in query_params:
            queryset = queryset.filter(event__id=query_params['event_id'])
        if 'owner_id' in query_params:
            queryset = queryset.filter(owner__id=query_params['owner_id'])
        if 'status_id' in query_params: # Se você filtrar pelo ID do status
            queryset = queryset.filter(status__id=query_params['status_id'])
        elif 'status_name' in query_params: # Se você filtrar pelo nome do status
             queryset = queryset.filter(status__name__icontains=query_params['status_name'])

        try:
            serializer = BlockchainSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            blockchain = Blockchain.objects.get(pk=id)
            blockchain.delete()
            return Response({'message': 'Blockchain deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            blockchain = Blockchain.objects.get(pk=id)
            serializer = BlockchainSerializer(instance=blockchain, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)