from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import BlockchainStatus, Blockchain
from .serializers import BlockchainStatusSerializer, BlockchainSerializer # Importe os serializers
from django.db.models import Sum, Value, F, Min, Max
from django.db.models.functions import Coalesce, TruncMonth, TruncYear
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import calendar

def format_cost_data(cost_wei_decimal):
    """
    Helper para converter Wei (Decimal) para uma string Ether formatada e retornar o Wei como string.
    """
    if cost_wei_decimal is None:
        cost_wei_decimal = Decimal('0')
    
    cost_wei_str = str(cost_wei_decimal)
    
    try:
        # 1 Ether = 10^18 Wei
        ether_value = cost_wei_decimal / Decimal('1e18')
        # Formata para até 18 casas decimais, remove zeros à direita e ponto decimal se for inteiro
        cost_ether_str = '{:.18f}'.format(ether_value).rstrip('0').rstrip('.')
        if not cost_ether_str or cost_ether_str == "0.": # Caso seja "0." ou string vazia após rstrip
            cost_ether_str = "0"
    except Exception:
        cost_ether_str = "Erro na conversão"
        
    return cost_wei_str, cost_ether_str

def format_wei_to_ether_string(wei_decimal_value):
    if wei_decimal_value is None or wei_decimal_value == Decimal('0'):
        return "0"
    ether_value = wei_decimal_value / Decimal('1e18') # 1 ETH = 10^18 Wei
    # Formata para exibir, removendo zeros desnecessários no final
    formatted_str = '{:.18f}'.format(ether_value).rstrip('0').rstrip('.')
    return formatted_str if formatted_str else "0"

class BlockchainStatusViewSet(ModelViewSet):
    queryset = BlockchainStatus.objects.all()
    serializer_class = BlockchainStatusSerializer
    permission_classes = [AllowAny] # Permissões para o status, ajuste conforme necessário

