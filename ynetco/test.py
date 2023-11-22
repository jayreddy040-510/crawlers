from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def get_article_links():
    # Set up Chrome options
    chrome_options = Options()
    # Run in headless mode if you don't need a browser UI
    chrome_options.add_argument("--headless")

    # Initialize the ChromeDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Go to the specified website
        driver.get("https://www.ynet.co.il/news")

        # Wait for the page to load
        time.sleep(5)

        # Find all <a> tags
        all_links = driver.find_elements(By.TAG_NAME, "a")

        # Filter links that contain the specified base URL and ensure href is not None
        article_links = {
            link.get_attribute('href') for link in all_links
            if link.get_attribute('href') and 'https://www.ynet.co.il/news/article/' in link.get_attribute('href')
        }

        return article_links

    finally:
        # Close the browser
        driver.quit()


# Example usage
article_links = get_article_links()
print(article_links)
