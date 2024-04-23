#students/views.py
from attendance.models import (
    StudentAttendance,
    PercentageDetails,
    BranchHoursDetails,
)
from .models import Students
from academia.models import Branch, Course
from accounts.models import CustomUser
from .serializers import (
    StudentAttendanceSerializer, 
    AttendanceStatsSerializer, 
    BranchHourDetailsSerializer,
    CourseSerializer,
    PredictionInputSerializer,
)
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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


class BranchDetailsView(APIView):
    def get(self, request):
        try:
            student = Students.objects.get(user=self.request.user)
            branch = Branch.objects.get(id=student.branch.id)
            last_attendance_update = branch.last_attendance_update
            respone_data = {
                'joining_year':branch.joining_year,
                'passout_year':branch.passout_year,
                'branch_name':branch.branch_name,
                'division':branch.division,
                'last_update':last_attendance_update,
            }
            return Response(respone_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Student or branch not found'}, status=status.HTTP_404_NOT_FOUND)



class FilteredDataView(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        student = get_object_or_404(Students, user=self.request.user)
        actual_courses = Course.objects.filter(branch=student.branch).order_by('slot')

        # Step 1: Filter BranchHourDetails based on the provided date range
        branch_hour_details = BranchHoursDetails.objects.filter(
            date__range=[start_date, end_date],
            branch=student.branch
        )

        # Step 2: Initialize counts for all courses to 0
        course_counts_conducted = {course: 0 for course in actual_courses}

        # Step 3: Identify the courses conducted during the specified date range
        for entry in branch_hour_details:
            for i in range(1, 8):
                course = getattr(entry, f'hour_{i}')
                if course:
                    course_counts_conducted[course] += 1
        
        # Step 4: Filter StudentAttendance based on the provided date range
        student_attendance = StudentAttendance.objects.filter(
            student=student,
            date__range=[start_date, end_date],
        )

        # Step 5: Initialize counts for all courses to 0
        course_counts_missed = {course: 0 for course in actual_courses}

        # Step 6: Identify the courses missed by the student during the specified date range
        for entry in student_attendance:
            for i in range(1, 8):
                course = getattr(entry, f'hour_{i}')
                if course:
                    course_counts_missed[course] += 1

        # Step 7: Calculate the percentage of attendance for each course missed by the student
        percentage_details = {}
        for course, count_missed in course_counts_missed.items():
            total_hours = course_counts_conducted[course]  # Total hours conducted for the course
            if total_hours > 0:
                percentage = ((total_hours - count_missed) / total_hours) * 100
            else:
                percentage = 100  # If no hours conducted, consider attendance as 100%
            percentage_details[course.short_form] = round(percentage, 2)

        # Step 8: Format student attendance data for response
        attendance_data = []
        for entry in student_attendance:
            attendance_record = {
                'date': entry.date,
                'hour_1': entry.hour_1.short_form if entry.hour_1 else '',
                'hour_2': entry.hour_2.short_form if entry.hour_2 else '',
                'hour_3': entry.hour_3.short_form if entry.hour_3 else '',
                'hour_4': entry.hour_4.short_form if entry.hour_4 else '',
                'hour_5': entry.hour_5.short_form if entry.hour_5 else '',
                'hour_6': entry.hour_6.short_form if entry.hour_6 else '',
                'hour_7': entry.hour_7.short_form if entry.hour_7 else '',
            }
            attendance_data.append(attendance_record)

        # Step 9: Format branch hour details data for response
        branch_hour_details_data = []
        for entry in branch_hour_details:
            branch_hour_record = {
                'date': entry.date,
                'hour_1': entry.hour_1.short_form if entry.hour_1 else '',
                'hour_2': entry.hour_2.short_form if entry.hour_2 else '',
                'hour_3': entry.hour_3.short_form if entry.hour_3 else '',
                'hour_4': entry.hour_4.short_form if entry.hour_4 else '',
                'hour_5': entry.hour_5.short_form if entry.hour_5 else '',
                'hour_6': entry.hour_6.short_form if entry.hour_6 else '',
                'hour_7': entry.hour_7.short_form if entry.hour_7 else '',
            }
            branch_hour_details_data.append(branch_hour_record)


        #Percentage Details
        percentage_details_table = []
        hours_lost = {course.short_form: course_counts_missed[course] for course in actual_courses}
        for index, (course_short_form, percentage) in enumerate(percentage_details.items(), start=1):
            course = get_object_or_404(Course, short_form=course_short_form)
            course_obj = {
                'SlNo': index,
                'course_code': course.course_code,  
                'course_name': course.course_name,  
                'short_form': course_short_form,
                'hours_lost': hours_lost[course_short_form],
                'percentage': round(percentage, 2)
            }
            percentage_details_table.append(course_obj)



        #Percentage Details
        course_table = []
        hours_conducted = {course.short_form: course_counts_conducted[course] for course in actual_courses}
        for index, (course_short_form, percentage) in enumerate(percentage_details.items(), start=1):
            course = get_object_or_404(Course, short_form=course_short_form)
            course_obj = {
                'SlNo': index,
                'course_code': course.course_code,  
                'course_name': course.course_name,  
                'short_form': course_short_form,
                'hours_conducted': hours_conducted[course_short_form],
            }
            course_table.append(course_obj)




        response_data = {
            'branch_hour_details_table': branch_hour_details_data,
            'course_table': course_table,
            'student_attendance_table': attendance_data,
            'percentage_details_table': percentage_details_table
            
            # 'hours_conducted': hours_conducted,
            # 'hours_lost': hours_lost,
            # 'percentage_details': percentage_details,
        }
        return Response(response_data, status=status.HTTP_200_OK) 
    


