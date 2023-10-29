from random import randint
from data import RoadEngager
import json
from config import DEMO_DATA
from helpers import OK

def uniform_spped_straight(x, y, ex, ey, start_stamp:int, end_stamp:int, id, type) -> list[dict]:
    result = []
    packets = randint(1, (end_stamp - start_stamp) / 0.1)
    sx = (ex - x) / packets
    sy = (ey - y) / packets
    for i in range(packets):
        result.append(RoadEngager((x + sx * i, y + sy * i), (sx, sy), id, type, str(int(start_stamp + i * (end_stamp - start_stamp) / packets))).to_dict())
    return result

def generate_demo():
    # gen car2
    with open(DEMO_DATA / "GENERATED_car2.json", "w") as f:
        f.write(json.dumps(uniform_spped_straight(40.00605,-83.00867, 40.00606,-83.01040, 1698541010, 1698541021, "UUID_FOR_CAR_2", "car")))
    OK("generated demo data for car2")
    # gen bike2
    with open(DEMO_DATA / "GENERATED_bike2.json", "w") as f:
        f.write(json.dumps(uniform_spped_straight(40.00502,-83.00905, 40.00584,-83.00924, 1698541010, 1698541021, "UUID_FOR_BIKE_2", "bike")))
    OK("generated demo data for bike2")
    # gen car3
    with open(DEMO_DATA / "GENERATED_car3.json", "w") as f:
        f.write(json.dumps(uniform_spped_straight(40.00658,-83.00932, 40.00623,-83.00924, 1698541010, 1698541021, "UUID_FOR_CAR_3", "car")))
    OK("generated demo data for car3")