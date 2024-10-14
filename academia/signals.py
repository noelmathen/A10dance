#academia/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course, Elective
from attendance.models import BranchHoursDetails
from django.db.models import Max

@receiver(post_save, sender=Course)
def sync_course_hours_with_elective(sender, instance, created, **kwargs):
    try:
        print("\n\n\nTRYING TO UPDATE ELECTIVE HOURS\n\n\n")
        elective = instance.elective
        if elective:
            related_courses = Course.objects.filter(elective=elective)
            max_hours = related_courses.aggregate(Max('number_of_hours'))['number_of_hours__max']
            for course in related_courses:
                if course.number_of_hours != max_hours:
                    course.number_of_hours = max_hours
                    course.save(update_fields=['number_of_hours'])
                    print(f"Updated {course.course_name} to {max_hours} hours.")
    except Exception as e:
        print(f"An error occurred: {e}")
