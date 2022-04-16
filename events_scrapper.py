from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
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


def getPic(_driver, link):
    _driver.get(link)
    soup = BeautifulSoup(_driver.page_source, "html.parser")
    pic = soup.find("img", {"data-imgperflogname": "profileCoverPhoto"})
    while(pic == None):
        soup = BeautifulSoup(_driver.page_source, "html.parser")
        pic = soup.find("img", {"data-imgperflogname": "profileCoverPhoto"})
    return pic['src']


def scrape_events(loc_id, link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(
        executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(soup)

    upcoming_events = soup.find("div", {"id": "upcoming_events_card"})

    loader = upcoming_events.find("div", {"class": "_p6a"})
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while(loader != None):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        upcoming_events = soup.find("div", {"id": "upcoming_events_card"})
        loader = upcoming_events.find("div", {"class": "_p6a"})

    events = []

    driver.execute_script(
        "let past = document.getElementById('past_events_card');" +
        "if(past !== undefined && past !== null) past.scrollIntoView(true);" +
        "else window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    upcoming_events = soup.find("div", {"id": "upcoming_events_card"})

    divs = upcoming_events.find_all("div", {"class": "_24er"})

    for id, div in enumerate(divs):
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

        obj = (loc_id, id, name, date, link, link_pic)

        events.append(obj)
    return events
