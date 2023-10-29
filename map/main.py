from pathlib import Path
from map_machine import mapper
from config import CACHE_PATH
from map_machine.ui.cli import parse_arguments

class MapGenerator:
    id = -25530
    start = ""
    content = ""
    end = "</osm>"
    loc = []
    def add_bicycle(self, lat, lon):
        self.id -= 1
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}'><tag k='bicycle' v='yes' /></node>"""
        return self.id
    def add_car(self, lat, lon, addi: dict= {}):
        self.id -= 1
        addis = "".join([f"<tag k='{k}' v='{v}' />" for k,v in addi.items()])
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}'><tag k='car' v='yes' />{addis}</node>"""
        return self.id
    def add_point(self, lat, lon):
        self.id -= 1
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}' />"""
        return self.id
    def add_line(self, points):
        self.id -= 1
        self.content += f"""<way id='{self.id}' action='modify' visible='true'>
    {"".join([f"<nd ref='{a}' />" for a in points])}
    <tag k='colour' v='purple' /><tag k='footway' v='sidewalk' /><tag k='highway' v='footway' /></way>"""
        return self.id
    def __init__(self, min_lat, min_lon, max_lat, max_lon) -> None:
        self.start = f"""<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='JOSM'>
<bounds minlat='{min_lat}' minlon='{min_lon}' maxlat='{max_lat}' maxlon='{max_lon}' origin='CGImap 0.8.8 (1915366 spike-06.openstreetmap.org)' />"""
        self.loc = [min_lon,min_lat,  max_lon,max_lat]

    def save_to(self, file: str):
        f = Path(file)
        assert f.exists()
        f.write_text(self.start + self.content + self.end)

    def generate_img(self, file: str):
        (CACHE_PATH / f"{file}.osm").write_text(self.start + self.content + self.end)
        mapper.render_map(parse_arguments(["main.py", "render", "-i", (CACHE_PATH / f"{file}.osm").absolute().__str__(), "--overlap=0", "-o", (CACHE_PATH / f"{file}.svg").absolute().__str__()]))
        assert (CACHE_PATH / f"{file}.svg").exists()
    
    def generate_base_map(self):
        mapper.render_map(parse_arguments(["main.py", "render", "-b", f"{self.loc[0]},{self.loc[1]},{self.loc[2]},{self.loc[3]}", "--level=all", "--buildings=isometric", "-o", f"{(CACHE_PATH / 'base.svg').absolute().__str__()}"]))
        assert (CACHE_PATH / "base.svg").exists()
    def clear(self):
        self.content = ""
    