from django.urls import path
from .views import MovementViewSet, WeighingViewSet, VacineViewSet, MedicineViewSet, ReproductionViewSet, SlaughterViewSet, SpecialOccurrencesViewSet, EventTypeViewSet, EventViewSet

urlpatterns = [
    path('movement-register/', MovementViewSet.register),
    path('movement-get/', MovementViewSet.get),
    path('movement-get/<int:id>/', MovementViewSet.get),
    path('movement-update/<int:id>/', MovementViewSet.update),
    path('movement-delete/<int:id>/', MovementViewSet.delete),
    path('movement-filter/', MovementViewSet.filter_get),

    path('weighing-register/', WeighingViewSet.register),
    path('weighing-get/', WeighingViewSet.get),
    path('weighing-get/<int:id>/', WeighingViewSet.get),
    path('weighing-update/<int:id>/', WeighingViewSet.update),
    path('weighing-delete/<int:id>/', WeighingViewSet.delete),
    path('weighing-filter/', WeighingViewSet.filter_get),

    path('vacine-register/', VacineViewSet.register),
    path('vacine-get/', VacineViewSet.get),
    path('vacine-get/<int:id>/', VacineViewSet.get),
    path('vacine-update/<int:id>/', VacineViewSet.update),
    path('vacine-delete/<int:id>/', VacineViewSet.delete),
    path('vacine-filter/', VacineViewSet.filter_get),

    path('medicine-register/', MedicineViewSet.register),
    path('medicine-get/', MedicineViewSet.get),
    path('medicine-get/<int:id>/', MedicineViewSet.get),
    path('medicine-update/<int:id>/', MedicineViewSet.update),
    path('medicine-delete/<int:id>/', MedicineViewSet.delete),
    path('medicine-filter/', MedicineViewSet.filter_get),

    path('reproduction-register/', ReproductionViewSet.register),
    path('reproduction-get/', ReproductionViewSet.get),
    path('reproduction-get/<int:id>/', ReproductionViewSet.get),
    path('reproduction-update/<int:id>/', ReproductionViewSet.update),
    path('reproduction-delete/<int:id>/', ReproductionViewSet.delete),
    path('reproduction-filter/', ReproductionViewSet.filter_get),

    path('slaughter-register/', SlaughterViewSet.register),
    path('slaughter-get/', SlaughterViewSet.get),
    path('slaughter-get/<int:id>/', SlaughterViewSet.get),
    path('slaughter-update/<int:id>/', SlaughterViewSet.update),
    path('slaughter-delete/<int:id>/', SlaughterViewSet.delete),
    path('slaughter-filter/', SlaughterViewSet.filter_get),

    path('special-occurrences-register/', SpecialOccurrencesViewSet.register),
    path('special-occurrences-get/', SpecialOccurrencesViewSet.get),
    path('special-occurrences-get/<int:id>/', SpecialOccurrencesViewSet.get),
    path('special-occurrences-update/<int:id>/', SpecialOccurrencesViewSet.update),
    path('special-occurrences-delete/<int:id>/', SpecialOccurrencesViewSet.delete),
    path('special-occurrences-filter/', SpecialOccurrencesViewSet.filter_get),

    path('event-type/', EventTypeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('event-type/<int:pk>/', EventTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('event-register/', EventViewSet.register),
    path('event-get/', EventViewSet.get),
    path('event-get/<int:id>/', EventViewSet.get),
    path('event-update/<int:id>/', EventViewSet.update),
    path('event-delete/<int:id>/', EventViewSet.delete),
    path('event-filter/', EventViewSet.filter_get),

    path('event-register-batch/', EventViewSet.register_batch_event),
]