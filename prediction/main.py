from data import RoadEngager, Map
from copy import deepcopy
from helpers import OK, INFO


FRAME_RATE = 20


class Prediction:
    frame = 0
    engagers: dict[str, list[RoadEngager]] = {}
    map: Map

    def update_engager(self, engager: list[RoadEngager]):
        for e in engager:
            if e.id not in self.engagers.keys():
                self.engagers[e.id] = [[]] * FRAME_RATE
            self.engagers[e.id][self.frame % FRAME_RATE] = e
        self.frame += 1

    def __str__(self) -> str:
        return f"Prediction(frame={self.frame}, engagers={self.engagers}))"

    def need_update_map(self) -> bool:
        return False

    def predict(self):
        for k, v in self.engagers.items():
            OK(k, v)
