import pandas as pd

data = pd.read_csv("events_test.csv")
locations = pd.read_csv('locations.csv')
ret_data = pd.merge(how='left', left=data, left_on='loc_ID',
                    right=locations, right_on='loc_ID')

ret_data = ret_data.loc[ret_data['loc_link_part'] == "DorcolPlatz"]

ret_data = ret_data[["event_name",
                     "event_date", "event_link", "event_pic_link", "loc_name"]]
ret_data["event_date"] = pd.to_datetime(ret_data["event_date"])
ret_data = ret_data[""]
ret_data = ret_data.sort_values(by="event_date")
ret_data = ret_data.to_dict('records')

ret_data
