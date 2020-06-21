import numpy as np


def sigma(volume):
    return 0.1


def time_by_scraps(volume):
    return 0.0003 * volume ** 3 - 0.0092 * volume ** 2 + 0.0882 * volume


def volume_by_capacity(capacity):
    mean_percentage = 0.7
    std_percentage = 0.4
    random = np.random.normal(
        capacity * mean_percentage, capacity * std_percentage)
    return min(capacity, random)


def time(volume):
    random = np.random.normal(time_by_scraps(volume), sigma(volume))
    return max(0, random)


class Point:
    def __init__(self, **kwargs):
        self.id = int(kwargs['id'])
        self.name = kwargs['namePoint'].strip()

        self.lat = float(kwargs['lat'])
        self.lon = float(kwargs['lon'])

        self.volume = volume_by_capacity(float(kwargs['volume']))
        self.time = time(self.volume)

    @property
    def coords(self):
        return {'lat': self.lat, 'lng': self.lon}

    def __repr__(self):
        return f"'({self.id}) {self.name}'"
