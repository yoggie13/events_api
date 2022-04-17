from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import csv
import os


def scrape_loc(url):
    load_dotenv()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    print(os.environ.get("CHROMEDRIVER_PATH"))

    driver = webdriver.Chrome(service=Service(
        executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
    driver.get(url)

    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    name = soup.find("h1", {"class": "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"})

    while(name == None):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        name = soup.find(
            "h1", {"class": "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"})

    return name.text
