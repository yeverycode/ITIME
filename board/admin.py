from django.contrib import admin
from .models import Board,ArticleComment

admin.site.register(Board)
admin.site.register(ArticleComment)  # 댓글 모델을 등록
