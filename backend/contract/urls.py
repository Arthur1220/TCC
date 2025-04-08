from django.urls import path
from .views import contract_status, register_contract_event, get_contract_event, get_number_events, add_registrar_view, remove_registrar_view

urlpatterns = [
    path('status/', contract_status),
    path('register-event/', register_contract_event),
    path('get-event/<int:animal_id>/', get_contract_event),
    path('get-number/<int:animal_id>/', get_number_events),
    path('add-registrar/', add_registrar_view),
    path('remove-registrar/', remove_registrar_view),
]
