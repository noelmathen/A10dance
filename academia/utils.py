#academia/utils.py
from .models import Course
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from .models import Branch
import logging

logger = logging.getLogger(__name__)

def fetch_subject_details(branch_name, excel_file):
    try:
        student_details_df = pd.read_excel(excel_file)
        print(student_details_df)

        # Fetch subjects details for the first student
        first_uid = str(student_details_df.loc[0, 'UID'])
        first_password = str(student_details_df.loc[0, 'Password'])
        # subjects_df = fetch_subject_details(first_uid, first_password)

        # Open a new Chrome window
        driver = webdriver.Chrome()

        # Log in using the student's credentials
        driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
        driver.find_element(By.NAME, "Userid").send_keys(first_uid)
        driver.find_element(By.NAME, "Password").send_keys(first_password)
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Navigate to the Sessional Marks page
        driver.find_element(By.LINK_TEXT, "Sessional Marks").click()

        #get semester
        Select(driver.find_element(By.NAME, "code")).select_by_index(0)
        semester = Select(driver.find_element(By.NAME, "code")).first_selected_option.text.split('S')[1][0]
        logger.info("Semester: %s", semester)

        # Submit the form to fetch the subjects
        driver.find_element(By.XPATH, "//input[@value='SUBMIT']").click()

        # Extract subject data from the table
        table = driver.find_element(By.XPATH, "//table[@width='50%']")
        table_html = table.get_attribute("outerHTML")
        soup = BeautifulSoup(table_html, "html.parser")
        df = pd.read_html(str(soup), header=0)[0].iloc[:]
        df = df.rename(columns={"Code": "Subject Code"})
        print(df)
        logger.info(df)

        # Assuming df is the DataFrame containing subject details
        courses = []
        for index, row in df.iterrows():
            course_code = row['Subject Code']
            course_name = row['Subject']
            branch = Branch.objects.get(branch_name=branch_name)

            course = Course(
                course_code=course_code,
                course_name=course_name,
                number_of_hours=0,
                semester=semester,
                branch=branch
            )
            courses.append(course)

        Course.objects.bulk_create(courses)

    except Exception as e:
        logger.error(f"Error fetching subjects: {e}")


def process_excel_file(branch, excel_file):
    fetch_subject_details(branch.branch_name, excel_file)


