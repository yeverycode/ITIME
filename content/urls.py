from django.urls import path
from .views import Main, LectureView

urlpatterns = [
    path('', Main.as_view(), name='main'),
path('lectures/', LectureView.as_view(), name='lectures'),

]
