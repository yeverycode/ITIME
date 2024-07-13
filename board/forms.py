# board/forms.py


from django import forms
from .models import Post, ArticleComment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_anonymous']

class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content']
