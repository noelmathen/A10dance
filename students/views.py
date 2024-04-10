#students/views.py
from rest_framework import viewsets, permissions
from attendance.models import StudentAttendance
from .serializers import StudentAttendanceSerializer
from rest_framework.generics import ListAPIView


class StudentAttendanceListView(ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = self.request.user
        return StudentAttendance.objects.filter(student__user=logged_in_user)


