from pathlib import Path
import json
from data.structures import RoadEngager, Map

class JsonDict(dict):
    """
    General json object that allows attributes 
    to be bound to and also behaves like a dict.
    """
    def __getattr__(self, attr: str):
        return self.get(attr)

    def __setattr__(self, attr: str, value):
        self[attr] = value

def parse_data(engager_file: str, map_file: str) -> (RoadEngager, Map):
    path = Path(engager_file)
    path2 = Path(map_file)
    assert path.exists()
    assert path2.exists()
    return json.loads(path.read_text(), object_hook=JsonDict), json.loads(path2.read_text(), object_hook=JsonDict)
