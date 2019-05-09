from army import Army
from unit_factories import *
from interface import *
from event_handling import *
import os
from sprite import KnightSprite, ZombieSprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Battle for Indent :: Main Menu"


class Game:
    def __init__(self):
        print('Game is created')
        self.screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1 / 60, window=MainMenuState)

    def create_army(self):
        army = Army()
        knight_factory = KnightFactory()
        bandit_factory = BanditFactory()
        army.add_unit(knight_factory.create())
        army.add_unit(bandit_factory.create())
        print('Game created Army ')


class Example:
    def __init__(self):
        self.player = KnightSprite(scale=0.25)
        self.zombie = ZombieSprite(scale=0.22)

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)
        self.setup()

    def setup(self):
        self.player.setup(300, 300)
        self.zombie.setup(500, 300)

    def on_draw(self):
        arcade.start_render()
        self.player.on_draw()
        self.zombie.on_draw()

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.zombie.move_left = True
        elif key == arcade.key.RIGHT:
            self.zombie.move_right = True
        elif key == arcade.key.W:
            self.zombie.attack = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.zombie.move_left = False
        if key == arcade.key.RIGHT:
            self.zombie.move_right = False
        if key == arcade.key.W:
            self.zombie.attack = False

    def on_update(self, delta_time):
        self.player.update(delta_time * 60)
        self.zombie.update(delta_time * 60)


class MainMenuState:
    def __init__(self):
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.setup()
        self.parent = None

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

    def on_draw(self):
        arcade.start_render()

        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

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
        self.parent.change_window(Example)
        # позже будет game.change_state(BattleFieldState())

    def continue_game(self):
        print("Game continued!")

    def open_options(self):
        print("Options opened!")

    def exit_game(self):
        print("Goodbye!")


class Screen(arcade.Window):
    def __init__(self, width, height, title, update_rate=1 / 60, window=MainMenuState):
        super().__init__(width, height, title=title, update_rate=update_rate)
        self.window = window()
        self.window.parent = self

    def setup(self):
        self.window.setup()

    def on_draw(self):
        self.window.on_draw()

    def on_update(self, delta_time: float):
        self.window.on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        self.window.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.window.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.window.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.window.on_mouse_release(x, y, button, key_modifiers)

    def change_window(self, window):
        self.window = window()


class BattlefieldState:
    pass


class UnitSelectState:
    pass


class PauseState:
    pass


def main():
    game_ = Game()
    game_.create_army()
    arcade.run()


if __name__ == "__main__":
    main()
