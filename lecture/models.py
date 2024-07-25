from django.db import models

class Lecture(models.Model):
    course_name = models.CharField(max_length=255, default="Default Course Name")
    course_code = models.CharField(max_length=20, default="DEFAULT_CODE")
    section = models.CharField(max_length=10, default="A")
    schedule = models.CharField(max_length=255, default="MWF 10-11 AM")
    professor = models.CharField(max_length=255, default="Default Professor")
    credits = models.IntegerField(default=3)
    capacity = models.IntegerField(default=30)
    summary = models.TextField(default="Course summary goes here.")
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.course_name


class Review(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(default="No comment")
    homework = models.CharField(max_length=10, default='N/A')
    groupwork = models.CharField(max_length=10, default='N/A')
    grading = models.CharField(max_length=10, default='N/A')
    attendance = models.CharField(max_length=20, default='N/A')
    exams = models.CharField(max_length=20, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.lecture.course_name}'
