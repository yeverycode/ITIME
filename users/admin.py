# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Board, Category, Post

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'name', 'phone', 'nickname', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'nickname')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'nickname', 'password1', 'password2', 'is_admin', 'is_active')}
        ),
    )
    search_fields = ('email', 'name', 'phone', 'nickname')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'board', 'category', 'created_at', 'updated_at')
