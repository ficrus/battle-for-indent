
from textbutton import *
import sprites

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600


class AddKnightButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Add Knight", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class AddBanditButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Add Bandit", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.LIGHT_GREEN)

        self.sprite_factory = sprites.SpriteFactory()
        self.bandit_list = None
        self.knight_list = None
        self.button_list = None

    def setup(self):
        # Create your sprites and sprite lists here
        self.bandit_list = arcade.SpriteList()
        self.knight_list = arcade.SpriteList()

        # Create our on-screen GUI buttons
        self.button_list = []

        add_knight_button = AddKnightButton(60, 570, self.add_knight)
        self.button_list.append(add_knight_button)

        add_bandit_button = AddBanditButton(60, 515, self.add_bandit)
        self.button_list.append(add_bandit_button)

    def on_draw(self):
        arcade.start_render()

        self.bandit_list.draw()
        self.knight_list.draw()

        for button in self.button_list:
            button.draw()

    def update(self, delta_time):
        self.bandit_list.update()
        self.knight_list.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        Check.check_mouse_enter_for_buttons(x, y, self.button_list)

    def on_mouse_press(self, x, y, button, key_modifiers):
        Check.check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        Check.check_mouse_release_for_buttons(x, y, self.button_list)

    def add_knight(self):
        knight = self.sprite_factory.create_unit_sprite(unit='Knight')
        knight.center_x = len(self.knight_list)*100
        knight.center_y = SCREEN_HEIGHT * 2/3
        self.knight_list.append(knight)

    def add_bandit(self):
        bandit = self.sprite_factory.create_unit_sprite(unit='Bandit')
        bandit.center_x = len(self.bandit_list) * 100
        bandit.center_y = SCREEN_HEIGHT / 3
        self.bandit_list.append(bandit)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()