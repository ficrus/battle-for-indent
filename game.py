from army import Army
from unit_factories import *
from interface import *


class Game:
    def __init__(self):
        self.gui = None
        self.armies = []
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.armies.append(Army())
        self.armies.append(Army())

        knight_factory = KnightFactory()
        zombie_factory = ZombieFactory()

        """Временное решение"""
        self.armies[0].add_unit(knight_factory.create(x=300, y=300))
        self.armies[1].add_unit(zombie_factory.create(x=1290, y=300))

        for army in self.armies:
            '''for unit in army.units.get_leaves():
                unit.sprite.set_speed_decorator(70)'''
            self.gui.add(army.units)

    def update(self):

        visitor1 = LeftArmyVisitor(self.armies)
        for unit in self.armies[0].units.get_leaves():
            unit.accept(visitor1)

        visitor2 = RightArmyVisitor(self.armies)
        for unit in self.armies[1].units.get_leaves():
            unit.accept(visitor2)