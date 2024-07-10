# attendance/forms.py
from django import forms
from .models import BranchHoursDetails, Course

class BranchHoursDetailsForm(forms.ModelForm):
    class Meta:
        model = BranchHoursDetails
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        branch = getattr(self, 'branch', None)
        super().__init__(*args, **kwargs)
        if branch:
            self.fields['hour_1'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_2'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_3'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_4'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_5'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_6'].queryset = Course.objects.filter(branch=branch)
            self.fields['hour_7'].queryset = Course.objects.filter(branch=branch)
        else:
            self.fields['hour_1'].queryset = Course.objects.none()
            self.fields['hour_2'].queryset = Course.objects.none()
            self.fields['hour_3'].queryset = Course.objects.none()
            self.fields['hour_4'].queryset = Course.objects.none()
            self.fields['hour_5'].queryset = Course.objects.none()
            self.fields['hour_6'].queryset = Course.objects.none()
            self.fields['hour_7'].queryset = Course.objects.none()

