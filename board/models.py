from django.db import models
from django.conf import settings

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

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)  # 익명 필드 추가
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_posts', blank=True)
    view_count = models.IntegerField(default=0)  # 추가된 view_count 필드

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings

class ArticleComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255, blank=True)  # 닉네임 필드 추가
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)  # 익명 여부 필드 추가

    def save(self, *args, **kwargs):
        if self.is_anonymous:
            self.nickname = '익명'
        else:
            self.nickname = self.user.profile.nickname
        super().save(*args, **kwargs)


class LectureReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user}"
