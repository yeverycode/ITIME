from django.db import models

class Lecture(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    schedule = models.CharField(max_length=200)
    professor = models.CharField(max_length=100)
    credits = models.CharField(max_length=20)
    capacity = models.IntegerField()
    course_type = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class Review(models.Model):
    lecture = models.ForeignKey(Lecture, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecture.course_name} - {self.rating}"
