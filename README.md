# Employee Task Report Generator

## Description

This Python script automates the process of extracting employee task data from a local HTML page, analyzing the data for leave, overtime (hours > 8), and undertime (hours < 8), generating CSV reports, and finally creating a PDF report with salary calculations based on the extracted data. It also includes functionality to automatically fill and submit a contact form on the website with summaries of leave, overtime, and undertime.

## Prerequisites

*   **Python 3.6+**: Ensure you have Python installed.
*   **Selenium**: Install using `pip install selenium`.
*   **Pandas**: Install using `pip install pandas`.
*   **ReportLab**: Install using `pip install reportlab`.
*   **Local HTML page**:  A locally served HTML file (`index.html`) containing the employee task data in a table format. The script is specifically designed to work with a specific HTML structure; modifications might be needed for different structures.
*   use this script to download my requirement:
*   **Install Dependencies**:
    ```bash
    pip install selenium pandas reportlab
    pip install -r requirements.txt

    ```
## Setup and Installation

1.  **Install Dependencies**:
    ```bash
    pip install selenium pandas reportlab
    ```

2.  **HTML File**:
    *   Ensure you have the `index.html` file with the employee data table.  The script assumes this file is located at `http://127.0.0.1:5500/HTML/index.html`.  Adjust the URL if your file is served at a different address, do this by hosting a live server in VS-code for index.html then copying it and pasting in the main code. The HTML structure is assumed to be as follows:
    *   A navigation menu with links to "Employee" and "Contact".
    *   An employee tasks section with the id "employee-tasks" containing a table.
    *   The table has a header row (`<tr>` with `<th>`) and subsequent data rows (`<tr>` with `<td>`).
    *   The table columns are assumed to be in the following order: Date, Task Listings, Time IN, Time OUT, Hours, Task Assigned.

3.  **Directory Structure:**
    Ensure you have a directory named `HTML` with `index.html` inside it if you're using the default URL.  Adjust the script if your HTML file is in a different location.

## Usage

1.  **Configuration**:
    *   **HTML Path**: Verify and adjust the `driver.get("http://127.0.0.1:5500/HTML/index.html")` line to point to the correct URL of your HTML file.
    *   **XPath expressions**:  Carefully inspect and adjust the XPath expressions for locating the elements on your HTML page if necessary. The script relies on very specific XPaths for the elements.  Use the browser's developer tools to inspect the HTML and obtain the correct XPaths.

2.  **Run the script**:

    ```bash
    python real.py # or your script name based on what you want to change the name of the python file
    ```

3.  **Review Output**:

    *   The script will:
        *   Open a Chrome browser and navigate to the specified HTML page.
        *   Extract employee task data from the table.
        *   Identify leave tasks, tasks with less than 8 hours (excluding 0 hours on Saturdays), and tasks with more than 8 hours.
        *   Print identified tasks to the console.
        *   Create CSV files: `employee_report.csv`, `leave_report.csv` (if leave tasks are found).
        *   Generate a PDF report: `employee_report.pdf` including a salary summary (with leave deductions, overtime pay, and underwork deductions). The `employee_report.pdf` file includes employee information and salary summary.
        *   Fill and submit the contact form with summary information about leave, overtime, and underwork on the website
        *   Close the browser.

## Output Files

The script generates the following output files:

*   `employee_report.csv`: Contains all the extracted employee task data.
*   `leave_report.csv`: Contains only the rows where the task listing contains "leave".
*   `employee_report.pdf`: A PDF document summarizing employee tasks, leave, underwork, overtime, and salary calculations.

## Outpur for Contact form
- use `F12` in your keyboard or use `inspect` to open `developer tools`
- expand or lookout for `application tab` there
- after that look for `local storage`, here you can see the `data stored` in the contact page
  
## Code Explanation

*   **Selenium Webdriver**: Used to automate browser interactions.  It navigates to the HTML page, locates elements (buttons, tables, form fields), and performs actions (clicks, data extraction, form filling, submissions).
*   **Pandas**: Used for data manipulation and creating CSV files.
*   **ReportLab**: Used to generate the PDF report.  It allows creating text, paragraphs, and other elements on a PDF canvas.
*   **Data Extraction**: Extracts data from the HTML table using Selenium's `find_element` and `find_elements` methods.
*   **Data Analysis**: Iterates through the extracted data to identify leave tasks, tasks with less than 8 hours, and tasks with more than 8 hours.
*   **Report Generation**: Creates CSV files using Pandas DataFrames.  Creates the PDF report using ReportLab.
*   **Contact Form Automation**: Locates the contact form elements using XPaths, fills the fields with summary messages, and submits the form.
*   **Error Handling**: Basic error handling is implemented to catch `ValueError` exceptions that might occur when converting the "Hours" column to a float or parsing the date. This will prevent the script from crashing if there is invalid data in the table.  It also includes a `try...except...finally` block around the contact form filling and submission to ensure the browser goes back even if an error occurs.

## Important Considerations

*   **XPath Stability**: The script relies heavily on XPath expressions. Changes to the HTML structure of your `index.html` file will likely break the script. Always inspect and update the XPaths if the HTML structure is modified.
*   **HTML Structure**: The script is written for a specific HTML structure. If your HTML table has a different structure, you'll need to modify the script to correctly locate the table, rows, and columns.
*   **Error Handling**: The script has some basic error handling, but it could be improved to handle more potential errors, such as network issues, incorrect data formats, or missing elements on the page.
*   **Local Server**: The script assumes the HTML file is served locally. Ensure a local server (like Python's `http.server` or a web server like Apache or Nginx) is serving the file.
*   **Assumptions**: The script makes assumptions about the data in the table, such as the format of the date and the data type of the "Hours" column.
*   **User Interaction**:  The script is fully automated and does not require any user interaction once it is running.
*   **Security**: Exercise caution when running scripts that interact with web pages, especially if the pages contain sensitive information.
