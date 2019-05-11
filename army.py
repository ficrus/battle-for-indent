from abc import ABC
from units import BaseUnit
from interface import *


class Army(ABC):
    def __init__(self):
        print('Army is initialized')
        self.units = Composite()

    def action(self):
        pass        
    
    def add_unit(self, unit: BaseUnit):
        self.units.add(unit)
