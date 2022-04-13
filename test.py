import pandas as pd

data = pd.read_csv("events_by_location.csv")
locations = pd.read_csv('locations.csv')
ret_data = pd.merge(how='left', left=data, left_on='loc_ID',
                    right=locations, right_on='loc_ID')

ret_data = ret_data[["event_name",
                     "event_date", "event_link", "loc_name"]]
ret_data = ret_data.to_dict('records')
ret_data
