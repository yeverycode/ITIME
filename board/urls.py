from django.urls import path
from .views import (
    Main, BoardDetailView, PostDetailView, CommentCreateView,
    CommentDeleteView, like_post, bookmark_post, BoardWriteView,
    UserCommentsView, PostUpdateView, PostDeleteView, SearchResultsView, scrapped_posts  # 추가된 부분
)

urlpatterns = [
    path('main/', Main.as_view(), name='main'),
    path('board/<str:board_name>/', BoardDetailView.as_view(), name='board_detail'),
    path('board/<str:board_name>/write/', BoardWriteView.as_view(), name='board_write'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', bookmark_post, name='bookmark_post'),
    path('post/<int:post_id>/comment/add/', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:post_id>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('user/comments/', UserCommentsView.as_view(), name='user_comments'),
    path('user/scrapped_posts/', scrapped_posts, name='scrapped_posts'),  # 스크랩한 글 URL 추가
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
