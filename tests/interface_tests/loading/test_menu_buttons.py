import numpy as np
from game import *


COUNT = 200
PAUSE = 1
RUN_TIME = 20


class PressChecker:
    def __init__(self, state, x, y, width, height, num):
        self.state = state
        self.xs = list(np.random.rand(num) * width + x)
        self.ys = list(np.random.rand(num) * height + y)
        self.time = list(np.random.rand(num) * RUN_TIME)
        self.pressed = list([False] * num)
        self.released = list([False] * num)
        self.num = num
        self.count = 0
        self.button_pressed = list([False]*len(self.state.button_list))

    def raise_press(self):
        for i in range(self.num):
            if self.time[i] <= self.state.TIME and self.pressed[i] is False:
                self.state.on_mouse_press(self.xs[i], self.ys[i], 0, None)
                self.pressed[i] = True
                for j in range(len(self.state.button_list)):
                    button = self.state.button_list[j]
                    if self.xs[i] > button.center_x + button.width / 2:
                        continue
                    if self.xs[i] < button.center_x - button.width / 2:
                        continue
                    if self.ys[i] > button.center_y + button.height / 2:
                        continue
                    if self.ys[i] < button.center_y - button.height / 2:
                        continue
                    self.button_pressed[j] = True
            if self.time[i] + PAUSE <= self.state.TIME and self.released[i] is False:
                self.state.on_mouse_release(self.xs[i], self.ys[i], 0, None)
                for j in range(len(self.state.button_list)):
                    if self.button_pressed[j] is True:
                        self.count += 1
                        self.button_pressed[j] = False
                self.released[i] = True

    def check(self):
        assert self.state.count == self.count


class TestState(MainMenuState):
    def __init__(self, game, width, height, title):
        super().__init__(game, width, height, title)
        self.count = 0
        self.TIME = 0
        self.press_checker = PressChecker(self, 35, 300, 150, 180, COUNT)

    def set_press_checker(self, press_checker):
        self.press_checker = press_checker

    def update(self, delta_time: float):
        self.TIME += delta_time
        self.press_checker.raise_press()
        self.press_checker.check()
        if self.TIME > RUN_TIME:
            arcade.quick_run(1)

    def start_new_game(self):
        self.count += 1

    def continue_game(self):
        self.count += 1

    def open_options(self):
        self.count += 1

    def exit_game(self):
        self.count += 1


def test_presses_and_releases_on_buttons():
    game_ = Game()
    game_.set_state(TestState(game_, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE))
    arcade.run()


def test_presses_and_releases_everywere():
    game_ = Game()
    state = TestState(game_, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state.set_press_checker(PressChecker(state, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, COUNT))
    game_.set_state(state)
    arcade.run()


def test_presses_and_releases_on_one_button():
    game_ = Game()
    state = TestState(game_, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state.set_press_checker(PressChecker(state, 35, 465, 150, 50, COUNT))
    game_.set_state(state)
    arcade.run()
