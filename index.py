from sys import exit
import argparse
from programs import Simulator, Fetcher, LongSimulator
from helpers import week_day

ROUTES_PATH = 'original_routes.csv'
TRUCKS_PATH = 'trucks.csv'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    simulate = parser.add_subparsers()
    simulate_parser = simulate.add_parser('simulate')
    fetch_parser = simulate.add_parser('fetch')
    simulate_parser.add_argument('--log', help='whether to log events',
                                 dest='log', action='store_true',
                                 default=False, required=False)
    simulate_parser.add_argument('--file', help='file name, should be in data directory',
                                 default=ROUTES_PATH, required=False)
    simulate_parser.set_defaults(which='simulate')
    fetch_parser.set_defaults(which='fetch')

    args = parser.parse_args()
    if args.which == 'simulate':
        """ Simulator """
        for idx in range(5):
            day = str(idx)
            print(f'\n----------------\n{week_day(day)}\n----------------')
            simulator = Simulator(day, args.file,
                                  TRUCKS_PATH, should_event_log=args.log)
            simulator.run()
    elif args.which == 'fetch':
        """ Fetch new routes """
        fetcher = Fetcher(ROUTES_PATH)
        fetcher.run()
