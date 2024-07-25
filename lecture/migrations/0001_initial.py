# Generated by Django 3.2.16 on 2024-07-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200)),
                ('course_code', models.CharField(max_length=20)),
                ('section', models.CharField(max_length=10)),
                ('course_type', models.CharField(max_length=50)),
                ('schedule', models.CharField(max_length=200)),
                ('professor', models.CharField(max_length=100)),
                ('credits', models.CharField(max_length=10)),
                ('capacity', models.IntegerField()),
            ],
        ),
    ]