from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('schoolid', 'nickname')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('schoolid', 'nickname')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
