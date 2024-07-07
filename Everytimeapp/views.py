from django.views import View
from .models import Category
from rest_framework import viewsets
from .models import Account, Board, Post
from .serializers import BoardSerializer, PostSerializer
import json
import bcrypt
import re
from django.db.models import Q
from django.http import JsonResponse
from .forms import CustomUserCreationForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

MINIMUM_PASSWORD_LENGTH = 8  # 비밀번호 최소 길이 설정

# 회원가입 뷰 (폼 기반)
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 로그인 추가
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 이메일 유효성 검사
def validate_email(email):
    pattern = re.compile(r'^.+@+.+\.+.+$')
    if not pattern.match(email):
        return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

# 비밀번호 유효성 검사
def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'users/login.html', {'error': '로그인 실패', 'form': form})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# 전화번호 유효성 검사
def validate_phone(phone):
    pattern = re.compile(r'^[0]\d{9,10}$')
    if not pattern.match(phone):
        return JsonResponse({'message': 'INVALID_PHONE_NUMBER'}, status=400)

# 로그인 뷰 (폼 기반)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # 로그인 성공 시 리디렉션할 URL
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Wrong Credentials'})
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Wrong Credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
# 사용자 프로필 뷰
def user_profile_view(request):
    # 여기에 프로필 관련 로직 추가
    return render(request, 'users/profile.html')

def index(request):
    # 최근 게시물 가져오기
    recent_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'recent_posts': recent_posts
    }
    return render(request, 'index.html', context)
# 사용자 설정 뷰
def user_settings_view(request):
    # 사용자 설정 관련 로직 추가
    return render(request, 'users/settings.html')

def category_list(request):
    # 모든 카테고리 가져오기
    categories = Category.objects.all()

    # 각 카테고리에 속하는 게시물 수 계산
    category_data = []
    for category in categories:
        post_count = Post.objects.filter(board__category=category).count()
        category_data.append({
            'category': category,
            'post_count': post_count
        })

    context = {
        'categories': category_data
    }
    return render(request, 'category_list.html', context)

# 회원가입 뷰 (API 기반)
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data.get('email', None)
            password = data.get('password', None)
            name = data.get('name', None)
            nickname = data.get('nickname', None)
            phone = data.get('phone', None)

            if not (password and email and name and phone and nickname):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # Validation checks
            email_response = validate_email(email)
            if email_response:
                return email_response
            password_response = validate_password(password)
            if password_response:
                return password_response
            phone_response = validate_phone(phone)
            if phone_response:
                return phone_response

            # Check for existing user
            user = Account.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists()
            if user:
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

            # Create user
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            Account.objects.create(
                email=email,
                name=name,
                phone=phone,
                nickname=nickname,
                password=hashed_password
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)



import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

logger = logging.getLogger(__name__)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"Authenticating user: {username}")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            logger.debug(f"User authenticated, token: {token.key}")
            return Response({"token": token.key})
        else:
            logger.debug("Authentication failed")
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)



# Board ViewSet
class CustomBoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

# Post ViewSet
class CustomPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
