#students/admin.py
from django.contrib import admin
from .models import Students
from attendance.admin import PercentageDetailsInline

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'branch'] 
    ordering = ['branch', 'user']  
    list_filter = ['user', 'branch'] 
    search_fields = ['user__first_name', 'branch__branch_name'] 
    inlines = [PercentageDetailsInline]
    
    def delete_model(self, request, obj):
        """
        Override the delete_model method to ensure cascade deletion of associated CustomUser.
        """
        obj.user.delete()  # This will delete the associated CustomUser
        obj.delete()  # This will delete the Students object
        


    
# admin.site.register(Students)