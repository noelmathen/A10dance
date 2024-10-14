#academia/admin.py
from django.contrib import admin, messages
from .models import Branch, Course
from django import forms
from .utils import process_excel_file
from students.utils import iterate_through_students
from attendance.utils import get_attendance_percentage
from attendance.update_attendance import update_attendance_details


class BranchAdminForm(forms.ModelForm):
    excel_file = forms.FileField(label='Excel File')

    class Meta:
        model = Branch
        fields = '__all__'

    def save(self, commit=True):
        branch = super().save(commit=False)
        
        if not branch.pk:
            commit = True
        
        if commit:
            branch.save()

        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            subject_df = process_excel_file(branch, excel_file)
            iterate_through_students(subject_df, branch, excel_file)
            get_attendance_percentage(branch)

        self.save_m2m()
        return branch


# To update attendance details(in the dropdown of branch model)
def update_attendance_action(modeladmin, request, queryset):
    for branch in queryset:
        try:
            update_attendance_details(branch)
            messages.success(request, f"Attendance details updated successfully for {branch.branch_name}.")
        except Exception as e:
            messages.error(request, f"Failed to update attendance details for {branch.branch_name}: {e}")

update_attendance_action.short_description = "Update Attendance Details"  # Action display name


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    form = BranchAdminForm
    list_display = ['branch_name', 'joining_year', 'passout_year', 'division']
    list_filter = ['joining_year']
    actions = [update_attendance_action]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'course_code', 'number_of_hours', 'short_form', 'branch']
    list_filter = ['branch', 'branch__joining_year']
    search_fields = ['course_code', 'course_name', 'short_form', 'semester', 'branch__branch_name', 'branch__joining_year'] 
    ordering = ['branch', 'slot']
    
    
