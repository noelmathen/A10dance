#attendance/update_attendance.py
from students.models import Students
from attendance.models import StudentAttendance, PercentageDetails, BranchHoursDetails
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from academia.models import Course
from django.utils import timezone

def get_attendance_percentage(branch):
    students = Students.objects.filter(branch=branch)
    
    for student in students:
        # Fetch all attendance details for the student
        percentage_details = PercentageDetails.objects.filter(student=student)
        for percentage_detail in percentage_details:
            tot_hours = Course.objects.get(course_code=percentage_detail.course.course_code).number_of_hours
            hours_lost = percentage_detail.hours_lost_with_duty
            if tot_hours > 0:
                course_percentage = ((tot_hours - hours_lost) / tot_hours) * 100
            else:
                course_percentage = 0 
            percentage_detail.percentage_of_subject = course_percentage
            percentage_detail.save()
            print(f"Attendance percentage for {student.user.first_name} for {percentage_detail.course.course_name}: {course_percentage}%")
        student.save()
    #     print("outside 2nd for loop")
    # print("outside 1st for loop")
    



def check_and_get_course_object(course_code, existing_hour_code):
        print("\nInside 2nd function\n")
        if pd.isnull(course_code):
            if existing_hour_code!=None:
                return Course.objects.get(course_code=existing_hour_code)
            return None
        else:
            return Course.objects.get(course_code=course_code)



def insert_branch_attendance(common_attendance_df, branch):
    for _, row in common_attendance_df.iterrows():
        date_obj = datetime.strptime(row[0], "%d-%b-%Y").date()
        
        try:
            branch_hours = BranchHoursDetails.objects.get(branch=branch.id, date=date_obj)
        except ObjectDoesNotExist:
            print("BranchHoursDetails object does not exist for the specified branch and date.")
            # Create a dummy instance of BranchHoursDetails
            branch_hours = BranchHoursDetails(branch=branch, date=date_obj)
        
        defaults = {}
        
        for i in range(1, 8):
            hour_field = f"hour_{i}"
            if hasattr(branch_hours, hour_field):  # Check if attribute exists
                existing_hour_code = getattr(branch_hours, hour_field).course_code if getattr(branch_hours, hour_field) else None
                defaults[hour_field] = check_and_get_course_object(row[i], existing_hour_code)
        
        branch_hours_details, created = BranchHoursDetails.objects.update_or_create(
            branch=branch,
            date=date_obj,
            defaults=defaults
        )
        
        print(f"\n{'Inserted' if created else 'Updated'} branch hours details: {branch_hours_details}")



def update_course_number_of_hours(subject_df, common_attendance_df):
    #since signals to update number of hours in course is already implemented, this ight not be necessary. In future if its removed or something, implement this
    pass



def get_course_object(course_code):
    if pd.isnull(course_code):
        return None
    else:
        return Course.objects.get(course_code=course_code)


def insert_percentage_details_for_student(student, attendance_df, branch):
    # Calculate number of missing hours of each subject for student
    courses = Course.objects.filter(branch=branch)
    total_hours_lost_student = {course.course_code: {'With Duty': 0, 'Without Duty': 0} for course in courses}

    for column_name in attendance_df.columns[1:8]:  # Start from the second column
        col_index = int(column_name)  # Convert column name to integer
        for index, row in attendance_df.iterrows():
            subject_code = row[column_name]
            duty_hour_col_name = f"duty_hour_{col_index}"
            
            # Count hours lost with duty
            if pd.notna(subject_code):
                total_hours_lost_student[subject_code]['With Duty'] += 1

            # Count hours lost without duty
            if pd.notna(subject_code) and not row[duty_hour_col_name]:
                total_hours_lost_student[subject_code]['Without Duty'] += 1

    # Convert the dictionary to a DataFrame
    total_hours_lost_student_df = pd.DataFrame(total_hours_lost_student).transpose().reset_index()
    total_hours_lost_student_df.columns = ['Subject Code', 'Total Hours Lost(With Duty)', 'Total Hours Lost(Without Duty)']

    # print(f"{student_name}'s Number of hours lost:")
    print(total_hours_lost_student_df)
    
    # Iterate through each row of total_hours_lost_student_df
    for _, row in total_hours_lost_student_df.iterrows():
        # Retrieve the Course object corresponding to the course code
        course_code = row['Subject Code']
        course = Course.objects.filter(course_code=course_code).first()
        
        # Insert values into PercentageDetails table
        if course:
            percentage_details = PercentageDetails.objects.update_or_create(
                student=student,
                course=course,
                defaults={
                    'hours_lost_with_duty': row['Total Hours Lost(With Duty)'],
                    'hours_lost_without_duty': row['Total Hours Lost(Without Duty)'],
                }
            )
            print(f"\nPercentage details inserted for {student.user.first_name} - {course.course_name}: {percentage_details}")
        else:
            print(f"\nCourse with code {course_code} not found for {student.user.first_name}. Skipping insertion of PercentageDetails.")



