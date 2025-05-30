from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import contract.web3_client as web3_client


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def contract_status(request):
    """Retorna se o contrato está ativo."""
    try:
        return Response({"active": web3_client.is_active()}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_contract_event(request, animal_id):
    """Retorna um evento específico por índice."""
    try:
        index = int(request.query_params.get("index", 0))
        ev = web3_client.get_event_by_index(animal_id, index)
        keys = ["eventId", "animalId", "eventType", "dataHash", "registrant", "userHash", "timestamp"]
        return Response(dict(zip(keys, ev)), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def list_contract_events(request, animal_id):
    """Retorna todos os eventos de um animal."""
    try:
        evs = web3_client.get_events_by_animal(animal_id)
        keys = ["eventId", "animalId", "eventType", "dataHash", "registrant", "userHash", "timestamp"]
        # transforma lista de tuples em lista de dicts
        data = [dict(zip(keys, ev)) for ev in evs]
        return Response({"events": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_number_events(request):
    """Retorna a contagem de eventos de um animal via ?animal_id=."""
    pid = request.query_params.get("animal_id")
    if pid is None:
        return Response({"error": "animal_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        count = web3_client.get_number_of_events(int(pid))
        return Response({"count": count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated]) # Ou quem quer que possa chamar isso
def register_contract_event(request):
    data = request.data
    required = ["event_id", "animal_id", "event_type", "data_hash", "user_hash"]
    if not all(field in data for field in required):
        return Response(
            {"error": f"Campos faltando: {', '.join(required)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        # A função web3_client.register_event agora retorna um dicionário
        tx_details = web3_client.register_event(
            int(data["event_id"]),
            int(data["animal_id"]),
            int(data["event_type"]),
            data["data_hash"],
            data["user_hash"],
        )
        # tx_details deve conter: "tx_hash", "transaction_cost_wei", "gas_used", "effective_gas_price_wei"
        return Response(tx_details, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_registrar_view(request):
    """Chama addRegistrar no contrato."""
    addr = request.data.get("registrar_address")
    if not addr:
        return Response({"error": "registrar_address é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        txh = web3_client.add_registrar(addr)
        return Response({"tx_hash": txh}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_registrar_view(request):
    try:
        registrar = request.data.get("registrar_address")
        if not registrar:
            return Response({"error": "Registrar address is required."}, status=status.HTTP_400_BAD_REQUEST)
        tx_hash = web3_client.remove_registrar(registrar)
        return Response({"tx_hash": tx_hash}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_registrar_view(request):
    """Chama removeRegistrar no contrato."""
    addr = request.data.get("registrar_address")
    if not addr:
        return Response({"error": "registrar_address é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        txh = web3_client.remove_registrar(addr)
        return Response({"tx_hash": txh}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pause_contract_view(request):
    """Chama pause() no contrato."""
    try:
        txh = web3_client.pause_contract()
        return Response({"tx_hash": txh}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unpause_contract_view(request):
    """Chama unpause() no contrato."""
    try:
        txh = web3_client.unpause_contract()
        return Response({"tx_hash": txh}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
