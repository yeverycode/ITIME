from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'login_id', 'username', 'name', 'status', 'is_staff', 'is_superuser', 'is_admin')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('login_id', 'username', 'name', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'login_id', 'username', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'login_id', 'username', 'name')
    ordering = ('email',)
    filter_horizontal = ()

# User 모델을 관리 사이트에 등록하기 전에 이미 등록되어 있는지 확인
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Profile 모델을 관리 사이트에 등록
try:
    admin.site.register(Profile)
except admin.sites.AlreadyRegistered:
    pass
