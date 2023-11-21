import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

load_dotenv()

# Retrieve credentials from environment variables
username = os.environ.get('LINKEDIN_USER')
password = os.environ.get('LINKEDIN_PW')
linkedin_jobs_url = os.environ.get('LINKEDIN_JOBS_URL')

# Initialize the WebDriver (Chrome in this case)
driver = webdriver.Chrome()

# Open LinkedIn
driver.get("https://www.linkedin.com")

# Wait for the login page to load
time.sleep(2)

# Find the username field and enter the username
username_field = driver.find_element(By.ID, 'session_key')
username_field.send_keys(username)

# Find the password field and enter the password
password_field = driver.find_element(By.ID, 'session_password')
password_field.send_keys(password)

# Find the sign-in button and click it
sign_in_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
sign_in_button.click()

# Wait for the main page to load
time.sleep(5)

# Navigate to the 'Jobs' section
driver.get(linkedin_jobs_url)
# Add additional code here to interact with the jobs page

# Close the browser after a delay
time.sleep(5)
driver.quit()
