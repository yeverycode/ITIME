from django.urls import path
from .views import user_profile_view, user_settings_view
from Everytimeapp.views import signup, login  # 필요에 따라 views를 import
from .views import login_view, signup_view, user_profile_view, user_settings_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', user_profile_view, name='profile'),
    path('settings/', user_settings_view, name='settings'),
    # 다른 URL 패턴들 추가
]
