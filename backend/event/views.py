from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event
from django.core.exceptions import ObjectDoesNotExist
from .serializers import BatchEventRegisterSerializer, MovementSerializer, WeighingSerializer, VacineSerializer, MedicineSerializer, ReproductionSerializer, SlaughterSerializer, SpecialOccurrencesSerializer, EventTypeSerializer, EventSerializer
from django.db import transaction # Importe transaction para garantir atomicidade

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
    def register(request):
        data = {
            'animal': request.data['animal'],
            'event_type': request.data['event_type'],
            'date': request.data['date'],
            'location': request.data['location'],
            'observations': request.data['observations'],
            'recorded_by': request.user.id
        }

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    @transaction.atomic # Garante que todas as operações sejam bem-sucedidas ou nenhuma seja
    def register_batch_event(request):
        serializer = BatchEventRegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                # O método create do serializer irá criar os eventos e seus detalhes
                events_created = serializer.save()
                return Response({
                    "message": f"{len(events_created)} eventos registrados com sucesso para o lote.",
                    "events": [EventSerializer(e).data for e in events_created]
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Se algo der errado dentro do transaction.atomic, ele fará um rollback
                return Response({"error": f"Erro ao registrar eventos em lote: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                event = Event.objects.get(pk=id, recorded_by=request.user.id)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = Event.objects.filter(recorded_by=request.user.id)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_filters = [field.name for field in Event._meta.fields]

        for key, value in query_params.items():
            if key in allowed_filters:
                filters[key] = value

        try:
            events = Event.objects.filter(**filters)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            event = Event.objects.get(pk=id)
            event.delete()
            return Response({'message': 'Event deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            event = Event.objects.get(pk=id)
            serializer = EventSerializer(instance=event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
