import os
import googlemaps
from datetime import datetime
from classes import Point


class GoogleMapsHelper:
    def __init__(self):
        self.client = googlemaps.Client(key=os.environ['GOOGLE_API_KEY'])

    def time_between_points(self, origin, destination, unit='hours'):
        now = datetime.now()

        directions = self.client.directions(origin.coords, destination.coords,
                                            mode="transit", departure_time=now)

        if unit == 'hours':
            factor = 3600
        elif unit == 'minutes':
            factor = 60
        else:
            factor = 1

        return directions[0]['legs'][0]['duration']['value'] / factor
