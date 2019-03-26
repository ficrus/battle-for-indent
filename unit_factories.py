from units import *


class UnitFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass


class KnightFactory(UnitFactory):
    def __init__(self):
        print('Knight Factory Created')
        super().__init__()

    def create(self) -> BaseUnit:
        print('KnightFactory creates knight')
        return Knight()


class BanditFactory(UnitFactory):
    def __init__(self):
        print('Bandit Factory Created')
        super().__init__()

    def create(self) -> BaseUnit:
        print('BanditFactory creates bandit')
        return Bandit()
