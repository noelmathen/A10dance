from django.contrib import admin
from .models import BranchHoursDetails, PercentageDetails, StudentAttendance

@admin.register(BranchHoursDetails)
class BranchHoursDetailsAdmin(admin.ModelAdmin):
    list_display = ['date', 'branch']  # Display these fields in the admin list
    ordering = ['date']  # Order by the 'date' field in ascending order


# admin.site.register(BranchHoursDetails)
admin.site.register(PercentageDetails)
admin.site.register(StudentAttendance)


