#attendance/admin.py
from django.contrib import admin
from .models import BranchHoursDetails, PercentageDetails, StudentAttendance
from academia.models import Course
from .forms import BranchHoursDetailsForm

@admin.register(BranchHoursDetails)
class BranchHoursDetailsAdmin(admin.ModelAdmin):
    form = BranchHoursDetailsForm
    list_display = ['branch', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'finished_marking']  # Display these fields in the admin list
    ordering = ['branch', 'date']  # Order by the 'date' field in ascending order
    list_filter = ['branch', 'date' , 'branch__joining_year',]
    search_fields = ['branch', 'date']
    
    def get_form(self, request, obj=None, **kwargs):
        # Get the form class
        form = super(BranchHoursDetailsAdmin, self).get_form(request, obj, **kwargs)
        
        # Inject branch into the form's kwargs
        if obj:
            form.branch = obj.branch
        else:
            branch_id = request.GET.get('branch')
            if branch_id:
                form.branch = branch_id
        return form



class PercentageDetailsInline(admin.TabularInline):
    model = PercentageDetails
    extra = 0
    fields = ['course_name', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject']
    readonly_fields = fields  # Make all fields read-only

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete permission for inline items

    def __str__(self):
        return self.course.course_name

    def has_add_permission(self, request, obj):
        return False  # Disable adding new PercentageDetails inline

    def has_change_permission(self, request, obj=None):
        return False  # Disable changing existing PercentageDetails inline

    def course_name(self, obj):
        return obj.course.course_name

    course_name.short_description = 'Course Name'



@admin.register(PercentageDetails)
class PercentageDetailsAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject')
    list_filter = ('student__branch', 'student__branch__joining_year', 'student__user__first_name', 'course__course_name')
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
    list_filter = ['student__branch', 'student__branch__joining_year', 'student__user__first_name', 'date']  # Enable filtering based on student's first name, date, and duty_hour fields



