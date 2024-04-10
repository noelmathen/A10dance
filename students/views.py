#students/views.py
from rest_framework import viewsets, permissions
from attendance.models import StudentAttendance, PercentageDetails
from .serializers import StudentAttendanceSerializer, AttendanceStatsSerializer
from rest_framework.generics import ListAPIView


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
    
    
