# attendance/signals.py
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from .models import (
    BranchHoursDetails, 
    Course, 
    PercentageDetails, 
    Students, 
    StudentAttendance,)
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import async_to_sync
import threading


def update_attendance_percentages_for_course_students(course):
    students = Students.objects.filter(branch=course.branch)
    for student in students:
        try:
            percentage_detail = PercentageDetails.objects.get(student=student, course=course)
            tot_hours = course.number_of_hours
            hours_lost = percentage_detail.hours_lost_without_duty
            if tot_hours > 0:
                course_percentage = ((tot_hours - hours_lost) / tot_hours) * 100
            else:
                course_percentage = 0  
            percentage_detail.percentage_of_subject = course_percentage
            percentage_detail.save()
            # print("before print")
            print(f"Attendance percentage for {student.user.first_name} for {course.course_name}: {course_percentage}%  (UPDATED)")
            # print("After print")
        except PercentageDetails.DoesNotExist:
            print(f"No attendance percentage record found for {student.user.first_name} for {course.course_name}")



def get_changed_courses(old_instance, new_instance):
    changed_courses = []
    for i in range(1, 8):
        hour_field = f'hour_{i}'
        old_course = getattr(old_instance, hour_field) if old_instance else None
        new_course = getattr(new_instance, hour_field) if new_instance else None
        if old_course != new_course:
            if new_course:
                changed_courses.append(new_course)
            if old_course:
                changed_courses.append(old_course)
    return list(set(changed_courses))



def cleanup_empty_entries(table_class):
    for entry in table_class.objects.all():
        if all(getattr(entry, f'hour_{i}') in [None, ''] for i in range(1, 8)):
            entry.delete()
      
          
            
@receiver(pre_save, sender=BranchHoursDetails)
def handle_branch_hours_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_state = BranchHoursDetails.objects.get(pk=instance.pk)
        except BranchHoursDetails.DoesNotExist:
            instance._previous_state = None
    else:
        instance._previous_state = None



@receiver(post_save, sender=BranchHoursDetails)
def update_course_number_of_hours(sender, instance, created, **kwargs):
    old_instance = getattr(instance, '_previous_state', None)
    changed_courses = get_changed_courses(old_instance, instance)

    if changed_courses:
        branch = instance.branch
        for course in changed_courses:
            print(f"\n\n{course}\n\n")
            if course:
                total_hours = sum([
                    getattr(branch_hours, f'hour_{i}') == course for i in range(1, 8)
                    for branch_hours in BranchHoursDetails.objects.filter(branch=branch)
                ])
                course.number_of_hours = total_hours
                print("\n\n\n\nSaving course instance...")
                course.save(update_fields=['number_of_hours'])
                print("Course instance saved.\n\n\n\n")
                update_attendance_percentages_for_course_students(course)
    cleanup_empty_entries(BranchHoursDetails)
    


@receiver(pre_delete, sender=BranchHoursDetails)
def handle_branch_hours_pre_delete(sender, instance, **kwargs):
    instance._previous_state = instance
    instance._changed_course_ids = [getattr(instance, f'hour_{i}').id for i in range(1, 8) if getattr(instance, f'hour_{i}')]



@receiver(post_delete, sender=BranchHoursDetails)
def update_course_number_of_hours_on_delete(sender, instance, **kwargs):
    changed_course_ids = getattr(instance, '_changed_course_ids', [])
    branch = instance.branch
    for course_id in changed_course_ids:
        print(f"\n\n{course_id}\n\n")
        try:
            course = Course.objects.get(id=course_id)
            total_hours = sum([
                getattr(branch_hours, f'hour_{i}') == course for i in range(1, 8)
                for branch_hours in BranchHoursDetails.objects.filter(branch=branch)
            ])
            course.number_of_hours = total_hours
            course.save(update_fields=['number_of_hours'])
            update_attendance_percentages_for_course_students(course)
        except Course.DoesNotExist:
            print(f"Course with id {course_id} does not exist.")
    cleanup_empty_entries(BranchHoursDetails)      
       


@receiver(pre_save, sender=StudentAttendance)
def handle_student_attendance_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_state = StudentAttendance.objects.get(pk=instance.pk)
        except StudentAttendance.DoesNotExist:
            instance._previous_state = None
    else:
        instance._previous_state = None

@receiver(post_save, sender=StudentAttendance)
def cleanup_student_attendance_after_save(sender, instance, created, **kwargs):
    # Cleanup empty entries after save
    cleanup_empty_entries(StudentAttendance)

@receiver(pre_delete, sender=StudentAttendance)
def handle_student_attendance_pre_delete(sender, instance, **kwargs):
    instance._previous_state = instance

@receiver(post_delete, sender=StudentAttendance)
def cleanup_student_attendance_after_delete(sender, instance, **kwargs):
    # Cleanup empty entries after delete
    cleanup_empty_entries(StudentAttendance)
    
    

        
# #Handle sending mails when attendance of students are updated hehe
# @receiver(pre_save, sender=StudentAttendance)
# def handle_attendance_pre_save(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             instance._previous_state = StudentAttendance.objects.get(pk=instance.pk)
#         except StudentAttendance.DoesNotExist:
#             instance._previous_state = None
#     else:
#         instance._previous_state = None


