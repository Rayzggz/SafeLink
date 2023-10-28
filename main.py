from data import parse_data
from prediction import Prediction
from extern import Communication, Indicator
from data import RoadEngager
from config import UUID, FRAME_RATE

if __name__ == "__main__":
    print("start")
    # car, map1 = parse_data('data/sample_car.json', 'data/sample_map.json')

    a = Prediction()
    conn = Communication()
    conn.start()
    indicator = Indicator()
    indicator.start()

    while not indicator.is_shutdown():
        curr = indicator.get_position()
        motion = indicator.get_motion()
        conn.brocast(RoadEngager(curr, motion, UUID))
        engagers = conn.recv(1/FRAME_RATE)
        a.update_engager(engagers)
        re = a.predict()
        pass

    print(a)

