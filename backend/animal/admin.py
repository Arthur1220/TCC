from django.contrib import admin
from .models import Sex, Status, Species, Breed, Animal

admin.site.register(Sex)
admin.site.register(Status)
admin.site.register(Species)
admin.site.register(Breed)
admin.site.register(Animal)