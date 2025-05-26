from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
# MUDANÇA AQUI: Importar permission_classes com um alias
from rest_framework.decorators import permission_classes as drf_permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Specie, Breed, AnimalGroup, Gender, Status, IdentificationType, Animal
from .serializers import (
    AnimalBatchUpdateSerializer, SpecieSerializer, BreedSerializer,
    AnimalGroupSerializer, GenderSerializer, StatusSerializer,
    IdentificationTypeSerializer, AnimalSerializer
)

# ViewSets para Lookups (Specie, Breed, AnimalGroup, etc.) permanecem como antes:
class SpecieViewSet(ModelViewSet):
    queryset = Specie.objects.all().order_by('name')
    serializer_class = SpecieSerializer
    permission_classes = [AllowAny]

class BreedViewSet(ModelViewSet):
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Breed.objects.all().order_by('name')
        specie_id = self.request.query_params.get('specie_id')
        if specie_id:
            try:
                queryset = queryset.filter(specie_id=int(specie_id))
            except ValueError:
                pass
        return queryset

class AnimalGroupViewSet(ModelViewSet):
    serializer_class = AnimalGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnimalGroup.objects.filter(owner=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all().order_by('name')
    serializer_class = GenderSerializer
    permission_classes = [AllowAny]

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all().order_by('name')
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]

class IdentificationTypeViewSet(ModelViewSet):
    queryset = IdentificationType.objects.all().order_by('name')
    serializer_class = IdentificationTypeSerializer
    permission_classes = [AllowAny]


class AnimalViewSet(ModelViewSet):
    serializer_class = AnimalSerializer
    # Este atributo de classe é usado por ações padrão do ModelViewSet (se houvesse)
    # e pela ação 'update_batch' se ela não especificasse suas próprias permission_classes.
    permission_classes = [IsAuthenticated]


    @staticmethod
    @api_view(['POST'])
    @drf_permission_classes([IsAuthenticated]) # MUDANÇA: Usando o alias
    def register(request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = AnimalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET'])
    @drf_permission_classes([IsAuthenticated]) # MUDANÇA: Usando o alias
    def get(request, id=None):
        if id:
            try:
                animal = Animal.objects.select_related(
                    'breed__specie', 'group', 'gender', 'status', 'identification_type', 'owner'
                ).get(pk=id, owner=request.user)
                serializer = AnimalSerializer(animal)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Animal não encontrado ou não pertence ao usuário.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            query_params = request.query_params.copy()
            filters = {'owner': request.user}
            status_id = query_params.get('status')
            if status_id:
                try:
                    filters['status_id'] = int(status_id)
                except ValueError:
                    return Response({'error': 'ID de status inválido.'}, status=status.HTTP_400_BAD_REQUEST)
            
            animals = Animal.objects.select_related(
                'breed__specie', 'group', 'gender', 'status', 'identification_type', 'owner'
            ).filter(**filters).order_by('identification')
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['GET'])
    @drf_permission_classes([IsAuthenticated]) # MUDANÇA: Usando o alias
    def filter_get(request):
        query_params = request.query_params
        filters = {'owner': request.user}
        filter_map = {
            'identification': 'identification__icontains',
            'birth_date': 'birth_date',
            'breed': 'breed_id',
            'group': 'group_id',
            'gender': 'gender_id',
            'status': 'status_id',
            'identification_type': 'identification_type_id',
            'specie': 'breed__specie_id'
        }
        for param, value in query_params.items():
            if param == 'owner':
                 if str(value) != str(request.user.id):
                     return Response({'error': 'Não é permitido filtrar por outros proprietários.'}, status=status.HTTP_403_FORBIDDEN)
                 continue
            if param in filter_map:
                filters[filter_map[param]] = value
        try:
            animals = Animal.objects.select_related(
                'breed__specie', 'group', 'gender', 'status', 'identification_type', 'owner'
            ).filter(**filters).order_by('identification')
            serializer = AnimalSerializer(animals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Erro ao filtrar animais: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['PUT', 'PATCH'])
    @drf_permission_classes([IsAuthenticated]) # MUDANÇA: Usando o alias
    def update(request, id):
        try:
            animal = Animal.objects.get(pk=id, owner=request.user)
            partial = request.method == 'PATCH'
            serializer = AnimalSerializer(instance=animal, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal não encontrado ou não pertence ao usuário.'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(['DELETE'])
    @drf_permission_classes([IsAuthenticated]) # MUDANÇA: Usando o alias
    def delete(request, id):
        try:
            animal = Animal.objects.get(pk=id, owner=request.user)
            animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': 'Animal não encontrado ou não pertence ao usuário.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='update-batch') # permission_classes=[IsAuthenticated] é herdado da classe AnimalViewSet
    def update_batch(self, request):
        serializer = AnimalBatchUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        animal_ids = serializer.validated_data['animal_ids']
        animals_to_update_qs = Animal.objects.filter(id__in=animal_ids, owner=self.request.user)
        actual_animal_ids_owned = list(animals_to_update_qs.values_list('id', flat=True))
        
        if len(actual_animal_ids_owned) != len(set(animal_ids)):
            missing_or_not_owned_ids = set(animal_ids) - set(actual_animal_ids_owned)
            return Response({
                "error": f"Um ou mais IDs de animais não foram encontrados ou você não tem permissão para editá-los. IDs problemáticos: {list(missing_or_not_owned_ids)}."
            }, status=status.HTTP_403_FORBIDDEN)

        update_data = {}
        validated_data = serializer.validated_data

        if validated_data.get('new_status_id') is not None:
            update_data['status_id'] = validated_data['new_status_id']
        if 'new_group_id' in validated_data:
            update_data['group_id'] = validated_data['new_group_id']
        if validated_data.get('new_identification_type_id') is not None:
            update_data['identification_type_id'] = validated_data['new_identification_type_id']
        if 'new_breed_id' in validated_data:
            update_data['breed_id'] = validated_data['new_breed_id']

        if not update_data:
            return Response({"message": "Nenhum campo de atualização válido foi fornecido.", "updated_animals_count": 0}, status=status.HTTP_200_OK)

        updated_count = animals_to_update_qs.update(**update_data)
        return Response(
            {"message": f"{updated_count} animais foram atualizados com sucesso.", "updated_animals_count": updated_count},
            status=status.HTTP_200_OK
        )