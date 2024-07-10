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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import ProfileUpdateForm
import logging

logger = logging.getLogger(__name__)

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

            if User.objects.filter(student_id=student_id).exists():
                return JsonResponse({'error': 'Student ID already exists'}, status=400)

            user = User.objects.create(
                name=name,
                student_id=student_id,
                nickname=nickname,
                password=make_password(password),
                email=email,
                phone=phone,
                profile_image="default_profile.png"
            )

            Profile.objects.create(user=user)

            return JsonResponse({'message': '회원가입 성공'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Login(View):
    def get(self, request):
        next_url = request.GET.get('next', 'profile')
        return render(request, "user/login.html", {'next': next_url})

    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        next_url = data.get('next', 'profile')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'redirect': next_url})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

class LogOut(View):
    def get(self, request):
        auth_logout(request)
        return redirect('/main/')

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
        user_profile = request.user.profile
        context = {
            'profile_image_url': user_profile.profile_image.url if user_profile.profile_image else None,
            'nickname': user_profile.nickname,
            'realname': request.user.name,
            'email': request.user.email,
            'student_id': request.user.student_id,
            'phone': request.user.phone,
            'additional_info': user_profile.additional_info,
        }
        return render(request, 'user/profile.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def get(self, request):
        user_profile = request.user.profile
        form = ProfileUpdateForm(instance=user_profile)
        return render(request, 'user/profile_update.html', {'form': form})

    def post(self, request):
        logger.debug('Received POST request')
        logger.debug(request.POST)
        logger.debug(request.FILES)

        user_profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})

        else:
            logger.error('Form is not valid')
            logger.error(form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