class BlockchainViewSet(ModelViewSet):
    # Adicione select_related aqui para otimizar todas as operações de listagem/recuperação
    # que usam este queryset base (como list, retrieve, etc., se você os habilitasse)
    queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')
    serializer_class = BlockchainSerializer
    # permission_classes = [IsAuthenticated] # Defina uma permissão padrão para o ViewSet se usar seus métodos padrão (list, retrieve, etc.)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def register(request):
        data = {
            'animal': request.data.get('animal'),
            'event': request.data.get('event'),
            'transaction_hash': request.data.get('transaction_hash'),
            'owner': request.user.id, 
            'status': request.data.get('status'),
            # NOVOS CAMPOS - esperando que venham do frontend/serviço chamador
            'transaction_cost': request.data.get('transaction_cost_wei'), # Nome do campo no payload
            'cost_currency_symbol': request.data.get('cost_currency_symbol', 'WEI'), # Default para WEI
        }

        serializer = BlockchainSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get(request, id=None):
        # Otimiza a consulta para carregar os objetos relacionados
        queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')

        if id:
            try:
                blockchain = queryset.get(pk=id)
                serializer = BlockchainSerializer(blockchain)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            blockchains = queryset.all() # Usar o queryset otimizado
            serializer = BlockchainSerializer(blockchains, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def filter_get(request):
        query_params = request.query_params
        
        # Otimiza a consulta para carregar os objetos relacionados
        queryset = Blockchain.objects.all().select_related('animal', 'event', 'owner', 'status')

        # Filtros para campos diretos (transaction_hash, registration_date, etc.)
        for field_name in ['transaction_hash', 'registration_date']: # Adicione outros campos diretos se necessário
            if field_name in query_params:
                queryset = queryset.filter(**{f'{field_name}__icontains': query_params[field_name]}) # Use icontains para busca parcial de strings

        # Filtros para chaves estrangeiras (pelo ID ou pelo nome do campo relacionado)
        if 'animal_id' in query_params:
            queryset = queryset.filter(animal__id=query_params['animal_id'])
        if 'event_id' in query_params:
            queryset = queryset.filter(event__id=query_params['event_id'])
        if 'owner_id' in query_params:
            queryset = queryset.filter(owner__id=query_params['owner_id'])
        if 'status_id' in query_params: # Se você filtrar pelo ID do status
            queryset = queryset.filter(status__id=query_params['status_id'])
        elif 'status_name' in query_params: # Se você filtrar pelo nome do status
             queryset = queryset.filter(status__name__icontains=query_params['status_name'])

        try:
            serializer = BlockchainSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_user_blockchain_costs_summary(request): # Nome mais específico
        user = request.user
        # Considerar apenas registros que têm um custo e pertencem ao usuário
        blockchain_records = Blockchain.objects.filter(owner=user, transaction_cost__isnull=False)

        # Custo Total
        total_cost_agg = blockchain_records.aggregate(
            sum_cost=Coalesce(Sum('transaction_cost'), Decimal('0'))
        )
        total_cost_wei = total_cost_agg['sum_cost']

        # Custo do Mês Atual
        now = timezone.now()
        start_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_cost_agg = blockchain_records.filter(registration_date__gte=start_of_current_month)\
            .aggregate(sum_cost=Coalesce(Sum('transaction_cost'), Decimal('0')))
        current_month_cost_wei = current_month_cost_agg['sum_cost']

        # Custo dos Últimos 30 Dias
        thirty_days_ago = now - timedelta(days=30)
        last_30_days_cost_agg = blockchain_records.filter(registration_date__gte=thirty_days_ago)\
            .aggregate(sum_cost=Coalesce(Sum('transaction_cost'), Decimal('0')))
        last_30_days_cost_wei = last_30_days_cost_agg['sum_cost']

        # Determinar a moeda (simplificado, assume consistência ou pega do primeiro)
        currency_symbol_wei = "WEI" # Default
        # Poderia pegar a moeda do primeiro registro se houvesse variação, mas para WEI->ETH é fixo.

        return Response({
            'total_cost_wei': str(total_cost_wei),
            'current_month_cost_wei': str(current_month_cost_wei),
            'last_30_days_cost_wei': str(last_30_days_cost_wei),

            'total_cost_display': format_wei_to_ether_string(total_cost_wei),
            'current_month_cost_display': format_wei_to_ether_string(current_month_cost_wei),
            'last_30_days_cost_display': format_wei_to_ether_string(last_30_days_cost_wei),

            'currency_wei': currency_symbol_wei,
            'currency_display': 'ETH' # Assumindo que a exibição principal será em ETH
        })

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_user_blockchain_costs(request):
        user = request.user
        filter_type = request.query_params.get('filter_type', 'all_time') # 'all_time', 'last_month', 'specific_month', 'by_month_in_year'
        year_param = request.query_params.get('year')
        month_param = request.query_params.get('month') # 1-12

        base_queryset = Blockchain.objects.filter(owner=user, transaction_cost__isnull=False)
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'currency_symbol_wei': 'WEI', # Ou a menor unidade da sua L2
            'currency_symbol_display': 'ETH (aprox. de WEI)', # A moeda principal para exibição
        }

        if filter_type == 'last_month':
            today = timezone.now().date()
            first_day_current_month = today.replace(day=1)
            last_day_last_month = first_day_current_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            
            queryset = base_queryset.filter(registration_date__date__gte=first_day_last_month,
                                            registration_date__date__lte=last_day_last_month)
            
            aggregation = queryset.aggregate(total_cost_wei_agg=Coalesce(Sum('transaction_cost'), Decimal('0')))
            cost_wei, cost_ether = format_cost_data(aggregation['total_cost_wei_agg'])
            
            response_data.update({
                'filter_applied': 'last_month',
                'period_description': first_day_last_month.strftime('%B de %Y'), # Ex: "Maio de 2025"
                'total_transaction_cost_wei': cost_wei,
                'total_transaction_cost_display': cost_ether,
            })

        elif filter_type == 'specific_month':
            if not year_param or not month_param:
                return Response({'error': 'Parâmetros "year" e "month" são obrigatórios para "specific_month".'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                year = int(year_param)
                month = int(month_param)
                if not (1 <= month <= 12 and 2000 <= year <= timezone.now().year + 5): # Validação básica
                    raise ValueError("Ano ou mês inválido.")
                # Garante que estamos pegando do primeiro ao último dia do mês/ano especificado
                start_date = date(year, month, 1)
                end_date = date(year, month, calendar.monthrange(year, month)[1])

            except ValueError as e:
                return Response({'error': f'Parâmetros "year" e "month" inválidos: {e}'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = base_queryset.filter(registration_date__date__range=(start_date, end_date))
            aggregation = queryset.aggregate(total_cost_wei_agg=Coalesce(Sum('transaction_cost'), Decimal('0')))
            cost_wei, cost_ether = format_cost_data(aggregation['total_cost_wei_agg'])
            
            period_desc = start_date.strftime('%B de %Y')

            response_data.update({
                'filter_applied': 'specific_month',
                'period_description': period_desc,
                'total_transaction_cost_wei': cost_wei,
                'total_transaction_cost_display': cost_ether,
            })

        elif filter_type == 'by_month_in_year' or filter_type == 'all_months_summary':
            # Retorna um resumo de custos para cada mês que teve atividade.
            query_for_monthly_breakdown = base_queryset
            description = "Resumo mensal de todos os tempos"

            if filter_type == 'by_month_in_year':
                if not year_param:
                    return Response({'error': 'Parâmetro "year" é obrigatório para "by_month_in_year".'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    year = int(year_param)
                    if not (2000 <= year <= timezone.now().year + 5):
                        raise ValueError("Ano inválido.")
                    query_for_monthly_breakdown = query_for_monthly_breakdown.filter(registration_date__year=year)
                    description = f"Resumo mensal para o ano de {year}"
                except ValueError as e:
                    return Response({'error': f'Parâmetro "year" inválido: {e}'}, status=status.HTTP_400_BAD_REQUEST)

            monthly_costs_data = query_for_monthly_breakdown \
                .annotate(month_year_group=TruncMonth('registration_date')) \
                .values('month_year_group') \
                .annotate(total_cost_for_month_wei=Sum('transaction_cost')) \
                .order_by('month_year_group')

            monthly_summary = []
            for item in monthly_costs_data:
                cost_wei, cost_ether = format_cost_data(item['total_cost_for_month_wei'])
                monthly_summary.append({
                    'month_year_iso': item['month_year_group'].strftime('%Y-%m'), # "2025-05"
                    'month_year_display': item['month_year_group'].strftime('%B de %Y'), # "Maio de 2025"
                    'total_transaction_cost_wei': cost_wei,
                    'total_transaction_cost_display': cost_ether,
                })
            
            response_data.update({
                'filter_applied': filter_type,
                'period_description': description,
                'monthly_summary': monthly_summary,
            })
        
        else: # Default: 'all_time'
            aggregation = base_queryset.aggregate(total_cost_wei_agg=Coalesce(Sum('transaction_cost'), Decimal('0')))
            cost_wei, cost_ether = format_cost_data(aggregation['total_cost_wei_agg'])
            
            response_data.update({
                'filter_applied': 'all_time',
                'period_description': 'Todo o período',
                'total_transaction_cost_wei': cost_wei,
                'total_transaction_cost_display': cost_ether,
            })
            
        return Response(response_data, status=status.HTTP_200_OK)

    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete(request, id):
        try:
            blockchain = Blockchain.objects.get(pk=id)
            blockchain.delete()
            return Response({'message': 'Blockchain deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update(request, id):
        try:
            blockchain = Blockchain.objects.get(pk=id)
            serializer = BlockchainSerializer(instance=blockchain, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Blockchain not found'}, status=status.HTTP_404_NOT_FOUND)