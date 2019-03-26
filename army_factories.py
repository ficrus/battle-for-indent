from unit_factories import *


class ArmyFactory(ABC):
    @abstractmethod
    def create_unit(self, unit_factory):
        return unit_factory.create()


class SpacersArmyFactory(ArmyFactory):
    def __init__(self):
        print('Spacers ArmyFactory is created')

    def create_unit(self, unit_factory):
        """ special creating"""
        print('Spacers ArmyFactory use UnitFactory to create unit')
        return unit_factory.create()


class TabbersArmyFactory(ArmyFactory):
    def __init__(self):
        print('Tabbers ArmyFactory is created')

    def create_unit(self, unit_factory):
        """ special creating"""
        print('Tabbers ArmyFactory use UnitFactory to create unit')
        return unit_factory.create()

