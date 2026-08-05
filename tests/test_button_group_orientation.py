"""Regression: QCustomButtonGroup.orientation was a Designer-exposed stub —
setting it after construction did nothing, so a .ui-promoted group was
permanently vertical (uic can only set properties post-construction).
"""
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout


def _group(qapp):
    from Custom_Widgets.QCustomButtonGroup import QCustomButtonGroup

    group = QCustomButtonGroup()
    for label in ("Day", "Week", "Month"):
        group.addButton(label)
    group.setSelectedId(1)
    return group


def test_orientation_setter_switches_layout(qapp):
    group = _group(qapp)
    assert isinstance(group.layout(), QVBoxLayout)

    group.orientation = "horizontal"  # the uic/.ui setProperty path
    assert isinstance(group.layout(), QHBoxLayout)
    assert group.orientation == "horizontal"

    # Buttons survive the swap: same order, same parent, selection intact.
    layout = group.layout()
    texts = [layout.itemAt(i).widget().text() for i in range(layout.count())]
    assert texts == ["Day", "Week", "Month"]
    assert all(layout.itemAt(i).widget().parent() is group
               for i in range(layout.count()))
    assert group.selectedId() == 1
    assert group.selectedText() == "Week"

    group.orientation = "vertical"
    assert isinstance(group.layout(), QVBoxLayout)
    assert group.selectedId() == 1


def test_orientation_noop_and_normalization(qapp):
    group = _group(qapp)
    layout_before = group.layout()
    group.orientation = "vertical"  # unchanged -> same layout object
    assert group.layout() is layout_before
    group.orientation = "HORIZONTAL"  # case-insensitive
    assert isinstance(group.layout(), QHBoxLayout)
    group.orientation = "sideways"  # unknown -> vertical (ctor behaviour)
    assert isinstance(group.layout(), QVBoxLayout)
