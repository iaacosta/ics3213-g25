import simpy
from classes import Truck, Point, Route
from services import GoogleMapsHelper
from helpers import week_day, read_routes, read_times

TAB = '  '


class SimulationTruck:
    def __init__(self, env, truck):
        self.truck = truck
        self.resource = simpy.Resource(env)

        # Statistics relative to truck capacity
        self.fills = 0
        self.current_load = 0
        self.unloaded = 0

        # Statistics relative to time on transit and working
        self.transit_time = 0
        self.unload_time = 0

    def transit(self, time):
        self.transit_time += time

    def load(self, time, load):
        self.unload_time += time
        self.current_load += load

        if (self.current_load >= 40):
            self.unloaded += self.current_load
            self.current_load = 0
            self.fills += 1


class Simulator:
    def __init__(self, day, trucks_file_path, should_log=True):
        self.day = day
        self.should_log = should_log
        self.env = simpy.Environment()
        self.times = read_times()

        original_trucks = read_routes(trucks_file_path)
        self.simulation_trucks = dict(map(
            lambda truck: (truck.id, SimulationTruck(self.env, truck)),
            original_trucks.values()
        ))

    def raw_log(self, message, n_tabs=0):
        print(f'{TAB*n_tabs} {message}')

    def event_log(self, message):
        if not self.should_log:
            return

        self.raw_log(f'[t={self.env.now:.2f}] {message}', 1)

    def simulate_trucks(self):
        for simulation_truck in self.simulation_trucks.values():
            all_routes = self.simulate_routes(simulation_truck)
            self.env.process(all_routes)
            yield self.env.timeout(0)

    def route_defined(self, truck):
        try:
            truck.routes[self.day]
            return True
        except KeyError:
            return False

    def simulate_routes(self, simulation_truck):
        truck = simulation_truck.truck

        if not self.route_defined(truck):
            return

        route = truck.routes[self.day]
        arrive = self.env.now

        self.event_log(f'Camión {truck.id} comienza ruta')

        for idx in range(len(route.points)):
            current_point = route.points[idx]

            if idx < len(route.points) - 1:
                next_point = route.points[idx + 1]
            else:
                next_point = None

            with simulation_truck.resource.request() as request_truck:
                # Wait if truck is being used (for making each point sequential)
                results = yield request_truck

                # Process in point
                self.event_log(
                    f'Camión {truck.id} comienza trabajo en {current_point.name}')

                yield self.env.timeout(current_point.time)
                simulation_truck.load(current_point.time,
                                      current_point.capacity)

                self.event_log(
                    f'Camión {truck.id} termina trabajo en {current_point.name}')

                # Process in route
                if next_point:
                    self.event_log(
                        f'Camión {truck.id} viaja de {current_point.name} a {next_point.name}')

                    trip_time = self.times[current_point.id][next_point.id]

                    yield self.env.timeout(trip_time)
                    simulation_truck.transit(trip_time)

        self.event_log(f'Camión {truck.id} vuelve a municipalidad')

    def log_statistics(self):
        self.raw_log('------------', 1)
        self.raw_log('Estadísticas', 1)
        self.raw_log('------------\n', 1)

        self.raw_log(
            f'TIEMPO TOTAL DE SIMULACIÓN - {self.env.now:.3f}hrs\n', 2)

        for sim_truck in self.simulation_trucks.values():
            truck = sim_truck.truck
            self.raw_log(f'Camión {truck.id}', 2)

            if not self.route_defined(truck) or len(truck.routes[self.day].points) == 0:
                self.raw_log('Sin rutas', 3)
                print()
                continue

            self.raw_log(
                f'Cantidad de veces que sobrepasó su capacidad: {sim_truck.fills}', 3)

            self.raw_log(
                f'Tiempo en descarga: {sim_truck.unload_time:.3f}hrs', 3)

            self.raw_log(
                f'Tiempo en tránsito: {sim_truck.transit_time:.3f}hrs', 3)

            print()

    def run(self):
        self.env.process(self.simulate_trucks())
        self.env.run()
        self.log_statistics()
