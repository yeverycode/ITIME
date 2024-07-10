from django.urls import path
from .views import Join, Login, LogOut, UploadProfile, ProfileView, ProfileUpdateView

urlpatterns = [
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('upload_profile/', UploadProfile.as_view(), name='upload_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
