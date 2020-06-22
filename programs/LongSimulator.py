import pandas as pd
from .Simulator import Simulator


def gen():
    i = 0
    while True:
        yield i
        i += 1


class LongSimulator:
    idx = gen()

    def __init__(self, day, routes_file_path, trucks_file_path, iterations=1000):
        self.iterations = iterations
        self.day = day
        self.routes_file_path = routes_file_path
        self.trucks_file_path = trucks_file_path

        self.times = {}
        self.capacities = {}
        self.collected_wastes = {}
        self.trips = {}
        self.load_times = {}
        self.transit_times = {}

        self.data = []

    def run(self):
        for i in range(self.iterations):
            simulation = Simulator(self.day,
                                   self.routes_file_path,
                                   self.trucks_file_path,
                                   False, False)

            simulation.run()

            for sim_truck in simulation.simulation_trucks.values():
                truck = sim_truck.truck

                if self.capacities.get(truck.id) is None:
                    self.capacities[truck.id] = truck.capacity

                self.data.append({
                    'simulation_id': next(LongSimulator.idx),
                    'truck': truck.id,
                    'simulation_time': sim_truck.finished,
                    'total_load': sim_truck.current_load + sim_truck.unloaded,
                    'trips': sim_truck.trips,
                    'load_time': sim_truck.unload_time,
                    'transit_time': sim_truck.transit_time,
                })

        return self.data
