# attendance/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BranchHoursDetails, Course


@receiver([post_save, post_delete], sender=BranchHoursDetails)
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
