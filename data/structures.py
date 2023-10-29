class RoadEngager:
    speed: (float, float)
    position: (float, float, float)
    id: str
    time_stamp: float
    type: str
    def __init__(self, position, speed, id, type,time_stamp):
        self.position = position
        self.speed = speed
        self.id = id
        self.type = type
        self.time_stamp = time_stamp