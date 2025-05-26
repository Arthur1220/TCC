from rest_framework import serializers
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event
from animal.models import Animal

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

class BatchEventRegisterSerializer(serializers.Serializer):
    animal_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Lista de IDs dos animais para os quais o evento será registrado."
    )
    event_type = serializers.IntegerField(
        help_text="ID do tipo de evento (e.g., Vacina, Pesagem)."
    )
    date = serializers.DateTimeField(
        help_text="Data e hora do evento."
    )
    location = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True,
        help_text="Localização do evento."
    )
    observations = serializers.CharField(
        allow_blank=True, allow_null=True, required=False,
        help_text="Observações gerais sobre o evento."
    )

    # Campos específicos para cada tipo de evento (opcional, dependendo do event_type)
    # Estes campos serão validados e usados para criar as instâncias filhas de Event
    movement_details = MovementSerializer(required=False, allow_null=True)
    weighing_details = WeighingSerializer(required=False, allow_null=True)
    vacine_details = VacineSerializer(required=False, allow_null=True)
    medicine_details = MedicineSerializer(required=False, allow_null=True)
    reproduction_details = ReproductionSerializer(required=False, allow_null=True)
    slaughter_details = SlaughterSerializer(required=False, allow_null=True)
    special_occurrences_details = SpecialOccurrencesSerializer(required=False, allow_null=True)

    def validate(self, data):
        event_type_id = data.get('event_type')
        try:
            event_type = EventType.objects.get(id=event_type_id)
        except EventType.DoesNotExist:
            raise serializers.ValidationError({"event_type": "Tipo de evento não encontrado."})

        # Validação condicional baseada no tipo de evento
        if event_type.name.lower() == 'movimento':
            if not data.get('movement_details'):
                raise serializers.ValidationError({"movement_details": "Detalhes de movimento são necessários para este tipo de evento."})
        elif event_type.name.lower() == 'pesagem':
            if not data.get('weighing_details'):
                raise serializers.ValidationError({"weighing_details": "Detalhes de pesagem são necessários para este tipo de evento."})
        # Adicione validações para outros tipos de eventos se eles tiverem campos obrigatórios específicos
        elif event_type.name.lower() == 'vacina':
             if not data.get('vacine_details'):
                raise serializers.ValidationError({"vacine_details": "Detalhes de vacina são necessários para este tipo de evento."})
        elif event_type.name.lower() == 'medicamento':
            if not data.get('medicine_details'):
                raise serializers.ValidationError({"medicine_details": "Detalhes de medicamento são necessários para este tipo de evento."})
        elif event_type.name.lower() == 'reproducao':
            if not data.get('reproduction_details'):
                raise serializers.ValidationError({"reproduction_details": "Detalhes de reprodução são necessários para este tipo de evento."})
        elif event_type.name.lower() == 'abate':
            if not data.get('slaughter_details'):
                raise serializers.ValidationError({"slaughter_details": "Detalhes de abate são necessários para este tipo de evento."})
        elif event_type.name.lower() == 'ocorrencia especial': # Certifique-se de usar o nome exato do EventType
            if not data.get('special_occurrences_details'):
                raise serializers.ValidationError({"special_occurrences_details": "Detalhes de ocorrência especial são necessários para este tipo de evento."})


        # Valida que todos os animal_ids existem
        animal_ids = data.get('animal_ids', [])
        if not animal_ids:
            raise serializers.ValidationError({"animal_ids": "Pelo menos um ID de animal é necessário."})
        
        for animal_id in animal_ids:
            try:
                Animal.objects.get(id=animal_id)
            except Animal.DoesNotExist:
                raise serializers.ValidationError(f"Animal com ID {animal_id} não encontrado.")

        data['event_type_object'] = event_type # Passa o objeto EventType validado
        return data

    def create(self, validated_data):
        animal_ids = validated_data.pop('animal_ids')
        event_type_object = validated_data.pop('event_type_object') # Pega o objeto EventType
        recorded_by = self.context['request'].user # Obtém o usuário logado

        event_specific_data = {}
        if event_type_object.name.lower() == 'movimento':
            event_specific_data['movement_details'] = validated_data.pop('movement_details', None)
        elif event_type_object.name.lower() == 'pesagem':
            event_specific_data['weighing_details'] = validated_data.pop('weighing_details', None)
        elif event_type_object.name.lower() == 'vacina':
            event_specific_data['vacine_details'] = validated_data.pop('vacine_details', None)
        elif event_type_object.name.lower() == 'medicamento':
            event_specific_data['medicine_details'] = validated_data.pop('medicine_details', None)
        elif event_type_object.name.lower() == 'reproducao':
            event_specific_data['reproduction_details'] = validated_data.pop('reproduction_details', None)
        elif event_type_object.name.lower() == 'abate':
            event_specific_data['slaughter_details'] = validated_data.pop('slaughter_details', None)
        elif event_type_object.name.lower() == 'ocorrencia especial':
            event_specific_data['special_occurrences_details'] = validated_data.pop('special_occurrences_details', None)


        created_events = []
        for animal_id in animal_ids:
            animal = Animal.objects.get(id=animal_id) # Já validado que existe

            # Cria o Evento principal para o animal
            event = Event.objects.create(
                recorded_by=recorded_by,
                animal=animal,
                event_type=event_type_object,
                date=validated_data['date'],
                location=validated_data.get('location'),
                observations=validated_data.get('observations')
            )
            created_events.append(event)

            # Cria a instância do evento específico
            if event_type_object.name.lower() == 'movimento' and event_specific_data.get('movement_details'):
                Movement.objects.create(event=event, **event_specific_data['movement_details'])
            elif event_type_object.name.lower() == 'pesagem' and event_specific_data.get('weighing_details'):
                Weighing.objects.create(event=event, **event_specific_data['weighing_details'])
            elif event_type_object.name.lower() == 'vacina' and event_specific_data.get('vacine_details'):
                Vacine.objects.create(event=event, **event_specific_data['vacine_details'])
            elif event_type_object.name.lower() == 'medicamento' and event_specific_data.get('medicine_details'):
                Medicine.objects.create(event=event, **event_specific_data['medicine_details'])
            elif event_type_object.name.lower() == 'reproducao' and event_specific_data.get('reproduction_details'):
                # Para reprodução, male_id e female_id são ForeignKeys para Animal.
                # O serializer aninhado pode já ter resolvido isso para IDs,
                # mas se ele receber IDs, precisamos buscar os objetos Animal.
                repro_details = event_specific_data['reproduction_details']
                male_animal = Animal.objects.get(id=repro_details['male_id'])
                female_animal = Animal.objects.get(id=repro_details['female_id'])
                Reproduction.objects.create(
                    event=event,
                    reproduction_type=repro_details['reproduction_type'],
                    male_id=male_animal,
                    female_id=female_animal,
                    date=repro_details['date'],
                    result=repro_details.get('result')
                )
            elif event_type_object.name.lower() == 'abate' and event_specific_data.get('slaughter_details'):
                Slaughter.objects.create(event=event, **event_specific_data['slaughter_details'])
            elif event_type_object.name.lower() == 'ocorrencia especial' and event_specific_data.get('special_occurrences_details'):
                SpecialOccurrences.objects.create(event=event, **event_specific_data['special_occurrences_details'])


        return created_events # Retorna a lista de eventos criados