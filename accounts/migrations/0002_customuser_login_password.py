# Generated by Django 5.0.2 on 2024-03-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='login_password',
            field=models.CharField(max_length=9, null=True),
        ),
    ]
