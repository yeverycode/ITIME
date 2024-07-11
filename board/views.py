from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Post
from .forms import PostForm

class BoardView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'board/post_list.html', {'posts': posts})

class BoardWriteView(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'message': '성공'}, status=200)
        return JsonResponse({'message': '에러', 'errors': form.errors}, status=400)

class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'board/post_detail.html', {'post': post})

