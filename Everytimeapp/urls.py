from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    user_profile_view, user_settings_view, LoginAPIView,
    signup_view, login_view, SignUpView, CustomBoardViewSet,
    CustomPostViewSet, index, category_list
)

# 라우터 설정
router = DefaultRouter()
router.register(r'boards', CustomBoardViewSet)
router.register(r'posts', CustomPostViewSet)

# URL 패턴 설정
urlpatterns = [
    path('profile/', user_profile_view, name='profile'),
    path('settings/', user_settings_view, name='settings'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('signup_api/', SignUpView.as_view(), name='signup_api'),
    path('login_api/', LoginAPIView.as_view(), name='login_api'),
    path('index/', index, name='index'),
    path('category/', category_list, name='category_list'),
    path('', include(router.urls)),  # 라우터 URL 포함
]

