from abc import ABC, abstractmethod


class FromFile(ABC):
    @abstractmethod
    def __init__(self, filename):
        pass

    @abstractmethod
    def __iter__(self):
        pass
    @abstractmethod
    def getPackets(self):
        pass