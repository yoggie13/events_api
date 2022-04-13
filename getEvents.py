from datetime import datetime
from bs4 import BeautifulSoup

html_doc = open("index.html")

soup = BeautifulSoup(html_doc, 'html.parser')


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

divs = soup.find_all("div", {"class": "_24er"})

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
