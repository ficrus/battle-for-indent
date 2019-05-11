from army import Army
from unit_factories import *
from interface import *
from event_handling import *
import os
from sprite import KnightSprite, ZombieSprite
import pickle
import memento
import units


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
        self.armies[0].add_unit(knight_factory.create(x=330, y=300))
        self.armies[0].add_unit(knight_factory.create(x=360, y=300))
        self.armies[0].add_unit(knight_factory.create(x=390, y=300))
        self.armies[1].add_unit(zombie_factory.create(x=500, y=300))
        self.armies[1].add_unit(zombie_factory.create(x=530, y=300))
        self.armies[1].add_unit(zombie_factory.create(x=560, y=300))
        self.armies[1].add_unit(zombie_factory.create(x=590, y=300))

        for army in self.armies:
            self.gui.add(army.units)


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

    def update(self, delta_time: float):
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

        knight_count_button = MenuButton(320, 480, 50, 50, "{}".format(self._info.unit_count[units.Knight]), self.clear_unit, units.Knight)
        knight_buttons.add(knight_count_button)

        remove_knight_button = MenuButton(380, 480, 50, 50, "+", self.add_unit, units.Knight)
        knight_buttons.add(remove_knight_button)

        zombie_buttons = Composite()
        self.gui.add(zombie_buttons)

        zombie_button = MenuButton(110, 420, 150, 50, "Zombie", self.show_unit_description, units.Zombie)
        zombie_buttons.add(zombie_button)

        add_zombie_button = MenuButton(260, 420, 50, 50, "-", self.remove_unit, units.Zombie)
        zombie_buttons.add(add_zombie_button)

        zombie_count_button = MenuButton(320, 420, 50, 50, "{}".format(self._info.unit_count[units.Zombie]), self.clear_unit, units.Zombie)
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
            arcade.draw_text(units.get_decription(self._info.described_unit), 450, 275, arcade.color.BLACK, 15)

        arcade.draw_text(UNIT_SELECT_TEXT.format(self._info.current_power, self._info.max_power), 200, 600, arcade.color.BLACK, 15)

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


def play_menu_music(*args):
    music = arcade.load_sound("./sounds/main-menu-theme.wav")
    arcade.play_sound(music)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_state(MainMenuState(window))

    play_menu_music()
    arcade.schedule(play_menu_music, 22)

    arcade.run()


if __name__ == "__main__":
    main()
