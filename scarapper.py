from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import requests

# Instantiate options
opts = Options()
# opts.add_argument(" — headless")  # Uncomment if the headless version needed
opts.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Set the location of the webdriver
chrome_driver = os.getcwd() + "/chromedriver.exe"

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

# Load the HTML page
driver.get("https://www.facebook.com/pg/barutanabeograd/events?ref=page_internal")

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source)

upcoming_events = soup.find("div", {"id": "upcoming_events_card"})
found = upcoming_events.find("div", {"class": "_p6a"})

while(found != None):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source)
    upcoming_events = soup.find("div", {"id": "upcoming_events_card"})
    found = upcoming_events.find("div", {"class": "_p6a"})

# print(soup.find(id="test").get_text())

# soup = BeautifulSoup(page.content, 'html.parser')


def returnIndex(month):
    return{
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }[month]


class Event:
    def __init__(self, name, date, link):
        self.name = name
        self.date = date
        self.link = link


events = []

divs = upcoming_events.find_all("div", {"class": "_24er"})

for div in divs:
    name = div.find("span", {"class": "_50f7"})
    name = name.text
    name = name.replace("  ", "")
    name = name.lstrip('\n')
    name = name.replace('\n', " & ")
    name = name.split(" | ", 1)[0]

    month = div.find("span", {"class": "_5a4-"})
    month = month.text
    month = returnIndex(month)

    day = div.find("span", {"class": "_5a4z"})
    day = day.text
    day = int(day)

    date = datetime(2022, month, day)

    link = div.find("div", {"class", "_4dmk"})
    link = "https://www.facebook.com" + link.a.get('href')

    obj = Event(name, date, link)

    events.append(obj)
    print(obj.name)
