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
        return PercentageDetails.objects.filter(student__user=self.request.user)
    
    
class BranchHourDetailsView(ListAPIView):
    serializer_class =  BranchHourDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        student = Students.objects.get(user=self.request.user)
        return BranchHoursDetails.objects.filter(branch=student.branch)
    
    
class CourseTableView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        student = Students.objects.get(user=self.request.user)
        return Course.objects.filter(branch=student.branch)
    