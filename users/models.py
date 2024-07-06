from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    schoolid = models.CharField(max_length=20, unique=True, blank=True, null=True)  # 학번 필드에 기본값 추가
    nickname = models.CharField(max_length=50, unique=True, default='닉네임')  # 닉네임 필드에 기본값 추가
