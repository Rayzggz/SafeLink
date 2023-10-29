from data import RoadEngager
from helpers import OK, INFO
from scipy.optimize import least_squares
from concurrent.futures.thread import ThreadPoolExecutor
from config import FRAME_RATE, CORE_NUM, UUID


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
    def polynomial_fit(x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p):
        return a * x ** 15 + b * x ** 14 + c * x ** 13 + d * x ** 12 + e * x ** 11 \
            + f * x ** 10 + g * x ** 9 + h * x ** 8 + i * x ** 7 + j * x ** 6 + k * x ** 5 \
            + l * x ** 4 + m * x ** 3 + n * x ** 2 + o * x + p

    def cal_linear(self, x_data, y_data):
        def objective(params):
            x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = params
            return [(Prediction.polynomial_fit(x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p) - y) for x, y in
                    zip(x_data, y_data)]

        initial_guess = [1] * 17
        result = least_squares(objective, initial_guess)
        
        _, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = result.x
        return a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p


    def predict(self) ->tuple[list[tuple], dict[str, bool]]:
        results = {}
        print(self.engagers)
        x_data = [float(item["position"]["x"]) for item in self.engagers[UUID] if item is not None]
        x_time = [int(item["time_stamp"]) for item in self.engagers[UUID] if item is not None]
        y_data = [float(item["position"]["y"]) for item in self.engagers[UUID] if item is not None]
        y_time = [int(item["time_stamp"]) for item in self.engagers[UUID] if item is not None]
        me = [self.cal_linear(x_time, x_data),self.cal_linear(y_time, y_data)]
        

        for _, v in self.engagers.items():
            if len(v) == 0 or v[0]["id"] == UUID:
                continue
            x_data = [float(item.position.x) for item in v if item is not None]
            x_time = [int(item.time_stamp) for item in v if item is not None]
            y_data = [float(item.position.y) for item in v if item is not None]
            y_time = [int(item.time_stamp) for item in v if item is not None]
            it = [self.cal_linear(x_time, x_data),self.cal_linear(y_time, y_data)]
            # determine if it will me and it will crash within 5 sec
            i = 1
            t = int([a for a in self.engagers[UUID] if a is not None][-1]["time_stamp"])
            while i <= 3:
                lat = Prediction.polynomial_fit(t + i, *me[0])\
                    - Prediction.polynomial_fit(t + i, *it[0])
                lon = Prediction.polynomial_fit(t + i, *me[1])\
                    - Prediction.polynomial_fit(t + i, *it[1])
                results[v[0]["id"]] = lat * LAT_LON_TO_M < LIMIT and lon * LAT_LON_TO_M < LIMIT
                i += 0.1
        return me, results
        

