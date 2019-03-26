from army import Army
import unit_factories

knight_factory = unit_factories.KnightFactory()
knight = knight_factory.create()
bandit_factory = unit_factories.BanditFactory()
bandit = bandit_factory.create()
army1 = Army()
army2 = Army()
army2.add_unit(knight)
army3 = Army()
army3.add_unit(knight)
army3.add_unit(bandit)


def test_empty():
    assert (army1.units == []) is True


def test_one():
    assert (len(army2.units) == 1) is True


def test_two():
    assert (len(army3.units) == 2) is True


def test_difference():
    assert (army1.units is army2.units) is False
