from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Account

# 사용자 생성 폼 정의
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'name', 'phone', 'nickname', 'password1', 'password2')

# 사용자 정보 수정 폼 정의
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email', 'name', 'phone', 'nickname')

# 사용자 로그인 폼 정의
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사용자 이름'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))
