from django.urls import path
from .views import PropertyViewSet

urlpatterns = [
    path('register/', PropertyViewSet.register),
    path('get/', PropertyViewSet.get),
    path('get/<int:id>/', PropertyViewSet.get),
    path('update/<int:id>/', PropertyViewSet.update),
    path('delete/<int:id>/', PropertyViewSet.delete),
]