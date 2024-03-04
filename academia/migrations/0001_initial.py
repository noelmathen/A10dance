# Generated by Django 5.0.2 on 2024-03-04 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joining_year', models.PositiveIntegerField()),
                ('passout_year', models.PositiveIntegerField()),
                ('branch_name', models.CharField(choices=[('CSBS', 'CSBS'), ('AI&DS', 'AI&DS'), ('IT', 'IT'), ('ME', 'ME'), ('CE', 'CE'), ('CSE', 'CSE'), ('EEE', 'EEE'), ('ECE', 'ECE'), ('AEI', 'AEI')], max_length=100)),
                ('division', models.CharField(choices=[('', ''), ('Alpha', 'Alpha'), ('Beta', 'Beta'), ('Gamma', 'Gamma')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=100)),
                ('number_of_hours', models.PositiveIntegerField(default=0)),
                ('semester', models.PositiveIntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.branch')),
            ],
        ),
    ]