from abc import ABC, abstractmethod
from interface import Leaf


class BaseUnit(Leaf):
    def __init__(self, sprite=None, x=0, y=0, scale=1):
        self.sprite = None
        if sprite is not None:
            self.sprite = sprite(scale=scale)
        self.fraction = ""
        self.job = ""
        self.description = ""
        self.power = 0
        self.hp = 0
        self.physical_damage = 0
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 0
        self.setup(x, y)

    def setup(self, x, y):
        if self.sprite is not None:
            self.sprite.setup(x, y)
            self.sprite.move_speed = self.move_speed

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
        self.description = "Strong and self-confident knight"
        self.power = 10
        self.hp = 100
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 1
        self.magical_resist = 0
        self.move_speed = 4
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target: BaseUnit):
        super().attack(target)


class Paladin(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=1):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)

        self.job = "Paladin"
        self.description = "Master of spear and base magic"
        self.power = 20
        self.hp = 100
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 1
        self.magical_resist = 0
        self.move_speed = 5
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target: BaseUnit):
        super().attack(target)


class Zombie(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.15):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)

        self.job = "Zombie"
        self.description = "It's not a bandit at all"
        self.power = 10
        self.hp = 30
        self.physical_damage = 2
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 6
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target: BaseUnit):
        super().attack(target)


def get_decription(UnitClass: BaseUnit) -> str:
    full_dectiption = """
    This is {u.job}
    {u.description}

    Stats:
        Power Cost: {u.power}
        HP: {u.hp}
        Physical Damage: {u.physical_damage}
        Magical Damage: {u.magical_damage}
        Physical Resist: {u.physical_resist}
        Magical Resist: {u.magical_resist}
        Move Speed: {u.move_speed}
    """.format(u=UnitClass())

    return full_dectiption
