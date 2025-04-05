from django.urls import path
from .views import contract_status, register_contract_event, get_contract_event, get_number_events

urlpatterns = [
    path('status/', contract_status, name="contract-status"),
    path('register-event/', register_contract_event, name="register-contract-event"),
    path('get-event/', get_contract_event, name="get-contract-event"),
    path('get-number/', get_number_events, name="get-number-events"),
]