# @receiver(post_save, sender=StudentAttendance)
# def handle_attendance_save(sender, instance, created, **kwargs):
#     if created:
#         # Case 1: New entry
#         send_absence_email(instance, new_entry=True)
#     else:
#         # Case 2: Existing entry modified
#         send_absence_email(instance, new_entry=False)



# @receiver(post_delete, sender=StudentAttendance)
# def handle_attendance_delete(sender, instance, **kwargs):
#     # Case 3: Entry deleted
#     send_absence_email(instance, deleted=True)



# # Function to send email in a new thread
# def send_mail_thread(subject, message, recipient_list):
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

# def send_absence_email(instance, new_entry=False, deleted=False):
#     student = instance.student
#     email = student.user.email
#     date = instance.date
#     added_absences = []
#     removed_absences = []
#     marked_duty_hours = []
#     unmarked_duty_hours = []

#     if deleted:
#         # print("\n\nTRIGGER EXECUTED, DELETED ABSENT, GOING TO SEND EMAIL\n\n")
#         subject = 'Absent Entry Removed'
#         message = f"Dear {student.user.first_name},\n\nYour absent hours for {date} has been removed.\n\nBest regards\na10dance"
#         # threading.Thread(target=send_mail_thread, args=(subject, message, [email])).start()
#     else:
#         previous_state = instance._previous_state

#         for hour in range(1, 8):
#             course = getattr(instance, f'hour_{hour}')
#             duty_hour = getattr(instance, f'duty_hour_{hour}')
#             prev_course = getattr(previous_state, f'hour_{hour}') if previous_state else None
#             prev_duty_hour = getattr(previous_state, f'duty_hour_{hour}') if previous_state else None

#             # Track added absences and removed absences
#             if course and not duty_hour:
#                 if new_entry or (course != prev_course and not duty_hour):
#                     added_absences.append(f'Hour {hour} - {course}')
#             elif prev_course and not prev_duty_hour and not (course and not duty_hour):
#                 removed_absences.append(f'Hour {hour} - {prev_course}')

#             # Track duty hour changes separately
#             if duty_hour and (prev_duty_hour is None or not prev_duty_hour):
#                 marked_duty_hours.append(f'Hour {hour} - {course}')
#             elif not duty_hour and prev_duty_hour:
#                 unmarked_duty_hours.append(f'Hour {hour} - {course}')

#         # Prepare email messages
#         email_messages = []

#         # Send duty hour marked email
#         if marked_duty_hours:
#             print("\n\nTRIGGER EXECUTED, MARKED DUTY HOUR, GOING TO SEND EMAIL\n\n")
#             subject = 'Duty Hour Marked'
#             message = f"Dear {student.user.first_name},\n\nYour attendance for {date} has been updated with the following DUTY HOURS:\n" + "\n".join(marked_duty_hours) + "\n\nBest regards\na10dance"
#             email_messages.append((subject, message, email))

#         # Send duty hour unmarked email
#         if unmarked_duty_hours:
#             print("\n\nTRIGGER EXECUTED, UNMARKED DUTY HOUR, GOING TO SEND EMAIL\n\n")
#             subject = 'Duty Hour Unmarked'
#             message = f"Dear {student.user.first_name},\n\nYour duty hour for {date} has been unmarked for the following hours:\n" + "\n".join(unmarked_duty_hours) + "\n\nBest regards\na10dance"
#             email_messages.append((subject, message, email))

#         # Send absence update emails only if there are no duty hour changes
#         if not marked_duty_hours and not unmarked_duty_hours:
#             if added_absences:
#                 if new_entry:
#                     print("\n\nTRIGGER EXECUTED, ADDED ABSENT, GOING TO SEND EMAIL\n\n")
#                     subject = 'Absent Marked in RSMS!'
#                     message = f"Dear {student.user.first_name},\n\nYou have been marked absent on {date} for the following hours:\n" + "\n".join(added_absences) + "\n\nPlease check with your teacher if this is a mistake.\n\nBest regards\na10dance"
#                 else:
#                     print("\n\nTRIGGER EXECUTED, MODIFIED ABSENT, GOING TO SEND EMAIL\n\n")
#                     subject = 'Absent Updated in RSMS!'
#                     message = f"Dear {student.user.first_name},\n\nYour attendance for {date} has been updated for the following hours:\n" + "\n".join(added_absences) + "\n\nPlease check with your teacher if this is a mistake.\n\nBest regards\na10dance"
#                 email_messages.append((subject, message, email))

#             if removed_absences:
#                 print("\n\nTRIGGER EXECUTED, REMOVED ABSENT, GOING TO SEND EMAIL\n\n")
#                 subject = 'Absent Removed in RSMS!'
#                 message = f"Dear {student.user.first_name},\n\nYour attendance for {date} has been corrected(unmarked as absent) for the following hours:\n" + "\n".join(removed_absences) + "\n\nBest regards\na10dance"
#                 email_messages.append((subject, message, email))

#         for subject, message, recipient in email_messages:
#             threading.Thread(target=send_mail_thread, args=(subject, message, [recipient])).start()


