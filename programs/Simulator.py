import simpy
from classes import Truck, Point, Route
from services import GoogleMapsHelper
from helpers import week_day, read_routes, read_times


class Simulator:
    def __init__(self, day, trucks_file_path, times_file_path='times_matrix.csv'):
        self.day = day
        self.env = simpy.Environment()
        self.trucks = read_routes(trucks_file_path)
        self.times = read_times(times_file_path)

        self.resources = dict([(truck.id, simpy.Resource(self.env, 1))
                               for truck in self.trucks.values()])

    def log(self, message):
        print(f'[t={self.env.now:.2f}] {message}')

    def simulate_trucks(self):
        for truck in self.trucks.values():
            all_routes = self.simulate_routes(truck)
            self.env.process(all_routes)
            yield self.env.timeout(0)

    def simulate_routes(self, truck):
        try:
            route = truck.routes[self.day]
        except KeyError:
            return

        arrive = self.env.now

        self.log(f'Camión {truck.id} comienza ruta')

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
                self.log(
                    f'Camión {truck.id} pasó por punto {current_point.name}')

                # Time in route
                if next_point:
                    self.log(
                        f'Camión viaja de {current_point.name} a {next_point.name}')
                    yield self.env.timeout(self.times[current_point.id][next_point.id])

        self.log(f'Camión vuelve a municipalidad')

    def run(self):
        self.env.process(self.simulate_trucks())
        self.env.run()
