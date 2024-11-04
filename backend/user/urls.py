from django.urls import path
from .views import UserViewSet, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserViewSet.register, name='register'),
    path('login/', UserViewSet.login, name='login'),
    path('profile/', UserViewSet.profile, name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
]