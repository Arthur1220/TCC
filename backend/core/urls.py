from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/', include('user.urls')),
    path('property/', include('property.urls')),
    path('animal/', include('animal.urls')),
    path('event/', include('event.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('contract/', include('contract.urls')),

    path('admin/', admin.site.urls),
]