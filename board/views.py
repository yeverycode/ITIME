# board/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from .models import Post, Board, ArticleComment, LectureReview, PostBookmark
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
class Main(APIView):
    def get(self, request):
        feeds = Post.objects.all().order_by('-created_at')

        boards = Board.objects.all()
        boards_with_posts = {}
        for board in boards:
            boards_with_posts[board.name] = Post.objects.filter(board=board).order_by('-created_at')[:5]

        popular_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
        hot_posts = Post.objects.order_by('-view_count')[:3]
        recent_reviews = LectureReview.objects.order_by('-created_at')[:5]

        context = {
            'feeds': feeds,
            'boards_with_posts': boards_with_posts,
            'popular_posts': popular_posts,
            'hot_posts': hot_posts,
            'recent_reviews': recent_reviews,
        }

        return render(request, "techtime/main.html", context)

class BoardWriteView(View):
    @method_decorator(login_required)
    def get(self, request, board_name):
        form = PostForm()
        return render(request, 'board/post_form.html', {'form': form, 'board_name': board_name})

    @method_decorator(login_required)
    def post(self, request, board_name):
        board = get_object_or_404(Board, name=board_name)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = board
            post.is_anonymous = form.cleaned_data.get('anonymous', False)  # 익명 설정
            post.save()
            return redirect('board_detail', board_name=board_name)
        return render(request, 'board/post_form.html', {'form': form, 'board_name': board_name})

class BoardDetailView(View):
    def get(self, request, board_name):
        board = get_object_or_404(Board, name=board_name)
        posts = Post.objects.filter(board=board).order_by('-created_at')
        form = PostForm()  # 게시글 작성 폼 추가
        return render(request, 'board/board_detail.html', {'board': board, 'posts': posts, 'form': form})

    @method_decorator(login_required)
    def post(self, request, board_name):
        board = get_object_or_404(Board, name=board_name)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = board
            post.save()
            return redirect('board_detail', board_name=board_name)
        posts = Post.objects.filter(board=board).order_by('-created_at')
        return render(request, 'board/board_detail.html', {'board': board, 'posts': posts, 'form': form})

from django.db.models import Count

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.view_count += 1  # 조회수 증가
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = ArticleComment.objects.filter(post=post)
        context['comment_form'] = CommentForm()
        context['is_liked'] = post.likes.filter(id=self.request.user.id).exists()
        context['is_bookmarked'] = post.bookmarks.filter(id=self.request.user.id).exists()
        context['bookmark_count'] = PostBookmark.objects.filter(post=post).count()  # 스크랩 카운트 추가

        # 실시간 인기 글: 가장 많은 좋아요를 받은 게시물 (3개)
        context['popular_posts'] = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

        # HOT 게시물: 가장 많은 조회수를 가진 게시물 (3개)
        context['hot_posts'] = Post.objects.order_by('-view_count')[:3]

        # 최근 강의평: 가장 최근에 작성된 강의 평가
        context['recent_reviews'] = LectureReview.objects.order_by('-created_at')[:5]

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
    bookmark, created = PostBookmark.objects.get_or_create(user=request.user, post=post)

    if not created:
        # 이미 북마크가 존재하는 경우 삭제
        bookmark.delete()
        is_bookmarked = False
    else:
        # 북마크가 새로 생성된 경우
        is_bookmarked = True

    # bookmark_count를 PostBookmark 모델에서 직접 계산
    bookmark_count = PostBookmark.objects.filter(post=post).count()

    return JsonResponse({'bookmarked': is_bookmarked, 'bookmark_count': bookmark_count})


class CommentCreateView(CreateView):
    model = ArticleComment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.is_anonymous = self.request.POST.get('anonymous') == 'on'
        form.save()
        return redirect('post_detail', post_id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse('post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(DeleteView):
    model = ArticleComment
    template_name = 'techtime/post_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class CommentCreateView(CreateView):
    model = ArticleComment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.is_anonymous = form.cleaned_data.get('anonymous', False)  # 익명 필드 설정
        form.save()
        return redirect('post_detail', post_id=self.kwargs['post_id'])

# board/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class UserCommentsView(LoginRequiredMixin, ListView):
    model = ArticleComment
    template_name = 'board/user_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        # post가 None이 아닌 댓글만 필터링
        return ArticleComment.objects.filter(user=self.request.user).exclude(post__isnull=True).select_related('post')

from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Post  # 사용 중인 Post 모델을 가져옵니다

# Post 업데이트 뷰
# Post 업데이트 뷰
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'file', 'is_anonymous']
    template_name = 'board/post_edit.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

# Post 삭제 뷰
# Post 삭제 뷰
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    success_url = reverse_lazy('main')
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

from django.views.generic import ListView
from .models import Post

class SearchResultsView(ListView):
    model = Post
    template_name = 'board/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(content__icontains=query)

from .models import PostBookmark

@login_required
def scrapped_posts(request):
    scrapped_posts_list = PostBookmark.objects.filter(user=request.user).select_related('post').order_by('-created_at')
    paginator = Paginator(scrapped_posts_list, 10)  # 한 페이지에 10개 게시글을 표시

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'board/scrap_list.html', context)

# views.py
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'board/post_detail.html', {'post': post, 'form': form, 'comments': post.comments.filter(parent__isnull=True)})

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(ArticleComment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('post_detail', post_id=post_id)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent__isnull=True)
    form = CommentForm()
    return render(request, 'board/post_detail.html', {'post': post, 'comments': comments, 'form': form})
