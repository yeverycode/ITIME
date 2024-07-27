import csv
from django.core.management.base import BaseCommand
from lecture.models import Lecture

class Command(BaseCommand):
    help = 'Import courses from a CSV file'

    def handle(self, *args, **kwargs):
        with open('EXPORT.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Lecture.objects.create(
                    course_code=row['\ufeff과목번호'],
                    course_name_ko=row['과목명(국문)'],
                    course_name_en=row['과목명(영문)'],
                    course_type=row['인정교과구분'],
                    level=row['이수단계'],
                    credits=row['학점/이론/실습'],
                    pf=row.get('P/F', ''),
                    semester=row['개설학기'],
                    department=row['주관학과'],
                    summary='Course summary goes here.'  # 기본 요약
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {row["과목명(국문)"]}'))
