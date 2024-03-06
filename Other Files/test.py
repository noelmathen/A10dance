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
    attendance_df_with_duty = pd.read_html(StringIO(table_html))[0][1:].drop([1]).reset_index(drop=True)

    #Discard duty attendance because it doesnt contrivute to attendance percentage
    rows = []
    for row in soup.find_all('tr'):
        cells = []
        for cell in row.find_all(['td', 'th']):
            if cell.has_attr('bgcolor') and cell['bgcolor'] == '#cccc00':
                cells.append(np.nan)
            else:
                cells.append(cell.text.strip())
        rows.append(cells)

    # Convert the list of rows to a DataFrame
    attendance_df_with_duty = pd.read_html(StringIO(table_html))[0][1:].drop([1]).reset_index(drop=True)
    attendance_df = pd.DataFrame(rows[1:], columns=rows[0]).drop([0]).reset_index(drop=True)
    attendance_df.columns = attendance_df_with_duty.columns
    attendance_df.replace('', np.nan, inplace=True)

    print(f"{student_name}'s attendance:")
    print(attendance_df)
    print(attendance_df_with_duty)
    print("\n")




    # Calculate number of missing hours of each subejct for student
    total_hours_lost_student = {subject: 0 for subject in subjects_df['Subject Code']}
    for col in range(1, attendance_df.shape[1]):
        for index, row in attendance_df.iterrows():
            subject_code = row[col]
            if pd.notna(subject_code):
                total_hours_lost_student[subject_code] = total_hours_lost_student.get(subject_code, 0) + 1
    total_hours_lost_student_df = pd.DataFrame(list(total_hours_lost_student.items()), columns=['Subject Code', 'Total Hours Lost'])
    print(f"{student_name}'s Number of hours lost:")
    print(total_hours_lost_student_df)


    # Logout
    driver.find_element(By.LINK_TEXT, "Logout").click()

    # Clean up
    driver.quit()


if __name__ == "__main__":
    main()
