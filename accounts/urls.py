from django.urls import path
from .views import signup_view, login_view, user_profile_view, user_settings_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', user_profile_view, name='profile'),
    path('settings/', user_settings_view, name='settings'),
]
