from django.contrib import admin
from .models import Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences, EventType, Event

admin.site.register(Movement)
admin.site.register(Weighing)
admin.site.register(Vacine)
admin.site.register(Medicine)
admin.site.register(Reproduction)
admin.site.register(Slaughter)
admin.site.register(SpecialOccurrences)
admin.site.register(EventType)
admin.site.register(Event)