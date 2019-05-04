"""
Тестируется способность отрисовать анимацию 200 рыцарей (1600 объектов) одновременно
"""
import time
import collections
import random
import arcade
from sprite import KnightSprite
from animation_of_character import SCREEN_WIDTH, SCREEN_HEIGHT


def test_simple_animation():
    window = StressAnimationTest()
    window.setup()
    arcade.run()


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


COUNT_KNIGHTS = 200


class StressAnimationTest(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1/60)
        self.players = []
        for i in range(COUNT_KNIGHTS):
            self.players.append(KnightSprite(scale=0.25))

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)
        self.TIME = 0
        arcade.set_background_color(arcade.color.LIGHT_GREEN)
        self.fps = FPSCounter()

    def setup(self):
        for player in self.players:
            player.setup(300 + int(random.random()*500), 300 + int(random.random()*500))
            player.move_right = True

    def on_draw(self):
        arcade.start_render()

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 80, arcade.color.BLACK, 16)

        for player in self.players:
            player.on_draw()

        self.fps.tick()

    def update(self, delta_time):
        self.TIME += delta_time
        if self.TIME < 10:
            pass
        else:
            assert (self.fps.get_fps() > 15)
            for player in self.players:
                player.update(delta_time*60)
                if player.move_right:
                    if player.center_x < SCREEN_WIDTH - 500:
                        pass
                    else:
                        player.move_right = False
                        player.move_left = True
                if player.move_left:
                    if player.center_x > 200:
                        pass
                    else:
                        player.move_left = False
                        player.move_right = True
        if self.TIME > 15:
            arcade.quick_run(1)

