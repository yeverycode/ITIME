from django import forms
from techtime.models import Post  # 변경된 부분

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
