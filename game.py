from army import Army
from unit_factories import *


class Game:
    def __init__(self):
        print('Game is created')

    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())
        print('Game created Army ')


game = Game()
game.create_army()
