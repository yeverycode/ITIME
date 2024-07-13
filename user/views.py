from uuid import uuid4
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import json
import os
from django.http import JsonResponse
from .models import User, Profile
from techtime.models import Post
from techtime.forms import PostForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from config.utils import convert_to_korea_time

class Join(View):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            student_id = data.get('student_id')
            nickname = data.get('nickname')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')

            # 중복된 student_id 확인
            if User.objects.filter(student_id=student_id).exists():
                return JsonResponse({'error': 'Student ID already exists'}, status=400)

            user = User.objects.create(
                username=email,  # Django 기본 User 모델의 username 필드 사용
                name=name,
                student_id=student_id,
                password=make_password(password),
                email=email,
                phone=phone
            )

            Profile.objects.create(
                user=user,
                nickname=nickname,
                phone=phone,
                profile_image="profile_images/default_profile.png"
            )

            return JsonResponse({'message': '회원가입 성공'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Login(View):
    def get(self, request):
        next_url = request.GET.get('next', 'profile')  # GET 요청에서 next 매개변수를 가져옵니다.
        return render(request, "user/login.html", {'next': next_url})

    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        next_url = data.get('next', 'profile')  # POST 요청에서 next 매개변수를 가져옵니다.

        # User 모델이 이메일을 사용자명으로 사용하도록 설정되어 있는지 확인
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'redirect': next_url})  # 로그인 후 next_url로 리디렉션
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

class LogOut(View):
    def get(self, request):
        auth_logout(request)
        return redirect('/main/')  # 로그아웃 후 메인 페이지로 리디렉션

class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(settings.MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        if user:
            user.profile.profile_image = profile_image
            user.profile.save()

        return Response(status=200)

class BoardView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'techtime/post.html', {'posts': posts})

class BoardWriteView(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 작성자를 현재 사용자로 설정
            post.save()
            return JsonResponse({'message': '성공'}, status=200)
        return JsonResponse({'message': '에러', 'errors': form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        context = {
            'profile_image_url': user.profile.profile_image.url if user.profile.profile_image else None,
            'nickname': user.profile.nickname,
            'realname': user.name,
            'email': user.email,
            'student_id': user.student_id,
            'phone': user.profile.phone,  # 수정된 부분
        }
        return render(request, 'user/profile.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'user/profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'user/profile_update.html', {'form': form})

@login_required
def profile_image(request):
    profile = request.user.profile
    response_data = {
        'image_url': profile.profile_image.url if profile.profile_image else '/media/default_profile.png'
    }
    return JsonResponse(response_data)
