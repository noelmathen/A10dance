from django.db import models
from accounts.models import CustomUser
from academia.models import Branch

class Students(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} - {self.branch_name} {self.division} - ({self.joining_year} - {self.passout_year})"