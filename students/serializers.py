#students/serializers.py
from rest_framework import serializers
from attendance.models import StudentAttendance, PercentageDetails, BranchHoursDetails
from academia.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'short_form', 'number_of_hours']

class StudentAttendanceSerializer(serializers.ModelSerializer):
    hour_1 = CourseSerializer()
    hour_2 = CourseSerializer()
    hour_3 = CourseSerializer()
    hour_4 = CourseSerializer()
    hour_5 = CourseSerializer()
    hour_6 = CourseSerializer()
    hour_7 = CourseSerializer()
    
    class Meta:
        model = StudentAttendance
        fields = ['date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'duty_hour_1', 'duty_hour_2', 'duty_hour_3', 'duty_hour_4', 'duty_hour_5', 'duty_hour_6', 'duty_hour_7']
        
        
        
class AttendanceStatsSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = PercentageDetails
        fields = ['student', 'student_name', 'course', 'hours_lost_with_duty', 'hours_lost_without_duty', 'percentage_of_subject']
        
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name}"
    
    
class BranchHourDetailsSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    hour_1 = CourseSerializer()
    hour_2 = CourseSerializer()
    hour_3 = CourseSerializer()
    hour_4 = CourseSerializer()
    hour_5 = CourseSerializer()
    hour_6 = CourseSerializer()
    hour_7 = CourseSerializer()
    
    class Meta:
        model = BranchHoursDetails
        fields = ['branch_name', 'date', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'finished_marking']
    
    def get_branch_name(self, obj):
        return f"{obj.branch.branch_name} {obj.branch.division} ({obj.branch.joining_year} - {obj.branch.passout_year})"
        


# Serializer for handling input data
class PredictionInputSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    hours_missed = serializers.IntegerField()
    
    