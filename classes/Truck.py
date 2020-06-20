from .Route import Route


class Truck:
    def __init__(self, _id):
        self.id = int(_id)
        self.routes = {}

    def add_point(self, route_id, point):
        if self.routes.get(route_id):
            self.routes[route_id].add_point(point)
        else:
            self.routes[route_id] = Route(route_id, point)

    def compute_route_times(self, service):
        times = {}

        for route in list(self.routes.values()):
            times[route.id] = route.compute_times(service)

        return times
