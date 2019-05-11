from units import *


class Singleton(ABC, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UnitFactory(metaclass=Singleton):
    @abstractmethod
    def create(self):
        pass


class KnightFactory(UnitFactory):
    def create(self) -> BaseUnit:
        print('KnightFactory creates knight')
        return Knight()

class ZombieFactory(UnitFactory):
    def create(self) -> BaseUnit:
        print('ZombieFactory creates  zombie')
        return Zombie()
