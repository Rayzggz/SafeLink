from prediction import Prediction
from extern import Communication, Indicator
from data import RoadEngager
from config import UUID, CACHE_PATH, DEMO_DATA
from map import MapGenerator
import json
from pathlib import Path
# delete all in folder
from shutil import rmtree
from data import JsonDict
import glob
from helpers import svg_combine, svg_to_gif, INFO, WARNING, OK, FAIL
from data import generate_demo

if __name__ == "__main__":
    generate_demo()
    OK("start")
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
    # base map svg
    base_img = CACHE_PATH / "base.svg"

    # load all mock data
    datas = glob.glob("*.json", root_dir=DEMO_DATA)
    mock_engager_data = []
    for i in datas:
        with open(DEMO_DATA / i, "r") as f: 
            mock_engager_data.append(json.load(f, object_hook=JsonDict))
    # get median length
    for i in range(sorted([len(a) for a in mock_engager_data])[int(len(mock_engager_data) / 2)]):
        gen.clear()
        engagers = [a[i] for a in mock_engager_data if len(a) > i]
        curr = indicator.get_position()
        motion = indicator.get_speed()
        gen.add_car(curr[0], curr[1])
        # conn.brocast(RoadEngager(curr, motion, UUID))
        # engagers = conn.recv(1/FRAME_RATE)
        # print(engagers)
        a.update_engager(engagers + [RoadEngager(curr, motion, UUID, "car", engagers[0].time_stamp).to_dict()])
        predictions = a.predict()
        # mark our car as red
        gen.add_car(curr[0], curr[1], {"colour": "red"})
        WARNING(engagers)
        crash = False
        for e in engagers:
            INFO(f"handling {e['id']} for {i}")
            if predictions is not None:
                params = predictions[1][e["id"]][1]
                if predictions[1][e["id"]][0]:
                    FAIL(f"Alarm! This vechice will crash with {e['type']}({e['id']})")
                    crash = True
                ids = []
                for j in range(10):
                    ids.append(gen.add_point(Prediction.polynomial_fit(int(e["time_stamp"][-4:])/100 + j/1000, *params[0]), Prediction.polynomial_fit(int(e["time_stamp"][-4:])/100 + j/1000, *params[1])))
                gen.add_line(ids)
            match e["type"]:
                case "car":
                    gen.add_car(e.position.x, e.position.y)
                case "bike":
                    gen.add_bicycle(e.position.x, e.position.y)
                case _:
                    raise KeyError(f"Unknown type {e.type}")
        gen.generate_img(f"{i}")
        f = svg_combine(base_img, CACHE_PATH / f"{i}.svg", crash)
        with open(CACHE_PATH / f"{i}.svg", "w") as f1:
            f1.write(f)
    svg_to_gif(CACHE_PATH, CACHE_PATH)
    OK("Finished")
    