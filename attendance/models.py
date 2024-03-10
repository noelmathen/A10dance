from django.db import models
from academia.models import Branch, Course
from students.models import Students


class BranchHoursDetails(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_1')
    hour_2 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_2')
    hour_3 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_3')
    hour_4 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_4')
    hour_5 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_5')
    hour_6 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_6')
    hour_7 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='branch_hour_7')

    def __str__(self):
        return f"{self.date} - {self.branch}"



class StudentAttendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_1')
    hour_2 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_2')
    hour_3 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_3')
    hour_4 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_4')
    hour_5 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_5')
    hour_6 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_6')
    hour_7 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='hour_7')
    duty_hour_1 = models.BooleanField(default=False)
    duty_hour_2 = models.BooleanField(default=False)
    duty_hour_3 = models.BooleanField(default=False)
    duty_hour_4 = models.BooleanField(default=False)
    duty_hour_5 = models.BooleanField(default=False)
    duty_hour_6 = models.BooleanField(default=False)
    duty_hour_7 = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student.user.first_name} - {self.date}"



class PercentageDetails(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    hours_lost_with_duty = models.PositiveIntegerField(default=0)
    hours_lost_without_duty = models.PositiveIntegerField(default=0)
    percentage_of_subject = models.FloatField(default=100)

    def __str__(self):
        return f"{self.student.user.first_name} - {self.student.branch.branch_name} - {self.course.course_name} - {self.percentage_of_subject}"


