from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Account
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, LoginForm

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])
        name = request.POST['name']
        nickname = request.POST['nickname']

        account = Account(email=email, phone=phone, password=password, name=name, nickname=nickname)
        account.save()
        return redirect('login')
    return render(request, 'register.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_profile_view(request):
    # 여기에 사용자 프로필 관련 로직을 추가하세요
    return render(request, 'users/profile.html')

def user_settings_view(request):
    # 여기에 사용자 설정 관련 로직을 추가하세요
    return render(request, 'users/settings.html')