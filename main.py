from data import parse_data
from prediction import Prediction
from extern import Communication, Indicator
from data import RoadEngager
from config import UUID, FRAME_RATE, CACHE_PATH
from map import MapGenerator

if __name__ == "__main__":
    print("start")
    a = Prediction()
    conn = Communication()
    conn.start()
    indicator = Indicator()
    indicator.start()
    loc = indicator.get_position()
    gen = MapGenerator(loc[0] - 0.001, loc[1] - 0.001, loc[0] + 0.001, loc[1] + 0.001)
    gen.generate_base_map()
    base_img = CACHE_PATH / "base.svg"

    while not indicator.is_shutdown():
        gen.clear()
        curr = indicator.get_position()
        motion = indicator.get_speed()
        gen.add_car(curr[0], curr[1])
        conn.brocast(RoadEngager(curr, motion, UUID))
        engagers = conn.recv(1/FRAME_RATE)
        a.update_engager(engagers)
        re = a.predict()
        
        for e in engagers:
            match e.type:
                case "car":
                    gen.add_car(e.position[0], e.position[1])
                case "bicycle":
                    gen.add_bicycle(e.position[0], e.position[1])
                case _:
                    raise KeyError(f"Unknown type {e.type}")
        gen.generate_img()

    print(a)

