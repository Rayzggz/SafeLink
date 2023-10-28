from data import RoadEngager
from config import UUID
# this is a concept class
class Communication:
    __buffer = []
    def start(self):
        pass
    def brocast(self, e: RoadEngager):
        assert e.id == UUID
        pass
    def recv(self, timeout=None) -> list[RoadEngager]:
        """
        :param timeout: timeout in seconds, default is None
        :return: list of RoadEngager, recv from other engagers
        """
        pass