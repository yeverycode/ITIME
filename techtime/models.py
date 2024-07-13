from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 가져오기

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

from django.conf import settings

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name='techtime_posts')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, default=1, related_name='techtime_posts')
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
    post = models.ForeignKey(Post, related_name='techtime_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='techtime_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content