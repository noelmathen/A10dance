# Generated by Django 5.0.2 on 2024-03-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0003_branch_excel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='division',
            field=models.CharField(blank=True, choices=[('', 'N/A'), ('Alpha', 'Alpha'), ('Beta', 'Beta'), ('Gamma', 'Gamma')], max_length=10),
        ),
    ]
