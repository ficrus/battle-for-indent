from Army import Army
from UnitFactories import *


class Game:
    def __init__(self):
        print('Game is created')

    def create_army(self, army_factory):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(army_factory.create_unit(knight_factory))
        army.add_unit(army_factory.create_unit(bandit_factory))
        print('Game created Army ')
