from django.urls import path
from .views import BoardView, BoardWriteView

urlpatterns = [
    path('board/', BoardView.as_view(), name='board'),
    path('board/write/', BoardWriteView.as_view(), name='board_write'),
]
