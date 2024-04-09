#attendance/utils.py
from students.models import Students
from .models import PercentageDetails
from academia. models import Course

def get_attendance_percentage(branch):
    students = Students.objects.filter(branch=branch)
    
    for student in students:
        # Fetch all attendance details for the student
        percentage_details = PercentageDetails.objects.filter(student=student)
        for percentage_detail in percentage_details:
            tot_hours = Course.objects.get(course_code=percentage_detail.course.course_code).number_of_hours
            hours_lost = percentage_detail.hours_lost_with_duty
            course_percentage = ((tot_hours-hours_lost)/tot_hours)*100
            percentage_detail.percentage_of_subject = course_percentage
            percentage_detail.save()
            print(f"Attendance percentage for {student.user.first_name} for {percentage_detail.course.course_name}: {course_percentage}%")
        student.save()


