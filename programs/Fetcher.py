from services import GoogleMapsHelper
from helpers import read_routes, write_times_between


class Fetcher:
    def __init__(self, file_path):
        self.google_maps = GoogleMapsHelper()
        self.trucks = read_routes(file_path)

    def run(self):
        self.create_matrix()

    def create_matrix(self):
        times = []

        for truck in list(self.trucks.values()):
            truck_times = truck.compute_route_times(self.google_maps)
            for route_times in truck_times.values():
                for time in route_times:
                    times.append(time)

        write_times_between(times)
