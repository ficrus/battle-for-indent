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
        if road == 1:
            knight.sprite.set_speed_decorator(1.5)
        if road == 3:
            knight.sprite.set_speed_decorator(0.6)
        return knight


class ZombieFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0) -> BaseUnit:
        print('ZombieFactory creates  zombie')
        zombie = Zombie(sprite=ZombieSprite, x=x, y=y, scale=scale)
        zombie.sprite.set_speed_decorator(70)
        if road == 1:
            zombie.sprite.set_speed_decorator(1.4)
        if road == 3:
            zombie.sprite.set_speed_decorator(0.7)
        return zombie
