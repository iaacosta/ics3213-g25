import numpy as np


def time_by_capacity(capacity):
    return 0.0003 * capacity ** 3 - 0.0092 * capacity ** 2 + 0.0882 * capacity


class Point:
    def __init__(self, **kwargs):
        self.id = int(kwargs['id'])
        self.name = kwargs['name'].strip()

        self.lat = float(kwargs['lat'])
        self.lon = float(kwargs['lon'])

        if kwargs.get('volume'):
            self.capacity = float(kwargs['volume'])
        else:
            self.capacity = 0.0

        self.time = max(0, np.random.normal(
            time_by_capacity(self.capacity), 0.1))

    @property
    def coords(self):
        return {'lat': self.lat, 'lng': self.lon}

    def __repr__(self):
        return f"'({self.id}) {self.name}'"
