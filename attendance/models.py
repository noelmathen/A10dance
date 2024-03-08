from django.db import models
from academia.models import Branch, Course
from students.models import Students

HOUR_OPTIONS = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
]

class BranchHoursDetails(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_2 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_3 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_4 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_5 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_6 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_7 = models.PositiveIntegerField(choices=HOUR_OPTIONS)

    def __str__(self):
        return f"{self.date} - {self.branch}"

class StudentAttendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_2 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_3 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_4 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_5 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_6 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    hour_7 = models.PositiveIntegerField(choices=HOUR_OPTIONS)
    duty_hour_1 = models.BooleanField(default=False)
    duty_hour_2 = models.BooleanField(default=False)
    duty_hour_3 = models.BooleanField(default=False)
    duty_hour_4 = models.BooleanField(default=False)
    duty_hour_5 = models.BooleanField(default=False)
    duty_hour_6 = models.BooleanField(default=False)
    duty_hour_7 = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student} - {self.date}"




class PercentageDetails(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    hours_lost_with_duty = models.PositiveIntegerField(default=0)
    hours_lost_without_duty = models.PositiveIntegerField(default=0)
    percentage_of_subject = models.FloatField(default=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.student.branch.branch_name} - {self.course.course_name} - {self.percentage_of_subject}"
