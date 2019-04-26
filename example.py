from game import *
import unit_factories
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
        self.bandit_sprite_list_1 = None
        self.bandit_sprite_list_2 = None
        self.knight_sprite_list_1 = None
        self.knight_sprite_list_2 = None
        self.button_list = None

        self.knight_factory = None
        self.bandit_factory = None
        self.army1 = None
        self.army2 = None
        self.game = None

    def setup(self):
        self.game = Game()
        self.army1 = Army()
        self.army2 = Army()
        self.knight_factory = unit_factories.KnightFactory()
        self.bandit_factory = unit_factories.BanditFactory()
        self.sprite_factory = sprites.SpriteFactory()

        # Create your sprites and sprite lists here
        self.bandit_sprite_list_1 = arcade.SpriteList()
        self.bandit_sprite_list_2 = arcade.SpriteList()
        self.knight_sprite_list_1 = arcade.SpriteList()
        self.knight_sprite_list_2 = arcade.SpriteList()

        # Create our on-screen GUI buttons
        self.button_list = []

        add_knight_button_1 = AddKnightButton(60, 570, self.add_knight_1)
        self.button_list.append(add_knight_button_1)

        add_bandit_button_1 = AddBanditButton(60, 515, self.add_bandit_1)
        self.button_list.append(add_bandit_button_1)

        add_knight_button_2 = AddKnightButton(SCREEN_WIDTH/2+60, 570, self.add_knight_2)
        self.button_list.append(add_knight_button_2)

        add_bandit_button_2 = AddBanditButton(SCREEN_WIDTH/2+60, 515, self.add_bandit_2)
        self.button_list.append(add_bandit_button_2)

    def on_draw(self):
        arcade.start_render()

        self.bandit_sprite_list_1.draw()
        self.bandit_sprite_list_2.draw()
        self.knight_sprite_list_1.draw()
        self.knight_sprite_list_2.draw()

        for button in self.button_list:
            button.draw()

    def update(self, delta_time):
        self.bandit_sprite_list_1.update()
        self.bandit_sprite_list_2.update()
        self.knight_sprite_list_1.update()
        self.knight_sprite_list_2.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        Check.check_mouse_enter_for_buttons(x, y, self.button_list)

    def on_mouse_press(self, x, y, button, key_modifiers):
        Check.check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        Check.check_mouse_release_for_buttons(x, y, self.button_list)

    def add_knight_1(self):
        if len(self.knight_sprite_list_1) < 12:
            knight = self.knight_factory.create()
            self.army1.add_unit(knight)
            knight_sprite = self.sprite_factory.create_unit_sprite(unit='Knight')
            knight_sprite.center_x = 50 + len(self.knight_sprite_list_1) * 50
            knight_sprite.center_y = SCREEN_HEIGHT * 2/3
            self.knight_sprite_list_1.append(knight_sprite)

    def add_bandit_1(self):
        if len(self.bandit_sprite_list_1) < 12:
            bandit = self.bandit_factory.create()
            self.army1.add_unit(bandit)
            bandit_sprite = self.sprite_factory.create_unit_sprite(unit='Bandit')
            bandit_sprite.center_x = 50 + len(self.bandit_sprite_list_1) * 50
            bandit_sprite.center_y = SCREEN_HEIGHT / 3
            self.bandit_sprite_list_1.append(bandit_sprite)

    def add_knight_2(self):
        if len(self.knight_sprite_list_2) < 12:
            knight = self.knight_factory.create()
            self.army2.add_unit(knight)
            knight_sprite = self.sprite_factory.create_unit_sprite(unit='Knight')
            knight_sprite.center_x = SCREEN_WIDTH / 2 + 50 + len(self.knight_sprite_list_2) * 50
            knight_sprite.center_y = SCREEN_HEIGHT * 2 / 3
            self.knight_sprite_list_2.append(knight_sprite)

    def add_bandit_2(self):
        if len(self.bandit_sprite_list_2) < 12:
            bandit = self.bandit_factory.create()
            self.army2.add_unit(bandit)
            bandit_sprite = self.sprite_factory.create_unit_sprite(unit='Bandit')
            bandit_sprite.center_x = SCREEN_WIDTH / 2 + 50 + len(self.bandit_sprite_list_2) * 50
            bandit_sprite.center_y = SCREEN_HEIGHT / 3
            self.bandit_sprite_list_2.append(bandit_sprite)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()