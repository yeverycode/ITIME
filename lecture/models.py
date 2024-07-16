from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    course_name = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    summary = models.TextField()
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.course_name

class Review(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    homework = models.CharField(max_length=10, default='N/A')
    groupwork = models.CharField(max_length=10, default='N/A')
    grading = models.CharField(max_length=10, default='N/A')
    attendance = models.CharField(max_length=20, default='N/A')
    exams = models.CharField(max_length=20, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.lecture.course_name}'
