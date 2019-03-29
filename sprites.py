import arcade
from abc import ABC, abstractmethod


class UnitSprite(ABC, arcade.Sprite):
    sprite_name = ""
    scale = 1.0

    @abstractmethod
    def __init__(self):
        super().__init__(self.sprite_name, self.scale)


class KnightSprite(UnitSprite):
    sprite_name = "lib/textures/knight.png"
    scale = 0.25

    def __init__(self):
        super().__init__()


class ZombieSprite(UnitSprite):
    sprite_name = "lib/textures/zombie.png"
    scale = 0.25

    def __init__(self):
        super().__init__()


class SpriteFactory(ABC):

    def create_unit_sprite(self, unit):
        if unit == 'Knight':
            return KnightSprite()
        if unit == 'Bandit':
            return ZombieSprite()




