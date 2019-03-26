from abc import ABC


class Army(ABC):
    def __init__(self):
        print('Army is initialized')
        self.units = []

    def action(self):
        pass

    def add_unit(self, unit):
        self.units.append(unit)
        print('Unit is added to the Army')
