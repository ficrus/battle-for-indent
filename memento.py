from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits


class Memento(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass


class OptionsMemento(Memento):
    def __init__(self, state: list) -> None:
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self) -> list:
        return self._state

    def get_name(self) -> str:
        return f"{self._date} / ({self._state[0:9]}...)"

    def get_date(self) -> str:
        return self._date
