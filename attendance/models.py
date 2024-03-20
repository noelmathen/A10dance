# attendance/models.py
from django.db import models
from academia.models import Branch, Course
from students.models import Students


class BranchHoursDetails(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_1')
    hour_2 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_2')
    hour_3 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_3')
    hour_4 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_4')
    hour_5 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_5')
    hour_6 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_6')
    hour_7 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='branch_hour_7')
    # null_values_intentional = models.BooleanField(default=False)    
    
    def __str__(self):
        return f"{self.date} - {self.branch}"

    # def save(self, *args, **kwargs):
    #     # Check if any of the hour fields have null values
    #     if any([getattr(self, f'hour_{i}') is None for i in range(1, 8)]):
    #         self.null_values_intentional = False
    #     else:
    #         self.null_values_intentional = True

    #     super().save(*args, **kwargs)

# class BranchHoursDetailsModification(models.Model):
#     branch_hours_details = models.ForeignKey('BranchHoursDetails', on_delete=models.CASCADE)
#     modified_by_admin = models.BooleanField(default=False)
#     modified_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Modification for {self.branch_hours_details} - {'Modified' if self.modified_by_admin else 'Not Modified'}"



class StudentAttendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField()
    hour_1 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_1')
    hour_2 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_2')
    hour_3 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_3')
    hour_4 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_4')
    hour_5 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_5')
    hour_6 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_6')
    hour_7 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='hour_7')
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


