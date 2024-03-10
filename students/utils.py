#students/utils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
from students.models import Students
from accounts.models import CustomUser
from academia.models import Branch
from attendance.models import StudentAttendance, PercentageDetails, BranchHoursDetails
from datetime import datetime

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
        print(f"{name}' - {uid} - {password} - {email}")

        if not Students.objects.filter(user__username=uid).exists():
            user = CustomUser.objects.create_user(
                username=uid, 
                password=password, 
                email=email, 
                first_name=name
            )
            student = Students.objects.create(
                user=user,
                branch_id=branch.id
            )
            print(f"Student details inserted: {student}")
        else:
            print(f"Student with UID {uid} already exists in the database.")

    except Exception as e:
        print(f"Error inserting student details: {e}")


def insert_student_attendance_details(driver, student_row, branch):
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
            student_attendance = StudentAttendance.objects.create(
                student=student,
                date=date_obj,
                hour_1=row[1],
                hour_2=row[2],
                hour_3=row[3],
                hour_4=row[4],
                hour_5=row[5],
                hour_6=row[6],
                hour_7=row[7],
                duty_hour_1=row['duty_hour_1'],
                duty_hour_2=row['duty_hour_2'],
                duty_hour_3=row['duty_hour_3'],
                duty_hour_4=row['duty_hour_4'],
                duty_hour_5=row['duty_hour_5'],
                duty_hour_6=row['duty_hour_6'],
                duty_hour_7=row['duty_hour_7']
            )
            print(f"Student attendance inserted: {student_attendance}")
    
    except Exception as e:
        print(f"Error inserting student attendance details: {e}")
    # student_attendance_df = attendance_df.iloc[:, 0:8]
    # print(student_attendance_df)
    # print("\n")





def iterate_through_students(branch, excel_file):
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
        insert_student_attendance_details(driver, student_row, branch)
        

        # #get studetns name
        # text_element = driver.find_element(By.XPATH, "//div[@class='scroller']")
        # text_content = text_element.text
        # index = text_content.find('Logged In User :')
        # student_name = text_content[index + len('Logged In User :'):].strip()
        # print("Student's Name:", student_name)



        # #get attendance
        # driver.find_element(By.LINK_TEXT, "Attendance").click()

        # #get semester
        # Select(driver.find_element(By.NAME, "code")).select_by_index(0)
        # semester = Select(driver.find_element(By.NAME, "code")).first_selected_option.text.split('S')[1][0]
        # print("Semester:", semester)
        # driver.find_element(By.XPATH, "//input[@value='SUBMIT']").click()