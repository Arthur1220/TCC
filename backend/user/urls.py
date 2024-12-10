from django.urls import path
from .views import UserViewSet, LogoutAPIView, RoleViewSet, UserRoleViewSet
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserViewSet.register, name='register'),
    path('login/', UserViewSet.login, name='login'),
    path('profile/', UserViewSet.profile, name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),

    
    path('getRoles/', RoleViewSet.get, name='getRoles'),
    path('getRole/<int:pk>/', RoleViewSet.get, name='getRole'),

    path('getUserRoles/', UserRoleViewSet.get, name='getUserRoles'),
    path('getUserRole/<int:pk>/', UserRoleViewSet.get, name='getUserRole'),
    path('createUserRole/', UserRoleViewSet.register, name='createUserRole'),
]