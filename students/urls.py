#students/urls.py
from django.urls import path
from .views import StudentAttendanceListView

urlpatterns = [
    path('attendance-table/', StudentAttendanceListView.as_view(), name='student-attendance'),    
]