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


class TestEasingProps:
    CASES = [
        ("QCustomSidebar", "QCustomSidebar", "animationEasingCurve"),
        ("QCustomHamburgerMenu", "QCustomHamburgerMenu", "animationEasingCurve"),
        ("QCustomCheckBox", "QCustomCheckBox", "animationEasingCurve"),
        ("QCustomQStackedWidget", "QCustomQStackedWidget", "fadeInCurve"),
        ("QCustomQStackedWidget", "QCustomQStackedWidget", "transitionEasingCurve"),
    ]

    def test_easing_props_are_int(self, qapp):
        import importlib
        from qtpy.QtCore import QEasingCurve
        from qtpy.QtWidgets import QWidget

        parent = QWidget()  # some setters trigger layout that needs a parent
        parent.resize(400, 300)
        for module, cls, prop in self.CASES:
            mod = importlib.import_module(f"Custom_Widgets.{module}")
            w = getattr(mod, cls)(parent)
            p = _prop(w, prop)
            assert p is not None and p.typeName() == "int", f"{cls}.{prop}"
            setattr(w, prop, QEasingCurve.InBounce)   # QEasingCurve.Type
            assert getattr(w, prop) == QEasingCurve.InBounce.value
            setattr(w, prop, "out_quad")              # snake legacy
            assert getattr(w, prop) == QEasingCurve.OutQuad.value


class TestChartProps:
    def test_chart_state_props_are_int(self, qapp):
        import importlib
        from Custom_Widgets.QCustomCharts.QCustomChartConstants import QCustomChartEnums as E

        cases = {
            "QCustomLineChart": ["theme", "legendPosition", "defaultLineStyle", "defaultMarkerStyle"],
            "QCustomBarChart": ["theme", "legendPosition", "labelsPosition"],
            "QCustomPieChart": ["theme", "legendPosition", "labelsPosition"],
            "QCustomHorizontalBarSeries": ["theme", "legendPosition", "barPattern",
                                           "barSelectionMode", "valueLabelsPosition", "labelsPosition"],
            "QCustomVerticalBarSeries": ["theme", "legendPosition", "barPattern",
                                         "barSelectionMode", "valueLabelsPosition", "labelsPosition"],
        }
        for cls, props in cases.items():
            mod = importlib.import_module(f"Custom_Widgets.QCustomCharts.{cls}")
            w = getattr(mod, cls)()
            for name in props:
                p = _prop(w, name)
                assert p is not None and p.typeName() == "int", f"{cls}.{name}"

    def test_chart_enum_roundtrip(self, qapp):
        from Custom_Widgets.QCustomCharts.QCustomLineChart import QCustomLineChart
        from Custom_Widgets.QCustomCharts.QCustomChartConstants import QCustomChartEnums as E

        w = QCustomLineChart()
        w.theme = int(E.ChartTheme.Dark)
        assert w.theme == int(E.ChartTheme.Dark)
        w.legendPosition = int(E.LegendPosition.Right)
        assert w.legendPosition == int(E.LegendPosition.Right)
        w.theme = "Light"  # legacy string coerced
        assert w.theme == int(E.ChartTheme.Light)

    def test_bar_labels_position_roundtrip(self, qapp):
        import importlib
        from Custom_Widgets.QCustomCharts.QCustomChartConstants import QCustomChartEnums as E

        for cls in ("QCustomHorizontalBarSeries", "QCustomVerticalBarSeries"):
            mod = importlib.import_module(f"Custom_Widgets.QCustomCharts.{cls}")
            w = getattr(mod, cls)()
            for name in ("valueLabelsPosition", "labelsPosition"):
                for member in E.BarLabelsPosition:
                    setattr(w, name, int(member))
                    assert getattr(w, name) == int(member), f"{cls}.{name}={member.name}"
            # both aliases stay in sync and coerce legacy strings
            w.valueLabelsPosition = "center"
            assert w.valueLabelsPosition == int(E.BarLabelsPosition.Center)
            assert w.labelsPosition == int(E.BarLabelsPosition.Center)


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
