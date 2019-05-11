from abc import ABC, abstractmethod
import arcade


class Component(ABC):
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, component) -> None:
        pass

    def remove(self, component) -> None:
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def get_leaves(self) -> list:
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self, delta_time: float):
        pass


class Leaf(Component):
    def get_leaves(self) -> list:
        return []

    def draw(self):
        pass

    def update(self, delta_time: float):
        pass


class Composite(Component):
    def __init__(self) -> None:
        self._children = []

    def add(self, component: Component) -> None:
        self._children.append(component)

        component.parent = self

    def remove(self, component: Component):
        self._children.remove(component)

        component.parent = None

    def is_composite(self) -> bool:
        return True

    def get_leaves(self) -> list:
        return self._children + sum([child.get_leaves() for child in self._children], [])

    def demonstrate(self) -> None:
        for i in self._children:
            print(i)
            if i.is_composite():
                i.demonstrate()

    def draw(self):
        for child in self._children:
            child.draw()
    
    def update(self, delta_time: float) -> None:
        for child in self._children:
            child.update(delta_time)


class UnitButton(Leaf):
    def __init__(self, unit_job: str) -> None:
        self.unit_job = unit_job

    def draw(self):
        self.portrait = "eeeee"
        print("Draw unit button for {0}".format(self.unit_job))


# Это желательно вынести в другой файл, так как реализует не наполнение state, а наполнение игры
class HealthBar(Leaf):
    def __init__(self, fraction: str) -> None:
        self.fraction = fraction

    def draw(self):
        self.hp = 100
        print("Draw hp bar for {0}".format(self.fraction))


class PauseButton(Leaf):
    def __init__(self) -> None:
        pass

    def draw(self):
        print("Draw pause button")


# Это желательно вынести в другой файл, так как реализует не наполнение state, а наполнение игры
class Castle(Leaf):
    def __init__(self, fraction):
        self.fraction = fraction

    def draw(self):
        print("Draw Castle for {0}".format(self.fraction))


class Button(Leaf):
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class MenuButton(Button):
    def __init__(self, center_x, center_y, width, height, text, action_function, argument=None):
        self.action_function = action_function
        self.argument = argument
        super().__init__(center_x, center_y, width, height, text)

    def on_release(self):
        super().on_release()

        if self.argument is None:
            self.action_function()
        else:
            self.action_function(self.argument)


if __name__ == "__main__":
    gui_ = Composite()

    unit_bar = Composite()
    unit_bar.add(UnitButton("knight"))
    unit_bar.add(UnitButton("bandit"))

    info_bar = Composite()
    info_bar.add(PauseButton())
    info_bar.add(HealthBar("tabbers"))
    info_bar.add(HealthBar("spacers"))

    game_map = Composite()
    game_map.add(Castle("tabbers"))
    game_map.add(Castle("spacers"))

    gui_.add(unit_bar)
    gui_.add(info_bar)
    gui_.add(game_map)

    # gui.demonstrate()
    gui_.draw()
