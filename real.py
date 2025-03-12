from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import datetime

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5500/HTML/index.html")
time.sleep(3)
employee_button = driver.find_element(By.XPATH, "/html/body/header/div/nav/ul/li[2]/a")
employee_button.click()
time.sleep(3)
table = driver.find_element(By.XPATH, "//*[@id='employee-tasks']/div/table")
rows = table.find_elements(By.TAG_NAME, "tr")
table_data = []
leave_tasks_data = []
leave_found = False
less_than_8_hours_data = []
more_than_8_hours_data = []
less_than_8_found = False
more_than_8_found = False

for row in rows[1:]:
    columns = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text for col in columns]
    table_data.append(row_data)

    if len(row_data) > 1 and "leave" in row_data[1].lower():
        leave_tasks_data.append(row_data)
        leave_found = True
        print("Leave Task Found:")
        print(row_data)

    if len(row_data) > 4:
        try:
            hours_str = row_data[4]
            hours = float(hours_str) if hours_str else 0.0  # Handle empty hours as 0
            date_str = row_data[0] # Assuming date is in the first column
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() # Adjust format if needed
            day_of_week = date_obj.strftime('%A') # e.g., "Monday", "Tuesday", etc.

            if hours < 8:
                if not (day_of_week == "Saturday" and hours == 0): # Exclude Saturday 0 hours
                    less_than_8_hours_data.append(row_data)
                    less_than_8_found = True
                    print("Less than 8 Hours Task Found:")
                    print(row_data)
            elif hours > 8:
                more_than_8_hours_data.append(row_data)
                more_than_8_found = True
                print("More than 8 Hours Task Found:")
                print(row_data)
        except ValueError as e:
            print(f"Warning: Could not process hours or date for row: {row_data}. Error: {e}")


print(table_data)
df = pd.DataFrame(table_data, columns=["Date", "Task Listings", "Time IN", "Time OUT", "Hours", "Task Assigned"])
df.to_csv("employee_report.csv", index=False)

if leave_found:
    df_leave = pd.DataFrame(leave_tasks_data, columns=["Date", "Task Listings", "Time IN", "Time OUT", "Hours", "Task Assigned"])
    df_leave.to_csv("leave_report.csv", index=False)
    print("Leave report generated and saved as 'leave_report.csv'")
else:
    print("No leave tasks found.")

if less_than_8_found:
    df_less_than_8 = pd.DataFrame(less_than_8_hours_data, columns=["Date", "Task Listings", "Time IN", "Time OUT", "Hours", "Task Assigned"])
    df_less_than_8.to_csv("less_than_8_hours_report.csv", index=False)
    print("Less than 8 hours report generated and saved as 'less_than_8_hours_report.csv'")
else:
    print("No tasks with less than 8 hours found (excluding Saturday 0 hours).")

if more_than_8_found:
    df_more_than_8 = pd.DataFrame(more_than_8_hours_data, columns=["Date", "Task Listings", "Time IN", "Time OUT", "Hours", "Task Assigned"])
    df_more_than_8.to_csv("more_than_8_hours_report.csv", index=False)
    print("More than 8 hours report generated and saved as 'more_than_8_hours_report.csv'")
else:
    print("No tasks with more than 8 hours found.")

pdf_filename = "employee_report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)
styles = getSampleStyleSheet()
title_style = styles['Heading1']
normal_style = styles['Normal']
c.setTitle("Employee Task Report and Salary Summary")

y_position = 750

employee_name = "Sanket"
monthly_salary = 5000
paid_leave_days = 2
leave_deduction_per_day = 200
underwork_deduction_per_hour = 100
overtime_rate_per_hour = 50

title_text = "Employee Task and Salary Report"
p = Paragraph(title_text, title_style)
p.wrapOn(c, letter[0], letter[1])
p.drawOn(c, 50, y_position)
y_position -= 40

c.setFont("Helvetica-Bold", 12)
c.drawString(50, y_position, f"Employee Name: {employee_name}")
y_position -= 20
c.drawString(50, y_position, f"Monthly Salary: {monthly_salary}")
y_position -= 20
c.setFont("Helvetica", 12)
y_position -= 10

leave_days_taken = len(leave_tasks_data)
extra_leave_days = max(0, leave_days_taken - paid_leave_days)
leave_deduction = extra_leave_days * leave_deduction_per_day

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y_position, "Leave Tasks Report:")
y_position -= 20
c.setFont("Helvetica", 12)
c.drawString(50, y_position, f"Paid Leave Days Allowed: {paid_leave_days}")
y_position -= 20
c.drawString(50, y_position, f"Leave Days Taken: {leave_days_taken}")
y_position -= 20
c.drawString(50, y_position, f"Extra Leave Days (beyond paid): {extra_leave_days}")
y_position -= 20
c.drawString(50, y_position, f"Leave Deduction: {leave_deduction}")
y_position -= 20

if leave_tasks_data:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y_position, "Leave Task Details:")
    y_position -= 20
    c.setFont("Helvetica", 10)
    for task_data in leave_tasks_data:
        task_str = ", ".join(task_data)
        p = Paragraph(task_str, normal_style)
        p.wrapOn(c, letter[0] - 100, letter[1])
        p.drawOn(c, 90, y_position)
        y_position -= 15
        if y_position < 50:
            c.showPage()
            y_position = 750
else:
    c.drawString(70, y_position, "No leave tasks found in data.")
    y_position -= 20
y_position -= 10

underwork_hours_total = 0
if less_than_8_found:
    for task_data in less_than_8_hours_data:
        try:
            hours_str = task_data[4]
            hours_worked = float(hours_str) if hours_str else 0.0
            underwork_hours_total += (8 - hours_worked)
        except ValueError:
            pass

