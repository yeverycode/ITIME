from django.db import models
from user.models import User  # User 모델을 올바른 경로에서 가져오기

class Feed(models.Model):
    content = models.TextField()  # 글내용
    email = models.EmailField(default='')  # 글쓴이
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return self.content

class Like(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} likes {self.feed}"

class Reply(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='replies')
    email = models.EmailField(default='')
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Reply by {self.email} on {self.feed}"

class Bookmark(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='bookmarks')
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} bookmarked {self.feed}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_posts', default=1)

    def __str__(self):
        return self.title
