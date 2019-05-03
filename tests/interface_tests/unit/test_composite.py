import interface

composite = interface.GUIComposite()
another_composite = interface.GUIComposite()

leaf = interface.GUILeaf()
another_leaf = interface.GUILeaf()
2

def test_inheritance():
    assert isinstance(composite, interface.GUIComponent) is True
    assert isinstance(another_composite, interface.GUIComponent) is True

    assert isinstance(leaf, interface.GUIComponent) is True
    assert isinstance(another_leaf, interface.GUIComponent) is True


def test_difference():
    assert (composite is another_composite) is False
    assert (leaf is another_leaf) is False
    assert (composite is leaf) is False


def test_type():
    assert composite.is_composite() is True
    assert leaf.is_composite() is False


def test_add_remove():
    composite.add(leaf)
    composite.remove(leaf)


def test_get_leaves():
    assert leaf.get_leaves() == []
    assert composite.get_leaves() == []

    composite.add(leaf)

    assert composite.get_leaves() == [leaf]

    composite.remove(leaf)
