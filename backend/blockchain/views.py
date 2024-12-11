from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Status, Blockchain
from django.core.exceptions import ObjectDoesNotExist
from .serializers import StatusSerializer, BlockchainSerializer

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]

class BlockchainViewSet(ModelViewSet):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'animal': request.data['animal'],
            'event': request.data['event'],
            'transaction_hash': request.data['transaction_hash'],
            'owner': request.user.id,
            'status': request.data['status']
        }

        serializer = BlockchainSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id=None):
        if id:
            try:
                blockchain = Blockchain.objects.get(pk=id)
                serializer = BlockchainSerializer(blockchain)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            blockchains = Blockchain.objects.all()
            serializer = BlockchainSerializer(blockchains, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_filters = [field.name for field in Blockchain._meta.fields]

        for key, value in query_params.items():
            if key in allowed_filters:
                filters[key] = value

        try:
            blockchains = Blockchain.objects.filter(**filters)
            serializer = BlockchainSerializer(blockchains, many=True)
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