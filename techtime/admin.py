from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Post  # Post 모델 가져오기
from user.models import User  # User 모델을 올바른 경로에서 가져오기

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'login_id', 'username', 'name', 'status', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('login_id', 'username', 'name', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
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

# Group 모델을 관리 사이트에서 제거
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Post 모델을 관리 사이트에 등록
try:
    admin.site.register(Post)
except admin.sites.AlreadyRegistered:
    pass
