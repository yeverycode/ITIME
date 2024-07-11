from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    login_id = models.CharField(max_length=30, unique=True, default=uuid.uuid4)
    username = models.CharField(max_length=30, default='default_username')
    name = models.CharField(max_length=30, default='default_name')
    phone = models.CharField(max_length=15, blank=True, null=True)  # 새로운 필드 추가
    student_id = models.CharField(max_length=30, default='')  # student_id 필드 추가
    status = models.CharField(max_length=30, default='default_status')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login_id', 'username', 'name']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/default_profile.png')
    nickname = models.CharField(max_length=100, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)  # phone 필드 추가

    def __str__(self):
        return self.nickname or self.user.email
