from django.urls import path
from .views import SexViewSet, StatusViewSet, SpeciesViewSet, BreedViewSet, AnimalViewSet

urlpatterns = [
    path('registerSex/', SexViewSet.create, name='register'),
    path('getSex/', SexViewSet.list, name='get'),
    path('getSex/<int:pk>/', SexViewSet.list, name='get'),
    path('deleteSex/<int:pk>/', SexViewSet.delete, name='delete'),

    path('registerStatus/', StatusViewSet.create, name='register'),
    path('getStatus/', StatusViewSet.list, name='get'),
    path('getStatus/<int:pk>/', StatusViewSet.list, name='get'),
    path('deleteStatus/<int:pk>/', StatusViewSet.delete, name='delete'),

    path('registerSpecies/', SpeciesViewSet.create, name='register'),
    path('getSpecies/', SpeciesViewSet.list, name='get'),
    path('getSpecies/<int:pk>/', SpeciesViewSet.list, name='get'),
    path('deleteSpecies/<int:pk>/', SpeciesViewSet.delete, name='delete'),

    path('registerBreed/', BreedViewSet.create, name='register'),
    path('getBreed/', BreedViewSet.list, name='get'),
    path('getBreed/<int:pk>/', BreedViewSet.list, name='get'),
    path('deleteBreed/<int:pk>/', BreedViewSet.delete, name='delete'),

    path('registerAnimal/', AnimalViewSet.create, name='register'),
    path('getAnimal/', AnimalViewSet.list, name='get'),
    path('getAnimal/<int:pk>/', AnimalViewSet.list, name='get'),
    path('deleteAnimal/<int:pk>/', AnimalViewSet.delete, name='delete'),
    path('updateAnimal/<int:pk>/', AnimalViewSet.update, name='update'),
]