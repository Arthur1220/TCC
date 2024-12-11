from django.urls import path
from .views import BlockchainViewSet, StatusViewSet

urlpatterns = [
    path('status/', StatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('status/<int:pk>/', StatusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('blockchain-register/', BlockchainViewSet.register),
    path('blockchain-get/', BlockchainViewSet.get),
    path('blockchain-get/<int:id>/', BlockchainViewSet.get),
    path('blockchain-update/<int:id>/', BlockchainViewSet.update),
    path('blockchain-delete/<int:id>/', BlockchainViewSet.delete),
    path('blockchain-filter/', BlockchainViewSet.filter_get)
]