from army import Army
from unit_factories import *
from interface import *
import random
import numpy as np

class Game:
    def __init__(self):
        self.gui = None
        self.armies = []
        self.max_cnt = 40
        self.cnt = 0
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
        self.armies[1].add_unit(knight_factory.create(x=SCREEN_WIDTH - 20, y=y, mirrored=True, road=selected_road))

        for army in self.armies:
            self.gui.add(army.units)

    def update(self):
        cnt1 = 0
        visitor1 = LeftArmyVisitor(self.armies)
        for unit in self.armies[0].units.get_leaves():
            if unit.sprite.center_x > SCREEN_WIDTH:
                self.armies[0].units.remove(unit)
            cnt1 += 1
            unit.accept(visitor1)

        cnt2 = 0
        visitor2 = RightArmyVisitor(self.armies)
        for unit in self.armies[1].units.get_leaves():
            if unit.sprite.center_x < 0:
                self.armies[1].units.remove(unit)
                return False
            cnt2 += 1
            unit.accept(visitor2)

        if cnt2 < cnt1:
            print("Add")
            for i in range(random.randint(5, 8)):
                if self.cnt < self.max_cnt:
                    self.cnt += 1
                    knight_factory = KnightFactory()
                    zombie_factory = ZombieFactory()
                    factories = [knight_factory, zombie_factory]
                    selected_road = random.randint(1, 3)
                    y = int(SCREEN_HEIGHT *
                            (3 - selected_road)) / 3 + SCREEN_HEIGHT / 10 + np.random.sample() * SCREEN_HEIGHT / 10
                    self.armies[1].add_unit(factories[int(np.random.sample()*2)].create(x=SCREEN_WIDTH - 20*np.random.sample(), y=y, mirrored=True, road=selected_road))
        return True
