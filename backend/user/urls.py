from django.urls import path
from .views import UserViewSet, RoleViewSet, UserRoleViewSet


urlpatterns = [
    path('register/', UserViewSet.register),
    path('login/', UserViewSet.login),
    path('profile/', UserViewSet.profile),
    path('update/', UserViewSet.update),
    path('refresh/', UserViewSet.refresh),
    path('logout/', UserViewSet.logout),
    path('all_users/', UserViewSet.list_all_users, name='list_all_users'), # NOVO ENDPOINT

    path('roles/', RoleViewSet.get, name='get_roles'),
    path('roles/<int:pk>/', RoleViewSet.get, name='get_role_detail'),

    path('user_roles/', UserRoleViewSet.get, name='get_user_roles'),
    path('user_roles/<int:pk>/', UserRoleViewSet.get, name='get_user_role_detail'),
    path('user_roles/assign/', UserRoleViewSet.assign_role, name='assign_user_role'),
    path('user_roles/remove/<int:user_id>/<int:role_id>/', UserRoleViewSet.remove_role, name='remove_user_role'),
]