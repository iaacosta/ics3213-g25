from programs import Simulator, Fetcher
from helpers import week_day

ROUTES_PATH = 'routes.csv'
TRUCKS_PATH = 'trucks.csv'

if __name__ == '__main__':
    """ Fetch new routes """
    # fetcher = Fetcher(ROUTES_PATH)
    # fetcher.run()

    """ Simulator """
    for idx in range(5):
        day = str(idx)
        print(f'\n----------------\n{week_day(day)}\n----------------')
        simulator = Simulator(day, ROUTES_PATH, TRUCKS_PATH, should_log=False)
        simulator.run()
