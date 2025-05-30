from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, action, permission_classes as drf_permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction, IntegrityError

from .models import OwnershipTransferRequest # OwnershipTransferRequest já com o campo removido
from .serializers import OwnershipTransferRequestSerializer, TransferActionSerializer
from animal.models import Animal

# Importe seu app 'contract' e a função de transferência on-chain
# from contract_app.utils import initiate_blockchain_transfer # Exemplo

class OwnershipTransferViewSet(ViewSet):
    permission_classes = [IsAuthenticated] # Permissão padrão para o ViewSet

    # 1. Criar uma nova solicitação de transferência
    @staticmethod
    @api_view(['POST'])
    @drf_permission_classes([IsAuthenticated])
    def create_request(request):
        serializer = OwnershipTransferRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(initiated_by=request.user)
            # TODO: Enviar notificação para serializer.instance.requested_to
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # ADICIONE ESTA LINHA PARA DEBUG:
        print(f"DEBUG: Erros do Serializer ao criar solicitação: {serializer.errors}")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 2. Listar solicitações enviadas pelo usuário logado
    @staticmethod
    @api_view(['GET'])
    @drf_permission_classes([IsAuthenticated])
    def list_sent_requests(request):
        requests = OwnershipTransferRequest.objects.filter(initiated_by=request.user).prefetch_related('animals', 'requested_to').select_related('initiated_by')
        serializer = OwnershipTransferRequestSerializer(requests, many=True)
        return Response(serializer.data)

    # 3. Listar solicitações recebidas pelo usuário logado (pendentes de ação)
    @staticmethod
    @api_view(['GET'])
    @drf_permission_classes([IsAuthenticated])
    def list_received_requests(request):
        # Filtrar por status também, se necessário (ex: apenas PENDING_APPROVAL)
        requests = OwnershipTransferRequest.objects.filter(
            requested_to=request.user, 
            status='PENDING_APPROVAL' # Ou outros status que o destinatário precise ver
        ).prefetch_related('animals', 'initiated_by').select_related('requested_to')
        serializer = OwnershipTransferRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    # 4. Ver detalhes de uma solicitação específica (pode ser acessada por initiated_by ou requested_to)
    @staticmethod
    @api_view(['GET'])
    @drf_permission_classes([IsAuthenticated])
    def retrieve_request(request, pk):
        try:
            transfer_request = OwnershipTransferRequest.objects.prefetch_related('animals__breed__specie', 'animals__status', 'animals__gender', 'animals__group', 'animals__identification_type').select_related('initiated_by', 'requested_to').get(pk=pk)
            if request.user != transfer_request.initiated_by and request.user != transfer_request.requested_to:
                return Response({'error': 'Você não tem permissão para ver esta solicitação.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = OwnershipTransferRequestSerializer(transfer_request)
            return Response(serializer.data)
        except OwnershipTransferRequest.DoesNotExist:
            return Response({'error': 'Solicitação não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

    # Ações no ViewSet (para usar /requests/{pk}/action_name/)
    # Precisaremos instanciar o ViewSet nas URLs para estas actions
    
    def get_object(self, pk):
        # Método helper para actions que operam sobre uma instância
        return get_object_or_404(OwnershipTransferRequest, pk=pk)

    # 5. Cancelar uma solicitação (pelo solicitante)
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_request(self, request, pk=None):
        transfer_request = self.get_object(pk)
        if request.user != transfer_request.initiated_by:
            return Response({'error': 'Apenas o solicitante pode cancelar esta solicitação.'}, status=status.HTTP_403_FORBIDDEN)
        if transfer_request.status != 'PENDING_APPROVAL':
            return Response({'error': f'Esta solicitação não pode ser cancelada (status atual: {transfer_request.get_status_display()}).'}, status=status.HTTP_400_BAD_REQUEST)
        
        transfer_request.status = 'CANCELLED_BY_INITIATOR'
        transfer_request.action_date = timezone.now() # Ou um campo 'cancellation_date'
        transfer_request.save()
        # TODO: Enviar notificação para transfer_request.requested_to
        return Response({'status': 'Solicitação cancelada com sucesso.'}, status=status.HTTP_200_OK)

    # 6. Rejeitar uma solicitação (pelo destinatário)
    @action(detail=True, methods=['post'], url_path='reject')
    def reject_request(self, request, pk=None):
        transfer_request = self.get_object(pk)
        if request.user != transfer_request.requested_to:
            return Response({'error': 'Apenas o destinatário pode rejeitar esta solicitação.'}, status=status.HTTP_403_FORBIDDEN)
        if transfer_request.status != 'PENDING_APPROVAL':
            return Response({'error': f'Esta solicitação não pode mais ser rejeitada (status atual: {transfer_request.get_status_display()}).'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransferActionSerializer(data=request.data)
        if serializer.is_valid():
            transfer_request.status = 'REJECTED'
            transfer_request.recipient_notes = serializer.validated_data.get('recipient_notes')
            transfer_request.action_date = timezone.now()
            transfer_request.save()
            # TODO: Enviar notificação para transfer_request.initiated_by
            return Response({'status': 'Solicitação rejeitada com sucesso.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 7. Aceitar uma solicitação e processar a transferência (pelo destinatário)
    @action(detail=True, methods=['post'], url_path='approve')
    def approve_and_process_request(self, request, pk=None):
        # 1. Obter a solicitação ou retornar 404
        transfer_request = self.get_object(pk)

        # 2. Validações de permissão e status da solicitação
        if request.user != transfer_request.requested_to:
            return Response({'error': 'Apenas o destinatário pode aprovar esta solicitação.'}, status=status.HTTP_403_FORBIDDEN)
        
        if transfer_request.status != 'PENDING_APPROVAL':
            return Response({'error': f'Esta solicitação não pode mais ser aprovada (status atual: {transfer_request.get_status_display()}).'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Validar dados da ação (ex: notas do destinatário)
        action_serializer = TransferActionSerializer(data=request.data)
        if not action_serializer.is_valid():
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 4. Mudar status para 'PROCESSING' e salvar ANTES do bloco try principal.
        # Isso garante que, se algo falhar depois, o status 'PROCESSING' já está registrado.
        transfer_request.status = 'PROCESSING'
        transfer_request.recipient_notes = action_serializer.validated_data.get('recipient_notes')
        transfer_request.action_date = timezone.now()
        transfer_request.save()
        
        try:
            # 5. Operações de banco de dados (atualização de animais) em uma transação atômica
            with transaction.atomic():
                # Re-fetch com select_for_update para bloquear a linha da solicitação durante a transação,
                # embora o principal aqui seja a lógica dos animais.
                # Isso pode ser overkill se não houver alta concorrência neste ponto específico.
                # request_in_transaction = OwnershipTransferRequest.objects.select_for_update().get(pk=transfer_request.pk)
                
                for animal_to_transfer in transfer_request.animals.all(): # Usar o transfer_request original aqui está ok
                    # Verificação CRUCIAL: o proprietário do animal ainda é o solicitante original?
                    if animal_to_transfer.owner != transfer_request.initiated_by:
                        # Se o proprietário mudou, levantamos uma IntegrityError.
                        # Isso fará o rollback da transação atômica.
                        raise IntegrityError(
                            f"Propriedade do animal {animal_to_transfer.identification} (ID: {animal_to_transfer.pk}) "
                            f"mudou. Proprietário esperado: {transfer_request.initiated_by.username}, "
                            f"proprietário encontrado: {animal_to_transfer.owner.username}."
                        )
                    
                    animal_to_transfer.owner = transfer_request.requested_to
                    animal_to_transfer.group = None # Conforme requisito
                    animal_to_transfer.save() # Salva as alterações no animal

                # Se o loop completou sem erros, todas as alterações nos animais foram preparadas.
                # Agora, atualize o status final da solicitação DENTRO da transação.
                # Precisamos buscar o objeto novamente se usamos select_for_update no request_in_transaction,
                # ou podemos continuar usando o objeto 'transfer_request' que está em memória se
                # não houver preocupação de que ele esteja desatualizado por outra thread/processo.
                # Para simplicidade e dado que já estamos em 'PROCESSING', vamos atualizar o objeto em memória.
                transfer_request.status = 'COMPLETED'
                transfer_request.completion_date = timezone.now()
                transfer_request.save() # Este save também está dentro da transação atômica

            # Fora da transação atômica: se chegou aqui, tudo foi commitado com sucesso.
            # TODO: Enviar notificações de conclusão para o solicitante e o destinatário.
            
            # Re-fetch para garantir que o serializer obtenha o estado mais recente após a transação.
            final_transfer_request = self.get_object(pk)
            final_serializer = OwnershipTransferRequestSerializer(final_transfer_request)
            return Response(final_serializer.data, status=status.HTTP_200_OK)

        except IntegrityError as ie:
            # Captura a falha específica de mudança de proprietário.
            # A transação atômica já fez rollback das alterações nos animais.
            # O status da solicitação no BD ainda é 'PROCESSING' (salvo antes do try).
            # Mudamos para 'ERROR_PROCESSING'.
            print(f"IntegrityError ao processar transferência (ID: {transfer_request.pk}): {str(ie)}")
            
            # É importante re-fetch ou usar o objeto correto para atualizar o status
            request_to_mark_error = self.get_object(pk) # Garante que estamos trabalhando com o objeto do BD
            request_to_mark_error.status = 'ERROR_PROCESSING'
            request_to_mark_error.save()
            
            # Retornar um erro 400 (Bad Request) ou 409 (Conflict) pode ser mais apropriado
            # do que 500 para uma falha de pré-condição de dados.
            return Response({'error': str(ie)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Captura qualquer outra exceção inesperada durante o processo.
            # A transação atômica (se iniciada) também teria feito rollback.
            # O status no BD é 'PROCESSING'. Mudamos para 'ERROR_PROCESSING'.
            print(f"Exceção genérica ao processar transferência (ID: {transfer_request.pk}): {str(e)}")
            
            request_to_mark_error = self.get_object(pk)
            request_to_mark_error.status = 'ERROR_PROCESSING'
            request_to_mark_error.save()
            
            return Response({'error': f'Erro interno inesperado ao processar a transferência: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
