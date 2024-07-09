from django.urls import path
from .views import Join, Login, LogOut, UploadProfile, ProfileView, BoardView, BoardWriteView

urlpatterns = [
    path('join/', Join.as_view(), name='join'),  # 슬래시 추가
    path('login/', Login.as_view(), name='login'),  # 슬래시 추가
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/upload/', UploadProfile.as_view(), name='upload_profile'),  # 슬래시 추가
    path('profile/', ProfileView.as_view(), name='profile'),
    path('board/', BoardView.as_view(), name='board'),
    path('board/write/', BoardWriteView.as_view(), name='board_write'),
]
