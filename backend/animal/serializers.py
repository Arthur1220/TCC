from rest_framework import serializers
from .models import Animal, IdentificationType, Specie, Breed, AnimalGroup, Gender, Status

class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class AnimalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalGroup
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class AnimalBatchUpdateSerializer(serializers.Serializer):
    animal_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Lista de IDs dos animais a serem atualizados."
    )
    # Campos opcionais para atualização em lote
    new_status_id = serializers.IntegerField(
        required=False,
        help_text="ID do novo status a ser aplicado aos animais."
    )
    new_group_id = serializers.IntegerField(
        required=False,
        allow_null=True, # Permitir que o grupo seja nulo (sem lote)
        help_text="ID do novo grupo/lote a ser aplicado aos animais. Pode ser nulo para remover do lote."
    )
    new_identification_type_id = serializers.IntegerField(
        required=False,
        help_text="ID do novo tipo de identificação a ser aplicado aos animais."
    )
    new_breed_id = serializers.IntegerField(
        required=False,
        allow_null=True, # Permitir que a raça seja nula
        help_text="ID da nova raça a ser aplicada aos animais."
    )
    new_specie_id = serializers.IntegerField( # Adicionando specie para consistência, embora a mudança de raça já implique espécie
        required=False,
        allow_null=True,
        help_text="ID da nova espécie a ser aplicada aos animais. (A raça deve ser compatível)."
    )

    def validate(self, data):
        # Garante que pelo menos um campo de atualização foi fornecido
        update_fields = [
            'new_status_id', 
            'new_group_id', 
            'new_identification_type_id', 
            'new_breed_id',
            'new_specie_id'
        ]
        if not any(field in data for field in update_fields):
            raise serializers.ValidationError("Pelo menos um campo de atualização (status, grupo, tipo de identificação, raça, espécie) deve ser fornecido.")

        # Validações individuais para IDs estrangeiros
        if 'new_status_id' in data and not Status.objects.filter(id=data['new_status_id']).exists():
            raise serializers.ValidationError({"new_status_id": "O ID do status fornecido não é válido."})
        
        if 'new_group_id' in data and data['new_group_id'] is not None and not AnimalGroup.objects.filter(id=data['new_group_id']).exists():
            raise serializers.ValidationError({"new_group_id": "O ID do grupo/lote fornecido não é válido."})

        if 'new_identification_type_id' in data and not IdentificationType.objects.filter(id=data['new_identification_type_id']).exists():
            raise serializers.ValidationError({"new_identification_type_id": "O ID do tipo de identificação fornecido não é válido."})

        if 'new_breed_id' in data:
            if data['new_breed_id'] is not None:
                breed_instance = Breed.objects.filter(id=data['new_breed_id']).first()
                if not breed_instance:
                    raise serializers.ValidationError({"new_breed_id": "O ID da raça fornecido não é válido."})
                # Se uma nova espécie também foi fornecida, valida a compatibilidade
                if 'new_specie_id' in data and data['new_specie_id'] is not None and breed_instance.specie_id != data['new_specie_id']:
                    raise serializers.ValidationError({"new_breed_id": "A raça selecionada não pertence à espécie fornecida."})
            elif 'new_specie_id' in data and data['new_specie_id'] is not None:
                 raise serializers.ValidationError({"new_breed_id": "Se a espécie é fornecida, a raça não pode ser nula (ou você pode deixar ambos nulos se não quiser alterar a raça/espécie)."
                                                    + " Considere deixar 'new_specie_id' nulo se 'new_breed_id' for nulo."})


        if 'new_specie_id' in data and data['new_specie_id'] is not None and not Specie.objects.filter(id=data['new_specie_id']).exists():
            raise serializers.ValidationError({"new_specie_id": "O ID da espécie fornecido não é válido."})

        return data