from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np

def main():
    data = {
        'Sl No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Subject Code': ['101009/IT500A', '101009/IT500B', '101009/MS500C', '101009/MS500D', '101009/EN500E',
                '101009/IT503F', '101009/IT522G', '100004/IT501H', '101009/IT522S', '101009/IT522T'],
        'Subject': ['SOFTWARE DESIGN WITH UML', 'COMPILER DESIGN', 'FUNDAMENTALS OF MANAGEMENT',
                    'BUSINESS STRATEGY', 'BUSINESS COMMUNICATION & VALUE SCIENCE III',
                    'MACHINE LEARNING', 'COMPILER DESIGN LAB (LEX & YACC)', 'WIRELESS COMMUNICATION',
                    'MACHINE LEARNING LAB', 'MINI PROJECT']
    }
    subjects_df = pd.DataFrame(data)
    print(subjects_df)


    # Read student details from Excel
    student_details_df = pd.read_excel(r'C:\Users\noelm\Documents\PROJECTS\A10dance\Other Files\CSBS_2021-2025.xlsx')
    # print(student_details_df)
    # Initialize a Chrome driver
    driver = webdriver.Chrome()

    # Login with student credentials
    driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
    driver.find_element(By.NAME, "Userid").send_keys('u2109053')
    driver.find_element(By.NAME, "Password").send_keys('210825')
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    #get studetns name
    text_element = driver.find_element(By.XPATH, "//div[@class='scroller']")
    text_content = text_element.text
    index = text_content.find('Logged In User :')
    student_name = text_content[index + len('Logged In User :'):].strip()
    print("Student's Name:", student_name)

    #get attendance
    driver.find_element(By.LINK_TEXT, "Attendance").click()

    #get semester
    Select(driver.find_element(By.NAME, "code")).select_by_index(1)
    semester = Select(driver.find_element(By.NAME, "code")).first_selected_option.text.split('S')[1][0]
    print("Semester:", semester)
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

    print(f"{student_name}'s attendance with duty hours:")
    print(attendance_df)
    print("\n")


    # Calculate number of missing hours of each subject for student
    total_hours_lost_student = {subject: {'With Duty': 0, 'Without Duty': 0} for subject in subjects_df['Subject Code']}

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

    print(f"{student_name}'s Number of hours lost:")
    print(total_hours_lost_student_df)



    # Logout
    driver.find_element(By.LINK_TEXT, "Logout").click()

    # Clean up
    driver.quit()


if __name__ == "__main__":
    main()
