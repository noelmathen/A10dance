#students/views.py
from rest_framework import permissions
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
    PredictionInputSerializer,
    DateFilterSerializer,
    FilteredPercentageDetailsSerializer
)
from academia.models import Course
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Students
from accounts.models import CustomUser
from datetime import datetime
from django.db.models import Sum
from collections import Counter


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
    
    

class PredictPercentageView(APIView):
    def post(self, request):
        # Deserialize input data
        serializer = PredictionInputSerializer(data=request.data)
        if serializer.is_valid():
            # Extract input data from validated data
            course_id = serializer.validated_data['course_id']
            hours_missed = serializer.validated_data['hours_missed']
            
            # Get the course object
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Get the student profile of the logged-in user
            try:
                user = request.user
                student = user.students  # Assuming students is a related model of CustomUser
            except CustomUser.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                percentage_details = PercentageDetails.objects.get(
                    student=student,  # Assuming the logged-in user has a student profile
                    course=course                
                )
            except PercentageDetails.DoesNotExist:
                return Response({'error': 'PercentageDetails object not found'}, status=status.HTTP_404_NOT_FOUND)
            
            tot_hours = course.number_of_hours + hours_missed
            hours_lost = percentage_details.hours_lost_without_duty + hours_missed
            predicted_percentage = ((tot_hours - hours_lost) / tot_hours) * 100
            
            return Response({'predicted_percentage': predicted_percentage}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilteredDataView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        print(start_date, end_date)
        student = Students.objects.get(user=self.request.user)
        print(student)
        
        # Step 1: Filter BranchHourDetails based on the provided date range
        branch_hour_details = BranchHoursDetails.objects.filter(
            date__range=[start_date, end_date],
            branch=student.branch
        )
        print(branch_hour_details)
        
        # Step 2: Identify the courses conducted during the specified date range
        courses_conducted = []
        for entry in branch_hour_details:
            courses_conducted.extend([
                entry.hour_1,
                entry.hour_2,
                entry.hour_3,
                entry.hour_4,
                entry.hour_5,
                entry.hour_6,
                entry.hour_7
            ])
        print(courses_conducted)
        
        #Step 3: Calculating the number of hours for each course(None value excluded)
        courses_conducted_without_none = [course for course in courses_conducted if course is not None]
        course_counts_conducted = Counter(courses_conducted_without_none)
        for course, count in course_counts_conducted.items():
            print(f"Course: {course}, Hours Conducted: {count}")
            
            
        
        

        # Step 4: Filter StudentAttendance based on the provided date range
        student_attendance = StudentAttendance.objects.filter(
            student=student,
            date__range=[start_date, end_date],
        )
        print(f"\n{student_attendance}")

        # Step 5: Identify the courses conducted during the specified date range
        courses_missed = []
        for entry in student_attendance:
            courses_missed.extend([
                entry.hour_1,
                entry.hour_2,
                entry.hour_3,
                entry.hour_4,
                entry.hour_5,
                entry.hour_6,
                entry.hour_7
            ])
        print(f"{courses_missed}")
        
        #Step 6: Calculating the number of hours for each course(None value excluded)
        courses_missed_without_none = [course for course in courses_missed if course is not None]
        course_counts_missed = Counter(courses_missed_without_none)
        for course, count in course_counts_missed.items():
            print(f"Course: {course}, Hours Missed: {count}")
            
            
            
        # Step 7: Calculate the percentage of attendance for each course missed by the student
        percentage_details = {}
        for course, count_missed in course_counts_missed.items():
            total_hours = course_counts_conducted[course]  # Total hours conducted for the course
            percentage = ((total_hours - count_missed) / total_hours) * 100
            percentage_details[course.short_form] = round(percentage, 2)
        print(percentage_details)
        
        response_data = {
            'percentage_details': percentage_details
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
