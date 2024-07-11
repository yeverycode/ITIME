# board/forms.py


from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_anonymous']  # 익명 필드 추가
