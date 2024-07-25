from django.contrib import admin
from .models import Post, Lecture, Message, ChatRoom, Board, ArticleComment, Feed, Like, Reply, Bookmark
from user.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# UserAdmin 설정
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

# User 모델 등록
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

# Group 모델 등록 해제
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# PostAdmin 설정 및 등록
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_anonymous')
    search_fields = ('title', 'content')

# 다른 모델 등록
models = [Lecture, ChatRoom, Message, Board, ArticleComment, Feed, Like, Reply, Bookmark]

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass