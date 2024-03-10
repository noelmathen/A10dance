#students/models.py
from django.db import models
from accounts.models import CustomUser

class Students(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    branch = models.ForeignKey('academia.Branch', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} - {self.branch.branch_name} {self.branch.division} - ({self.branch.joining_year} - {self.branch.passout_year})"
    
    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the associated CustomUser object.
        """
        self.user.delete()
        super().delete(*args, **kwargs)
