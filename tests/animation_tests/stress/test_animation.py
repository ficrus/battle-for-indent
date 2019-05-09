"""
Тестируется способность отрисовать анимацию 200 рыцарей (1600 объектов) одновременно
"""

from base_animation import *


def test_simple_animation():
    window = SimpleAnimationTest(count_knights=200)
    window.setup()
    arcade.quick_run(20)


class SimpleAnimationTest(AnimationTest):
    def __init__(self, count_knights):
        super().__init__(count_knights)

    def update(self, delta_time):
            self.TIME += delta_time
            if self.TIME < 8:
                pass
            else:
                assert (self.fps.get_fps() > 15)
                for player in self.players:
                    player.update(delta_time * 60)
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
