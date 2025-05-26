from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Specie, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AnimalBatchUpdateSerializer , SpecieSerializer, BreedSerializer, AnimalGroupSerializer, GenderSerializer, StatusSerializer, IdentificationTypeSerializer, AnimalSerializer

class SpecieViewSet(ModelViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    permission_classes = [AllowAny]

class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action  # se precisar de ações customizadas
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import AnimalGroup
from .serializers import AnimalGroupSerializer

class AnimalGroupViewSet(ModelViewSet):
    queryset = AnimalGroup.objects.all()
    serializer_class = AnimalGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Para registrar (criar) um novo grupo
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'owner': request.user.id,
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Lista os grupos de animais do usuário logado
        animal_groups = AnimalGroup.objects.filter(owner=request.user.id)
        serializer = self.get_serializer(animal_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # Recupera um grupo específico, garantindo que o usuário é o dono
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            serializer = self.get_serializer(animal_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        # Atualiza um grupo específico
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            serializer = self.get_serializer(animal_group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        # Deleta um grupo específico
        try:
            animal_group = AnimalGroup.objects.get(pk=pk, owner=request.user.id)
            animal_group.delete()
            return Response({'message': 'Animal group deleted successfully'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal group not found'}, status=status.HTTP_404_NOT_FOUND)


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [AllowAny]

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]

class IdentificationTypeViewSet(ModelViewSet):
    queryset = IdentificationType.objects.all()
    serializer_class = IdentificationTypeSerializer
    permission_classes = [AllowAny]

class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'identification': request.data['identification'],
            'owner': request.user.id,
            'breed': request.data['breed'],
            'group': request.data['group'],
            'gender': request.data['gender'],
            'status': request.data['status'],
            'identification_type': request.data['identification_type'],
            'birth_date': request.data['birth_date'],
            'observations': request.data['observations'],
        }

        serializer = AnimalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @permission_classes([AllowAny])
    def get(request, id=None):
        if id:
            try:
                animal = Animal.objects.get(pk=id)
                serializer = AnimalSerializer(animal)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            animals = Animal.objects.all()
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def filter_get(request):
        query_params = request.query_params
        filters = {}

        allowed_fields = [field.name for field in Animal._meta.fields]

        for key, value in query_params.items():
            if key in allowed_fields:
                filters[key] = value

        try:
            animals = Animal.objects.filter(**filters)
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Search error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            animal = Animal.objects.get(pk=id)
            serializer = AnimalSerializer(instance=animal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            animal = Animal.objects.get(pk=id)
            animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['patch'], url_path='update-batch') # Renomeei para 'update-batch' para ser mais genérico
    @permission_classes([IsAuthenticated])
    def update_batch(self, request):
        """
        Permite a atualização de múltiplos campos (status, grupo, tipo de identificação, raça, espécie)
        para um lote de animais.
        """
        serializer = AnimalBatchUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        animal_ids = serializer.validated_data['animal_ids']
        
        # Filtra os animais que pertencem ao usuário logado e que estão na lista de IDs
        animals_to_update = Animal.objects.filter(id__in=animal_ids, owner=request.user)
        
        if animals_to_update.count() != len(animal_ids):
            # Se algum ID não existir ou não pertencer ao usuário
            # Você pode detalhar isso se quiser, mas por enquanto, um erro genérico serve.
            return Response({"error": "Um ou mais IDs de animais não foram encontrados ou você não tem permissão para editá-los."}, 
                            status=status.HTTP_403_FORBIDDEN)

        update_data = {}
        
        # Processa a atualização do Status
        if 'new_status_id' in serializer.validated_data:
            try:
                status_instance = Status.objects.get(pk=serializer.validated_data['new_status_id'])
                update_data['status'] = status_instance
            except ObjectDoesNotExist:
                return Response({"error": "O ID do status fornecido não é válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Processa a atualização do Grupo/Lote
        if 'new_group_id' in serializer.validated_data:
            new_group_id = serializer.validated_data['new_group_id']
            if new_group_id is None:
                update_data['group'] = None # Remove o animal do lote
            else:
                try:
                    group_instance = AnimalGroup.objects.get(pk=new_group_id)
                    update_data['group'] = group_instance
                except ObjectDoesNotExist:
                    return Response({"error": "O ID do grupo/lote fornecido não é válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Processa a atualização do Tipo de Identificação
        if 'new_identification_type_id' in serializer.validated_data:
            try:
                identification_type_instance = IdentificationType.objects.get(pk=serializer.validated_data['new_identification_type_id'])
                update_data['identification_type'] = identification_type_instance
            except ObjectDoesNotExist:
                return Response({"error": "O ID do tipo de identificação fornecido não é válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Processa a atualização da Raça
        if 'new_breed_id' in serializer.validated_data:
            new_breed_id = serializer.validated_data['new_breed_id']
            if new_breed_id is None:
                update_data['breed'] = None # Permite remover a raça (se o campo no model permitir null)
                # Se a raça é nula, a espécie também deve ser considerada nula ou deixada como está
                # Dependendo da sua lógica de negócio, você pode forçar a especie a ser nula aqui também.
                if 'new_specie_id' not in serializer.validated_data: # Se espécie não foi explicitamente setada
                    update_data['specie'] = None # Ou deixar o Animal.specie como está
            else:
                try:
                    breed_instance = Breed.objects.get(pk=new_breed_id)
                    update_data['breed'] = breed_instance
                    # Ao definir a raça, também atualiza a espécie automaticamente para a espécie da raça
                    update_data['specie'] = breed_instance.specie
                except ObjectDoesNotExist:
                    return Response({"error": "O ID da raça fornecido não é válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Processa a atualização da Espécie (somente se não foi atualizada pela raça)
        # Se 'new_breed_id' foi fornecido, ele já define a espécie.
        if 'new_specie_id' in serializer.validated_data and 'new_breed_id' not in serializer.validated_data:
            new_specie_id = serializer.validated_data['new_specie_id']
            if new_specie_id is None:
                update_data['specie'] = None # Permite remover a espécie
                update_data['breed'] = None # Se a espécie é nula, a raça também deve ser.
            else:
                try:
                    specie_instance = Specie.objects.get(pk=new_specie_id)
                    update_data['specie'] = specie_instance
                except ObjectDoesNotExist:
                    return Response({"error": "O ID da espécie fornecido não é válido."}, status=status.HTTP_400_BAD_REQUEST)


        if not update_data:
            return Response({"error": "Nenhum campo válido para atualização foi fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = animals_to_update.update(**update_data)

        return Response(
            {"message": f"{updated_count} animais foram atualizados com sucesso.", "updated_animals_count": updated_count},
            status=status.HTTP_200_OK
        )