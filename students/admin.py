#students/admin.py
from django.contrib import admin
from .models import Students
from attendance.admin import PercentageDetailsInline

# @admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        """
        Override the delete_model method to ensure cascade deletion of associated CustomUser.
        """
        obj.user.delete()  # This will delete the associated CustomUser
        obj.delete()  # This will delete the Students object

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    inlines = [PercentageDetailsInline]