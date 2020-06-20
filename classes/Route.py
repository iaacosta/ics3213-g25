from .Point import Point


class Route:
    def __init__(self, _id, *points):
        self.id = _id
        self.points = []

        for point in points:
            self.add_point(point)

    def add_point(self, point):
        self.points.append(Point(**point))

    def compute_times(self, service):
        times = []

        for idx in range(len(self.points) - 1):
            origin = self.points[idx]
            destination = self.points[idx + 1]

            times.append({
                'origin': origin.id,
                'destination': destination.id,
                'time': int(service.time_between_points(origin, destination, unit='seconds'))
            })

        return times
