from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
<<<<<<< HEAD
    course_name = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    summary = models.TextField()
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.course_name
=======
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    schedule = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    credits = models.IntegerField()
    capacity = models.IntegerField()
>>>>>>> 681c4ee7779b45b291f92a244e7e5498b9468f80

class Review(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
<<<<<<< HEAD
    homework = models.CharField(max_length=10, default='N/A')
    groupwork = models.CharField(max_length=10, default='N/A')
    grading = models.CharField(max_length=10, default='N/A')
    attendance = models.CharField(max_length=20, default='N/A')
    exams = models.CharField(max_length=20, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.lecture.course_name}'
=======
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> 681c4ee7779b45b291f92a244e7e5498b9468f80
