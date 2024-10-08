from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 가져오기
from django.contrib.auth.models import User

class Feed(models.Model):
    content = models.TextField()  # 글내용
    email = models.EmailField(default='')  # 글쓴이
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return self.content

class Like(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # 기본값 설정
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} likes {self.feed}"

class Reply(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='replies', default=1)  # 기본값 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # 기본값 설정
    email = models.EmailField(default='')
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Reply by {self.email} on {self.feed}"

class Bookmark(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='bookmarks', default=1)  # 기본값 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # 기본값 설정
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} bookmarked {self.feed}"

class Lecture(models.Model):
    name = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return self.name

class ChatRoom(models.Model):
    chat_room_id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_rooms', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_rooms', on_delete=models.CASCADE)

    def __str__(self):
        return f'ChatRoom {self.chat_room_id}'

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.id} in Room {self.chat_room.chat_room_id}'

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    allow_anony = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='techtime_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    like_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_techtime_posts', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_techtime_posts', blank=True)

    def __str__(self):
        return self.title



class ArticleComment(models.Model):
    id = models.AutoField(primary_key=True)  # 기본 키 명시적으로 정의
    post = models.ForeignKey(Post, related_name='techtime_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='techtime_article_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Scrap(models.Model):
    id = models.AutoField(primary_key=True)  # 기본 키 명시적으로 정의
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='techtime_scraps')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # 기본 키 명시적으로 정의
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='techtime_post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    # 기타 필드들

    def __str__(self):
        return self.username


class Course(models.Model):
    course_number = models.CharField(max_length=20)
    course_name_ko = models.CharField(max_length=100)  # 수정할 필드 이름 확인
    course_name_en = models.CharField(max_length=100)
    course_type = models.CharField(max_length=50)
    course_level = models.CharField(max_length=10)
    credits = models.CharField(max_length=10)
    pf = models.CharField(max_length=2, null=True, blank=True)
    semester = models.CharField(max_length=10)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name_kr