from django.urls import path
from .views import UserViewSet, RoleViewSet, UserRoleViewSet


urlpatterns = [
    path('register/', UserViewSet.register),
    path('login/', UserViewSet.login),
    path('profile/', UserViewSet.profile),
    path('update/', UserViewSet.update),
    path('refresh/', UserViewSet.refresh),
    path('logout/', UserViewSet.logout),

    
    path('getRoles/', RoleViewSet.get, name='getRoles'),
    path('getRole/<int:pk>/', RoleViewSet.get, name='getRole'),

    path('getUserRoles/', UserRoleViewSet.get, name='getUserRoles'),
    path('getUserRole/<int:pk>/', UserRoleViewSet.get, name='getUserRole'),
    path('createUserRole/', UserRoleViewSet.register, name='createUserRole'),
]