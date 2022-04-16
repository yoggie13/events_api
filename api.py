from flask import Flask
from flask_restful import reqparse
from flask_cors import CORS
import pandas as pd
import csv
import loc_scrapper
import events_scrapper

app = Flask(__name__)
CORS(app)
# api = Api(app)


def get_events_func(param=None):
    data = pd.read_csv("events_test.csv")
    locations = pd.read_csv('locations.csv')
    ret_data = pd.merge(how='left', left=data, left_on='loc_ID',
                            right=locations, right_on='loc_ID')

    if param != None:
        ret_data = ret_data.loc[ret_data['loc_link_part'] == param]

    ret_data = ret_data[["event_name",
                         "event_date", "event_link", "event_pic_link", "loc_name"]]
    ret_data["event_date"] = pd.to_datetime(ret_data["event_date"])
    ret_data = ret_data.sort_values(by="event_date")

    return ret_data


@app.route("/events", methods=['GET'])
def get_events():
    parser = reqparse.RequestParser()

    parser.add_argument('filter', required=False, location='args')
    args = parser.parse_args()

    ret_data = get_events_func(args['filter']).to_dict('records')

    return {'data': ret_data}, 200


@app.route("/locations", methods=['GET'])
def get_locations():
    data = pd.read_csv("locations.csv")
    data = data.to_dict('records')
    return {'data': data}, 200


@app.route("/locations", methods=['POST'])
def add_location():
    parser = reqparse.RequestParser()

    parser.add_argument('link', required=True, location='args')
    args = parser.parse_args()

    name = loc_scrapper.scrape_loc(args['link'])

    link_part = args['link'].split(".facebook.com/")[1]
    link_part = link_part[0:-1]

    data = pd.read_csv('locations.csv')

    if 'Unnamed: 3' in data.columns:
        data = data.drop(['Unnamed: 3'], axis=1)

    id = 0

    if not data.empty:
        id = data.tail(1)['loc_ID']+1

    new_data = pd.DataFrame({
        'loc_ID': id,
        'loc_name': name,
        'loc_link_part': link_part,
        'locations': [[]]
    })

    new_data = new_data.iloc[:, :-1]

    data = data.append(new_data, ignore_index=True)
    data.to_csv('locations.csv', index=False)

    events = events_scrapper.scrape_events(
        new_data["loc_ID"].iloc[0], "https://www.facebook.com/pg/" + new_data["loc_link_part"].iloc[0] + "/events/?ref=page_internal")

    with open("events_test.csv", "a", newline='', encoding="utf-8") as stream:
        writer = csv.writer(stream)
        for event in events:
            writer.writerow(event)

    return {'data': data.to_dict('records')}, 200


# api.add_resource(Events, '/events')
# api.add_resource(Locations, '/locations')
if __name__ == '__main__':
    app.run()
