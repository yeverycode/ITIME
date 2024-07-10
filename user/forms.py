from django import forms
from techtime.models import Post  # 변경된 부분

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


# user/forms.py

from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'nickname']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_profile_image'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nickname'}),
        }