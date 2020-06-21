import simpy


class SimulationTruck:
    def __init__(self, env, truck):
        self.truck = truck
        self.resource = simpy.Resource(env)

        # Statistics relative to truck capacity
        self.trips = 1
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

        if (self.current_load >= self.truck.capacity):
            overcap = self.current_load // self.truck.capacity
            self.current_load -= self.truck.capacity * overcap
            self.unloaded += self.truck.capacity * overcap
            self.trips += int(overcap)
