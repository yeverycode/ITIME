from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "techtime/main.html")

    def post(self, request):
        print("포스트로 호출")
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
class ProfileView(View):
    def get(self, request):
        user = request.user  # 현재 로그인한 사용자
        return render(request, 'user/profile.html', {'user': user})