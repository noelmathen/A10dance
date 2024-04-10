#students/urls.py
from django.urls import path
from .views import (
    StudentAttendanceListView,
    AttendanceStatsView
)

urlpatterns = [
    path('attendance-table/', StudentAttendanceListView.as_view(), name='student-attendance'),    
    path('attendance-stats/', AttendanceStatsView.as_view(), name='student-attendance'),    
    
]

