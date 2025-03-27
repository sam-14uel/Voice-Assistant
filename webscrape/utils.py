import requests
from bs4 import BeautifulSoup



from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

from urllib.parse import urljoin, urlparse

from ai_agent.utils import generate_ai_response



def scrape_website(website):
    print("Launching Chrome Browser...")
    chrome_driver_path = "./chromedriver.exe"
    options =  webdriver.ChromeOptions()
    driver =  webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    try:
        driver.get(website)
        print("Page loaded...")

        html = driver.page_source
        return html

    finally:
        driver.quit()
    


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


# Define the parsing prompt template.
TEMPLATE = (
    "You are tasked with extracting specific information from the following text content: {dom_content}.\n"
    "Please follow these instructions carefully:\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_huggingface(dom_chunks, parse_description):
    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        # Compose the prompt by merging the DOM chunk with the parse description.
        prompt = TEMPLATE.format(dom_content=chunk, parse_description=parse_description)
        # Generate the AI response using the Hugging Face model.
        response = generate_ai_response(prompt)
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)
    return "\n".join(parsed_results)


