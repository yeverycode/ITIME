from django.contrib import admin
from .models import Post, Board, ArticleComment

# PostAdmin 설정 및 등록
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_anonymous')
    search_fields = ('title', 'content')

# 다른 모델 등록
admin.site.register(Board)
admin.site.register(ArticleComment)