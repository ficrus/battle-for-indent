from army import Army
from unit_factories import *
from interface import *
from event_handling import *
import os
from sprite import KnightSprite, ZombieSprite
import pickle
import memento


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Battle for Indent"


class Game:
    def __init__(self):
        self.gui = None
        self.first_army = None
        self.second_army = None


    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())





class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
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

    def on_key_press(self, symbol: int, modifiers: int):
        self.state.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        self.state.on_key_release(symbol, modifiers)


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

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass


class MainMenuState(State):
    def __init__(self, window: Window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
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

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def start_new_game(self):
        print("New game started!")
        self.window.change_state(PauseState(self.window))

        # позже будет game.change_state(BattleFieldState())

    def continue_game(self):
        print("Game continued!")

    def open_options(self):
        print("Options opened!")
        self.window.change_state(OptionsState(self.window))

    def exit_game(self):
        print("Goodbye!")
        exit(0)


class OptionsState(State):
    def __init__(self, window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self._state = None

        with open("./save_data/options", "rb") as options:
            self.restore(pickle.load(options))

        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        option_buttons = Composite()
        self.gui.add(option_buttons)

        option1_button = MenuButton(110, 480, 150, 50, "Option 1 {0}".format(self._state[0]), self.option1)
        option_buttons.add(option1_button)

        option2_button = MenuButton(110, 420, 150, 50, "Option 2 {0}".format(self._state[1]), self.option2)
        option_buttons.add(option2_button)

        option3_button = MenuButton(110, 360, 150, 50, "Option 3 {0}".format(self._state[2]), self.option3)
        option_buttons.add(option3_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)
    
        return_button = MenuButton(110, 300, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

    def on_draw(self):
        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_update(self, delta_time: float):
        pass

    def do_nothing(self):
        pass

    def option1(self):
        self._state[0] = not self._state[0]
        self.update_options()

    def option2(self):
        self._state[1] = not self._state[1]
        self.update_options()

    def option3(self):
        self._state[2] = not self._state[2]
        self.update_options()

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))

    def update_options(self) -> None:
        self.save_on_disk(self.save())

        self.window.change_state(OptionsState(self.window))

    def save(self) -> memento.OptionsMemento:
        return memento.OptionsMemento(self._state)

    def save_on_disk(self, memento: memento.OptionsMemento) -> None:
        with open("./save_data/options", "wb") as options:
            pickle.dump(memento, options)

    def restore(self, memento: memento.OptionsMemento) -> None:
        self._state = memento.get_state()


class TutorialState(State):
    pass


class UnitSelectState(State):
    pass


class BattlefieldState(State):
    def __init__(self, window: Window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        buttons = Composite()
        self.gui.add(buttons)

        pause_button = MenuButton(110, 480, 150, 50, " || ", self.pause_game)
        buttons.add(pause_button)

    def on_draw(self):
        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_update(self, delta_time: float):
        pass

    def pause_game(self):
        self.window.change_state(PauseState(self.window))


class PauseState(State):
    def __init__(self, window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)

        continue_button = MenuButton(110, 480, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        restart_button = MenuButton(110, 420, 150, 50, "Restart", self.restart_game)
        game_buttons.add(restart_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)
    
        return_button = MenuButton(110, 360, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

    def on_draw(self):
        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_update(self, delta_time: float):
        pass

    def do_nothing(self):
        pass

    def continue_game(self):
        self.window.change_state(BattlefieldState(self.window))

    def restart_game(self):
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_state(MainMenuState(window))
    arcade.run()


if __name__ == "__main__":
    main()
