from django.contrib import admin
from .models import User, Role, UserRole

admin.site.register(User)
admin.site.register(Role)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('user', 'role')
    search_fields = ('user__username', 'role__name')