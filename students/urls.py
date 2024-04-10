#students/urls.py
from django.urls import path
from .views import (
    StudentAttendanceListView,
    AttendanceStatsView,
    BranchHourDetailsView
)

urlpatterns = [
    path('attendance-table/', StudentAttendanceListView.as_view(), name='attendance-table'),    
    path('attendance-stats/', AttendanceStatsView.as_view(), name='attendance-stats'),    
    path('branch-hour-details/', BranchHourDetailsView.as_view(), name='branch-hour-details'),    
    
]

