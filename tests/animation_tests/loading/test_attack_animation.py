"""
Тестируется способность отрисовать анимацию 200 рыцарей (1600 объектов) одновременно
"""

from base_animation import *


def test_simple_animation():
    window = SimpleAnimationTest(count_knights=40)
    window.setup()
    arcade.run()


class SimpleAnimationTest(AnimationTest):
    def __init__(self, count_knights):
        super().__init__(count_knights)
        self.cnt = 0

    def setup(self):
        super().setup()
        for player in self.players:
            player.move_right = False

    def update(self, delta_time):
            self.TIME += delta_time
            if self.TIME < 7:
                pass
            else:
                assert (self.fps.get_fps() > 15)
                if self.cnt < 3:
                    b = False
                    for player in self.players:

                        if not player.start_attack:
                            if not b:
                                b = True
                            player.attack = True
                    if b:
                        self.cnt += 1
                for player in self.players:
                    player.update(delta_time * 60)
            if self.TIME > 10:
                arcade.quick_run(1)
