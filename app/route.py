from flask_restful import Resource, reqparse
from heuristics.loop import loop
from heuristics.out_and_back import out_and_back
import random, json, time

class Route(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('type',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('latitude',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('longitude',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('distance',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self):
        """
        return 

        {
            "route": [
                {'lat': 1234, 'long': 5678},
                {'lat': 1234, 'long': 5678},
                {'lat': 1234, 'long': 5678}
            ]
        }
        """  

        data = Route.parser.parse_args()
        lat_long = (data['latitude'], data['longitude'])  # getting lat/long tuple
        distance = data['distance']
        # loop conditional
        if data['type'] == 0:
            paths = loop.create_route(lat_long, distance)
            # print(paths)
        elif data['type'] == 1:
            paths = out_and_back.create_route(lat_long, distance)
            # print(paths)
        else:
            return "Error, not a valid route type!"
        
        coordinates = random.choice(paths)
        # print(coordinates)
        routeData = []
        
        for coord in coordinates:
            routeData.append({"lat": coord[0], "lng": coord[1]})

        return {"route": routeData}, 400 
