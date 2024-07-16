# board/forms.py


from django import forms
from .models import Post, ArticleComment

class PostForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label='익명')  # 익명 체크박스 추가

    class Meta:
        model = Post
        fields = ['title', 'content', 'anonymous']

from django import forms
from .models import ArticleComment

class CommentForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label='익명')  # 익명 체크박스 추가

    class Meta:
        model = ArticleComment
        fields = ['content', 'anonymous']


