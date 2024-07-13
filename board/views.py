from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Post, Board, ArticleComment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView

class BoardView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'board/post_list.html', {'posts': posts})

@method_decorator(login_required, name='dispatch')
class BoardWriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'board/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # 기본 보드를 가져오거나 생성합니다.
            board, created = Board.objects.get_or_create(name="기본 보드", defaults={'description': '기본 보드 설명'})
            post.board = board
            if form.cleaned_data['is_anonymous']:
                post.is_anonymous = True
            post.save()
            return redirect('board')
        return render(request, 'board/post_form.html', {'form': form})

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = ArticleComment.objects.filter(post=post)
        context['comment_form'] = CommentForm()
        context['is_liked'] = post.likes.filter(id=self.request.user.id).exists() if self.request.user.is_authenticated else False
        context['is_bookmarked'] = post.bookmarks.filter(id=self.request.user.id).exists() if self.request.user.is_authenticated else False
        return context

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked, 'bookmark_count': post.bookmarks.count()})

class CommentCreateView(CreateView):
    model = ArticleComment
    form_class = CommentForm
    template_name = 'board/post_detail.html'  # 댓글 생성 후 리디렉션할 템플릿

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.save()
        return redirect('post_detail', post_id=self.kwargs['post_id'])

class CommentDeleteView(DeleteView):
    model = ArticleComment
    template_name = 'board/post_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
