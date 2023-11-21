import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

username = os.environ.get('LINKEDIN_USER')
password = os.environ.get('LINKEDIN_PW')
linkedin_jobs_url = os.environ.get('LINKEDIN_JOBS_URL')

driver = webdriver.Chrome()

driver.get("https://www.linkedin.com")

wait = WebDriverWait(driver, 10)

username_field = wait.until(
    EC.visibility_of_element_located((By.ID, 'session_key')))
username_field.send_keys(username)

password_field = wait.until(
    EC.visibility_of_element_located((By.ID, 'session_password')))
password_field.send_keys(password)

sign_in_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[@type="submit"]')))
sign_in_button.click()

driver.get(linkedin_jobs_url)


driver.quit()
