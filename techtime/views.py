from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Post, Board, Lecture, ArticleComment, Message
from .forms import PostForm, ProfileUpdateForm, CommentForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView

class Sub(APIView):
    def get(self, request):
        return render(request, "techtime/main.html")

class BoardView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'techtime/post.html', {'posts': posts})

@method_decorator(login_required, name='dispatch')
class BoardWriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'techtime/post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = Board.objects.get(id=1)  # 기본 보드를 설정합니다.
            if form.cleaned_data['is_anonymous']:
                post.is_anonymous = True
            post.save()
            return redirect('board')
        return render(request, 'techtime/post_form.html', {'form': form})

class ProfileUpdateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'user/profile_update.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save()
            response_data = {
                'success': True,
                'profile_image_url': profile.profile_image.url
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)

class UploadProfile(View):
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            profile = user.profile
            profile.profile_image = profile_image
            profile.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

class LectureView(View):
    def get(self, request):
        lectures = Lecture.objects.all()
        return render(request, 'techtime/lectures.html', {'lectures': lectures})

@method_decorator(login_required, name='dispatch')
class MessageSendView(View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'techtime/message_form.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
        return render(request, 'techtime/message_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class MessageListView(View):
    def get(self, request):
        received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
        sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
        return render(request, 'techtime/message_list.html', {
            'received_messages': received_messages,
            'sent_messages': sent_messages
        })

class ChatView(View):
    def get(self, request):
        return render(request, 'techtime/chat.html')

class PostDetailView(DetailView):
    model = Post
    template_name = 'techtime/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = ArticleComment.objects.filter(post=post)
        context['comment_form'] = CommentForm()
        context['is_liked'] = post.likes.filter(id=self.request.user.id).exists()
        context['is_bookmarked'] = post.bookmarks.filter(id=self.request.user.id).exists()
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

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.save()
        return redirect('post_detail', post_id=self.kwargs['post_id'])

class CommentDeleteView(DeleteView):
    model = ArticleComment
    template_name = 'techtime/post_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
