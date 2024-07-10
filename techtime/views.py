from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from user.forms import ProfileUpdateForm  # 올바른 경로로 수정
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Sub(APIView):
    def get(self, request):
        return render(request, "techtime/main.html")

    def post(self, request):
        return render(request, "techtime/main.html")

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

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def get(self, request):
        user_profile = request.user.profile
        form = ProfileUpdateForm(instance=user_profile)
        return render(request, 'user/profile_update.html', {'form': form})

    def post(self, request):
        user_profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
