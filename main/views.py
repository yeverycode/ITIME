# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'techtime/main.html')

@login_required
def main(request):
    user = request.user
    context = {
        'nickname': user.profile.nickname,  # 사용자의 닉네임
        'realname': user.profile.realname,  # 사용자의 본명
        'userid': user.username,  # 사용자의 아이디
    }
    return render(request, 'main.html', context)

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'profile_image_url': user.profile.profile_image.url,  # 예시로 프로필 이미지를 가져오는 방법
    }
    return render(request, 'profile.html', context)

# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
