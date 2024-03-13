#academia/admin.py
from django.contrib import admin
from .models import Branch, Course
from django import forms
from .utils import process_excel_file
from students.utils import iterate_through_students
from attendance.utils import get_attendance_percentage


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


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    form = BranchAdminForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'course_code', 'number_of_hours', 'branch']
    list_filter = ['branch']
    ordering = ['branch', 'course_code']