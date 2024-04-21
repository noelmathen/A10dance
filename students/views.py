#students/views.py
from rest_framework import viewsets, permissions
from attendance.models import (
    StudentAttendance,
    PercentageDetails,
    BranchHoursDetails,
)
from .serializers import (
    StudentAttendanceSerializer, 
    AttendanceStatsSerializer, 
    BranchHourDetailsSerializer,
    CourseSerializer,
)
from academia.models import Course
from rest_framework.generics import ListAPIView
from .models import Students
from datetime import datetime

class StudentAttendanceListView(ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = self.request.user
        return StudentAttendance.objects.filter(student__user=logged_in_user)


class AttendanceStatsView(ListAPIView):
    serializer_class = AttendanceStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PercentageDetails.objects.filter(student__user=self.request.user).order_by('course__slot')
        
    
class BranchHourDetailsView(ListAPIView):
    serializer_class = BranchHourDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        student = Students.objects.get(user=self.request.user)
        queryset = BranchHoursDetails.objects.filter(branch=student.branch)
        return queryset.order_by('date')  # Sort entries by ascending order of dates
    
    def format_date(self, date):
        # Convert date string to datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        # Format date as "dd-Mon-YYYY (12-Feb-2024)"
        return date_obj.strftime('%d-%b-%Y').replace(date_obj.strftime('%b').lower(), date_obj.strftime('%b'))

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data:
            item['date'] = self.format_date(item['date'])
        return response
    
    
class CourseTableView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        student = Students.objects.get(user=self.request.user)
        return Course.objects.filter(branch=student.branch).order_by('slot')
    