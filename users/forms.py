from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'schoolid', 'nickname', 'password1', 'password2')
        labels = {
            'username': '사용자 이름',
            'email': '이메일 주소',
            'schoolid': '학번',
            'nickname': '닉네임',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        help_texts = {
            'username': '영어, 한글, 숫자, @/./+/-/_ 문자만 사용하세요.',
        }
        error_messages = {
            'username': {
                'required': '사용자 이름을 입력하세요.',
                'unique': '이미 존재하는 사용자 이름입니다.',
            },
            'email': {
                'required': '이메일 주소를 입력하세요.',
                'invalid': '유효한 이메일 주소를 입력하세요.',
            },
            'password1': {
                'required': '비밀번호를 입력하세요.',
                'min_length': '비밀번호는 최소 8자 이상이어야 합니다.',
            },
            'password2': {
                'required': '비밀번호 확인을 입력하세요.',
                'password_mismatch': '비밀번호가 일치하지 않습니다.',
            },
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'schoolid', 'nickname')
        labels = {
            'username': '사용자 이름',
            'email': '이메일 주소',
            'schoolid': '학번',
            'nickname': '닉네임',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사용자 이름'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))
