from django.urls import path
from .views import BoardView, BoardWriteView, PostDetailView, like_post, bookmark_post, CommentCreateView, CommentDeleteView

urlpatterns = [
    path('', BoardView.as_view(), name='board'),
    path('write/', BoardWriteView.as_view(), name='board_write'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/bookmark/', bookmark_post, name='bookmark_post'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]
