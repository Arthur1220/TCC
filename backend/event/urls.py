from django.urls import path
from .views import EventTypeViewSet, EventViewSet

urlpatterns = [
    path('event-type/', EventTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('event-type/<int:pk>/', EventTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('event-register/', EventViewSet.register),
    path('event-get/', EventViewSet.get),
    path('event-get/<int:id>/', EventViewSet.get),
    path('event-update/<int:id>/', EventViewSet.update),
    path('event-delete/<int:id>/', EventViewSet.delete),
    path('event-filter/', EventViewSet.filter_get)
]