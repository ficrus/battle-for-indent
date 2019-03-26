import unit_factories

knight_factory = unit_factories.KnightFactory()
first_knight = knight_factory.create()
second_knight = knight_factory.create()
bandit_factory = unit_factories.BanditFactory()
first_bandit = bandit_factory.create()
second_bandit = bandit_factory.create()


def test_knight_difference():
    assert (first_knight is second_knight) is False


def test_bandit_difference():
    assert (first_bandit is second_bandit) is False


def test_knight_class():
    assert (first_knight.__class__ is unit_factories.Knight) is True


def test_bandit_class():
    assert (first_bandit.__class__ is unit_factories.Bandit) is True
