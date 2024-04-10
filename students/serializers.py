#students/serializers.py
from rest_framework import serializers
from attendance.models import StudentAttendance, PercentageDetails, BranchHoursDetails



class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'duty_hour_1', 'duty_hour_2', 'duty_hour_3', 'duty_hour_4', 'duty_hour_5', 'duty_hour_6', 'duty_hour_7']
  
  
        
class AttendanceStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageDetails
        fields = ['student', 'course', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject']
        


class BranchHourDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchHoursDetails
        fields = ['branch', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'finished_marking']
    
        

