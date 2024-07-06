# Everytimeapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category_list, name='category_list'),
    path('', views.index, name='home'),  # 'home' URL 패턴 정의
]
