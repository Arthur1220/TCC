from django.db import models
from user.models import User
from animal.models import Animal

class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="events")
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="recorded_events")

    def __str__(self):
        return f"{self.event_type.name} for {self.animal.identification} on {self.event_date}"