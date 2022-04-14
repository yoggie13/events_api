import pandas as pd
import csv
import events_scrapper


def writeEvents(events):
    with open("events_test.csv", "w", newline='', encoding="utf-8") as stream:
        writer = csv.writer(stream)
        row = ("loc_ID", "event_ID", "event_name",
               "event_date", "event_link", "event_pic_link")
        writer.writerow(row)
        for event in events:
            writer.writerow(event)


locations = pd.read_csv('locations.csv')
events = []

for loc in locations.to_numpy():
    events += events_scrapper.scrape_events(
        loc[0], "https://www.facebook.com/pg/" + loc[2] + "/events/?ref=page_internal")

writeEvents(events)
