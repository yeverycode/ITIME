from django.core.management.base import BaseCommand
import csv
from lecture.models import Lecture

class Command(BaseCommand):
    help = 'Import lectures from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                lecture, created = Lecture.objects.get_or_create(
                    course_name=row['과목명'],
                    course_code=row['과목번호'],
                    section=row['분반'],
                    schedule=row['강의시간'],
                    professor=row['담당교수'],
                    credits=row['학점'],
                    capacity=row['정원'],
                    course_type=row['교과구분']
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added {lecture.course_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'{lecture.course_name} already exists'))
