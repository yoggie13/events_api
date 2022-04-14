
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os


def scrape_loc(url):
    # Instantiate a webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Load the HTML page
    driver.get(url)

    # Parse processed webpage with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    name = soup.find("h1", {"class": "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"})

    while(name == None):
        name = soup.find(
            "h1", {"class": "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"})

    return name.text
