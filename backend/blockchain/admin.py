from django.contrib import admin
from .models import Blockchain, Status

admin.site.register(Status)
admin.site.register(Blockchain)