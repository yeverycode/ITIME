# Generated by Django 3.2.16 on 2024-07-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techtime', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(max_length=20)),
                ('course_name_kr', models.CharField(max_length=100)),
                ('course_name_en', models.CharField(max_length=100)),
                ('course_type', models.CharField(max_length=50)),
                ('grade_level', models.CharField(max_length=10)),
                ('credits', models.CharField(max_length=10)),
                ('pf', models.CharField(max_length=5)),
                ('semester', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=100)),
            ],
        ),
    ]
