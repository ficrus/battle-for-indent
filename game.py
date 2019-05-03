from army import Army
from unit_factories import *
from interface import *


class Game:
    def __init__(self):
        self.state = MainMenuState(self, GUIComposite())
        print('Game is created')

    def change_state(self, state):
        self.state = state

    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())
        print('Game created Army ')


class State:
    def __init__(self, game: Game, gui: GUIComposite) -> None:
        self.game = game
        self.gui = gui


class MainMenuState(State):
    pass


class BattlefieldState(State):
    pass


class UnitSelectState(State):
    pass


class PauseState(State):
    pass


game_ = Game()
game_.create_army()
