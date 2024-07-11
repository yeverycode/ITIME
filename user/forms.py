from django import forms
from techtime.models import Post  # 변경된 부분
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

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

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'login_id', 'username', 'name', 'status')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'login_id', 'username', 'name', 'password', 'status', 'is_active', 'is_staff', 'is_superuser')