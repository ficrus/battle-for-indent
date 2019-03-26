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


class Bandit(BaseUnit):
    def __init__(self):
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


class Knight(BaseUnit):
    def __init__(self):
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


class UnitFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass


class BanditFactory(UnitFactory):
    def __init__(self):
        super().__init__()

    def create(self):
        return Bandit()


class KnightFactory(UnitFactory):
    def __init__(self):
        super().__init__()

    def create(self):
        return Knight()


class Army(ABC):
    def __init__(self):
        self.fraction = ""
        self.units = []

    @abstractmethod
    def hire(self, unit):
        unit.fraction = self.fraction

        self.units.append(unit)


class SpacersArmy(Army):
    def __init__(self):
        super().__init__()

        self.fraction = "spacers"

    def hire(self, unit):
        super().hire(unit)


class TabbersArmy(Army):
    def __init__(self):
        super().__init__()

        self.fraction = "tabbers"

    def hire(self, unit):
        super().hire(unit)
