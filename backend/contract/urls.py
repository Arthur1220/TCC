from django.urls import path
from .views import (
    contract_status,
    register_contract_event,
    get_contract_event,
    list_contract_events,
    get_number_events,
    add_registrar_view,
    remove_registrar_view,
    pause_contract_view,
    unpause_contract_view,
)

urlpatterns = [
    path("status/", contract_status, name="contract-status"),
    path("register-contract-event/", register_contract_event, name="register-contract-event"),

    # GET single event
    path("get-event/<int:animal_id>/", get_contract_event, name="get-contract-event"),
    # GET all events
    path("list-events/<int:animal_id>/", list_contract_events, name="list-contract-events"),
    # GET count via query param
    path("get-number-events/", get_number_events, name="get-number-events"),

    path("add-registrar/", add_registrar_view, name="add-registrar"),
    path("remove-registrar/", remove_registrar_view, name="remove-registrar"),

    # Pause / Unpause
    path("pause/", pause_contract_view, name="pause-contract"),
    path("unpause/", unpause_contract_view, name="unpause-contract"),
]
