# event/serializers.py
from rest_framework import serializers
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event
from animal.models import Animal, AnimalGroup, Status # Importe AnimalGroup e Status

# --- Serializers de Detalhes Específicos para Lote (sem o campo 'event') ---
class BatchMovementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        exclude = ['event']

class BatchWeighingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weighing
        exclude = ['event']

class BatchVacineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacine
        exclude = ['event']

class BatchMedicineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        exclude = ['event']

class BatchReproductionDetailSerializer(serializers.ModelSerializer):
    male_id = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Reproduction
        exclude = ['event', 'female_id'] 

class BatchSlaughterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slaughter
        exclude = ['event']

class BatchSpecialOccurrencesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOccurrences
        exclude = ['event']

# --- Serializers Originais ---
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
    # Você pode adicionar campos _name aqui para enriquecer a resposta do GET
    # Ex: event_type_name = serializers.CharField(source='event_type.name', read_only=True)
    #     animal_identification = serializers.CharField(source='animal.identification', read_only=True)
    #     recorded_by_username = serializers.CharField(source='recorded_by.username', read_only=True)
    class Meta:
        model = Event
        fields = '__all__' # Ou liste os campos específicos se adicionar os _name acima

# --- Serializer para Registro de Evento em Lote ---
class BatchEventRegisterSerializer(serializers.Serializer):
    animal_group_id = serializers.IntegerField(
        help_text="ID do grupo de animais (lote) para o qual o evento será registrado."
    )
    event_type = serializers.PrimaryKeyRelatedField( 
        queryset=EventType.objects.all(),
        help_text="ID do tipo de evento."
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

    movement_details = BatchMovementDetailSerializer(required=False, allow_null=True)
    weighing_details = BatchWeighingDetailSerializer(required=False, allow_null=True)
    vacine_details = BatchVacineDetailSerializer(required=False, allow_null=True)
    medicine_details = BatchMedicineDetailSerializer(required=False, allow_null=True)
    reproduction_details = BatchReproductionDetailSerializer(required=False, allow_null=True)
    slaughter_details = BatchSlaughterDetailSerializer(required=False, allow_null=True)
    special_occurrences_details = BatchSpecialOccurrencesDetailSerializer(required=False, allow_null=True)

    def validate_animal_group_id(self, value):
        request_user = self.context['request'].user
        try:
            # Assumindo que AnimalGroup tem um campo 'owner' que é um FK para User
            group = AnimalGroup.objects.prefetch_related('animals__status').get(id=value, owner=request_user) 
            
            try:
                # CORREÇÃO DO FieldError: usa o modelo Status para filtrar por nome "Ativo"
                active_status = Status.objects.get(name__iexact='Ativo')
            except Status.DoesNotExist:
                raise serializers.ValidationError({"animal_group_id": "Configuração de Status 'Ativo' não encontrada no sistema."})

            active_animals_in_group = group.animals.filter(status=active_status, owner=request_user)
            
            if not active_animals_in_group.exists():
                raise serializers.ValidationError({"animal_group_id": "O grupo de animais selecionado não possui animais com status 'Ativo' pertencentes a você."})
            return group 
        except AnimalGroup.DoesNotExist:
            raise serializers.ValidationError({"animal_group_id": "Grupo de animais (lote) não encontrado ou não pertence a você."})

    def validate(self, data):
        event_type_object = data.get('event_type') # Já é o objeto EventType
        if not event_type_object:
             raise serializers.ValidationError({"event_type": "Tipo de evento é obrigatório."})

        event_type_name_lower = event_type_object.name.lower()
        detail_field_map = {
            'movimento': 'movement_details', 'movimentação': 'movement_details',
            'pesagem': 'weighing_details',
            'vacinação': 'vacine_details', 'vacina': 'vacine_details',   
            'medicação': 'medicine_details', 'medicamento': 'medicine_details',
            'reprodução': 'reproduction_details', 'reproducao': 'reproduction_details',
            'abate': 'slaughter_details',
            'ocorrência especial': 'special_occurrences_details', 'ocorrencia especial': 'special_occurrences_details',
        }
        
        required_detail_field = detail_field_map.get(event_type_name_lower)
        
        if required_detail_field and not data.get(required_detail_field):
            raise serializers.ValidationError({required_detail_field: f"Detalhes de '{event_type_object.name}' são necessários."})
        
        for type_name_key in detail_field_map.keys():
            current_detail_key = detail_field_map[type_name_key]
            if event_type_name_lower != type_name_key and current_detail_key != required_detail_field :
                if current_detail_key in data:
                    data.pop(current_detail_key)
        return data

    def create(self, validated_data):
        animal_group = validated_data.pop('animal_group_id')
        event_type_object = validated_data.pop('event_type')
        recorded_by = self.context['request'].user

        try:
            active_status = Status.objects.get(name__iexact='Ativo')
        except Status.DoesNotExist:
            raise serializers.ValidationError({"internal_error": "Status 'Ativo' não encontrado para filtrar animais do lote."})

        # CORREÇÃO DO FieldError: usa o objeto active_status para filtrar
        animal_instances = list(animal_group.animals.filter(status=active_status, owner=recorded_by))
        
        if not animal_instances:
             raise serializers.ValidationError({"animal_group_id": "Nenhum animal com status 'Ativo' aplicável encontrado neste grupo para o usuário."})

        event_type_name_lower = event_type_object.name.lower()
        details_payload = None
        detail_key_map = { # Mapa para pegar a chave correta dos detalhes
            'movimento': 'movement_details', 'movimentação': 'movement_details',
            'pesagem': 'weighing_details',
            'vacinação': 'vacine_details', 'vacina': 'vacine_details',
            'medicação': 'medicine_details', 'medicamento': 'medicine_details',
            'reprodução': 'reproduction_details', 'reproducao': 'reproduction_details',
            'abate': 'slaughter_details',
            'ocorrência especial': 'special_occurrences_details', 'ocorrencia especial': 'special_occurrences_details',
        }
        relevant_detail_key = detail_key_map.get(event_type_name_lower)
        if relevant_detail_key and relevant_detail_key in validated_data:
            details_payload = validated_data.pop(relevant_detail_key)
        
        # Remove outros *_details que possam ter vindo no payload
        for key_to_check in list(validated_data.keys()):
            if key_to_check.endswith('_details'):
                validated_data.pop(key_to_check, None)
        
        created_events_batch = []
        for animal_instance in animal_instances:
            event_instance = Event.objects.create(
                recorded_by=recorded_by,
                animal=animal_instance,
                event_type=event_type_object,
                date=validated_data['date'],
                location=validated_data.get('location'),
                observations=validated_data.get('observations')
            )
            created_events_batch.append(event_instance)

            if details_payload:
                current_detail_data_for_model = details_payload.copy() 
                # Não precisamos mais setar 'date' aqui, pois os Batch...DetailSerializers
                # devem cuidar dos seus próprios campos de data se os tiverem (como Reproduction, Movement)
                # e o BatchVacineDetailSerializer não espera 'date'.

                if event_type_name_lower in ['movimento', 'movimentação']:
                    Movement.objects.create(event=event_instance, **current_detail_data_for_model)
                elif event_type_name_lower == 'pesagem':
                    Weighing.objects.create(event=event_instance, **current_detail_data_for_model)
                elif event_type_name_lower in ['vacinação', 'vacina']:
                    Vacine.objects.create(event=event_instance, **current_detail_data_for_model)
                elif event_type_name_lower in ['medicação', 'medicamento']:
                    Medicine.objects.create(event=event_instance, **current_detail_data_for_model)
                elif event_type_name_lower in ['reprodução', 'reproducao']:
                    male_animal_instance = current_detail_data_for_model.pop('male_id', None) 
                    Reproduction.objects.create(
                        event=event_instance,
                        female_id=animal_instance, 
                        male_id=male_animal_instance, 
                        **current_detail_data_for_model
                    )
                elif event_type_name_lower == 'abate':
                    Slaughter.objects.create(event=event_instance, **current_detail_data_for_model)
                elif event_type_name_lower in ['ocorrência especial', 'ocorrencia especial']:
                    SpecialOccurrences.objects.create(event=event_instance, **current_detail_data_for_model)
        
        return created_events_batch