from prediction import Prediction
from extern import Communication, Indicator
from data import RoadEngager
from config import UUID, CACHE_PATH
from map import MapGenerator
import json
from pathlib import Path
# delete all in folder
from shutil import rmtree
from data import JsonDict
from helpers import svg_combine, svg_to_gif, INFO, WARNING, OK

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

    for i in range(12):
        gen.clear()
        with open(Path("./data/sample_car.json"), "r") as f:
            with open(Path("./data/sample_bike.json"), "r") as f1:
                #!!!
                engagers = [json.load(f, object_hook=JsonDict)[i], json.load(f1, object_hook=JsonDict)[i]]
        curr = indicator.get_position()
        motion = indicator.get_speed()
        gen.add_car(curr[0], curr[1])
        # conn.brocast(RoadEngager(curr, motion, UUID))
        # engagers = conn.recv(1/FRAME_RATE)
        # print(engagers)
        a.update_engager(engagers + [RoadEngager(curr, motion, UUID, "car", engagers[0].time_stamp).to_dict()])
        predictions = a.predict()
        gen.add_car(curr[0], curr[1])
        WARNING(engagers)
        for e in engagers:
            INFO(f"handling {e['id']} for {i}")
            if predictions is not None:
                params = predictions[1][e["id"]][1]
                ids = []
                for j in range(3):
                    ids.append(gen.add_point(Prediction.polynomial_fit(int(e["time_stamp"][-4:])/100 + j/100, *params[0]), Prediction.polynomial_fit(int(e["time_stamp"][-4:])/100 + j/100, *params[1])))
                gen.add_line(ids)
            match e["type"]:
                case "car":
                    gen.add_car(e.position.x, e.position.y)
                case "bike":
                    gen.add_bicycle(e.position.x, e.position.y)
                case _:
                    raise KeyError(f"Unknown type {e.type}")
        gen.generate_img(f"{i}")
        f = svg_combine(base_img, CACHE_PATH / f"{i}.svg")
        with open(CACHE_PATH / f"{i}.svg", "w") as f1:
            f1.write(f)
    svg_to_gif(CACHE_PATH, CACHE_PATH)
    OK("Finished")
    