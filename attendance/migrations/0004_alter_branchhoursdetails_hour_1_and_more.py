# Generated by Django 5.0.2 on 2024-03-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_remove_percentagedetails_branch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_1',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_2',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_3',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_4',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_5',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_6',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='branchhoursdetails',
            name='hour_7',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_1',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_2',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_3',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_4',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_5',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_6',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='hour_7',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], max_length=20),
        ),
    ]
