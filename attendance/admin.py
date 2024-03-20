#attendance/admin.py
from django.contrib import admin
from .models import BranchHoursDetails, PercentageDetails, StudentAttendance


@admin.register(BranchHoursDetails)
class BranchHoursDetailsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7']  # Display these fields in the admin list
    ordering = ['branch', 'date']  # Order by the 'date' field in ascending order
    list_filter = ['branch', 'date']
    search_fields = ['branch', 'date']
    
    
    
# class BranchHoursDetailsInline(admin.TabularInline):
#     model = BranchHoursDetails
#     extra = 0
#     field = ['branch', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7']
    
    
    
# @admin.register(BranchHoursDetailsModification)
# class BranchHoursDetailsModificationAdmin(admin.ModelAdmin):
#     list_display = ('branch_hours_details_info', 'modified_by_admin', 'modified_at')
#     list_filter = ('modified_by_admin',)
#     inlines = [BranchHoursDetailsInline]
    
#     def branch_hours_details_info(self, obj):
#         return f"{obj.branch_hours_details.branch} - {obj.branch_hours_details.date}"
#     branch_hours_details_info.short_description = 'Branch Hours Details'
    
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     # Filter entries based on whether they are modified by admin or not
    #     return queryset.filter(modified_by_admin=True) if request.GET.get('modified_by_admin') == 'True' else queryset.filter(modified_by_admin=False)
    
    

class PercentageDetailsInline(admin.TabularInline):
    model = PercentageDetails
    extra = 0
    field = ['course_name', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject']

    # def student_name(self, obj):
    #     return obj.student.user.first_name
    # student_name.short_description = 'Student Name'

    def course_name(self, obj):
        return obj.course.course_name
    course_name.short_description = 'Course Name'



@admin.register(PercentageDetails)
class PercentageDetailsAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject')
    list_filter = ('student__user__first_name', 'course__course_name')
    search_fields = ('student__user__first_name', 'course__course_name')

    def student_name(self, obj):
        return obj.student.user.first_name
    student_name.admin_order_field = 'student__user__first_name'

    def course_name(self, obj):
        return obj.course.course_name
    course_name.admin_order_field = 'course__course_name'
    


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'duty_hour_1', 'duty_hour_2', 'duty_hour_3', 'duty_hour_4', 'duty_hour_5', 'duty_hour_6', 'duty_hour_7']
    ordering = ['student', 'date']  # Order by the 'date' field in ascending order
    search_fields = ['student__user__first_name', 'date']  # Enable search based on student's first name and date
    list_filter = ['student__user__first_name', 'date', 'duty_hour_1', 'duty_hour_2', 'duty_hour_3', 'duty_hour_4', 'duty_hour_5', 'duty_hour_6', 'duty_hour_7']  # Enable filtering based on student's first name, date, and duty_hour fields



