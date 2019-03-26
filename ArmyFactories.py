from UnitFactories import *


class ArmyFactory(ABC):
    @abstractmethod
    def create_unit(self, UnitFactory):
        return UnitFactory.create()


class SpacersArmyFactory(ArmyFactory):
    def __init__(self):
        print('Spacers ArmyFactory is created')

    def create_unit(self, UnitFactory):
        """ special creating"""
        print('Spacers ArmyFactory use UnitFactory to create unit')
        return UnitFactory.create()


class TabbersArmyFactory(ArmyFactory):
    def __init__(self):
        print('Tabbers ArmyFactory is created')

    def create_unit(self, UnitFactory):
        """ special creating"""
        print('Tabbers ArmyFactory use UnitFactory to create unit')
        return UnitFactory.create()

