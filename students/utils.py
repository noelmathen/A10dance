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


def iterate_through_students(branch, excel_file):
    student_details_df = pd.read_excel(excel_file)
    print(student_details_df) 

    common_attendance_df = pd.DataFrame()
    driver = webdriver.Chrome()


    # Loop through each student
    for _, student_row in student_details_df.iterrows():
        # Login with student credentials
        driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
        driver.find_element(By.NAME, "Userid").send_keys(student_row['UID'])
        driver.find_element(By.NAME, "Password").send_keys(student_row['Password'])
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        
        
        branch_obj = Branch.objects.get(branch_name=branch.branch_name)
        insert_student_details(driver, student_row, branch_obj)

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