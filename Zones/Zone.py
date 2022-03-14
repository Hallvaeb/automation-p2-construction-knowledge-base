# https://www.geeksforgeeks.org/abstract-classes-in-python/

from abc import ABC, abstractmethod


class Zone(ABC):

    @abstractmethod
    def create():
        pass

    @abstractmethod
    def addToKB():
        pass

    @abstractmethod
    def remove():
        pass

    @abstractmethod
    def getID():
        pass
