from data import RoadEngager, Map
from copy import deepcopy
from helpers import OK, INFO

FRAME_RATE = 20

class Prediction:
    frame = 0
    engagers: list[list[RoadEngager]]
    map: Map
    
    def __init__(self) -> None:
        self.engagers = [dict()] * FRAME_RATE

    def update_engager(self, engager: list[RoadEngager]):
        self.engagers[self.frame % FRAME_RATE] = deepcopy(engager)
        self.frame += 1
    
    def __str__(self) -> str:
        return f"Prediction(frame={self.frame}, engagers={self.engagers}))"
    
    def need_update_map(self) -> bool:
        return False
    def predict(self):
        pass
