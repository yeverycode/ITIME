from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Post
from .forms import PostForm, ProfileUpdateForm  # 올바른 경로로 수정
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Sub(APIView):
    def get(self, request):
        return render(request, "techtime/main.html")

    def post(self, request):
        return render(request, "techtime/main.html")

class BoardView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'techtime/board.html', {'posts': posts})

class BoardWriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'techtime/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = form.cleaned_data['category']
            if form.cleaned_data['anonymous']:
                post.is_anonymous = True
            post.save()
            return redirect('post_list')
        return render(request, 'techtime/post_form.html', {'form': form})

class ProfileUpdateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile)  # 수정된 부분
        return render(request, 'user/profile_update.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  # 수정된 부분
        if form.is_valid():
            profile = form.save()
            response_data = {
                'success': True,
                'profile_image_url':profile.profile_image.url   # 프로필 이미지 URL을 JSON 응답에 포함
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)
