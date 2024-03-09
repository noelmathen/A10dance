#acedmia/models.py
from django.db import models

class Branch(models.Model):
    BRANCH_CHOICES = [
        ('CSBS', 'CSBS'),
        ('AI&DS', 'AI&DS'),
        ('IT', 'IT'),
        ('ME', 'ME'),
        ('CE', 'CE'),
        ('CSE', 'CSE'),
        ('EEE', 'EEE'),
        ('ECE', 'ECE'),
        ('AEI', 'AEI'),
    ]
    DIVISION_CHOICES = [
        ('', 'N/A'),
        ('Alpha', 'Alpha'),
        ('Beta', 'Beta'),
        ('Gamma', 'Gamma'),
    ]

    joining_year = models.PositiveIntegerField()
    passout_year = models.PositiveIntegerField()
    branch_name = models.CharField(max_length=100, choices=BRANCH_CHOICES) 
    division = models.CharField(max_length=10, choices=DIVISION_CHOICES, blank=True)
    excel_file = models.FileField(upload_to='branch_excel_files', default=r'C:\Users\noelm\Documents\PROJECTS\A10dance\Other Files\CSBS_2021-2025.xlsx')
    
    def __str__(self):
        return f"{self.branch_name} {self.division} ({self.joining_year} - {self.passout_year})"
    
    def save(self, *args, **kwargs):
        self.passout_year = self.joining_year + 4;
        super().save(*args, **kwargs)


class Course(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    number_of_hours = models.PositiveIntegerField(default=0)
    semester = models.PositiveIntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"