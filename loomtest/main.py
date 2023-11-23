from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Environment variables for Azure OpenAI
AZURE_OPENAI_VERSION = os.environ.get("AZURE_OPENAI_VERSION", None)
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", None)
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Define a Pydantic model for the request body


class ProductData(BaseModel):
    product_title: str
    product_url: HttpUrl


# Create an instance of FastAPI
app = FastAPI()


def get_html_from_url(product_url):
    # Convert HttpUrl to string
    url = str(product_url)

    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Instantiate the WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load and for the element to be present
    time.sleep(5)

    try:
        # Find the span with the specified ID
        product_description_element = driver.find_element(
            By.ID, "productDescription")
        product_description = product_description_element.text
    except Exception as e:
        print(f"Error finding element: {e}")
        product_description = ""

    # Close the browser
    driver.quit()

    return product_description


def azure_openai_llm_handler(messages: list, stream: bool = False):
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_VERSION,
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        stream=stream
    )

    if stream:
        return async_wrapper(response)
    else:
        return response


async def generate_product_description(product_title, page_html):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Product Title: {product_title}\nSimilar Product Description: {page_html}\n\ngiven the following created title and a similar product's description, can you make a new product description?"}
    ]

    response = azure_openai_llm_handler(messages)
    if response.choices:
        # print(response.choices[0], flush=True)
        return response.choices[0].message.content.strip()
    else:
        return "No description generated."

# Define a route that handles POST requests


@app.post("/submit_product/")
async def submit_product(product_data: ProductData):
    # Use Selenium to get HTML from the product URL
    product_html = get_html_from_url(product_data.product_url)

    # Generate a product description using OpenAI
    product_description = await generate_product_description(product_data.product_title, product_html)

    return {
        "Product Title": product_data.product_title,
        "Generated Description": product_description
    }

# Define the main entry point for running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
