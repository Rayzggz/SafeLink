from render import osm_getter, BoundaryBox, main
from pathlib import Path

TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='JOSM'>
  <bounds minlat='<MIN_LAT>' minlon='<MIN_LON>' maxlat='<MAX_LAT>' maxlon='<MAX_LON>' origin='CGImap 0.8.8 (1915366 spike-06.openstreetmap.org)' />
<CONTENT>
</osm>"""

class MapGenerator:
    id = -25530
    start = ""
    content = ""
    end = "</osm>"
    def add_bicycle(self, lat, lon):
        self.id -= 1
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}'><tag k='bicycle' v='yes' /></node>"""
    def add_point(self, lat, lon):
        self.id -= 1
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}' />"""
    def add_car(self, lat, lon):
        self.id -= 1
        self.content += f"""<node id='{self.id}' action='modify' visible='true' lat='{lat}' lon='{lon}'><tag k='car' v='yes' /></node>"""
    def __init__(self, min_lat, min_lon, max_lat, max_lon) -> None:
        self.start = f"""<?xml version='1.0' encoding='UTF-8'?>
<osm version='0.6' generator='JOSM'>
<bounds minlat='{min_lat}' minlon='{min_lon}' maxlat='{max_lat}' maxlon='{max_lon}' origin='CGImap 0.8.8 (1915366 spike-06.openstreetmap.org)' />"""
    def save_to(self, file: str):
        f = Path(file)
        assert f.exists()
        f.write_text(self.start + self.content + self.end)
    def generate_file(self, file: str):
        self.save_to(file)
    