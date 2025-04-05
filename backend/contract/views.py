from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .web3_client import register_event, get_number_of_events, get_event_by_index, is_active

@api_view(['GET'])
@permission_classes([AllowAny])
def contract_status(request):
    try:
        active = is_active()
        return Response({"active": active}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_contract_event(request):
    try:
        event_id = int(request.data.get("event_id"))
        animal_id = int(request.data.get("animal_id"))
        event_type = int(request.data.get("event_type"))
        data_hash = request.data.get("data_hash")
        user_hash = request.data.get("user_hash")
        tx_hash = register_event(event_id, animal_id, event_type, data_hash, user_hash)
        return Response({"tx_hash": tx_hash}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_contract_event(request):
    try:
        animal_id = int(request.query_params.get("animal_id"))
        index = int(request.query_params.get("index", 0))
        event_data = get_event_by_index(animal_id, index)
        keys = ["eventId", "animalId", "eventType", "dataHash", "registrant", "userHash", "timestamp"]
        data = dict(zip(keys, event_data))
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_number_events(request):
    try:
        animal_id = int(request.query_params.get("animal_id"))
        count = get_number_of_events(animal_id)
        return Response({"count": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
