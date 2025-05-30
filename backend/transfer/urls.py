  # transfer/urls.py
from django.urls import path
from .views import OwnershipTransferViewSet

# Para actions no ViewSet, precisamos mapeá-las explicitamente se não usarmos routers
# e se os métodos não forem estáticos.
# Nossos métodos estáticos já são mapeados individualmente.

urlpatterns = [
    # URLs para métodos estáticos
    path('requests/create/', OwnershipTransferViewSet.create_request, name='transfer-request-create'),
    path('requests/sent/', OwnershipTransferViewSet.list_sent_requests, name='transfer-request-list-sent'),
    path('requests/received/', OwnershipTransferViewSet.list_received_requests, name='transfer-request-list-received'),
    path('requests/<int:pk>/', OwnershipTransferViewSet.retrieve_request, name='transfer-request-retrieve'),

    # URLs para @action no ViewSet (precisam de .as_view() com o mapeamento do método)
    path('requests/<int:pk>/cancel/', OwnershipTransferViewSet.as_view({'post': 'cancel_request'}), name='transfer-request-cancel'),
    path('requests/<int:pk>/reject/', OwnershipTransferViewSet.as_view({'post': 'reject_request'}), name='transfer-request-reject'),
    path('requests/<int:pk>/approve/', OwnershipTransferViewSet.as_view({'post': 'approve_and_process_request'}), name='transfer-request-approve'),
]