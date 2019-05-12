from army import Army
from unit_factories import *
from interface import *
import random
import numpy as np


class HP(Leaf):
    def __init__(self, hp, side=0):
        self.hp = hp
        self.side = side
        self.max_hp = hp

    def draw(self):
        lag = 20
        if self.side == 1:
            if self.hp > self.max_hp * 0.5:
                arcade.draw_rectangle_filled(SCREEN_WIDTH / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_GREEN)
            elif self.hp > self.max_hp * 0.25:
                arcade.draw_rectangle_filled(SCREEN_WIDTH / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_YELLOW)
            elif self.hp > 0:
                arcade.draw_rectangle_filled(SCREEN_WIDTH / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_CORAL)

            arcade.draw_rectangle_outline(SCREEN_WIDTH / 5,
                                          SCREEN_HEIGHT - lag,
                                          width=602, height=self.max_hp / 50 + 2, color=arcade.color.DARK_GREEN)
        else:
            if self.hp > self.max_hp * 0.5:
                arcade.draw_rectangle_filled(SCREEN_WIDTH * 4 / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_GREEN)
            elif self.hp > self.max_hp * 0.25:
                arcade.draw_rectangle_filled(SCREEN_WIDTH * 4 / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_YELLOW)
            elif self.hp > 0:
                arcade.draw_rectangle_filled(SCREEN_WIDTH * 4 / 5,
                                             SCREEN_HEIGHT - lag,
                                             width=self.hp / self.max_hp * 600, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_CORAL)

            arcade.draw_rectangle_outline(SCREEN_WIDTH * 4 / 5,
                                          SCREEN_HEIGHT - lag,
                                          width=602, height=self.max_hp / 50 + 2, color=arcade.color.DARK_GREEN)


class Game:
    def __init__(self, max_cnt_1):
        self.gui = None
        self.armies = []
        self.max_cnt_2 = 40
        self.max_cnt_1 = max_cnt_1
        self.cnt = 0
        self.left_side_hp = HP(2000, side=1)
        self.right_side_hp = HP(2000, side=2)
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.armies.append(Army())
        self.armies.append(Army())

        knight_factory = KnightFactory()
        zombie_factory = ZombieFactory()
        selected_road = random.randint(1, 3)
        y = int(SCREEN_HEIGHT *
                (3 - selected_road)) / 3 + SCREEN_HEIGHT / 10 + np.random.sample() * SCREEN_HEIGHT / 10
        self.armies[1].add_unit(zombie_factory.create(x=SCREEN_WIDTH, y=y, mirrored=True, road=selected_road))
        selected_road = random.randint(1, 3)
        y = int(SCREEN_HEIGHT *
                (3 - selected_road)) / 3 + SCREEN_HEIGHT / 10 + np.random.sample() * SCREEN_HEIGHT / 10
        self.armies[1].add_unit(knight_factory.create(x=SCREEN_WIDTH + 10, y=y, mirrored=True, road=selected_road))

        for army in self.armies:
            self.gui.add(army.units)
        self.gui.add(self.left_side_hp)
        self.gui.add(self.right_side_hp)

    def update(self):
        cnt1 = 0
        visitor1 = LeftArmyVisitor(self.armies)
        army1 = self.armies[0].units.get_leaves()
        army2 = self.armies[1].units.get_leaves()
        for unit in army1:
            if unit.sprite.center_x > SCREEN_WIDTH:
                self.right_side_hp.hp -= unit.hp
                self.armies[0].units.remove(unit)
            cnt1 += 1
            unit.accept(visitor1)

        cnt2 = 0
        visitor2 = RightArmyVisitor(self.armies)
        for unit in army2:
            if unit.sprite.center_x < 0:
                self.left_side_hp.hp -= unit.hp
                self.armies[1].units.remove(unit)
            cnt2 += 1
            unit.accept(visitor2)

        if self.left_side_hp.hp <= 0:
            return 2
        if self.right_side_hp.hp <= 0:
            return 1
        if self.armies[0].cnt == self.max_cnt_1 and self.armies[1].cnt == self.max_cnt_2 and len(army1) == 0 and len(
                army2) == 0:
            return 3
        if cnt2 < cnt1:
            print("Add")
            for i in range(random.randint(5, 8)):
                if self.cnt < self.max_cnt_2:
                    self.cnt += 1
                    knight_factory = KnightFactory()
                    zombie_factory = ZombieFactory()
                    paladinfactory = PaladinFactory()
                    walkerfactory = WalkerFactory()
                    factories = [knight_factory, zombie_factory, paladinfactory, walkerfactory]
                    selected_road = random.randint(1, 3)
                    y = int(SCREEN_HEIGHT *
                            (3 - selected_road)) / 3 + SCREEN_HEIGHT / 10 + np.random.sample() * SCREEN_HEIGHT / 10
                    self.armies[1].add_unit(
                        factories[random.randint(0, 3)].create(x=SCREEN_WIDTH + 20 * random.randint(1, 2), y=y,
                                                               mirrored=True, road=selected_road))
        return 0
