class RoadEngager:
    speed: (float, float)
    position: (float, float, float)
    id: str

class ReferenceLine:
    s: float
    x: float
    y: float
    hdg: float
    length: float

class RoadType:
    max_speed: float
    width: float
    road_id: str
    road_type: str
    country: str

class Map:
    reference_line: ReferenceLine
    t_road_type: RoadType