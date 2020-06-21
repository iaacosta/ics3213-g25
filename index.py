from programs import Simulator, Fetcher
from helpers import week_day

DATA_PATH = 'rutas_por_dia_por_camion.csv'

if __name__ == '__main__':
    """ Fetch new routes """
    # fetcher = Fetcher(DATA_PATH)
    # fetcher.run()

    """ Simulator """
    for idx in range(5):
        day = str(idx)
        print(f'\n----------------\n{week_day(day)}\n----------------')
        simulator = Simulator(day, DATA_PATH)
        simulator.run()
