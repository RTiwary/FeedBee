# Generated by Django 3.0.7 on 2020-07-19 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_auto_20200712_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='completed_students',
        ),
    ]