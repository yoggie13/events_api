from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os


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


def writeEvents(events):
    with open("events_test.csv", "a", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        for index, event in enumerate(events):
            row = (1, index, event.name, event.date,
                   event.link, event.link_pic)
            writer.writerow(row)


def getPic(_driver, link):
    _driver.get(link)
    soup = BeautifulSoup(_driver.page_source)
    pic = soup.find("img", {"data-imgperflogname": "profileCoverPhoto"})
    while(pic == None):
        soup = BeautifulSoup(_driver.page_source)
        pic = soup.find("img", {"data-imgperflogname": "profileCoverPhoto"})
    return pic['src']


class Event:
    def __init__(self, name, date, link, link_pic):
        self.name = name
        self.date = date
        self.link = link
        self.link_pic = link_pic


# Instantiate options
# opts.add_argument(" — headless")  # Uncomment if the headless version needed

# Set the location of the webdriver
chrome_driver = os.getcwd() + "\chromedriver.exe"

# Instantiate a webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Load the HTML page
driver.get("https://www.facebook.com/pg/barutanabeograd/events?ref=page_internal")

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

upcoming_events = soup.find("div", {"id": "upcoming_events_card"})

found = upcoming_events.find("div", {"class": "_p6a"})
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

while(found != None):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source)
    upcoming_events = soup.find("div", {"id": "upcoming_events_card"})
    found = upcoming_events.find("div", {"class": "_p6a"})

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

    link_pic = getPic(driver, link)

    obj = Event(name, date, link, link_pic)

    events.append(obj)

writeEvents(events)
