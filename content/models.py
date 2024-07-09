from django.db import models

class Feed(models.Model):
    content = models.TextField()  # 글내용
    email = models.EmailField(default='', blank=True, null=True)  # 글쓴이
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} - {self.content[:20]}"  # 글내용의 일부를 표시


class Like(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')
    email = models.EmailField(default='', blank=True, null=True)
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} likes {self.feed}"


class Reply(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='replies')
    email = models.EmailField(default='', blank=True, null=True)
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Reply by {self.email} on {self.feed}"


class Bookmark(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='bookmarks')
    email = models.EmailField(default='', blank=True, null=True)
    is_marked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.email} bookmarked {self.feed}"
