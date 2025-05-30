from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction # Importe transaction para garantir atomicidade
from django.shortcuts import get_object_or_404
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event
from .serializers import BatchEventRegisterSerializer, MovementSerializer, WeighingSerializer, VacineSerializer, MedicineSerializer, ReproductionSerializer, SlaughterSerializer, SpecialOccurrencesSerializer, EventTypeSerializer, EventSerializer
from animal.models import Animal # Para buscar Animal
from blockchain.models import Blockchain, BlockchainStatus # Para registrar na blockchain
from .utils import generate_event_data_hash # Nossa função de hash
import contract.web3_client as web3_client

class MovementViewSet(ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'event': request.data['event'],
            'origin_property': request.data['origin_property'],
            'destination_property': request.data['destination_property'],
            'date': request.data['date'],
            'reason': request.data['reason']
        }

        serializer = MovementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                movement = Movement.objects.get(pk=id)
                serializer = MovementSerializer(movement)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            movements = Movement.objects.all()
            serializer = MovementSerializer(movements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_filters = [field.name for field in Movement._meta.fields]

        for key, value in query_params.items():
            if key in allowed_filters:
                filters[key] = value

        try:
            movements = Movement.objects.filter(**filters)
            serializer = MovementSerializer(movements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            movement = Movement.objects.get(pk=id)
            movement.delete()
            return Response({'message': 'Movement deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            movement = Movement.objects.get(pk=id)
            serializer = MovementSerializer(instance=movement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
        
class WeighingViewSet(ModelViewSet):
    queryset = Weighing.objects.all()
    serializer_class = WeighingSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'event': request.data['event'],
            'weight': request.data['weight'],
            'date': request.data['date'],
        }

        serializer = WeighingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                weighing = Weighing.objects.get(pk=id)
                serializer = WeighingSerializer(weighing)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Weighing not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            weighings = Weighing.objects.all()
            serializer = WeighingSerializer(weighings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_filters = [field.name for field in Weighing._meta.fields]

        for key, value in query_params.items():
            if key in allowed_filters:
                filters[key] = value

        try:
            weighings = Weighing.objects.filter(**filters)
            serializer = WeighingSerializer(weighings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            weighing = Weighing.objects.get(pk=id)
            weighing.delete()
            return Response({'message': 'Weighing deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Weighing not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            weighing = Weighing.objects.get(pk=id)
            serializer = WeighingSerializer(instance=weighing, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Weighing not found'}, status=status.HTTP_404_NOT_FOUND)
        
class VacineViewSet(ModelViewSet):
    queryset = Vacine.objects.all()
    serializer_class = VacineSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'event': request.data['event'],
            'name': request.data['name'],
            'manufacturer': request.data['manufacturer'],
            'batch': request.data['batch'],
            'validity': request.data['validity'],
            'dose': request.data['dose'],
            'next_dose_date': request.data['next_dose_date'],
        }

        serializer = VacineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                vacine = Vacine.objects.get(pk=id)
                serializer = VacineSerializer(vacine)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Vacine not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            vacines = Vacine.objects.all()
            serializer = VacineSerializer(vacines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_filters = [field.name for field in Vacine._meta.fields]

        for key, value in query_params.items():
            if key in allowed_filters:
                filters[key] = value

        try:
            vacines = Vacine.objects.filter(**filters)
            serializer = VacineSerializer(vacines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            vacine = Vacine.objects.get(pk=id)
            vacine.delete()
            return Response({'message': 'Vacine deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Vacine not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            vacine = Vacine.objects.get(pk=id)
            serializer = VacineSerializer(instance=vacine, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Vacine not found'}, status=status.HTTP_404_NOT_FOUND)
        
class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'event': request.data['event'],
            'name': request.data['name'],
            'manufacturer': request.data['manufacturer'],
            'batch': request.data['batch'],
            'validity': request.data['validity'],
            'dose': request.data['dose'],
            'next_dose_date': request.data['next_dose_date'],
            'reason': request.data['reason'],
            'withdrawal_time': request.data['withdrawal_time'],
        }

        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id is not None:
            try:
                item = Medicine.objects.get(pk=id)
                serializer = MedicineSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        items = Medicine.objects.all()
        serializer = MedicineSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def filter_get(request):
        filters = {}
        for key, value in request.query_params.items():
            if key in [f.name for f in Medicine._meta.fields]:
                filters[key] = value
        try:
            results = Medicine.objects.filter(**filters)
            serializer = MedicineSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Search error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            item = Medicine.objects.get(pk=id)
            item.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @api_view(["PUT"])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            item = Medicine.objects.get(pk=id)
            serializer = MedicineSerializer(instance=item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            
class ReproductionViewSet(ModelViewSet):
    queryset = Reproduction.objects.all()
    serializer_class = ReproductionSerializer

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            "event": request.data.get("event"),
            'reproduction_type': request.data.get("reproduction_type"),
            'male_id': request.data.get("male_id"),
            'female_id': request.data.get("female_id"),
            'date': request.data.get("date"),
            'result': request.data.get("result"),
        }
        serializer = ReproductionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                reproduction = Reproduction.objects.get(pk=id)
                serializer = ReproductionSerializer(reproduction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Reproduction.objects.all()
        serializer = ReproductionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def filter_get(request):
        filters = {}
        for key, value in request.query_params.items():
            if key in [f.name for f in Reproduction._meta.fields]:
                filters[key] = value
        try:
            results = Reproduction.objects.filter(**filters)
            serializer = ReproductionSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Search error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            reproduction = Reproduction.objects.get(pk=id)
            reproduction.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @api_view(["PUT"])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            reproduction = Reproduction.objects.get(pk=id)
            serializer = ReproductionSerializer(instance=reproduction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

class SlaughterViewSet(ModelViewSet):
    queryset = Slaughter.objects.all()
    serializer_class = SlaughterSerializer

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            "event": request.data.get("event"),
            "date": request.data.get("date"),
            "location": request.data.get("location"),
            "final_weight": request.data.get("final_weight"),
            "inspection_result": request.data.get("inspection_result"),
        }
        serializer = SlaughterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                slaughter = Slaughter.objects.get(pk=id)
                serializer = SlaughterSerializer(slaughter)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Slaughter.objects.all()
        serializer = SlaughterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def filter_get(request):
        filters = {}
        for key, value in request.query_params.items():
            if key in [f.name for f in Slaughter._meta.fields]:
                filters[key] = value
        try:
            results = Slaughter.objects.filter(**filters)
            serializer = SlaughterSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Search error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            slaughter = Slaughter.objects.get(pk=id)
            slaughter.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @api_view(["PUT"])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            slaughter = Slaughter.objects.get(pk=id)
            serializer = SlaughterSerializer(instance=slaughter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

class SpecialOccurrencesViewSet(ModelViewSet):
    queryset = SpecialOccurrences.objects.all()
    serializer_class = SpecialOccurrencesSerializer

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            "event": request.data.get("event"),
            "occurrence_type": request.data.get("occurrence_type"),
            "description": request.data.get("description"),
            "date": request.data.get("date"),
            "actions_taken": request.data.get("actions_taken"),
        }
        serializer = SpecialOccurrencesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                special_occurrence = SpecialOccurrences.objects.get(pk=id)
                serializer = SpecialOccurrencesSerializer(special_occurrence)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        queryset = SpecialOccurrences.objects.all()
        serializer = SpecialOccurrencesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def filter_get(request):
        filters = {}
        for key, value in request.query_params.items():
            if key in [f.name for f in SpecialOccurrences._meta.fields]:
                filters[key] = value
        try:
            results = SpecialOccurrences.objects.filter(**filters)
            serializer = SpecialOccurrencesSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Search error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            special_occurrence = SpecialOccurrences.objects.get(pk=id)
            special_occurrence.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @api_view(["PUT"])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            special_occurrence = SpecialOccurrences.objects.get(pk=id)
            serializer = SpecialOccurrencesSerializer(instance=special_occurrence, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

class EventTypeViewSet(ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [AllowAny]

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @transaction.atomic # Garante atomicidade para DB e Blockchain
    def register(request):
        # Criação do Evento Principal
        event_data = {
            'animal': request.data.get('animal'),
            'event_type': request.data.get('event_type'),
            'date': request.data.get('date'),
            'location': request.data.get('location'),
            'observations': request.data.get('observations'),
            'recorded_by': request.user.id
        }
        event_serializer = EventSerializer(data=event_data)
        if not event_serializer.is_valid():
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        event_instance = event_serializer.save()

        # Criação do Evento Específico (Movimento, Pesagem, etc.)
        # Esta lógica deve ser adaptada baseada em como seu frontend envia os dados
        # Assumindo que o frontend envia 'details' com os dados específicos.
        event_type_name = event_instance.event_type.name.lower()
        details_data = request.data.get('details', {}) # Espera um campo 'details' no payload
        specific_event_created = False

        if details_data: # Só tenta criar detalhes se 'details_data' for fornecido
            details_data['event'] = event_instance.id # Adiciona FK para o Evento principal
             # Mantém a data do detalhe igual à do evento principal se não especificada
            if 'date' not in details_data:
                details_data['date'] = event_instance.date 

            specific_serializer = None
            if event_type_name == 'movimento' or event_type_name == 'movimentação':
                specific_serializer = MovementSerializer(data=details_data)
            elif event_type_name == 'pesagem':
                specific_serializer = WeighingSerializer(data=details_data)
            elif event_type_name == 'vacinação' or event_type_name == 'vacina':
                specific_serializer = VacineSerializer(data=details_data)
            elif event_type_name == 'medicação' or event_type_name == 'medicamento':
                specific_serializer = MedicineSerializer(data=details_data)
            elif event_type_name == 'reprodução' or event_type_name == 'reproducao':
                specific_serializer = ReproductionSerializer(data=details_data)
            elif event_type_name == 'abate':
                specific_serializer = SlaughterSerializer(data=details_data)
            elif event_type_name == 'ocorrência especial' or event_type_name == 'ocorrencia especial':
                specific_serializer = SpecialOccurrencesSerializer(data=details_data)

            if specific_serializer:
                if specific_serializer.is_valid():
                    specific_serializer.save()
                    specific_event_created = True
                else:
                    # Se o detalhe falhar, faz rollback de tudo
                    transaction.set_rollback(True)
                    return Response({
                        "event_errors": event_serializer.data, # Evento principal foi salvo temporariamente
                        "detail_errors": specific_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif details_data: # Se details_data foi enviado mas o tipo não correspondeu
                 transaction.set_rollback(True)
                 return Response(
                     {"error": f"Detalhes específicos fornecidos, mas o tipo de evento '{event_type_name}' não requer ou não suporta detalhes desta forma."},
                     status=status.HTTP_400_BAD_REQUEST
                 )


        # Registro na Blockchain
        try:
            user_hash_for_blockchain = request.user.user_hash
            if not user_hash_for_blockchain: # Gera um se não existir, embora deva existir
                user_hash_for_blockchain = "default_user_placeholder_hash" # Ou maneje o erro
            
            data_hash = generate_event_data_hash(event_instance)

            # Parâmetros para o contrato inteligente
            # O contrato espera event_id, animal_id, event_type_id (como inteiros)
            contract_event_id = event_instance.id # Usamos o ID do evento no nosso DB
            contract_animal_id = event_instance.animal.id
            contract_event_type_id = event_instance.event_type.id

            # Chama web3_client que agora retorna um dicionário com detalhes da tx
            tx_blockchain_details = web3_client.register_event(
                event_id=contract_event_id,
                animal_id=contract_animal_id,
                event_type=contract_event_type_id,
                data_hash=data_hash,
                user_hash=user_hash_for_blockchain
            )

            # Extrai os detalhes retornados
            tx_hash = tx_blockchain_details.get("tx_hash")
            transaction_cost_wei = tx_blockchain_details.get("transaction_cost_wei")
            # gas_used = tx_blockchain_details.get("gas_used")
            # effective_gas_price_wei = tx_blockchain_details.get("effective_gas_price_wei")

            # Salva o registro da blockchain no DB
            status_confirmado, _ = BlockchainStatus.objects.get_or_create(name="Confirmado")
            Blockchain.objects.create(
                animal=event_instance.animal,
                event=event_instance,
                transaction_hash=tx_hash,
                owner=request.user,
                status=status_confirmado,
                # SALVANDO O CUSTO AQUI:
                transaction_cost=transaction_cost_wei, # Já vem como string, DecimalField aceita
                cost_currency_symbol="WEI" # Ou a unidade da sua L2
            )
            
            # Prepara a resposta final com todos os dados
            final_response_data = event_serializer.data
            if specific_event_created and specific_serializer: # Adiciona detalhes se foram criados
                final_response_data['details'] = specific_serializer.data

            final_response_data['blockchain_registration'] = {
                "tx_hash": tx_hash,
                "cost_wei": transaction_cost_wei
                # "gas_used": gas_used, # Opcional
                # "effective_gas_price_wei": effective_gas_price_wei # Opcional
            }
            
            return Response(final_response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Se o registro na blockchain falhar, faz rollback de tudo (graças ao @transaction.atomic)
            transaction.set_rollback(True) # Garante o rollback em caso de exceção não pega pelo atomic
            return Response({
                "error": "Falha ao registrar o evento na blockchain.",
                "event_db_id": event_instance.id if event_instance else None, # ID do evento que falhou na blockchain
                "blockchain_error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @transaction.atomic # Garante que todas as operações sejam bem-sucedidas ou nenhuma seja
    def register_batch_event(request):
        # O serializer BatchEventRegisterSerializer já espera animal_ids
        # Se o frontend envia animal_group_id, o BatchEventRegisterSerializer precisa ser ajustado
        # para resolver animal_group_id para uma lista de animal_ids.
        # Por enquanto, vamos seguir o serializer atual.
        
        batch_serializer = BatchEventRegisterSerializer(data=request.data, context={'request': request})
        if not batch_serializer.is_valid():
            return Response(batch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # O método .save() do BatchEventRegisterSerializer já lida com a criação
        # dos eventos principais e seus detalhes específicos.
        # Precisamos modificar o .save() ou o .create() do BatchEventRegisterSerializer
        # para incluir a lógica de blockchain para cada evento criado.
        # OU, fazemos aqui após o serializer.save() retornar os eventos criados.
        # A segunda abordagem é mais limpa para separar responsabilidades.

        # Assumindo que serializer.save() agora retorna os `Event` instances criados.
        # Se não, precisaremos buscar ou o serializer precisa ser modificado.
        # O serializer atual retorna uma lista de 'eventos criados' (objetos Event).

        try:
            # Esta chamada ao serializer.save() já cria os eventos no DB
            # (Event e seus detalhes específicos como Movement, Weighing, etc.)
            # Veja o método .create() do seu BatchEventRegisterSerializer
            events_created_in_db = batch_serializer.save() 
            
            blockchain_registrations_summary = []
            status_confirmado, _ = BlockchainStatus.objects.get_or_create(name="Confirmado")
            status_falhou, _ = BlockchainStatus.objects.get_or_create(name="Falhou") # Para falhas individuais

            user_hash_for_blockchain = request.user.user_hash
            if not user_hash_for_blockchain:
                 user_hash_for_blockchain = "default_user_placeholder_hash" 

            for event_instance in events_created_in_db:
                try:
                    data_hash = generate_event_data_hash(event_instance)
                    
                    contract_event_id = event_instance.id
                    contract_animal_id = event_instance.animal.id
                    contract_event_type_id = event_instance.event_type.id

                    # Chama web3_client que agora retorna um dicionário
                    tx_blockchain_details = web3_client.register_event(
                        event_id=contract_event_id,
                        animal_id=contract_animal_id,
                        event_type=contract_event_type_id,
                        data_hash=data_hash,
                        user_hash=user_hash_for_blockchain
                    )
                    tx_hash = tx_blockchain_details.get("tx_hash")
                    transaction_cost_wei = tx_blockchain_details.get("transaction_cost_wei")

                    Blockchain.objects.create(
                        animal=event_instance.animal,
                        event=event_instance,
                        transaction_hash=tx_hash,
                        owner=request.user,
                        status=status_confirmado,
                        # SALVANDO O CUSTO AQUI:
                        transaction_cost=transaction_cost_wei,
                        cost_currency_symbol="WEI" 
                    )
                    blockchain_registrations_summary.append({
                        "event_db_id": event_instance.id, 
                        "tx_hash": tx_hash, 
                        "cost_wei": transaction_cost_wei,
                        "status": "success"
                    })
                except Exception as blockchain_exc:
                    # Registra a falha na blockchain para este evento específico mas continua o lote
                    Blockchain.objects.create(
                        animal=event_instance.animal,
                        event=event_instance,
                        transaction_hash=f"Falha no registro on-chain: {str(blockchain_exc)[:60]}", # Limita tamanho da msg de erro
                        owner=request.user,
                        status=status_falhou,
                        transaction_cost=None # Ou 0, se preferir
                    )
                    blockchain_registrations_summary.append({
                        "event_db_id": event_instance.id, 
                        "error": str(blockchain_exc), 
                        "status": "failed_on_blockchain"
                    })
                    # Se uma falha na blockchain para UM evento do lote deve reverter TUDO:
                    # transaction.set_rollback(True)
                    # return Response({"error": f"Falha ao registrar evento {event_instance.id} na blockchain: {str(blockchain_exc)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # A decisão acima (continuar ou reverter tudo) depende do seu requisito de negócio.
                    # A implementação atual continua e apenas marca a falha para aquele evento.

            # Se você decidiu que qualquer falha na blockchain reverte tudo, o @transaction.atomic já cuidaria disso
            # se uma exceção não tratada fosse levantada. Se você trata e continua, o rollback não acontece.

            return Response({
                "message": f"{len(events_created_in_db)} eventos processados para o lote.",
                "events_db_ids": [e.id for e in events_created_in_db],
                "blockchain_registrations": blockchain_registrations_summary
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Erro geral durante o processamento do lote (ex: dentro do serializer.save() antes da blockchain)
            return Response({"error": f"Erro ao registrar eventos em lote: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id=None):
        user = request.user

        # Campos para select_related. Ajuste 'animal__breed__specie' se a relação for diferente.
        related_fields = [
            'animal__owner', 
            'animal__breed__specie', # SUPOSIÇÃO: Evento -> Animal -> Raça -> Espécie
            'animal__breed',         # Para dados da Raça
            'animal__group', 
            'animal__status', 
            'event_type', 
            'recorded_by'
        ]

        if id:
            try:
                event = Event.objects.select_related(*related_fields).get(pk=id)
                
                serializer = EventSerializer(event) 
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Evento não encontrado ou acesso não permitido.'}, status=status.HTTP_404_NOT_FOUND)
        else: 
            events_qs = Event.objects.select_related(*related_fields).all().order_by('-date')
            
            serializer = EventSerializer(events_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    @permission_classes([IsAuthenticated]) 
    def filter_get(request):
        query_params = request.query_params
        user = request.user
        
        related_fields = [ # Mesmo select_related da view 'get'
            'animal__owner', 'animal__breed__specie', 'animal__breed',
            'animal__group', 'animal__status', 'event_type', 'recorded_by'
        ]

        filters = {} 
        

        filter_mapping = {
            'animal': 'animal__id',
            'event_type': 'event_type__id',
            'date_after': 'date__gte',
            'date_before': 'date__lte',
            'location': 'location__icontains',
            'owner_id': 'animal__owner__id' 
        }

        for query_key, orm_key in filter_mapping.items():
            value = query_params.get(query_key)
            if value:
                if query_key == 'owner_id':
                    if int(value) != user.id: 
                        continue 
                filters[orm_key] = value
        
        try:
            events_qs = Event.objects.select_related(*related_fields).filter(**filters).order_by('-date')
            serializer = EventSerializer(events_qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

       
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    @transaction.atomic # Para garantir que o evento e o registro na blockchain (se houver) sejam tratados
    def delete(request, id):
        try:
            event = Event.objects.get(pk=id, animal__owner=request.user) # Garante que o usuário é dono
            
            # Opcional: Lógica para interagir com a blockchain para "anular" um evento, se aplicável.
            # Isso dependeria da funcionalidade do seu contrato.
            # Por agora, apenas deletamos do DB.

            # Deleta registros associados na tabela Blockchain
            Blockchain.objects.filter(event=event).delete()
            
            event.delete() # Isso também deletará em cascata os detalhes (Movement, Weighing, etc)
            return Response({'message': 'Evento deletado com sucesso.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Evento não encontrado ou acesso não permitido.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erro ao deletar evento: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    @transaction.atomic
    def update(request, id):
        try:
            event_instance = Event.objects.get(pk=id, animal__owner=request.user)
        except ObjectDoesNotExist:
            return Response({'error': 'Evento não encontrado ou acesso não permitido.'}, status=status.HTTP_404_NOT_FOUND)

        # Atualiza o Evento Principal
        event_data = request.data.copy() # Copia para poder modificar
        event_data['recorded_by'] = request.user.id # Garante que o recorded_by não seja alterado indevidamente
        
        event_serializer = EventSerializer(instance=event_instance, data=event_data, partial=True)
        if not event_serializer.is_valid():
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        updated_event_instance = event_serializer.save()

        # Atualiza/Cria o Evento Específico (Movimento, Pesagem, etc.)
        event_type_name = updated_event_instance.event_type.name.lower()
        details_data = request.data.get('details', {})
        specific_event_updated_or_created = False

        if details_data:
            details_data['event'] = updated_event_instance.id
            if 'date' not in details_data:
                 details_data['date'] = updated_event_instance.date

            specific_model_map = {
                'movimento': (Movement, MovementSerializer),
                'movimentação': (Movement, MovementSerializer),
                'pesagem': (Weighing, WeighingSerializer),
                'vacinação': (Vacine, VacineSerializer),
                'vacina': (Vacine, VacineSerializer),
                'medicação': (Medicine, MedicineSerializer),
                'medicamento': (Medicine, MedicineSerializer),
                'reprodução': (Reproduction, ReproductionSerializer),
                'reproducao': (Reproduction, ReproductionSerializer),
                'abate': (Slaughter, SlaughterSerializer),
                'ocorrência especial': (SpecialOccurrences, SpecialOccurrencesSerializer),
                'ocorrencia especial': (SpecialOccurrences, SpecialOccurrencesSerializer),
            }

            ModelClass, DetailSerializerClass = specific_model_map.get(event_type_name, (None, None))

            if ModelClass and DetailSerializerClass:
                # Tenta buscar um detalhe existente para atualizar, ou cria um novo
                # Acessa via related_name (ex: updated_event_instance.movements)
                related_manager_name = ModelClass._meta.get_field('event').remote_field.name + 's' # Ex: movements, weighings
                if hasattr(updated_event_instance, related_manager_name.lower()): # Verifica se o related_name existe
                    related_manager = getattr(updated_event_instance, related_manager_name.lower())
                    detail_instance = related_manager.first()
                else: # Fallback se o related_name não for o plural padrão ou caso específico
                    try:
                        detail_instance = ModelClass.objects.get(event=updated_event_instance)
                    except ModelClass.DoesNotExist:
                        detail_instance = None
                    except ModelClass.MultipleObjectsReturned: # Tratar caso raro
                        detail_instance = related_manager.first() # Ou outra lógica para pegar o correto

                if detail_instance: # Atualiza existente
                    specific_serializer = DetailSerializerClass(instance=detail_instance, data=details_data, partial=True)
                else: # Cria novo
                    specific_serializer = DetailSerializerClass(data=details_data)
                
                if specific_serializer.is_valid():
                    specific_serializer.save()
                    specific_event_updated_or_created = True
                else:
                    transaction.set_rollback(True)
                    return Response({
                        "event_data": event_serializer.data,
                        "detail_errors": specific_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif details_data : # Detalhes fornecidos mas tipo não mapeado
                 transaction.set_rollback(True)
                 return Response(
                     {"error": f"Detalhes específicos fornecidos, mas o tipo de evento '{event_type_name}' não é gerenciado para detalhes específicos desta forma na atualização."},
                     status=status.HTTP_400_BAD_REQUEST
                 )

        # Re-Registro na Blockchain (se a política for registrar cada atualização)
        # ATENÇÃO: Registrar cada atualização na blockchain pode ser custoso e gerar muitos registros.
        # Considere se isso é realmente necessário ou se apenas o evento original é imutável na blockchain.
        # Se for para atualizar, você precisaria de uma função no contrato para "atualizar" um evento
        # ou marcar o anterior como obsoleto e registrar um novo.
        # Para simplificar, vamos assumir que atualizações no DB não geram novas transações na blockchain,
        # mas se gerassem, a lógica seria similar à do registro.
        # Se for registrar uma nova entrada na blockchain para a atualização:
        try:
            user_hash_for_blockchain = request.user.user_hash or "default_user_placeholder_hash"
            data_hash = generate_event_data_hash(updated_event_instance) # Novo hash com dados atualizados
            
            # O contrato precisaria de uma forma de vincular esta atualização ao evento original na blockchain
            # ou você simplesmente registraria como um novo evento de blockchain.
            # Usaremos os mesmos IDs para registrar, o que pode sobrescrever ou ser tratado pelo contrato.
            contract_event_id = updated_event_instance.id 
            contract_animal_id = updated_event_instance.animal.id
            contract_event_type_id = updated_event_instance.event_type.id

            # tx_hash = web3_client.register_event(...) # Descomente e ajuste se for registrar atualização
            # status_confirmado, _ = BlockchainStatus.objects.get_or_create(name="Confirmado")
            # Blockchain.objects.create(...)

            final_response_data = event_serializer.data
            if specific_event_updated_or_created and specific_serializer:
                final_response_data['details'] = specific_serializer.data
            # final_response_data['blockchain_update_tx_hash'] = tx_hash # Se registrar atualização

            return Response(final_response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Se a atualização na blockchain falhar, mas o DB foi salvo.
            # Dependendo da sua política, você pode querer fazer rollback ou apenas logar.
            # O @transaction.atomic já está ativo, então se esta exceção não for tratada, fará rollback.
            # transaction.set_rollback(True) # Força rollback se você tratar a exceção mas ainda quiser rollback.
            return Response({
                "error": "Evento atualizado no banco de dados, mas falha ao interagir com a blockchain para a atualização.",
                "event_db_id": updated_event_instance.id,
                "blockchain_error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) # Ou 207 Multi-Status