def update_student_attendance_details(student, driver, branch):
    #get attendance
    driver.find_element(By.LINK_TEXT, "Attendance").click()
    Select(driver.find_element(By.NAME, "code")).select_by_index(0)
    driver.find_element(By.XPATH, "//input[@value='SUBMIT']").click()


    # Scrape the attendance details for the current student
    table = driver.find_element(By.XPATH, "//table[@width='96%']")
    table_html = table.get_attribute("outerHTML")
    soup = BeautifulSoup(table_html, "html.parser")
    attendance_df = pd.read_html(StringIO(table_html))[0][1:].drop([1]).reset_index(drop=True)

    # Extract duty attendance information and mark corresponding duty_hour columns as True
    duty_hours = []
    for row in soup.find_all('tr')[2:]:
        cells = row.find_all(['td', 'th'])
        duty_hours_row = [False] * 7  # Initialize all duty_hour columns to False for each row
        for i, cell in enumerate(cells):
            if cell.has_attr('bgcolor') and cell['bgcolor'] == '#cccc00':
                duty_hours_row[i-1] = True
        duty_hours.append(duty_hours_row)

    # Ensure the number of rows in the duty_hours list matches the number of rows in the attendance DataFrame
    if len(duty_hours) != len(attendance_df):
        # Adjust the length of the duty_hours list to match the number of rows in the attendance DataFrame
        if len(duty_hours) > len(attendance_df):
            duty_hours = duty_hours[:len(attendance_df)]
        else:
            # Append extra rows with default duty hour values (False) if necessary
            extra_rows = len(attendance_df) - len(duty_hours)
            for _ in range(extra_rows):
                duty_hours.append([False] * 7)

    # Add duty attendance columns to the DataFrame with extracted duty hours
    for i in range(1, 8):
        column_name = f"duty_hour_{i}"
        attendance_df[column_name] = [row[i-1] for row in duty_hours]

    print(attendance_df)

    for _, row in attendance_df.iterrows():
        date_str = row[0]
        date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()
        hours = []

        for i in range(1, 8):
            course_code = row[i]
            if course_code and course_code != 'nan':  # Check if course code is present and not 'nan'
                try:
                    course = Course.objects.get(course_code=course_code)
                except ObjectDoesNotExist:
                    course = None
            else:
                course = None
            hours.append(course)

        student_attendance, created = StudentAttendance.objects.update_or_create(
            student=student,
            date=date_obj,
            defaults={
                'hour_1': hours[0],
                'hour_2': hours[1],
                'hour_3': hours[2],
                'hour_4': hours[3],
                'hour_5': hours[4],
                'hour_6': hours[5],
                'hour_7': hours[6],
                'duty_hour_1': row['duty_hour_1'],
                'duty_hour_2': row['duty_hour_2'],
                'duty_hour_3': row['duty_hour_3'],
                'duty_hour_4': row['duty_hour_4'],
                'duty_hour_5': row['duty_hour_5'],
                'duty_hour_6': row['duty_hour_6'],
                'duty_hour_7': row['duty_hour_7']
            }
        )
        
        if created:
            print(f"\nStudent attendance inserted: {student_attendance}")
        else:
            print(f"\nStudent attendance updated: {student_attendance}")
     
    student_attendance_df = attendance_df.iloc[:, 0:8]
    insert_percentage_details_for_student(student, attendance_df, branch)
    
    return student_attendance_df




def update_attendance_details(branch):
    try:
        common_attendance_df = pd.DataFrame()
        driver = webdriver.Chrome()
        students = Students.objects.filter(branch=branch)
        for student in students:
            uid = student.user.username
            password = student.user.login_password
            # print(password)
            driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
            driver.find_element(By.NAME, "Userid").send_keys(uid)
            driver.find_element(By.NAME, "Password").send_keys(password)
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            student_attendance_df = update_student_attendance_details(student, driver, branch)
            common_attendance_df = pd.concat([common_attendance_df, student_attendance_df], ignore_index=True)
            common_attendance_df = common_attendance_df.groupby(common_attendance_df.columns[0]).apply(lambda x: x.ffill()).reset_index(drop=True)
            common_attendance_df = common_attendance_df.drop_duplicates(subset=common_attendance_df.columns[0], keep='last').reset_index(drop=True)
        
        insert_branch_attendance(common_attendance_df, branch)
        update_course_number_of_hours(common_attendance_df, branch)    
        get_attendance_percentage(branch)
        
        naive_datetime_object = datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime_object)
        branch.last_attendance_update = aware_datetime
        branch.save()
        
    except Exception as e:
        print(f"Error: {e}")
