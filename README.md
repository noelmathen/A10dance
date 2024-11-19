# A10dance

[![Watch the Walkthrough](https://img.youtube.com/vi/4Y2YtqheJu4/maxresdefault.jpg)](https://www.youtube.com/watch?v=4Y2YtqheJu4&ab_channel=NoelMathenEldho){:target="_blank"}
**Click to watch the video walkthrough of A10dance!**

**A10dance** is a powerful backend system designed to automate and enhance attendance tracking and management for educational institutions. Leveraging **Django**, **Selenium**, and other advanced technologies, it supports multi-branch tracking, email notifications, and attendance prediction, ensuring a seamless experience for administrators and students alike.

---

## 🚀 Features

### **Core Features**

- **Automated Attendance Scraping**: Uses Selenium to scrape attendance details directly from institutional systems.
- **Dynamic Attendance Percentage Calculation**: Real-time tracking and updates whenever attendance or course hours are modified.
- **Elective Courses Handling**:
  - Automatically detects elective courses.
  - Synchronizes attendance and hours between main and elective courses.
  - Displays user-friendly elective names in the frontend instead of technical course codes.
- **Signals for Automation**:
  - Updates `PercentageDetails` automatically when models like `Course`, `BranchHourDetails`, or `StudentAttendance` are modified.

---

### **Enhanced Features**

1. **Multiple Branch Tracking**:

   - Supports attendance management for multiple branches.
   - Tracks and updates attendance percentages for students across branches seamlessly.
2. **Duty Attendance and Leave Consideration**:

   - Differentiates between regular absences, duty leave, and approved leaves.
   - Adjusts attendance percentages accurately based on duty hours or leaves granted to students.
3. **Email Notifications for Attendance Changes**:

   - Sends automated emails to students whenever there’s an update in their attendance:
     - Marked absent
     - Duty attendance added or removed
     - Absent changed to present
   - Ensures transparency and immediate communication with students.
4. **Attendance Percentage Prediction**:

   - Predicts future attendance percentages based on:
     - Current total hours.
     - Hours already missed.
     - Estimated future absences.
   - Helps students plan their attendance to avoid falling below the required threshold.

---

### **Frontend Integration**

- **Dynamic Data Fetching**:
  - APIs provide real-time attendance data to the frontend.
  - Automatically updates tables to reflect elective names, attendance percentages, and predictions.
- **Visual Representation**:
  - Displays attendance statistics in a clean, intuitive interface.
  - Screenshots (to be added):
    - [Dashboard Overview](screenshots/dashboard_overview.png)
    - [Course Details](screenshots/course_details.png)
    - [Email Notification Sample](screenshots/email_notification_sample.png)

---

## 💻 Technologies Used

- **Django**: Backend framework for logic and database management.
- **Selenium**: For scraping attendance data.
- **PostgreSQL**: Database solution for robust data handling.
- **Django REST Framework**: For creating APIs to serve attendance data to the frontend.
- **HTML + JavaScript**: Frontend technologies for dynamic user interaction.
- **SMTP Email Integration**: Sends real-time email notifications.

---

## 📖 How It Works

1. **Attendance Updates**:

   - Uses **signals** (`pre_save`, `post_save`, `pre_delete`, `post_delete`) to automatically:
     - Recalculate attendance percentages.
     - Sync hours and details across `BranchHourDetails` and `Course` models.
   - Tracks changes in attendance and generates real-time updates.
2. **Email Notification System**:

   - Integrated with Django's email framework.
   - Notifies students immediately when their attendance records change.
3. **Attendance Prediction**:

   - Uses the following formula to estimate future percentages:
     ```
     Predicted Percentage = ((Current Total Hours - Total Missed Hours - Estimated Future Missed Hours) / Current Total Hours) * 100
     ```
   - Displays predictions in the frontend for proactive planning.
4. **Frontend Integration**:

   - APIs provide:
     - Branch and course-level attendance details.
     - Attendance percentages and predictions.
   - Frontend dynamically updates to reflect changes in real-time.

---

## 📖 Support
For any issues or inquiries, please contact [noelmathen03@gmail.com].

---

## Screenshots of project

Index Page![Screenshot 1](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%201.jpg)

Student Leave and Percentage Details Page 1![Screenshot 2](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%202.jpg)

Student Percentage Details with predict percentage feature![Screenshot 3](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%203.jpg)

Student Percentage Details filtering feature![Screenshot 4](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%204.jpg)

Class Attendance Details![Screenshot 5](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%205.jpg)

Class Attendance Details 2![Screenshot 6](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%206.jpg)

Admin Page - Branch Details![Screenshot 7](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%207.jpg)

Admin Page - Course Details![Screenshot 8](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%208.jpg)

Admin Page - Branch Hours Details![Screenshot 9](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%209.jpg)

Admin Page - Branch Hours Details Editing Options![Screenshot 10](https://github.com/noelmathen/A10dance/blob/main/Walkthoughs%20and%20Screenshots/Screenshot%2010.jpg)
