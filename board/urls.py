# board/urls.py

from django.urls import path
from .views import BoardView, BoardWriteView, PostDetailView

urlpatterns = [
    path('', BoardView.as_view(), name='board'),
    path('user/', BoardView.as_view(), name='user_board'),
    path('write/', BoardWriteView.as_view(), name='board_write'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
