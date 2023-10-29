from data import RoadEngager
from helpers import OK, INFO
from scipy.optimize import least_squares
from concurrent.futures.thread import ThreadPoolExecutor
from config import FRAME_RATE, CORE_NUM, UUID
from prediction.check_collision import check_collision


LIMIT = 2
LAT_LON_TO_M = 111320

class Prediction:
    frame = 0
    engagers: dict[str, list[RoadEngager]] = {}
    pool = ThreadPoolExecutor(CORE_NUM)

    def update_engager(self, engager: list[RoadEngager]):
        for e in engager:
            if e["id"] not in self.engagers.keys():
                self.engagers[e["id"]] = [None] * FRAME_RATE
            self.engagers[e["id"]][self.frame % FRAME_RATE] = e
        self.frame += 1

    def __str__(self) -> str:
        return f"Prediction(frame={self.frame}, engagers={self.engagers}))"

    def need_update_map(self) -> bool:
        return False

    # 15 degree polynomial
    def polynomial_fit(x, a, b, c, d):
        return a * x ** 3 + b * x ** 2 + c * x + d

    def cal_linear(self, x_data, y_data):
        def objective(params):
            _, a, b, c, d = params
            return [(Prediction.polynomial_fit(x, a, b, c, d) - y) for x, y in
                    zip(x_data, y_data)]

        initial_guess = [1] * 5
        result = least_squares(objective, initial_guess)
        
        _, a, b, c, d = result.x
        return a, b, c, d


    def predict(self) ->tuple[tuple[tuple], dict[str, list]]:
        if self.frame <= 3:
            return None
        results = {}
        x_data = [float(item["position"]["x"]) for item in self.engagers[UUID] if item is not None]
        x_time = [int(item["time_stamp"][-4:]) / 100 for item in self.engagers[UUID] if item is not None]
        y_data = [float(item["position"]["y"]) for item in self.engagers[UUID] if item is not None]
        y_time = [int(item["time_stamp"][-4:]) / 100 for item in self.engagers[UUID] if item is not None]
        me = [self.cal_linear(x_time, x_data),self.cal_linear(y_time, y_data)]

        # for checking collision
        me_speed = ([float(item["speed"]["x"]) for item in self.engagers[UUID] if item is not None],\
            [float(item["speed"]["y"]) for item in self.engagers[UUID] if item is not None])
        

        for _, v in self.engagers.items():
            if len(v) == 0 or v[0]["id"] == UUID:
                continue
            x_data = [float(item.position.x) for item in v if item is not None]
            x_time = [int(item.time_stamp[-4:])/100 for item in v if item is not None]
            y_data = [float(item.position.y) for item in v if item is not None]
            y_time = [int(item.time_stamp[-4:])/100 for item in v if item is not None]

            # for checking collision
            it_speed = ([float(item.speed.x) for item in v if item is not None],\
                [float(item.speed.y) for item in v if item is not None])
            results[v[0]["id"]] = [None] * 2
            results[v[0]["id"]][0] = check_collision(me, (x_data, y_data), me_speed, it_speed)

            it = [self.cal_linear(x_time, x_data),self.cal_linear(y_time, y_data)]
            # determine if it will me and it will crash within 5 sec
            i = 1
            t = int([a for a in self.engagers[UUID] if a is not None][-1]["time_stamp"][-4:])/100
            while i <= 3:
                lat = Prediction.polynomial_fit(t + i/100, *me[0])\
                    - Prediction.polynomial_fit(t + i/100, *it[0])
                lon = Prediction.polynomial_fit(t + i/100, *me[1])\
                    - Prediction.polynomial_fit(t + i/100, *it[1])
                results[v[0]["id"]][0] = results[v[0]["id"]][0] or (abs(lat) * LAT_LON_TO_M < LIMIT and abs(lon) * LAT_LON_TO_M < LIMIT)
                i += 1
            results[v[0]["id"]][1] = it
        return me, results
        

