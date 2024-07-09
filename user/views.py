from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views import View
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from uuid import uuid4
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from techtime.models import Post  # 변경된 부분
from .forms import PostForm
import json
from rest_framework.views import APIView
from rest_framework.response import Response


class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(status=400, data=dict(message="Invalid JSON"))

        name = data.get('name')
        student_id = data.get('student_id')
        nickname = data.get('nickname')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')

        User.objects.create(
            name=name,
            student_id=student_id,
            nickname=nickname,
            password=make_password(password),
            email=email,
            phone=phone,
            profile_image="default_profile.png"
        )

        return Response(status=200)


class Login(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # 로그인 성공 시 프로필 페이지로 리디렉션
        else:
            return render(request, "user/login.html", {'error': 'Invalid credentials'})


class LogOut(View):
    def get(self, request):
        logout(request)
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
            user.profile_image = profile_image
            user.save()

        return Response(status=200)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        return render(request, 'user/profile.html', {'user': user})


class BoardView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'techtime/board.html', {'posts': posts})


class BoardWriteView(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': '성공'}, status=200)
        return JsonResponse({'message': '에러', 'errors': form.errors}, status=400)
