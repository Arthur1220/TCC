from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('user/', include('user.urls')),
    path('property/', include('property.urls')),
    path('animal/', include('animal.urls')),
    path('event/', include('event.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('contract/', include('contract.urls')),

    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] 