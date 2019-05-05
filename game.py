from army import Army
from unit_factories import *
from interface import *
from event_handling import *
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Battle for Indent :: Main Menu"


class Game:
    def __init__(self):
        self.state = None
        print('Game is created')

    def set_state(self, state=None):
        if state is None:
            self.state = MainMenuState(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        else:
            self.state = state

    def change_state(self, state):
        self.state = state

    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())
        print('Game created Army ')


class State(arcade.Window):
    def __init__(self, game: Game, width, height, title) -> None:
        super().__init__(width, height, title)
        self.game = game

    def on_draw(self):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


class MainMenuState(State, arcade.Window):
    def __init__(self, game, width, height, title):
        super().__init__(game, width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.GRAY_BLUE)

        self.pause = False
        self.listeners = None
        self.gui = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)

        new_game_button = MenuButton(110, 480, 150, 50, "New Game", self.start_new_game)
        game_buttons.add(new_game_button)

        continue_button = MenuButton(110, 420, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        options_button = MenuButton(110, 360, 150, 50, "Options", self.open_options)
        service_buttons.add(options_button)

        exit_button = MenuButton(110, 300, 150, 50, "Exit", self.exit_game)
        service_buttons.add(exit_button)

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        arcade.start_render()

        self.gui.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def start_new_game(self):
        print("New game started!")
        # позже будет game.change_state(BattleFieldState())

    def continue_game(self):
        print("Game continued!")

    def open_options(self):
        print("Options opened!")

    def exit_game(self):
        print("Goodbye!")


class BattlefieldState(State):
    pass


class UnitSelectState(State):
    pass


class PauseState(State):
    pass


def main():
    game_ = Game()
    game_.set_state()
    game_.create_army()
    arcade.run()


if __name__ == "__main__":
    main()
