# Generated by Django 5.0.2 on 2024-10-13 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_historicalstudentattendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchhoursdetails',
            name='finished_marking',
        ),
    ]
