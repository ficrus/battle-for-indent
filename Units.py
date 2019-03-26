from abc import ABC, abstractmethod


class BaseUnit(ABC):
    def __init__(self):
        self.fraction = ""
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
        print('Knight created')
        super().__init__()

        self.hp = 100
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 1
        self.magical_resist = 0
        self.move_speed = 4
        self.attack_speed = 1

    def attack(self, target):
        super().attack(target)



class Bandit(BaseUnit):
    def __init__(self):
        print("Bandit created")
        super().__init__()

        self.hp = 30
        self.physical_damage = 2
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 10
        self.attack_speed = 6

    def attack(self, target):
        super().attack(target)