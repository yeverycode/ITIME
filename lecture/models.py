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
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    homework = models.CharField(max_length=10, choices=[('many', '많음'), ('average', '보통'), ('none', '없음')])
    groupwork = models.CharField(max_length=10, choices=[('many', '많음'), ('average', '보통'), ('none', '없음')])
    grading = models.CharField(max_length=10, choices=[('generous', '너그러움'), ('average', '보통'), ('strict', '깐깐함')])
    attendance = models.CharField(max_length=10, choices=[('complex', '복합적'), ('direct', '직접호명'), ('designated', '지정좌석'), ('electronic', '전자출결'), ('none', '반영안함')])
    exams = models.CharField(max_length=10, choices=[('4_or_more', '네 번 이상'), ('3', '세 번'), ('2', '두 번'), ('1', '한 번'), ('none', '없음')])