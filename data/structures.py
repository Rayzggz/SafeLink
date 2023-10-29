class RoadEngager:
    speed: (float, float)
    position: (float, float, float)
    id: str
    time_stamp: int
    type: str
    def __init__(self, position, speed, id, type,time_stamp):
        self.position = position
        self.speed = speed
        self.id = id
        self.type = type
        self.time_stamp = time_stamp
    def to_dict(self):
        return {"position":{"x": self.position[0], "y": self.position[1]}, "speed":{"x": self.speed[0], "y": self.speed[1]}, "id":self.id, "type":self.type, "time_stamp":self.time_stamp}