# animal/urls.py
from django.urls import path
from .views import SpecieViewSet, BreedViewSet, AnimalGroupViewSet, GenderViewSet, StatusViewSet, IdentificationTypeViewSet, AnimalViewSet

urlpatterns = [
    # Species URLs
    path('species/', SpecieViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('species/<int:pk>/', SpecieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Breed URLs
    path('breed/', BreedViewSet.as_view({'get': 'list', 'post': 'create'})), # Frontend service pode precisar de ?specie_id=X
    path('breed/<int:pk>/', BreedViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Animal Group URLs
    path('animal-group/', AnimalGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('animal-group/<int:pk>/', AnimalGroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Gender URLs
    path('gender/', GenderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('gender/<int:pk>/', GenderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Status URLs
    path('status/', StatusViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('status/<int:pk>/', StatusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Identification Type URLs
    path('identification-type/', IdentificationTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('identification-type/<int:pk>/', IdentificationTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Animal URLs (usando os métodos estáticos e a ação de instância)
    path('animal-register/', AnimalViewSet.register),
    path('animal-get/', AnimalViewSet.get),
    path('animal-get/<int:id>/', AnimalViewSet.get), # :id será o parâmetro 'id' na view
    path('animal-update/<int:id>/', AnimalViewSet.update), # :id será o parâmetro 'id' na view
    path('animal-delete/<int:id>/', AnimalViewSet.delete), # :id será o parâmetro 'id' na view
    path('animal-filter/', AnimalViewSet.filter_get),

    # Ação de instância para update_batch
    path('update-batch/', AnimalViewSet.as_view({'patch': 'update_batch'}), name='animal-update-batch'),
]