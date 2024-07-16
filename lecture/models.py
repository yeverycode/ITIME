from django.db import models

class Lecture(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    schedule = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    credits = models.IntegerField()
    capacity = models.IntegerField()

class Review(models.Model):
    lecture = models.ForeignKey(Lecture, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)