# urls.py
from django.urls import path
from .views import lecture_room, lecture_detail, add_review

urlpatterns = [
    path('lecture-room/', lecture_room, name='lecture_room'),
    path('lecture/<int:lecture_id>/', lecture_detail, name='lecture_detail'),
    path('lecture/<int:lecture_id>/add_review/', add_review, name='add_review'),
]
