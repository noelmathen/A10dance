# Generated by Django 5.0.2 on 2024-03-14 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0004_alter_branch_division'),
        ('attendance', '0012_alter_branchhoursdetails_hour_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_1', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_2', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_3', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_4', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_5', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_6', to='academia.course'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_7',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hour_7', to='academia.course'),
        ),
    ]
