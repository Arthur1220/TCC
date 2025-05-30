from django.urls import path
from .views import BlockchainViewSet, BlockchainStatusViewSet

urlpatterns = [
    # Rotas para BlockchainStatus (usando ModelViewSet padrão)
    path('status/', BlockchainStatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('status/<int:pk>/', BlockchainStatusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Rotas para Blockchain (usando @api_view, então referenciamos as funções diretamente)
    path('blockchain-register/', BlockchainViewSet.register, name='blockchain-register'),
    path('blockchain-get/', BlockchainViewSet.get, name='blockchain-get'), # Rota para listar todos
    path('blockchain-get/<int:id>/', BlockchainViewSet.get, name='blockchain-get-detail'), # Rota para detalhe por ID
    path('blockchain-update/<int:id>/', BlockchainViewSet.update, name='blockchain-update'),
    path('blockchain-delete/<int:id>/', BlockchainViewSet.delete, name='blockchain-delete'),
    path('blockchain-filter/', BlockchainViewSet.filter_get, name='blockchain-filter'),

    # Rota para obter custos de blockchain do usuário
    path('user-costs/', BlockchainViewSet.get_user_blockchain_costs, name='user-blockchain-costs'),
    path('user-costs-summary/', BlockchainViewSet.get_user_blockchain_costs_summary, name='user_blockchain_costs_summary'),
]