# Generated by Django 3.2.16 on 2024-07-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_post_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]