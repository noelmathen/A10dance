# attendance/signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import BranchHoursDetails, Course, PercentageDetails, Students, StudentAttendance
from django.core.mail import send_mail
from django.conf import settings

def update_attendance_percentages_for_course_students(course):
    students = Students.objects.filter(branch=course.branch)
    for student in students:
        try:
            percentage_detail = PercentageDetails.objects.get(student=student, course=course)
            tot_hours = course.number_of_hours
            hours_lost = percentage_detail.hours_lost_without_duty
            course_percentage = ((tot_hours - hours_lost) / tot_hours) * 100
            percentage_detail.percentage_of_subject = course_percentage
            percentage_detail.save()
            print("before print")
            print(f"Attendance percentage for {student.user.first_name} for {course.course_name}: {course_percentage}%  (UPDATED)")
            print("After print")
        
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
        update_attendance_percentages_for_course_students(course)
        
       
       
        
#Handle sending mails when attendance of students are updated hehe
@receiver(pre_save, sender=StudentAttendance)
def handle_attendance_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_state = StudentAttendance.objects.get(pk=instance.pk)
        except StudentAttendance.DoesNotExist:
            instance._previous_state = None
    else:
        instance._previous_state = None


@receiver(post_save, sender=StudentAttendance)
def handle_attendance_save(sender, instance, created, **kwargs):
    if created:
        # Case 1: New entry
        send_absence_email(instance, new_entry=True)
    else:
        # Case 2: Existing entry modified
        send_absence_email(instance, new_entry=False)



@receiver(post_delete, sender=StudentAttendance)
def handle_attendance_delete(sender, instance, **kwargs):
    # Case 3: Entry deleted
    send_absence_email(instance, deleted=True)



def send_absence_email(instance, new_entry=False, deleted=False):
    student = instance.student
    email = student.user.email
    date = instance.date
    added_absences = []
    removed_absences = []
    marked_duty_hours = []
    unmarked_duty_hours = []

    if deleted:
        print("\n\nTRIGGER EXECUTED, DELETED ABSENT, GOING TO SEND EMAIL\n\n")
        subject = 'Absence Record Removed'
        message = f"Dear {student.user.first_name},\n\nYour absence record for {date} has been removed.\n\nBest regards,\nYour School Administration"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    else:
        previous_state = instance._previous_state

        for hour in range(1, 8):
            course = getattr(instance, f'hour_{hour}')
            duty_hour = getattr(instance, f'duty_hour_{hour}')
            prev_course = getattr(previous_state, f'hour_{hour}') if previous_state else None
            prev_duty_hour = getattr(previous_state, f'duty_hour_{hour}') if previous_state else None

            # Track added absences and removed absences
            if course and not duty_hour:
                if new_entry or (course != prev_course and not duty_hour):
                    added_absences.append(f'Hour {hour} - {course}')
            elif prev_course and not prev_duty_hour and not (course and not duty_hour):
                removed_absences.append(f'Hour {hour} - {prev_course}')

            # Track duty hour changes separately
            if duty_hour and (prev_duty_hour is None or not prev_duty_hour):
                marked_duty_hours.append(f'Hour {hour} - {course}')
            elif not duty_hour and prev_duty_hour:
                unmarked_duty_hours.append(f'Hour {hour} - {course}')

        # Prepare email messages
        email_messages = []

        # Send duty hour marked email
        if marked_duty_hours:
            print("\n\nTRIGGER EXECUTED, MARKED DUTY HOUR, GOING TO SEND EMAIL\n\n")
            subject = 'Duty Hour Marked'
            message = f"Dear {student.user.first_name},\n\nYour absence record for {date} has been updated with the following duty hours:\n" + "\n".join(marked_duty_hours) + "\n\nBest regards,\nYour School Administration"
            email_messages.append((subject, message, email))

        # Send duty hour unmarked email
        if unmarked_duty_hours:
            print("\n\nTRIGGER EXECUTED, UNMARKED DUTY HOUR, GOING TO SEND EMAIL\n\n")
            subject = 'Duty Hour Unmarked'
            message = f"Dear {student.user.first_name},\n\nYour duty hour for {date} has been unmarked for the following hours:\n" + "\n".join(unmarked_duty_hours) + "\n\nBest regards,\nYour School Administration"
            email_messages.append((subject, message, email))

        # Send absence update emails only if there are no duty hour changes
        if not marked_duty_hours and not unmarked_duty_hours:
            if added_absences:
                if new_entry:
                    print("\n\nTRIGGER EXECUTED, ADDED ABSENT, GOING TO SEND EMAIL\n\n")
                    subject = 'New Absence Recorded'
                    message = f"Dear {student.user.first_name},\n\nYou have been marked absent on {date} for the following hours:\n" + "\n".join(added_absences) + "\n\nPlease check with your teacher if this is a mistake.\n\nBest regards,\nYour School Administration"
                else:
                    print("\n\nTRIGGER EXECUTED, MODIFIED ABSENT, GOING TO SEND EMAIL\n\n")
                    subject = 'Absence Record Updated'
                    message = f"Dear {student.user.first_name},\n\nYour absence record for {date} has been updated for the following hours:\n" + "\n".join(added_absences) + "\n\nPlease check with your teacher if this is a mistake.\n\nBest regards,\nYour School Administration"
                email_messages.append((subject, message, email))

            if removed_absences:
                print("\n\nTRIGGER EXECUTED, REMOVED ABSENT, GOING TO SEND EMAIL\n\n")
                subject = 'Absence Record Corrected'
                message = f"Dear {student.user.first_name},\n\nYour absence record for {date} has been corrected for the following hours:\n" + "\n".join(removed_absences) + "\n\nBest regards,\nYour School Administration"
                email_messages.append((subject, message, email))

        for subject, message, recipient in email_messages:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])


