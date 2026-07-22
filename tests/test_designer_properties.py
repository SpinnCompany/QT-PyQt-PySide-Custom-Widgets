"""Custom widget properties exposed to Qt Designer should be typed (int /
Qt enums), not strings. These tests assert the metaobject types and the
value round-trips including legacy string coercion."""
import pytest


def _prop(widget, name):
    mo = widget.metaObject()
    for i in range(mo.propertyCount()):
        if mo.property(i).name() == name:
            return mo.property(i)
    return None


class TestStackedWidgetOrientation:
    def test_transition_direction_is_qt_orientation(self, qapp):
        from qtpy.QtCore import Qt
        from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget

        w = QCustomQStackedWidget()
        p = _prop(w, "transitionDirection")
        assert p is not None and p.isEnumType()
        assert p.typeName() == "Qt::Orientation"

        w.transitionDirection = Qt.Vertical
        assert w.transitionDirection == Qt.Vertical
        w.transitionDirection = "horizontal"  # legacy string still coerced
        assert w.transitionDirection == Qt.Horizontal
        w.setProperty("transitionDirection", Qt.Vertical)
        assert w.property("transitionDirection") == Qt.Vertical


class TestHamburgerPosition:
    def test_position_is_int_with_enum(self, qapp):
        from Custom_Widgets.QCustomHamburgerMenu import QCustomHamburgerMenu

        w = QCustomHamburgerMenu()
        p = _prop(w, "position")
        assert p is not None and p.typeName() == "int"

        w.position = QCustomHamburgerMenu.Position.Top
        assert int(w.property("position")) == 2
        w.position = 1  # from Designer
        assert int(w.property("position")) == 1
        w.position = "Bottom"  # legacy string
        assert int(w.property("position")) == 3
        assert w._position == "Bottom"  # internal string kept for QSS/layout


class TestSidebarSizes:
    SIZE_PROPS = ["defaultWidth", "defaultHeight", "collapsedWidth",
                  "collapsedHeight", "expandedWidth", "expandedHeight"]

    def test_size_props_are_int(self, qapp):
        from Custom_Widgets.QCustomSidebar import QCustomSidebar

        w = QCustomSidebar()
        for name in self.SIZE_PROPS:
            p = _prop(w, name)
            assert p is not None and p.typeName() == "int", name

    def test_match_parent_maps_to_minus_one(self, qapp):
        from Custom_Widgets.QCustomSidebar import QCustomSidebar

        w = QCustomSidebar()
        assert w._sizeToInt("parent") == -1
        assert w._sizeToInt(250) == 250
        assert w._intToSize(-1) == "parent"
        assert w._intToSize(300) == 300
        assert w._intToSize("parent") == "parent"  # legacy string
        assert w._intToSize("250") == 250          # legacy numeric string
