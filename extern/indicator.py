# this is a concept class
class Indicator:
    def start(self):
        pass
    def get_position(self) -> (float, float):
        return 40.00607,-83.00889
    def get_speed(self) -> (float, float):
        return 0, 0
    def is_shutdown(self) -> bool:
        return False