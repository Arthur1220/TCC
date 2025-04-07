from django.urls import path
from .views import contract_status, register_contract_event, get_contract_event, get_number_events

urlpatterns = [
    path('status/', contract_status),
    path('register-event/', register_contract_event),
    path('get-event/<int:pk>/', get_contract_event),
    path('get-number/<int:pk>/', get_number_events),
]
