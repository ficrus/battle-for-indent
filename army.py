from abc import ABC
from units import BaseUnit


class Army(ABC):
    def __init__(self):
        print('Army is initialized')
        self.units = []

    def action(self):
        pass

    def add_unit(self, unit: BaseUnit):
        self.units.append(unit)
        print('Unit is added to the Army')
