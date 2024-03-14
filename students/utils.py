#students/utils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from students.models import Students
from accounts.models import CustomUser
from academia.models import Course
from attendance.models import StudentAttendance, PercentageDetails, BranchHoursDetails
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


def insert_student_details(driver, student_row, branch):
    try:
        #get studetns name
        text_element = driver.find_element(By.XPATH, "//div[@class='scroller']")
        text_content = text_element.text
        index = text_content.find('Logged In User :')
        
        name = text_content[index + len('Logged In User :'):].strip()    
        uid = str(student_row['UID'])
        password = str(student_row['Password'])
        email = str(str(uid) + '@rajagiri.edu.in')
        print(f"\n{name}' - {uid} - {password} - {email}")

        if not Students.objects.filter(user__username=uid).exists():
            user = CustomUser.objects.create_user(
                username=uid, 
                password=password, 
                login_password=password,
                email=email, 
                first_name=name
            )
            student = Students.objects.create(
                user=user,
                branch_id=branch.id
            )
            print(f"\nStudent details inserted: {student}")
        else:
            print(f"\nStudent with UID {uid} already exists in the database.")

    except Exception as e:
        print(f"\nError inserting student details: {e}")



def insert_student_attendance_details(subject_df, driver, student_row, branch):
    try:
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
        
        # Insert attendance data into StudentAttendance table
        student = Students.objects.get(user__username=student_row['UID'])
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

            student_attendance = StudentAttendance.objects.create(
                student=student,
                date=date_obj,
                hour_1=hours[0],
                hour_2=hours[1],
                hour_3=hours[2],
                hour_4=hours[3],
                hour_5=hours[4],
                hour_6=hours[5],
                hour_7=hours[6],
                duty_hour_1=row['duty_hour_1'],
                duty_hour_2=row['duty_hour_2'],
                duty_hour_3=row['duty_hour_3'],
                duty_hour_4=row['duty_hour_4'],
                duty_hour_5=row['duty_hour_5'],
                duty_hour_6=row['duty_hour_6'],
                duty_hour_7=row['duty_hour_7']
            )
            print(f"\nStudent attendance inserted: {student_attendance}")
            
        student_attendance_df = attendance_df.iloc[:, 0:8]
        insert_percentage_details_for_student(subject_df, student, attendance_df)
        
        return student_attendance_df

    except Exception as e:
        print(f"\nError inserting student attendance details: {e}")




def insert_percentage_details_for_student(subject_df, student, attendance_df):
    # Calculate number of missing hours of each subject for student
    total_hours_lost_student = {subject: {'With Duty': 0, 'Without Duty': 0} for subject in subject_df['Subject Code']}

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
        course = get_course_object(course_code)
        
        # Insert values into PercentageDetails table
        if course:
            percentage_details = PercentageDetails.objects.create(
                student=student,
                course=course,
                hours_lost_with_duty=row['Total Hours Lost(With Duty)'],
                hours_lost_without_duty=row['Total Hours Lost(Without Duty)'],
                percentage_of_subject=100  # Default value
            )
            print(f"\nPercentage details inserted for {student.user.first_name} - {course.course_name}: {percentage_details}")
        else:
            print(f"\nCourse with code {course_code} not found for {student.user.first_name}. Skipping insertion of PercentageDetails.")
 
    
    
def get_course_object(course_code):
    if pd.isnull(course_code):
        return None
    else:
        return Course.objects.get(course_code=course_code)

    
def insert_branch_attendance(common_attendance_df, branch):
    for _, row in common_attendance_df.iterrows():
        date_str = row[0]
        date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()

        branch_hours_details = BranchHoursDetails.objects.create(
            branch=branch,
            date=date_obj,
            hour_1=get_course_object(row[1]),
            hour_2=get_course_object(row[2]),
            hour_3=get_course_object(row[3]),
            hour_4=get_course_object(row[4]),
            hour_5=get_course_object(row[5]),
            hour_6=get_course_object(row[6]),
            hour_7=get_course_object(row[7])
        )
        print(f"\nBranch hours details inserted: {branch_hours_details}")



def update_course_number_of_hours(subject_df, common_attendance_df):
    # Calculate total hours lost for each subject
    total_hours = {subject: 0 for subject in subject_df['Subject Code']}

    for col in range(1, common_attendance_df.shape[1]):
        for index, row in common_attendance_df.iterrows():
            subject_code = row[col]
            if pd.notna(subject_code):
                total_hours[subject_code] = total_hours.get(subject_code, 0) + 1

    # Create a DataFrame from the total hours lost dictionary
    total_hours_df = pd.DataFrame(list(total_hours.items()), columns=['Subject Code', 'Total Hours'])

    # Merge subject_df and total_hours_df to get the final result
    result_df = pd.merge(subject_df, total_hours_df, on='Subject Code', how='left')
    print(result_df)

    for _, row in result_df.iterrows():
        course_code = row['Subject Code']
        total_hours = row['Total Hours']
        try:
            course = Course.objects.get(course_code=course_code)
            course.number_of_hours = total_hours
            course.save()
            print(f"\nUpdated number_of_hours for {course_code} to {total_hours}")
        except Exception as e:
            print(f"\nCourse number of hours updation error!")



def iterate_through_students(subject_df, branch, excel_file):
    student_details_df = pd.read_excel(excel_file)
    print(student_details_df) 
    common_attendance_df = pd.DataFrame()
    driver = webdriver.Chrome()

    for _, student_row in student_details_df.iterrows():
        driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
        driver.find_element(By.NAME, "Userid").send_keys(student_row['UID'])
        driver.find_element(By.NAME, "Password").send_keys(student_row['Password'])
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        
        insert_student_details(driver, student_row, branch)
        student_attendance_df = insert_student_attendance_details(subject_df, driver, student_row, branch)
        
        common_attendance_df = pd.concat([common_attendance_df, student_attendance_df], ignore_index=True)
        common_attendance_df = common_attendance_df.groupby(common_attendance_df.columns[0]).apply(lambda x: x.ffill()).reset_index(drop=True)
        common_attendance_df = common_attendance_df.drop_duplicates(subset=common_attendance_df.columns[0], keep='last').reset_index(drop=True)

    # print(common_attendance_df)
    insert_branch_attendance(common_attendance_df, branch)
    update_course_number_of_hours(subject_df, common_attendance_df)
    
