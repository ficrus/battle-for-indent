from units import *
from sprite import KnightSprite, ZombieSprite


class Singleton(ABC, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UnitFactory(metaclass=Singleton):
    @abstractmethod
    def create(self, x=0, y=0):
        pass


class KnightFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0) -> BaseUnit:
        print('KnightFactory creates knight')
        knight = Knight(sprite=KnightSprite, x=x, y=y, scale=scale)
        knight.sprite.set_speed_decorator(70)
        return knight


class ZombieFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0) -> BaseUnit:
        print('ZombieFactory creates  zombie')
        zombie = Zombie(sprite=ZombieSprite, x=x, y=y, scale=scale)
        zombie.sprite.set_speed_decorator(70)
        return zombie
