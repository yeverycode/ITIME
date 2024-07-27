from django.db import models

class Lecture(models.Model):
    course_code = models.CharField(max_length=20)  # 과목번호
    course_name_ko = models.CharField(max_length=255)  # 과목명(국문)
    course_name_en = models.CharField(max_length=255)  # 과목명(영문)
    course_type = models.CharField(max_length=50)  # 인정교과구분 (전공필수, 전공선택 등)
    level = models.CharField(max_length=20, default="1학년")  # 이수단계 (학년)
    credits = models.CharField(max_length=10)  # 학점/이론/실습
    pf = models.CharField(max_length=10, blank=True, null=True)  # P/F 여부
    semester = models.CharField(max_length=20)  # 개설학기
    department = models.CharField(max_length=255)  # 주관학과
    summary = models.TextField(default="Course summary goes here.")  # 요약
    average_rating = models.FloatField(default=0.0)  # 평균 평점

    def __str__(self):
        return self.course_name_ko

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
        return f'{self.rating} - {self.lecture.course_name_ko}'
