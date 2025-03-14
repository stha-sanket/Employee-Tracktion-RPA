# Employee Task Report Generator

## Description

This Python script automates the process of extracting employee task data from a local HTML page, analyzing the data for leave, overtime (hours > 8), and undertime (hours < 8), generating CSV reports for each category, and finally creating a PDF report with salary calculations based on the extracted data. It also includes functionality to automatically fill and submit a contact form on the website with summaries of leave, overtime, and undertime.

## Prerequisites

*   **Python 3.6+**: Ensure you have Python installed.
*   **Selenium**: Install using `pip install selenium`.
*   **ChromeDriver**:  Download the appropriate ChromeDriver version for your Chrome browser and place it in a location accessible to your system's PATH or specify the path in the script.
*   **Pandas**: Install using `pip install pandas`.
*   **ReportLab**: Install using `pip install reportlab`.
*   **Local HTML page**:  A locally served HTML file (`index.html`) containing the employee task data in a table format. The script is specifically designed to work with a specific HTML structure; modifications might be needed for different structures.

## Setup and Installation

1.  **Install Dependencies**:
    ```bash
    pip install selenium pandas reportlab
    ```

2.  **ChromeDriver**:
    *   Download the ChromeDriver executable from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) that matches your Chrome browser version.
    *   Place the `chromedriver` executable in a directory included in your system's PATH (e.g., `/usr/local/bin` on Linux/macOS) or explicitly specify the path to the executable when initializing the `webdriver.Chrome()` object.

3.  **HTML File**:
    *   Ensure you have the `index.html` file with the employee data table.  The script assumes this file is located at `http://127.0.0.1:5500/HTML/index.html`.  Adjust the URL if your file is served at a different address. The HTML structure is assumed to be as follows:
    *   A navigation menu with links to "Employee" and "Contact".
    *   An employee tasks section with the id "employee-tasks" containing a table.
    *   The table has a header row (`<tr>` with `<th>`) and subsequent data rows (`<tr>` with `<td>`).
    *   The table columns are assumed to be in the following order: Date, Task Listings, Time IN, Time OUT, Hours, Task Assigned.

4.  **Directory Structure:**
    Ensure you have a directory named `HTML` with `index.html` inside it if you're using the default URL.  Adjust the script if your HTML file is in a different location.

## Usage

1.  **Configuration**:
    *   **HTML Path**: Verify and adjust the `driver.get("http://127.0.0.1:5500/HTML/index.html")` line to point to the correct URL of your HTML file.
    *   **XPath expressions**:  Carefully inspect and adjust the XPath expressions for locating the elements on your HTML page if necessary. The script relies on very specific XPaths for the elements.  Use the browser's developer tools to inspect the HTML and obtain the correct XPaths.

2.  **Run the script**:

    ```bash
    python your_script_name.py
    ```

3.  **Review Output**:

    *   The script will:
        *   Open a Chrome browser and navigate to the specified HTML page.
        *   Extract employee task data from the table.
        *   Identify leave tasks, tasks with less than 8 hours (excluding 0 hours on Saturdays), and tasks with more than 8 hours.
        *   Print identified tasks to the console.
        *   Create CSV files: `employee_report.csv`, `leave_report.csv` (if leave tasks are found), `less_than_8_hours_report.csv` (if tasks with less than 8 hours are found), and `more_than_8_hours_report.csv` (if tasks with more than 8 hours are found).
        *   Generate a PDF report: `employee_report.pdf` including a salary summary (with leave deductions, overtime pay, and underwork deductions). The `employee_report.pdf` file includes employee information and salary summary.
        *   Fill and submit the contact form with summary information about leave, overtime, and underwork on the website
        *   Close the browser.

## Output Files

The script generates the following output files:

*   `employee_report.csv`: Contains all the extracted employee task data.
*   `leave_report.csv`: Contains only the rows where the task listing contains "leave".
*   `less_than_8_hours_report.csv`: Contains rows where the hours are less than 8, excluding entries where the hours is 0 on Saturday.
*   `more_than_8_hours_report.csv`: Contains rows where the hours are more than 8.
*   `employee_report.pdf`: A PDF document summarizing employee tasks, leave, underwork, overtime, and salary calculations.

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
*   **Implicit vs. Explicit Waits**: The script uses `time.sleep()` for waiting.  This is generally not recommended for robust Selenium automation. Consider using explicit waits (`WebDriverWait` with `expected_conditions`) for more reliable behavior.
*   **Headless Mode**: The script runs the Chrome browser in visible mode. You can run it in headless mode (without a visible browser window) by adding options to the `webdriver.Chrome()` initialization:
    ```python
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    ```
*   **Local Server**: The script assumes the HTML file is served locally. Ensure a local server (like Python's `http.server` or a web server like Apache or Nginx) is serving the file.
*   **Assumptions**: The script makes assumptions about the data in the table, such as the format of the date and the data type of the "Hours" column.
*   **User Interaction**:  The script is fully automated and does not require any user interaction once it is running.
*   **Security**: Exercise caution when running scripts that interact with web pages, especially if the pages contain sensitive information.

## Potential Improvements

*   **Robust Error Handling**: Implement more comprehensive error handling to catch potential exceptions and provide informative error messages.
*   **Explicit Waits**: Replace `time.sleep()` with explicit waits for more reliable element loading.
*   **Configuration File**: Use a configuration file to store settings like the HTML file path, output file names, and employee salary information.
*   **Logging**: Add logging to track the script's progress and any errors that occur.
*   **Command-Line Arguments**: Allow users to specify input parameters (e.g., HTML file path) through command-line arguments.
*   **Data Validation**: Implement data validation to ensure the extracted data is in the correct format.
*   **Dynamic Table Handling**: Make the script more adaptable to changes in the HTML table structure by using more flexible locators (e.g., using CSS selectors or relative XPaths).
*   **GUI**: Develop a graphical user interface (GUI) to make the script easier to use.
*   **Database Integration**: Store the extracted data in a database instead of CSV files.
*   **Email Integration**: Send the generated reports via email.
