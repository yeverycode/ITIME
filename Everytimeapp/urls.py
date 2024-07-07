from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import user_profile_view, user_settings_view
from Everytimeapp.views import signup_view, login_view, SignUpView, CustomBoardViewSet, CustomPostViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'boards', CustomBoardViewSet)
router.register(r'posts', CustomPostViewSet)

urlpatterns = [
    path('profile/', user_profile_view, name='profile'),
    path('settings/', user_settings_view, name='settings'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('signup_api/', SignUpView.as_view(), name='signup_api'),
    path('', include(router.urls)),
]

