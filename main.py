from prediction import Prediction
from extern import Communication, Indicator
from data import RoadEngager
from config import UUID, FRAME_RATE, CACHE_PATH
from map import MapGenerator
import json
from pathlib import Path
# delete all in folder
from shutil import rmtree
from data import JsonDict
from helpers import svg_combine, svg_to_gif
counter = 0

if __name__ == "__main__":
    print("start")
    CACHE_PATH.mkdir(exist_ok=True)
    rmtree(CACHE_PATH)
    a = Prediction()
    conn = Communication()
    conn.start()
    indicator = Indicator()
    indicator.start()
    loc = indicator.get_position()
    gen = MapGenerator(loc[0] - 0.001, loc[1] - 0.001, loc[0] + 0.001, loc[1] + 0.001)
    gen.generate_base_map()
    base_img = CACHE_PATH / "base.svg"

    for _ in range(12):
        gen.clear()
        with open(Path("./data/sample_car.json"), "r") as f:
            with open(Path("./data/sample_bike.json"), "r") as f1:
                #!!!
                engagers = [json.load(f, object_hook=JsonDict)[counter], json.load(f1, object_hook=JsonDict)[counter]]
        curr = indicator.get_position()
        motion = indicator.get_speed()
        gen.add_car(curr[0], curr[1])
        # conn.brocast(RoadEngager(curr, motion, UUID))
        # engagers = conn.recv(1/FRAME_RATE)
        # print(engagers)
        a.update_engager(engagers + [RoadEngager(curr, motion, UUID, "car", engagers[0].time_stamp).to_dict()])
        print(a.predict())
        gen.add_car(curr[0], curr[1])
        for e in engagers:
            print(e)
            match e.type:
                case "car":
                    gen.add_car(e.position.x, e.position.y)
                case "bike":
                    gen.add_bicycle(e.position.x, e.position.y)
                case _:
                    raise KeyError(f"Unknown type {e.type}")
        gen.generate_img(f"{counter}")
        f = svg_combine(base_img, CACHE_PATH / f"{counter}.svg")
        with open(CACHE_PATH / f"{counter}.svg", "w") as f1:
            f1.write(f)
        counter += 1

    print(a)
    svg_to_gif(CACHE_PATH, CACHE_PATH)
    