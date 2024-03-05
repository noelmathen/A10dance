from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def fetch_subject_details(username, password):
    try:
        # Open a new Chrome window
        driver = webdriver.Chrome()

        # Log in using the student's credentials
        driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
        driver.find_element(By.NAME, "Userid").send_keys(username)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Navigate to the Sessional Marks page
        driver.find_element(By.LINK_TEXT, "Sessional Marks").click()

        #get semester
        Select(driver.find_element(By.NAME, "code")).select_by_index(0)
        semester = Select(driver.find_element(By.NAME, "code")).first_selected_option.text.split('S')[1][0]
        print("Semester:", semester)

        # Submit the form to fetch the subjects
        driver.find_element(By.XPATH, "//input[@value='SUBMIT']").click()

        # Extract subject data from the table
        table = driver.find_element(By.XPATH, "//table[@width='50%']")
        table_html = table.get_attribute("outerHTML")
        soup = BeautifulSoup(table_html, "html.parser")
        df = pd.read_html(str(soup), header=0)[0].iloc[:-1]
        df = df.rename(columns={"Code": "Subject Code"})

        return df

    except Exception as e:
        print(f"Error fetching subjects for {username}: {e}")
        return None


def sort_dates(date_series):
    return pd.to_datetime(date_series, format="%d-%b-%Y", errors='coerce')


def main():
    # Read student details from Excel
    student_details_df = pd.read_excel(r'C:\Users\noelm\Documents\PROJECTS\A10dance\Other Files\CSBS_2021-2025.xlsx')
    print(student_details_df)

    # Fetch subjects details for the first student
    first_uid = str(student_details_df.loc[0, 'UID'])
    first_password = str(student_details_df.loc[0, 'Password'])
    subjects_df = fetch_subject_details(first_uid, first_password)
    print(subjects_df)

    # Initialize an empty DataFrame for common attendance
    common_attendance_df = pd.DataFrame()

    # Initialize a Chrome driver
    driver = webdriver.Chrome()

    # Loop through each student
    for _, student_row in student_details_df.iterrows():
        # Login with student credentials
        driver.get("https://www.rajagiritech.ac.in/stud/ktu/student/")
        driver.find_element(By.NAME, "Userid").send_keys(student_row['UID'])
        driver.find_element(By.NAME, "Password").send_keys(student_row['Password'])
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

        # Concatenate the current student's attendance with the common DataFrame
        common_attendance_df = pd.concat([common_attendance_df, attendance_df], ignore_index=True)

        # Perform union and drop duplicates
        common_attendance_df = common_attendance_df.groupby(common_attendance_df.columns[0]).apply(lambda x: x.ffill()).reset_index(drop=True)
        common_attendance_df = common_attendance_df.drop_duplicates(subset=common_attendance_df.columns[0], keep='last').reset_index(drop=True)
        print(common_attendance_df)
        print("\n")

    # Remove duplicated columns
    # common_attendance_df = common_attendance_df.loc[:, ~common_attendance_df.columns.duplicated()]

    # Clean up
    driver.quit()

    # Sort the DataFrame based on the dates
    common_attendance_df[0] = sort_dates(common_attendance_df[0])
    common_attendance_df = common_attendance_df.sort_values(by=0).reset_index(drop=True)

    # Print the ordered DataFrame
    print(common_attendance_df)

    # Calculate total hours lost for each subject
    total_hours_lost = {subject: 0 for subject in subjects_df['Subject Code']}

    for col in range(1, common_attendance_df.shape[1]):
        for index, row in common_attendance_df.iterrows():
            subject_code = row[col]
            if pd.notna(subject_code):
                total_hours_lost[subject_code] = total_hours_lost.get(subject_code, 0) + 1

    # Create a DataFrame from the total hours lost dictionary
    total_hours_lost_df = pd.DataFrame(list(total_hours_lost.items()), columns=['Subject Code', 'Total Hours'])

    # Merge subjects_df and total_hours_lost_df to get the final result
    result_df = pd.merge(subjects_df, total_hours_lost_df, on='Subject Code', how='left')

    # Fill NaN values with 0
    # result_df['Total Hours Lost'] = result_df['Total Hours'].fillna(0).astype(int)
    print(result_df)

    # Write to Excel files
    common_attendance_df.to_excel('CSBS_2021-2025_Attendance.xlsx', index=False)
    result_df.to_excel('CSBS_2021-2025_NumberofHours.xlsx', index=False)


if __name__ == "__main__":
    main()
