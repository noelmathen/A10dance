from django.contrib import admin
from .models import Branch, Course
from django import forms
from .utils import process_excel_file

admin.site.register(Course)

class BranchAdminForm(forms.ModelForm):
    excel_file = forms.FileField(label='Excel File')

    class Meta:
        model = Branch
        fields = '__all__'

    def save(self, commit=True):
        branch = super().save(commit=False)
        
        # Check if a new Branch instance is being created
        if not branch.pk:
            commit = True  # Ensure that the branch is saved to generate a primary key
        
        if commit:
            branch.save()

        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            process_excel_file(branch, excel_file)

        # Save many-to-many relationships if any
        self.save_m2m()

        return branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    form = BranchAdminForm
