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

    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())
        print('Game created Army ')


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.state = None

    def set_state(self, state=None):
        if state is None:
            self.state = MainMenuState(self)
        else:
            self.state = state

    def change_state(self, state):
        self.state = state

    def on_draw(self):
        arcade.start_render()
        self.state.on_draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.state.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.state.on_mouse_release(x, y, button, key_modifiers)

    def update(self, delta_time: float):
        self.state.update(delta_time)


class State:
    def __init__(self, window: Window):
        self.window = window

    def update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


class MainMenuState(State):
    def __init__(self, window: Window):
        super().__init__(window)
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
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_state(MainMenuState(window))
    arcade.run()


if __name__ == "__main__":
    main()
