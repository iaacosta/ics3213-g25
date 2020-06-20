from os import path
from classes import Truck, Point
import csv


def get_data_path(file_name):
    return path.join(path.abspath('.'), 'data', file_name)


def write_times_between(times_between):
    with open(get_data_path('times_matrix.csv'), 'w') as file:
        writer = csv.DictWriter(file, times_between[0].keys())

        writer.writeheader()
        for time_between in times_between:
            writer.writerow(time_between)


def read_times(file_name):
    times = {}

    with open(get_data_path(file_name)) as file:
        for row in csv.DictReader(file):
            origin_id = int(row['origin'])
            destination_id = int(row['destination'])
            value = float(row['time']) / 3600

            if times.get(origin_id):
                times[origin_id].update({destination_id: value})
            else:
                times[origin_id] = {destination_id: value}

    return times


def read_routes(file_name):
    trucks = {}

    with open(get_data_path(file_name)) as file:
        for row in csv.DictReader(file):
            if trucks.get(row['truck']):
                trucks[row['truck']].add_point(row['day'], row)
            else:
                trucks[row['truck']] = Truck(row['truck'])
                trucks[row['truck']].add_point(row['day'], row)

    return trucks
