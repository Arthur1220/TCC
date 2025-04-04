from django.contrib import admin
from .models import Animal, IdentificationType, Specie, Breed, AnimalGroup, Gender, Status

admin.site.register(Specie)
admin.site.register(Breed)
admin.site.register(AnimalGroup)
admin.site.register(Animal)
admin.site.register(IdentificationType)
admin.site.register(Gender)
admin.site.register(Status)