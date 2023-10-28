# this is a concept class
class Indicator:
    def start(self):
        pass
    def get_position(self) -> (float, float, float):
        return 0, 0, 0
    def get_motion(self) -> (float, float):
        return 0, 0
    def is_shutdown(self) -> bool:
        return False