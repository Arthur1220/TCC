from django.db import models
from user.models import User
from animal.models import Animal
from property.models import Property
from simple_history.models import HistoricalRecords
    
class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="recorded_events")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="events")
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.event_type.name} for {self.animal.identification} on {self.date}"
    
class Movement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='movements')
    origin_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='movements')
    destination_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='movements_to')
    date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Movement from {self.origin_property.name} to {self.destination_property.name} on {self.date}"

class Weighing(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='weighings')
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return f"Weighing of {self.weight} kg on {self.date}"

class Vacine(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='vaccines')
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    validity = models.DateField()
    dose = models.DecimalField(max_digits=10, decimal_places=2)
    next_dose_date = models.DateTimeField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} vaccine - {self.manufacturer} ({self.batch})"

class Medicine(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    validity = models.DateField()
    dose = models.DecimalField(max_digits=10, decimal_places=2)
    next_dose_date = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    withdrawal_time = models.IntegerField(blank=True, null=True)  # em dias
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.name} medicine - {self.manufacturer} ({self.batch})"

class Reproduction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reproductions')
    reproduction_type  = models.CharField(max_length=50, choices=[('natural', 'Natural'), ('artificial', 'Artificial')])
    male_id = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='reproductions_male')
    female_id = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='reproductions_female')
    date = models.DateTimeField()
    result = models.CharField(max_length=50, choices=[('positive', 'Positive'), ('negative', 'Negative')], blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.male_id} - {self.female_id} results in {self.resut} on {self.date}"

class Slaughter(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='slaughters')
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    final_weight = models.DecimalField(max_digits=10, decimal_places=2)
    inspection_result = models.CharField(max_length=50, choices=[('passed', 'Passed'), ('failed', 'Failed')], blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Slaughter on {self.date} at {self.location} with final weight {self.final_weight} kg"

class SpecialOccurrences(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='special_occurrences')
    occurrence_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    actions_taken = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Special occurrence: {self.occurrence_type} on {self.date} for {self.event.animal.identification}"