# Generated by Django 5.0.2 on 2024-03-05 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='division',
            field=models.CharField(choices=[('N/A', ''), ('Alpha', 'Alpha'), ('Beta', 'Beta'), ('Gamma', 'Gamma')], max_length=10),
        ),
    ]