# animal/serializers.py
from rest_framework import serializers
from .models import Animal, IdentificationType, Specie, Breed, AnimalGroup, Gender, Status

class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specie
        fields = ['id', 'name'] # Recomendado: listar campos explicitamente

class BreedSerializer(serializers.ModelSerializer):
    # specie_name = serializers.CharField(source='specie.name', read_only=True) # Opcional, se precisar do nome da espécie ao serializar Breed
    specie = SpecieSerializer(read_only=True) # Para mostrar o objeto espécie aninhado
    specie_id = serializers.PrimaryKeyRelatedField(queryset=Specie.objects.all(), source='specie', write_only=True) # Para escrita

    class Meta:
        model = Breed
        fields = ['id', 'name', 'description', 'specie', 'specie_id'] # specie_id é para escrita, specie é para leitura

class AnimalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalGroup
        fields = ['id', 'name', 'description', 'owner']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name', 'description']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description']

class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = ['id', 'name', 'description']

class AnimalSerializer(serializers.ModelSerializer):
    # Campos para exibir nomes de FKs (read-only)
    specie_id = serializers.SerializerMethodField(read_only=True) # MUDANÇA: Renomeado para clareza
    specie_name = serializers.SerializerMethodField(read_only=True)
    breed_name = serializers.CharField(source='breed.name', read_only=True, allow_null=True)
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    gender_name = serializers.CharField(source='gender.name', read_only=True, allow_null=True) # Adicionado
    status_name = serializers.CharField(source='status.name', read_only=True, allow_null=True) # Adicionado
    identification_type_name = serializers.CharField(source='identification_type.name', read_only=True, allow_null=True) # Adicionado
    owner_username = serializers.CharField(source='owner.username', read_only=True, allow_null=True) # Adicionado

    # Campos de FK para escrita (recebem IDs do frontend)
    # O campo 'breed' já é um PrimaryKeyRelatedField por padrão se não especificado de outra forma
    # e receberá o ID da raça.

    class Meta:
        model = Animal
        fields = [
            'id', 'identification', 'owner', 'owner_username',
            'breed', # Este será o ID da raça para escrita/leitura
            'breed_name',
            'specie_id',   # MUDANÇA: Populado por get_specie_id
            'specie_name', # Populado por get_specie_name
            'group', 'group_name',
            'gender', 'gender_name',
            'status', 'status_name',
            'identification_type', 'identification_type_name',
            'birth_date', 'observations',
            'created_at', 'updated_at'
        ]

    def get_specie_id(self, obj): # MUDANÇA: Nome do método
        if obj.breed and obj.breed.specie:
            return obj.breed.specie.id
        return None

    def get_specie_name(self, obj):
        if obj.breed and obj.breed.specie:
            return obj.breed.specie.name
        return None

    # Ao criar/atualizar um Animal, o frontend deve enviar 'breed' (o ID da raça).
    # O 'specie_id' e 'specie_name' são apenas para leitura (derivados da raça).
    # O formulário no frontend usa um select de Espécie para filtrar o select de Raça.
    # O valor enviado para o backend é o ID da Raça selecionada.

# ... (AnimalBatchUpdateSerializer permanece o mesmo por enquanto, mas a validação de new_specie_id e new_breed_id deve ser cuidadosa)
# Na AnimalBatchUpdateSerializer, a lógica para new_specie_id e new_breed_id:
# Se new_breed_id é fornecido, new_specie_id deve ser ignorado ou validado para consistência.
# Se apenas new_specie_id é fornecido, a raça (new_breed_id) provavelmente deveria ser definida como nula.

class AnimalBatchUpdateSerializer(serializers.Serializer):
    animal_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Lista de IDs dos animais a serem atualizados."
    )
    new_status_id = serializers.IntegerField(required=False, allow_null=True)
    new_group_id = serializers.IntegerField(required=False, allow_null=True)
    new_identification_type_id = serializers.IntegerField(required=False, allow_null=True)
    new_breed_id = serializers.IntegerField(required=False, allow_null=True)
    # new_specie_id não é mais necessário aqui se a espécie é sempre derivada da raça.
    # Se for preciso mudar a espécie e anular a raça, a lógica no viewset.update_batch precisaria tratar isso.

    def validate_new_status_id(self, value):
        if value is not None and not Status.objects.filter(id=value).exists():
            raise serializers.ValidationError("O ID do status fornecido não é válido.")
        return value

    def validate_new_group_id(self, value):
        if value is not None and not AnimalGroup.objects.filter(id=value).exists():
            raise serializers.ValidationError("O ID do grupo/lote fornecido não é válido.")
        return value
    
    def validate_new_identification_type_id(self, value):
        if value is not None and not IdentificationType.objects.filter(id=value).exists():
            raise serializers.ValidationError("O ID do tipo de identificação fornecido não é válido.")
        return value

    def validate_new_breed_id(self, value):
        if value is not None and not Breed.objects.filter(id=value).exists():
            raise serializers.ValidationError("O ID da raça fornecido não é válido.")
        return value

    def validate(self, data):
        update_fields = ['new_status_id', 'new_group_id', 'new_identification_type_id', 'new_breed_id']
        if not any(field in data for field in update_fields if data.get(field) is not None):
            raise serializers.ValidationError("Pelo menos um campo de atualização válido deve ser fornecido.")
        
        # Se new_breed_id está presente e não é nulo, new_specie_id não é necessário no payload,
        # pois a espécie será derivada da raça.
        if data.get('new_breed_id') is not None:
            # Valida se a raça existe (já feito por validate_new_breed_id)
            pass # A espécie será automaticamente definida pela raça na view

        return data