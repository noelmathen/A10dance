# Generated by Django 5.0.2 on 2024-03-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0002_alter_branch_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='excel_file',
            field=models.FileField(default='C:\\Users\\noelm\\Documents\\PROJECTS\\A10dance\\Other Files\\CSBS_2021-2025.xlsx', upload_to='branch_excel_files'),
        ),
    ]
