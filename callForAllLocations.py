import pandas as pd

locations = pd.read_csv("locations.csv")


def function():
    for location in locations["loc_link_part"]:
        link = "https://www.facebook.com/pg/" + location + "/events/?ref=page_internal"
