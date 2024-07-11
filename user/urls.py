from django.urls import path
from .views import Join, Login, LogOut, UploadProfile, BoardView, BoardWriteView, ProfileView, ProfileUpdateView, profile_image

urlpatterns = [
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('upload-profile/', UploadProfile.as_view(), name='upload_profile'),
    path('board/', BoardView.as_view(), name='board'),
    path('board/write/', BoardWriteView.as_view(), name='board_write'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile-image/', profile_image, name='profile_image'),  # 추가된 부분
]
