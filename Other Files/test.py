from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def main():
    # Read student details from Excel
    student_details_df = pd.read_excel(r'C:\Users\noelm\Documents\PROJECTS\A10dance\Other Files\CSBS_2021-2025.xlsx')
    print(student_details_df)
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
    attendance_df = pd.read_html(StringIO(table_html))[0][1:].drop([1]).reset_index(drop=True)
    print(attendance_df)
    print("\n")

    # Logout
    driver.find_element(By.LINK_TEXT, "Logout").click()

    # Clean up
    driver.quit()


if __name__ == "__main__":
    main()
