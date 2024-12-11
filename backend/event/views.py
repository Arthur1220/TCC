from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import EventType, Event
from django.core.exceptions import ObjectDoesNotExist
from .serializers import EventTypeSerializer, EventSerializer

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
            'event_date': request.data['event_date'],
            'location': request.data['location'],
            'observations': request.data['observations'],
            'recorded_by': request.user.id
        }

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id=None):
        if id:
            try:
                event = Event.objects.get(pk=id)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
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
