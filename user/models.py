from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nickname, password, **extra_fields)

class User(AbstractBaseUser):
    """
        유저 프로파일 사진
        유저 닉네임     -> 화면에 표기되는 이름
        유저 이름       -> 실제 사용자 이름
        유저 이메일주소 -> 회원가입할때 사용하는 아이디
        유저 학번 -> 실제 학번
        유저 비밀번호 -> 디폴트 값
        익명 여부 -> 사용자가 익명으로 활동할지 여부
    """
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # 프로필 이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=10, unique=True)  # 학번 추가
    phone = models.CharField(max_length=15)  # 전화번호 추가
    is_anonymous_user = models.BooleanField(default=False)  # 익명 여부 추가

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = "User"

