from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
import os

WEBSITE_URL = "http://127.0.0.1:5500/index.html"
REPORT_FILE = "output/employee_task_report.txt"
CSV_REPORT_FILE = "output/employee_task_report.csv"
OUTPUT_DIR = "output"

def open_browser_to_website(browser_type="chrome"):
    """Opens the browser and navigates to the website."""
    browser_lib = Selenium()
    browser_lib.open_browser(WEBSITE_URL, browser=browser_type)
    browser_lib.maximize_browser_window()
    return browser_lib

def navigate_to_employee_page(browser_lib: Selenium):
    """Navigates to the Employee Tasks page."""
    browser_lib.click_link("Employee Tasks")

def scrape_task_table(browser_lib: Selenium):
    """Scrapes the employee task table from the website."""
    print("Scraping Employee Task Table...")
    table_element = browser_lib.get_element(selector="css:section#employee-tasks table")
    header_row = browser_lib.get_element(selector="css:thead tr", parent=table_element)
    header_cells = browser_lib.get_elements(selector="css:th", parent=header_row)
    table_headers = [browser_lib.get_text(header_cell) for header_cell in header_cells]

    table_body = browser_lib.get_element(selector="css:tbody", parent=table_element)
    table_rows = browser_lib.get_elements(selector="css:tr", parent=table_body)
    employee_task_table = Tables().create_table(headers=table_headers)

    for row in table_rows:
        cells = browser_lib.get_elements(selector="xpath:./td", parent=row) # Using xpath for cells in row
        row_data = {}
        for index, header in enumerate(table_headers):
            cell = browser_lib.get_element(selector=f"xpath:./td[{index+1}]", parent=row) # More precise xpath
            cell_text = browser_lib.get_text(cell)
            row_data[header] = cell_text
        employee_task_table.add_row(row_data)

    print("Scraped Table Data:")
    Tables().log_table(employee_task_table)
    return employee_task_table

def generate_text_report_from_table(task_table):
    """Generates a text report from the scraped table data."""
    print("Generating Text Report...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_content = Tables().convert_table_to_string(task_table)
    with open(REPORT_FILE, "w") as f:
        f.write(report_content)
    print(f"Text report generated at: {REPORT_FILE}")

def generate_csv_report_from_table(task_table):
    """Generates a CSV report from the scraped table data."""
    print("Generating CSV Report...")
    Tables().table_to_csv(task_table, CSV_REPORT_FILE, header=True)
    print(f"CSV report generated at: {CSV_REPORT_FILE}")

def main():
    """Main function to run the RPA bot."""
    try:
        browser = open_browser_to_website()
        navigate_to_employee_page(browser)
        task_table_data = scrape_task_table(browser)
        generate_text_report_from_table(task_table_data)
        generate_csv_report_from_table(task_table_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'browser' in locals() and browser: # Check if browser was initialized
            browser.close_browser()

if __name__ == "__main__":
    main()