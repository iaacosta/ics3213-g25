import simpy
from classes import SimulationTruck
from helpers import read_routes, read_times, read_capacities

TAB = '  '


class Simulator:
    def __init__(self, day, routes_file_path,
                 trucks_file_path, should_event_log=True,
                 should_global_log=True):
        self.day = day
        self.should_event_log = should_event_log
        self.should_global_log = should_global_log
        self.env = simpy.Environment()
        self.times = {}
        self.simulation_trucks = {}

        self.read(routes_file_path, trucks_file_path)

    def read(self, routes_file_path, trucks_file_path):
        self.times = read_times()
        original_trucks = read_routes(routes_file_path)
        read_capacities(trucks_file_path, original_trucks)
        self.simulation_trucks = dict(map(
            lambda truck: (truck.id, SimulationTruck(self.env, truck)),
            original_trucks.values()
        ))

    def raw_log(self, message, n_tabs=0):
        if not self.should_global_log:
            return

        print(f'{TAB*n_tabs} {message}')

    def event_log(self, message):
        if not self.should_event_log:
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
                                      current_point.volume)

                self.event_log(
                    f'Camión {truck.id} termina trabajo en {current_point.name}')

                # Process in route
                if next_point:
                    self.event_log(
                        f'Camión {truck.id} viaja de {current_point.name} a {next_point.name}')

                    trip_time = self.times[current_point.id][next_point.id]

                    yield self.env.timeout(trip_time)
                    simulation_truck.transit(trip_time)

        simulation_truck.finished = self.env.now
        self.event_log(f'Camión {truck.id} vuelve a municipalidad')

    def log_statistics(self):
        self.raw_log('------------', 1)
        self.raw_log('Estadísticas', 1)
        self.raw_log('------------\n', 1)

        self.raw_log(
            f'TIEMPO TOTAL DE SIMULACIÓN (hrs): {self.env.now:.3f}\n', 2)

        for sim_truck in self.simulation_trucks.values():
            truck = sim_truck.truck
            self.raw_log(f'Camión {truck.id}', 2)

            if not self.route_defined(truck) or len(truck.routes[self.day].points) == 0:
                self.raw_log('Sin rutas', 3)
                self.raw_log('')
                continue

            self.raw_log(
                f'Capacidad (m3): {sim_truck.truck.capacity}', 3)

            self.raw_log(
                f'Cantidad recolectada (m3): {(sim_truck.current_load + sim_truck.unloaded):.3f}', 3)

            self.raw_log(
                f'Cantidad de viajes: {sim_truck.trips}', 3)

            self.raw_log(
                f'Tiempo en descarga (hrs): {sim_truck.unload_time:.3f}', 3)

            self.raw_log(
                f'Tiempo en tránsito (hrs): {sim_truck.transit_time:.3f}', 3)

            self.raw_log('')

    def run(self):
        self.env.process(self.simulate_trucks())
        self.env.run()
        self.log_statistics()
