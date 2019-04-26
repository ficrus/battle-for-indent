import units

knight = units.Knight()
another_knight = units.Knight()

bandit = units.Bandit()
another_bandit = units.Bandit()


def test_inheritance():
    assert isinstance(knight, units.BaseUnit) is True
    assert isinstance(bandit, units.BaseUnit) is True


def test_difference():
    assert (knight is another_knight) is False
    assert (bandit is another_bandit) is False
    assert (knight is bandit) is False


def test_creation():
    assert knight.job == "knight"
    assert bandit.job == "bandit"

    assert knight.hp != 0
    assert bandit.hp != 0


def test_attack():
    health_before = bandit.hp
    knight.attack(bandit)
    health_after = bandit.hp

    assert health_after != health_before
    assert health_after != another_bandit.hp
