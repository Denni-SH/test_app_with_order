from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.user.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'username','phone_number', 'public_id', 'id', 'last_login']
    readonly_fields = ['last_login', ]


admin.site.register(User, UserAdmin)
