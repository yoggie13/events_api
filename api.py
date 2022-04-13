from crypt import methods
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)
# api = Api(app)


@app.route("/events", methods=['GET'])
def get_events():
    data = pd.read_csv("events_by_location.csv")
    locations = pd.read_csv('locations.csv')
    ret_data = pd.merge(how='left', left=data, left_on='loc_ID',
                            right=locations, right_on='loc_ID')

    ret_data = ret_data[["event_name",
                         "event_date", "event_link", "loc_name"]]
    ret_data = ret_data.to_dict('records')
    ret_data

    return {'data': ret_data}, 200


@app.route("/locations", methods=['GET'])
def get_locations():
    data = pd.read_csv("locations.csv")
    data = data.to_dict()
    return {'data': data}, 200


@app.route("/locations", methods=['POST'])
def add_location():
    parser = reqparse.RequestParser()

    parser.add_argument('id', required=True, location='args')
    parser.add_argument('name', required=True, location='args')
    parser.add_argument('link_part', required=True, location='args')
    args = parser.parse_args()

    new_data = pd.DataFrame({
        'loc_id': args['ID'],
        'loc_name': args['name'],
        'loc_link_part': args['link_part'],
        'locations': [[]]
    })

    new_data = new_data.iloc[:, :-1]

    data = pd.read_csv('locations.csv')
    data = data.append(new_data, ignore_index=True)
    data.to_csv('locations.csv', index=False)

    return {'data': data.to_dict()}, 200


# api.add_resource(Events, '/events')
# api.add_resource(Locations, '/locations')
if __name__ == '__main__':
    app.run()