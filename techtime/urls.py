from django.urls import path, include
from .views import (
    Sub, ProfileUpdateView, UploadProfile, LectureView,
    MessageSendView, MessageListView, ChatView
)

urlpatterns = [
    path('', Sub.as_view(), name='main'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('upload_profile/', UploadProfile.as_view(), name='upload_profile'),
    path('lectures/', LectureView.as_view(), name='lectures'),
    path('messages/send/', MessageSendView.as_view(), name='message_send'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('board/', include('board.urls')),  # board 앱의 URL 포함
]
