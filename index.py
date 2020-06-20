from programs import Simulator
from helpers import week_day

if __name__ == '__main__':
    for idx in range(5):
        day = str(idx)
        print(f'\n----------------\n{week_day(day)}\n----------------')
        simulator = Simulator(day, 'rutas_por_dia_por_camion.csv')
        simulator.run()
