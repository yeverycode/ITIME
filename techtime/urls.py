# urls.py
from django.urls import path, include
from .views import (
    Sub, Main, ProfileUpdateView, UploadProfile, LectureView,
    MessageSendView, MessageListView, ChatView, BoardDetailView
)

urlpatterns = [
    path('', Sub.as_view(), name='sub'),
    path('main/', Main.as_view(), name='main'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('upload_profile/', UploadProfile.as_view(), name='upload_profile'),
    path('lectures/', LectureView.as_view(), name='lectures'),
    path('messages/send/', MessageSendView.as_view(), name='message_send'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('board/<str:board_name>/', BoardDetailView.as_view(), name='board_detail'),  # 게시판 상세 보기 URL
]
