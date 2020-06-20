import simpy
from classes import Truck, Point, Route
from services import GoogleMapsHelper
from helpers import week_day, read_routes, read_times


class Simulator:
    def __init__(self, trucks_file_path, times_file_path='times_matrix.csv'):
        self.env = simpy.Environment()
        self.google_maps = GoogleMapsHelper()
        self.trucks = read_routes(trucks_file_path)
        self.times = read_times(times_file_path)

        self.resources = dict([(truck.id, simpy.Resource(self.env, 1))
                               for truck in self.trucks.values()])

    def log(self, message):
        print(f'[t={self.env.now * 60:.2f}] {message}')

    def simulate_trucks(self):
        for truck in self.trucks.values():
            c = self.simulate_routes(truck)
            self.env.process(c)
            yield self.env.timeout(0)

    def simulate_routes(self, truck):
        arrive = self.env.now
        self.log(f'Camión {truck.id} comenzó el día')

        for route in truck.routes.values():
            self.log(
                f'Camión {truck.id} comienza ruta día {week_day(route.id)}')
            for idx in range(len(route.points)):
                current_point = route.points[idx]

                if idx < len(route.points) - 1:
                    next_point = route.points[idx + 1]
                else:
                    next_point = None

                with self.resources[truck.id].request() as request_truck:
                    results = yield request_truck

                    # Time in point
                    yield self.env.timeout(current_point.time)
                    # Time in route
                    if next_point:
                        yield self.env.timeout(1)

                    self.log(
                        f'Camión {truck.id} pasó por punto {current_point.name}')

    def run(self):
        self.env.process(self.simulate_trucks())
        self.env.run()
