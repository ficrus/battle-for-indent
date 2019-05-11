from abc import ABC, abstractmethod


class BaseUnit(ABC):
    def __init__(self):
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

    @abstractmethod
    def attack(self, target):
        target.hp -= self.physical_damage


class Knight(BaseUnit):
    def __init__(self):
        super().__init__()

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
    def __init__(self):
        super().__init__()

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


class Zombie(BaseUnit):
    def __init__(self):
        super().__init__()

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
