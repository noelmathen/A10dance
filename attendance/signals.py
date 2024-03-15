# attendance/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BranchHoursDetails, Course, PercentageDetails, Students


def update_attendance_percentages_for_course_students(course):
    students = Students.objects.filter(branch=course.branch)
    for student in students:
        try:
            percentage_detail = PercentageDetails.objects.get(student=student, course=course)
            tot_hours = course.number_of_hours
            hours_lost = percentage_detail.hours_lost_with_duty
            course_percentage = ((tot_hours - hours_lost) / tot_hours) * 100
            percentage_detail.percentage_of_subject = course_percentage
            percentage_detail.save()
            print(f"Attendance percentage for {student.user.first_name} for {course.course_name}: {course_percentage}%  (UPDATED)")
        except PercentageDetails.DoesNotExist:
            print(f"No attendance percentage record found for {student.user.first_name} for {course.course_name}")
            


@receiver([post_save], sender=BranchHoursDetails)
def update_course_number_of_hours(sender, instance, created, **kwargs):
    if not created:
        branch = instance.branch
        courses = Course.objects.filter(branch=branch)
        
        # Iterate through each course and update the number_of_hours
        for course in courses:
            total_hours = sum([
                getattr(branch_hours, f'hour_{i}') == course for i in range(1, 8)
                for branch_hours in BranchHoursDetails.objects.filter(branch=branch)
            ])
            course.number_of_hours = total_hours
            course.save(update_fields=['number_of_hours'])
            update_attendance_percentages_for_course_students(course)


@receiver([post_delete], sender=BranchHoursDetails)
def update_course_number_of_hours(sender, instance, **kwargs):
    branch = instance.branch
    courses = Course.objects.filter(branch=branch)
    
    # Iterate through each course and update the number_of_hours
    for course in courses:
        total_hours = sum([
            getattr(branch_hours, f'hour_{i}') == course for i in range(1, 8)
            for branch_hours in BranchHoursDetails.objects.filter(branch=branch)
        ])
        course.number_of_hours = total_hours
        course.save(update_fields=['number_of_hours'])



