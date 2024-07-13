from django.contrib import admin
from .models import Post, Lecture, Message, ChatRoom, Board, ArticleComment, Feed, Like, Reply, Bookmark
from user.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

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

try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.register(Post)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Lecture)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(ChatRoom)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Message)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Board)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(ArticleComment)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Feed)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Like)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Reply)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Bookmark)
except admin.sites.AlreadyRegistered:
    pass
