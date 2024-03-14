#accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    login_password = models.CharField(max_length=9, blank=False, null=True)
    def __str__(self):
        return self.first_name
