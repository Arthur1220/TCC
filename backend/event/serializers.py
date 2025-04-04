from rest_framework import serializers
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'

class WeighingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weighing
        fields = '__all__'

class VacineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacine
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class ReproductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reproduction
        fields = '__all__'

class SlaughterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slaughter
        fields = '__all__'

class SpecialOccurrencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOccurrences
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'