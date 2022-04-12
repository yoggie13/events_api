from bs4 import BeautifulSoup

html_doc = open("index.html")

soup = BeautifulSoup(html_doc, 'html.parser')


class Event:
    def __init__(self, name, month, day, link):
        self.name = name
        self.month = month
        self.day = day
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

    day = div.find("span", {"class": "_5a4z"})
    day = day.text

    link = div.find("div", {"class", "_4dmk"})
    link = "https://www.facebook.com" + link.a.get('href')

    obj = Event(name, month, day, link)

    events.append(obj)
