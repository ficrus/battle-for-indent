from abc import ABC, abstractmethod
from interface import Leaf


class BaseUnit(Leaf):
    def __init__(self, sprite=None, x=0, y=0, scale=1):
        self.sprite = None
        if sprite is not None:
            self.sprite = sprite(scale)
        self.fraction = ""
        self.job = ""
        self.decription = ""
        self.power = 0
        self.hp = 0
        self.physical_damage = 0
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 0
        self.attack_speed = 0
        self.setup(x, y)

    def setup(self, x, y):
        if self.sprite is not None:
            self.sprite.setup(x, y)

    def draw(self):
        if self.sprite is not None:
            self.sprite.on_draw()

    def update(self, delta_time):
        if self.sprite is not None:
            self.sprite.update(delta_time)

    @abstractmethod
    def attack(self, target):
        target.hp -= self.physical_damage
        if self.sprite is not None:
            self.sprite.attack = True


class Knight(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.16):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)
        self.job = "Knight"
        self.decription = "Strong and self-confident knight"
        self.power = 10
        self.hp = 100
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 1
        self.magical_resist = 0
        self.move_speed = 4
        self.attack_speed = 1

    def attack(self, target: BaseUnit):
        super().attack(target)


class Paladin(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=1):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)

        self.job = "Paladin"
        self.decription = "Master of spear and base magic"
        self.power = 20
        self.hp = 100
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 1
        self.magical_resist = 0
        self.move_speed = 4
        self.attack_speed = 1

    def attack(self, target: BaseUnit):
        super().attack(target)

class Bandit(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.15):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)

        self.job = "Zombie"
        self.decription = "It's not a bandit at all"
        self.power = 10
        self.hp = 30
        self.physical_damage = 2
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 10
        self.attack_speed = 6

    def attack(self, target: BaseUnit):
        super().attack(target)
