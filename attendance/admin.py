from django.contrib import admin
from .models import BranchHoursDetails, PercentageDetails, StudentAttendance


admin.site.register(BranchHoursDetails)
admin.site.register(PercentageDetails)
admin.site.register(StudentAttendance)