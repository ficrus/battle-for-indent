from abc import ABC, abstractmethod


class GUIComponent(ABC):
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
    def draw(self):
        pass


class GUILeaf(GUIComponent):
    @abstractmethod
    def draw(self):
        pass


class GUIComposite(GUIComponent):
    def __init__(self) -> None:
        self._children = []

    def add(self, component: GUIComponent) -> None:
        self._children.append(component)

        component.parent = self

    def remove(self, component: GUIComponent):
        self._children.remove(component)

        component.parent = None

    def is_composite(self) -> bool:
        return True

    def demonstrate(self) -> None:
        for i in self._children:
            print(i)
            if i.is_composite():
                i.demonstrate()
    
    def draw(self):
        for child in self._children:
            child.draw()


class GUIUnitButton(GUILeaf):
    def __init__(self, unit_job: str) -> None:
        self.unit_job = unit_job
    
    def draw(self):
        pass


class GUIHealthBar(GUILeaf):
    def __init__(self, fraction: str) -> None:
        self.fraction = fraction
    
    def draw(self):
        pass


class GUIPauseButton(GUILeaf):
    def __init__(self) -> None:
        pass

    def draw(self):
        pass


if __name__ == "__main__":
    gui = GUIComposite()

    unit_bar = GUIComposite()
    unit_bar.add(GUIUnitButton("knight"))
    unit_bar.add(GUIUnitButton("bandit"))

    info_bar = GUIComposite()
    info_bar.add(GUIPauseButton())
    info_bar.add(GUIHealthBar("tabbers"))
    info_bar.add(GUIHealthBar("spacers"))

    gui.add(unit_bar)
    gui.add(info_bar)

    gui.demonstrate()
