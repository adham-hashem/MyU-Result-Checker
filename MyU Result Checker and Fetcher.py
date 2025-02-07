# MyU credentials (Replace them with your own credentials)
MyU_username = ""
MyU_password = ""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Uncomment the following lines if you want to see what is going in the background in the browser window

# # Configure Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (helps in some cases)
# chrome_options.add_argument("--window-size=1920x1080")  # Optional: Set window size for proper element detection
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection as a bot

# # Setup WebDriver
# driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome()

# Open MyU website
driver.get("https://myu.mans.edu.eg/")
print("Opened MyU website")

wait = WebDriverWait(driver, 20)

# Enter username
username_input = wait.until(EC.presence_of_element_located((By.NAME, "txtUserName")))
username_input.send_keys(f"{MyU_username}")
print("Entered username")

# Enter password
password_input = driver.find_element(By.NAME, "txtPassword")
password_input.send_keys(f"{MyU_password}")
print("Entered password")

# Click the login button
login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ls-dark-btn")))
login_button.click()
print("Clicked login button")

# Wait for login to complete
time.sleep(5)

# Click on "النتائج الدراسية"
results_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@appid='4']")))
driver.execute_script("arguments[0].click();", results_button)  # JavaScript click to bypass restrictions
print("Navigated to 'النتائج الدراسية' page")

# Wait for the first table to load
first_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

# Get all rows from the first table
rows = first_table.find_elements(By.TAG_NAME, "tr")

# Flag to check if results appeared
results_found = False

# Extract values from the fourth and fifth columns if they exist
for row in rows:
    tds = row.find_elements(By.TAG_NAME, "td")  # Get all <td> elements in the row
    if len(tds) >= 5:  # Ensure there are at least 5 columns
        first_td = tds[0].text.strip()
        second_td = tds[1].text.strip()
        third_td = tds[2].text.strip()
        fourth_td = tds[3].text.strip()
        fifth_td = tds[4].text.strip()

        if fourth_td and fifth_td:  # Check if both have values
            if not results_found:
                print("\n✅ The result appeared:")
                results_found = True
            print(f"📌 Subject Name: {second_td}, Hours: {third_td}, Grade: {fourth_td}, Letter: {fifth_td}")

# If no results were found, print a warning message
if not results_found:
    print("\n⚠️ The result did not appear yet.")

# Uncomment the following lines if you want the browser window be not closed automatically

# # Keep browser open for review
# print("\nProcess completed. The browser will remain open.")
# input("Press Enter to close the browser...")

# Close the browser
driver.quit()
print("\nProcess completed (Headless Mode).")
