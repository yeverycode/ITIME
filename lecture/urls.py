# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lecture_room, name='lecture_room'),
    path('<int:pk>/', views.lecture_detail, name='lecture_detail'),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
]