underwork_deduction = underwork_hours_total * underwork_deduction_per_hour


c.setFont("Helvetica-Bold", 14)
c.drawString(50, y_position, "Tasks Less Than 8 Hours Report:")
y_position -= 20
c.setFont("Helvetica", 12)
c.drawString(50, y_position, f"Total Underwork Hours: {underwork_hours_total:.2f}")
y_position -= 20
c.drawString(50, y_position, f"Underwork Deduction: {underwork_deduction}")
y_position -= 20

if less_than_8_hours_data:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y_position, "Tasks Less Than 8 Hours Details (excluding Saturday 0 hours):")
    y_position -= 20
    c.setFont("Helvetica", 10)
    for task_data in less_than_8_hours_data:
        task_str = ", ".join(task_data)
        p = Paragraph(task_str, normal_style)
        p.wrapOn(c, letter[0] - 100, letter[1])
        p.drawOn(c, 90, y_position)
        y_position -= 15
        if y_position < 50:
            c.showPage()
            y_position = 750
else:
    c.drawString(70, y_position, "No tasks less than 8 hours found (excluding Saturday 0 hours).")
    y_position -= 20
    y_position -= 10

overtime_hours_total = 0
if more_than_8_found:
    for task_data in more_than_8_hours_data:
        try:
            hours_str = task_data[4]
            hours_worked = float(hours_str) if hours_str else 0.0
            overtime_hours_total += (hours_worked - 8)
        except ValueError:
            pass

overtime_pay = overtime_hours_total * overtime_rate_per_hour

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y_position, "Tasks More Than 8 Hours (Overtime) Report:")
y_position -= 20
c.setFont("Helvetica", 12)
c.drawString(50, y_position, f"Total Overtime Hours: {overtime_hours_total:.2f}")
y_position -= 20
c.drawString(50, y_position, f"Overtime Pay: {overtime_pay}")
y_position -= 20

if more_than_8_hours_data:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y_position, "Tasks More Than 8 Hours Details:")
    y_position -= 20
    c.setFont("Helvetica", 10)
    for task_data in more_than_8_hours_data:
        task_str = ", ".join(task_data)
        p = Paragraph(task_str, normal_style)
        p.wrapOn(c, letter[0] - 100, letter[1])
        p.drawOn(c, 90, y_position)
        y_position -= 15
        if y_position < 50:
            c.showPage()
            y_position = 750
else:
    c.drawString(70, y_position, "No tasks more than 8 hours found.")
    y_position -= 20
y_position -= 10

final_salary = monthly_salary - leave_deduction - underwork_deduction + overtime_pay

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y_position, "Salary Summary:")
y_position -= 20
c.setFont("Helvetica", 12)
c.drawString(50, y_position, f"Gross Monthly Salary: {monthly_salary}")
y_position -= 20
c.drawString(50, y_position, f"Total Deductions:")
y_position -= 20
c.drawString(70, y_position, f"Leave Deduction: {leave_deduction}")
y_position -= 20
c.drawString(70, y_position, f"Underwork Deduction: {underwork_deduction}")
y_position -= 20
c.drawString(50, y_position, f"Total Additions:")
y_position -= 20
c.drawString(70, y_position, f"Overtime Pay: {overtime_pay}")
y_position -= 20
c.setFont("Helvetica-Bold", 12)
c.drawString(50, y_position, f"Net Salary: {final_salary}")
y_position -= 20


c.save()
print(f"PDF report with salary and overtime summary generated and saved as '{pdf_filename}'")

def fill_and_submit_contact_form(message_summary):
    """Fills and submits the contact form with the given message summary."""
    try:
        contact_button = driver.find_element(By.XPATH, "/html/body/header/div/nav/ul/li[3]/a")
        contact_button.click()
        time.sleep(2)

        name_field = driver.find_element(By.XPATH, "//*[@id='name']")
        email_field = driver.find_element(By.XPATH, "//*[@id='email']")
        message_field = driver.find_element(By.XPATH, "//*[@id='message']")
        submit_button = driver.find_element(By.XPATH, "//*[@id='contactForm']/button")

        name_field.send_keys("admin")
        email_field.send_keys("asd@gmail.com")
        message_field.send_keys(message_summary)
        submit_button.click()
        time.sleep(2)
        print("Contact form filled and submitted successfully.")

    except Exception as e:
        print(f"Error filling or submitting contact form: {e}")
    finally:
        driver.back()
        time.sleep(2)

leave_summary_message = f"""
Employee Leave Report Summary:

Employee Name: {employee_name}
Total Leave Days Taken: {leave_days_taken}
Extra Leave Days (beyond paid): {extra_leave_days}
Leave Deduction: {leave_deduction}

Please see the attached PDF report for detailed leave information.
"""
fill_and_submit_contact_form(leave_summary_message)

overtime_summary_message = f"""
Employee Overtime Report Summary:

Employee Name: {employee_name}
Total Overtime Hours: {overtime_hours_total:.2f}
Overtime Pay: {overtime_pay}

Please see the attached PDF report for detailed overtime information.
"""
fill_and_submit_contact_form(overtime_summary_message)

underwork_summary_message = f"""
Employee Underwork Report Summary:

Employee Name: {employee_name}
Total Underwork Hours: {underwork_hours_total:.2f}
Underwork Deduction: {underwork_deduction}

Please see the attached PDF report for detailed underwork information.
"""
fill_and_submit_contact_form(underwork_summary_message)

time.sleep(70)
driver.quit()
print("Report generation and contact form processing complete.")