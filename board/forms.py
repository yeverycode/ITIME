# board/forms.py


from django import forms
from .models import Post, ArticleComment

class PostForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label='익명')  # 익명 체크박스 추가

    class Meta:
        model = Post
        fields = ['title', 'content', 'anonymous','file']

# forms.py
from django import forms
from .models import ArticleComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content', 'is_anonymous', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'is_anonymous': forms.CheckboxInput(),
            'parent': forms.HiddenInput(),
        }


