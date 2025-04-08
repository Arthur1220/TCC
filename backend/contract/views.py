from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .web3_client import register_event, get_number_of_events, get_event_by_index, is_active, add_registrar, remove_registrar

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
        print("DEBUG - Received payload:", request.data)

        event_id_raw = request.data.get("event_id")
        animal_id_raw = request.data.get("animal_id")
        event_type_raw = request.data.get("event_type")
        data_hash = request.data.get("data_hash")
        user_hash = request.data.get("user_hash")

        if not event_id_raw or not animal_id_raw or not event_type_raw or not data_hash or not user_hash:
            raise ValueError("Missing required fields: certifique-se de que 'event_id', 'animal_id', 'event_type', 'data_hash' e 'user_hash' estejam preenchidos.")

        event_id = int(event_id_raw)
        animal_id = int(animal_id_raw)
        event_type = int(event_type_raw)
        print(f"DEBUG - Parsed values: event_id={event_id}, animal_id={animal_id}, event_type={event_type}, data_hash='{data_hash}', user_hash='{user_hash}'")

        tx_hash = register_event(event_id, animal_id, event_type, data_hash, user_hash)
        print("DEBUG - Transação realizada. TX Hash:", tx_hash)
        return Response({"tx_hash": tx_hash}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR in register_contract_event:", e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_contract_event(request, animal_id):
    try:
        index = int(request.query_params.get("index", 0))
        event_data = get_event_by_index(animal_id, index)
        keys = ["eventId", "animalId", "eventType", "dataHash", "registrant", "userHash", "timestamp"]
        data = dict(zip(keys, event_data))
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_number_events(request, animal_id):
    try:
        # Aqui, já temos o animal_id vindo da URL, não precisamos extraí-lo dos query params.
        count = get_number_of_events(animal_id)
        return Response({"count": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_registrar_view(request):
    print("DEBUG - Corpo recebido:", request.data)  # <-- ESSENCIAL
    try:
        registrar = request.data.get("registrar_address")
        if not registrar:
            return Response({"error": "Parâmetro 'registrar_address' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        tx_hash = add_registrar(registrar)
        return Response({"tx_hash": tx_hash}, status=status.HTTP_200_OK)
    except Exception as e:
        # Log para depuração
        print("ERROR in add_registrar_view:", e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_registrar_view(request):
    try:
        registrar = request.data.get("registrar")
        if not registrar:
            return Response({"error": "Registrar address is required."}, status=status.HTTP_400_BAD_REQUEST)
        tx_hash = remove_registrar(registrar)
        return Response({"tx_hash": tx_hash}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)