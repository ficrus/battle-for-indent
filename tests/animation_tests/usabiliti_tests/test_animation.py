"""Тестируется количество перекрываний рыцарями и зомби друг друга (от этого зависит,
может ли игрок ажекватно оценивать силы своей армии"""

from base_animation import *
from sprite import ZombieSprite


def test_simple_animation():
    window = UsabilityAnimationTest(count_knights=10, count_zombies=10)
    window.setup()
    arcade.run()


class UsabilityAnimationTest(AnimationTest):
    def __init__(self, count_knights, count_zombies):
        super().__init__(count_knights)
        for i in range(count_zombies):
            self.players.append(ZombieSprite(scale=0.25))
        self.knight_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.cnt_hits = 0

    def setup(self):
        for player in self.players:
            if type(player).__name__ == 'KnightSprite':
                player.setup(int(random.random()*250), 400 + int(random.random()*250))
                player.move_right = True
                for obj in player.object_parts:
                    self.knight_list.append(obj.sprite)
            else:
                player.setup(SCREEN_WIDTH - 550 + int(random.random() * 250), 400 + int(random.random() * 250))
                player.move_left = True
                for obj in player.object_parts:
                    self.zombie_list.append(obj.sprite)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text("collisions: "+str(self.cnt_hits), 20, SCREEN_HEIGHT - 120, arcade.color.BLACK, 16)

    def update(self, delta_time):
            self.cnt_hits = 0
            self.TIME += delta_time
            if self.TIME < 3:
                pass
            else:
                assert (self.fps.get_fps() > 15)
                for player in self.players:
                    if type(player).__name__ == 'KnightSprite':
                        for obj in player.object_parts:
                            self.cnt_hits += len(arcade.check_for_collision_with_list(obj.sprite,  self.zombie_list))
                    else:
                        for obj in player.object_parts:
                            self.cnt_hits += len(arcade.check_for_collision_with_list(obj.sprite, self.knight_list))

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

                    player.update(delta_time * 60)
                assert(self.cnt_hits < 2000)

            if self.TIME > 8:
                arcade.quick_run(1)
