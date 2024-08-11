# Generated by Django 3.2.16 on 2024-08-04 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20240731_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='board.articlecomment'),
        ),
    ]