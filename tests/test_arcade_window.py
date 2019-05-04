from abc import ABC

import arcade
from sprite import KnightSprite, ZombieSprite

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000


class Example(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1/60)

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)
        self.flag = True
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

    def update(self, delta_time):
        if self.flag:
            arcade.quick_run(1)


def test_main():
    window = Example()
    window.setup()
    arcade.run()
