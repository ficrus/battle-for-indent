import arcade
import random
import os
import interface

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Battle for Indent :: Main Menu"


def check_mouse_press_for_buttons(x, y, button_list):
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    for button in button_list:
        if button.pressed:
            button.on_release()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.GRAY_BLUE)

        self.pause = False
        self.button_list = None

    def setup(self):
        self.gui = interface.GUIComposite()

        game_buttons = interface.GUIComposite()
        self.gui.add(game_buttons)

        new_game_button = interface.GUIMenuButton(110, 480, 150, 50, "New Game", self.start_new_game)
        game_buttons.add(new_game_button)

        continue_button = interface.GUIMenuButton(110, 420, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        service_buttons = interface.GUIComposite()
        self.gui.add(service_buttons)

        options_button = interface.GUIMenuButton(110, 360, 150, 50, "Options", self.open_options)
        service_buttons.add(options_button)

        exit_button = interface.GUIMenuButton(110, 300, 150, 50, "Exit", self.exit_game)
        service_buttons.add(exit_button)

    def on_draw(self):
        arcade.start_render()
        
        self.gui.draw()

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, interface.GUIButton)]

    def on_mouse_press(self, x, y, button, key_modifiers):
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        check_mouse_release_for_buttons(x, y, self.button_list)

    def start_new_game(self):
        print("New game started!")
    
    def continue_game(self):
        print("Game continued!")

    def open_options(self):
        print("Options opened!")
    
    def exit_game(self):
        print("Goodbye!")


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()

    arcade.run()

if __name__ == "__main__":
    main()
