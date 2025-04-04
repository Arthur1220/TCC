from django.contrib import admin
from .models import Blockchain, BlockchainStatus

admin.site.register(BlockchainStatus)
admin.site.register(Blockchain)