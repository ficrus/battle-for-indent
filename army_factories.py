from unit_factories import *


class ArmyFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_unit(self, unit_factory: UnitFactory) -> BaseUnit:
        return unit_factory.create()


class SpacersArmyFactory(ArmyFactory):
    def __init__(self):
        super().__init__()
        print('Spacers ArmyFactory is created')

    def create_unit(self, unit_factory: UnitFactory) -> BaseUnit:
        """ special creating"""
        print('Spacers ArmyFactory use UnitFactory to create unit')
        return unit_factory.create()


class TabbersArmyFactory(ArmyFactory):
    def __init__(self):
        super().__init__()
        print('Tabbers ArmyFactory is created')

    def create_unit(self, unit_factory: UnitFactory) -> BaseUnit:
        """ special creating"""
        print('Tabbers ArmyFactory use UnitFactory to create unit')
        return unit_factory.create()

