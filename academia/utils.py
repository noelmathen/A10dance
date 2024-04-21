#academia/utils.py
from .models import Course
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from .models import Branch
import logging
from io import StringIO
from django.utils.text import slugify
import re

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
        df = pd.read_html(StringIO(table_html), header=0)[0].iloc[:]
        df = df.rename(columns={"Code": "Subject Code"})
        print(df)
        logger.info(df)

        # Define a function to handle special characters and Roman numerals
        def generate_short_form(course_name):
            short_form = ""
            words = re.findall(r"[\w']+|[.,!?;-]", course_name)  # Extract words, special characters, and hyphen (-)

            for word in words:
                if word.upper() == "AND" or word == "&":  # Ignore "AND" and "&"
                    continue
                elif word.upper() == "LAB" and course_name.upper().endswith("LAB"):
                    short_form += " LAB"  # Append " LAB" for courses ending with "LAB"
                else:
                    # Check for Roman numeral or special case
                    try:
                        roman_numeral = int(word)
                        short_form += f"-{roman_numeral}"  # Append Roman numeral with '-'
                    except ValueError:
                        # Check for hyphen followed by valid Roman numeral (including V)
                        if len(word) > 1 and word[0] == '-' and all(char in "IVXLCM" for char in word[1:]):
                            short_form += word  # Include the entire word (hyphen + Roman numeral)
                        else:
                            short_form += word[0].upper() if word.isalpha() else word  # First letter for words, entire word for special chars

            return short_form.strip()

        # Inside the fetch_subject_details function
        courses = []
        slot_counter = 1
        for index, row in df.iterrows():
            course_code = row['Subject Code']
            course_name = row['Subject']
            branch = Branch.objects.get(branch_name=branch_name)
            
            # Generate short form
            short_form = generate_short_form(course_name)
            print(short_form)
            course = Course(
                course_code=course_code,
                course_name=course_name,
                number_of_hours=0,
                semester=semester,
                branch=branch,
                short_form=short_form.strip(),
                slot=slot_counter
            )
            courses.append(course)
            slot_counter+=1
        Course.objects.bulk_create(courses)

    except Exception as e:
        logger.error(f"Error fetching subjects: {e}")
        
    return df


def process_excel_file(branch, excel_file):
    subject_df=fetch_subject_details(branch.branch_name, excel_file)
    return subject_df

