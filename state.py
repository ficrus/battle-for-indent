from event_handling import *
import os
import units
from options_manager import OptionsManager

SCREEN_TITLE = "Battle for Indent"
TUTORIAL_TEXT = """
Welcome to Battle for Indent!
I'm a strange voice inside your head that will teach you how to play.

At first, you should select units for the coming battle.
You can choose how much soldiers you will take.
Note, that number of units depepends on their power.

There are three roads on the battle map. Use 1, 2, 3 keys in order to choose suitable one.
Spawn unit on the selected road by pressing Q, W, E.

Good luck, King! Our victory is in your own hands.
"""
UNIT_SELECT_TEXT = """
Choose units for the battle.

Press
    Unit Name to see description
    - to remove unit
    Unit Count to zeroise it
    + to add unit

It's highly recommended to use as much Power, as you can.

Current Power: {0}
Max Power: {1}
"""


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True, update_rate=1/60)
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

        arcade.draw_text("Start new game (with tutorial)\n", 200, 455, arcade.color.BLACK, 15)
        arcade.draw_text("Continue your game (if you have one)\n", 200, 395, arcade.color.BLACK, 15)
        arcade.draw_text("Change game options\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Exit game (please, no)\n", 200, 275, arcade.color.BLACK, 15)

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
        self.window.change_state(TutorialState(self.window))

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

        self.setup()

    def setup(self):
        om = OptionsManager()

        self.gui = Composite()
        self.listeners = ListenersSupport()

        option_buttons = Composite()
        self.gui.add(option_buttons)

        option1_button = MenuButton(110, 480, 150, 50, "{}".format(["Off", "On"][om.is_music_enabled]),
                                    self.change_music)
        option_buttons.add(option1_button)

        option2_button = MenuButton(110, 420, 150, 50, "{}".format(["Off", "On"][om.is_sounds_enabled]),
                                    self.change_sound)
        option_buttons.add(option2_button)

        option3_button = MenuButton(110, 360, 150, 50, "{}".format(["Off", "!!!PARTY!!!"][om.is_easter_egg_enabled]),
                                    self.change_egg)
        option_buttons.add(option3_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        return_button = MenuButton(110, 300, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

    def on_draw(self):
        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

        arcade.draw_text("Background music (It may take some time to apply changes)\n", 200, 455, arcade.color.BLACK,
                         15)
        arcade.draw_text("Game sounds\n", 200, 395, arcade.color.BLACK, 15)
        arcade.draw_text("Use it if you aren't very serious\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Back to Main Menu\n", 200, 275, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def do_nothing(self):
        pass

    def update_options(self):
        self.window.change_state(OptionsState(self.window))

    def change_music(self):
        om = OptionsManager()
        om.change_music()

        self.update_options()

    def change_sound(self):
        om = OptionsManager()
        om.change_sounds()

        self.update_options()

    def change_egg(self):
        om = OptionsManager()
        om.change_egg()

        self.update_options()

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class TutorialState(State):
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

        unit_select_button = MenuButton(110, 480, 150, 50, "Select Units", self.unit_select)
        game_buttons.add(unit_select_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        return_button = MenuButton(110, 420, 150, 50, "I'm not ready", self.return_to_menu)
        service_buttons.add(return_button)

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        arcade.draw_text(TUTORIAL_TEXT, 200, 350, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def unit_select(self) -> None:
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class UnitSelectInfo:
    def __init__(self) -> None:
        self.current_power = 0
        self.max_power = 100

        self.described_unit = None

        self.unit_count = {
            units.Knight: 0,
            units.Zombie: 0
        }


class UnitSelectState(State):
    def __init__(self, window: Window, info=None):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None

        if info is None:
            self._info = UnitSelectInfo()
        else:
            self._info = info

        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        knight_buttons = Composite()
        self.gui.add(knight_buttons)

        knight_button = MenuButton(110, 480, 150, 50, "Knight", self.show_unit_description, units.Knight)
        knight_buttons.add(knight_button)

        add_knight_button = MenuButton(260, 480, 50, 50, "-", self.remove_unit, units.Knight)
        knight_buttons.add(add_knight_button)

        knight_count_button = MenuButton(320, 480, 50, 50, "{}".format(self._info.unit_count[units.Knight]),
                                         self.clear_unit, units.Knight)
        knight_buttons.add(knight_count_button)

        remove_knight_button = MenuButton(380, 480, 50, 50, "+", self.add_unit, units.Knight)
        knight_buttons.add(remove_knight_button)

        zombie_buttons = Composite()
        self.gui.add(zombie_buttons)

        zombie_button = MenuButton(110, 420, 150, 50, "Zombie", self.show_unit_description, units.Zombie)
        zombie_buttons.add(zombie_button)

        add_zombie_button = MenuButton(260, 420, 50, 50, "-", self.remove_unit, units.Zombie)
        zombie_buttons.add(add_zombie_button)

        zombie_count_button = MenuButton(320, 420, 50, 50, "{}".format(self._info.unit_count[units.Zombie]),
                                         self.clear_unit, units.Zombie)
        zombie_buttons.add(zombie_count_button)

        remove_zombie_button = MenuButton(380, 420, 50, 50, "+", self.add_unit, units.Zombie)
        zombie_buttons.add(remove_zombie_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        start_game_button = MenuButton(110, 360, 150, 50, "Start Game", self.start_game)
        service_buttons.add(start_game_button)

        return_button = MenuButton(110, 300, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        if (self._info.described_unit) is not None:
            sprite = arcade.Sprite("./lib/textures/{}.png".format(self._info.described_unit.__name__.lower()),
                                   center_x=550, center_y=375)
            sprite.draw()
            arcade.draw_text(units.get_decription(self._info.described_unit), 700, 275, arcade.color.BLACK, 15)

        arcade.draw_text(UNIT_SELECT_TEXT.format(self._info.current_power, self._info.max_power), 200, 600,
                         arcade.color.BLACK, 15)

        arcade.draw_text("Start game with these units\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Back to Main Menu\n", 200, 275, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def do_nothing(self) -> None:
        pass

    def update_unit_select(self):
        self.window.change_state(UnitSelectState(self.window, self._info))

    def show_unit_description(self, UnitClass: units.BaseUnit) -> None:
        self._info.described_unit = UnitClass

        self.update_unit_select()

    def clear_unit(self, UnitClass: units.BaseUnit) -> None:
        self._info.current_power -= UnitClass().power * self._info.unit_count[UnitClass]
        self._info.unit_count[UnitClass] = 0

        self.update_unit_select()

    def add_unit(self, UnitClass: units.BaseUnit) -> None:
        if (self._info.current_power + UnitClass().power <= self._info.max_power):
            self._info.current_power += UnitClass().power
            self._info.unit_count[UnitClass] += 1
        else:
            pass

        self.update_unit_select()

    def remove_unit(self, UnitClass: units.BaseUnit) -> None:
        if (self._info.unit_count[UnitClass] > 0):
            self._info.current_power -= UnitClass().power
            self._info.unit_count[UnitClass] -= 1
        else:
            pass

        self.update_unit_select()

    def start_game(self) -> None:
        unit_dict = {UnitClass().job: self._info.unit_count[UnitClass] for UnitClass in self._info.unit_count}
        self.window.change_state(BattlefieldState(self.window, unit_dict))

    def unit_select(self) -> None:
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class BattlefieldState(State):
    def __init__(self, window: Window, unit_dict):
        super().__init__(window)
        self.unit_dict = unit_dict
        self.pause = False
        self.listeners = None
        self.second_listeners = None
        self.gui = None
        self.pause_gui = None
        self.parent = None
        self.game = Game()
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()
        self.gui.add(Stage("images/stage/stage-back.png"))
        road_selection = RoadSelection()
        self.gui.add(road_selection)
        cooldown_indicators = Composite()
        self.gui.add(cooldown_indicators)

        x = 100
        y = 100
        width = 100
        height = 100
        key = 1

        cooldown_indicators_list = []
        for k, value in self.unit_dict.items():
            cooldown_indicator = CooldownIndicator(x, y, width, height, k, value, 10, key)
            cooldown_indicators.add(cooldown_indicator)
            x += width + 10
            key += 1
            cooldown_indicators_list.append(cooldown_indicator)
        key_listener = KeyListener(road_selection, cooldown_indicators_list, self.game)
        self.listeners.add_listener(key_listener)
        self.pause_setup()
        self.gui.add(self.game.gui)
        self.gui.add(Stage("images/stage/stage-front.png"))
        buttons = Composite()
        self.gui.add(buttons)

        pause_button = MenuButton(110, 480, 150, 50, " || ", self.pause_game)
        buttons.add(pause_button)
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

    def pause_setup(self):
        self.pause_gui = Composite()
        self.second_listeners = ListenersSupport()

        game_buttons = Composite()
        self.pause_gui.add(game_buttons)

        continue_button = MenuButton(110, 480, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        restart_button = MenuButton(110, 420, 150, 50, "Restart", self.restart_game)
        game_buttons.add(restart_button)

        service_buttons = Composite()
        self.pause_gui.add(service_buttons)

        return_button = MenuButton(110, 360, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)
        button_list = [button for button in self.pause_gui.get_leaves() if isinstance(button, Button)]
        self.second_listeners.add_listener(ButtonListener(button_list))

    def on_draw(self):
        self.gui.draw()
        if self.pause is True:
            self.pause_gui.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_key_press(self, symbol: int, modifiers: int):
        if self.pause is False:
            self.listeners.on_event(KeyPressEvent(symbol))

    def update(self, delta_time: float):
        if self.pause is False:
            self.gui.update(delta_time)
            self.game.update()

    def pause_game(self):
        self.pause = True
        t = self.second_listeners
        self.second_listeners = self.listeners
        self.listeners = t

    def continue_game(self):
        self.pause = False
        t = self.second_listeners
        self.second_listeners = self.listeners
        self.listeners = t

    def restart_game(self):
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


def play_music_once(*args):
    if OptionsManager().is_music_enabled:
        music = arcade.load_sound("./sounds/main-menu-theme.wav")
        arcade.play_sound(music)


def play_music():
    play_music_once()
    arcade.schedule(play_music_once, 22)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_state(MainMenuState(window))

    play_music()

    arcade.run()


if __name__ == "__main__":
    main()
