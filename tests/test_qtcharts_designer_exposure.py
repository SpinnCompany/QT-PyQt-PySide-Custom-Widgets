"""The QtCharts widgets must be fully authorable in Qt Designer.

They exposed 27-37 styling properties but no way to put data in them, so a
form author could pick colours and legends and still be left with an empty
chart. These cover the data entry, the catalog and the module paths.

Imported through the flat public path, which is what .ui headers carry.
"""
import importlib
import os

import pytest

pytest.importorskip("qtpy.QtCharts", reason="QtCharts not available")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS = ["QCustomLineChart", "QCustomAreaChart", "QCustomBarChart",
          "QCustomPieChart"]


def _chart(name):
    module = importlib.import_module("Custom_Widgets.QCustomCharts.%s" % name)
    return getattr(module, name)()


@pytest.mark.parametrize("name", CHARTS)
class TestDesignerContract:
    def test_declares_designer_constants(self, qapp, name):
        module = importlib.import_module("Custom_Widgets.QCustomCharts.%s" % name)
        cls = getattr(module, name)
        for attr in ("WIDGET_ICON", "WIDGET_TOOLTIP", "WIDGET_MODULE",
                     "WIDGET_DOM_XML", "__catalog__"):
            assert hasattr(cls, attr), "%s lacks %s" % (name, attr)

    def test_widget_module_is_per_class(self, qapp, name):
        """Designer writes this into the .ui <header>.

        All four used to share "Custom_Widgets.QCustomCharts", which is the
        package: it collapsed every generated stub onto one path and wrote a
        coarser header than the .ui files in this repo already carry.
        """
        module = importlib.import_module("Custom_Widgets.QCustomCharts.%s" % name)
        cls = getattr(module, name)
        assert cls.WIDGET_MODULE == "Custom_Widgets.QCustomCharts.%s" % name
        # and it must actually import
        importlib.import_module(cls.WIDGET_MODULE)

    def test_catalog_matches_the_real_metaobject(self, qapp, name):
        """A catalog that drifts from the metaObject misleads the MCP server."""
        from qtpy.QtWidgets import QWidget
        module = importlib.import_module("Custom_Widgets.QCustomCharts.%s" % name)
        cls = getattr(module, name)
        meta = cls.staticMetaObject
        first = QWidget.staticMetaObject.propertyCount()
        declared = {meta.property(i).name()
                    for i in range(first, meta.propertyCount())}
        catalogued = set(cls.__catalog__["props"])
        assert catalogued == declared, (
            "catalog drift: missing=%s extra=%s"
            % (sorted(declared - catalogued), sorted(catalogued - declared)))

    def test_stub_exists_at_the_public_path(self, qapp, name):
        stub = os.path.join(REPO, "Custom_Widgets", "QCustomCharts", name + ".pyi")
        assert os.path.isfile(stub)

    def test_csv_properties_are_designer_visible(self, qapp, name):
        """Settable through the Qt property system, which is how a .ui applies
        them — not merely present as Python attributes."""
        from qtpy.QtWidgets import QWidget
        module = importlib.import_module("Custom_Widgets.QCustomCharts.%s" % name)
        cls = getattr(module, name)
        meta = cls.staticMetaObject
        first = QWidget.staticMetaObject.propertyCount()
        names = {meta.property(i).name()
                 for i in range(first, meta.propertyCount())}
        assert {"seriesCsv", "categoriesCsv"} <= names


@pytest.mark.parametrize("name", CHARTS)
class TestCsvDataEntry:
    def test_round_trips(self, qapp, name):
        chart = _chart(name)
        chart.setProperty("seriesCsv", "Revenue=10,20,30;Costs=5,8,12")
        assert chart.property("seriesCsv") == "Revenue=10,20,30;Costs=5,8,12"

    def test_unnamed_series_gets_a_name(self, qapp, name):
        chart = _chart(name)
        chart.setProperty("seriesCsv", "10,20,30")
        assert chart.property("seriesCsv") == "Series 1=10,20,30"

    def test_reapplying_replaces_rather_than_appends(self, qapp, name):
        """A .ui describes the whole chart; re-applying must not stack."""
        chart = _chart(name)
        chart.setProperty("seriesCsv", "A=1,2,3")
        chart.setProperty("seriesCsv", "A=1,2,3")
        chart.setProperty("seriesCsv", "A=1,2,3")
        assert chart.property("seriesCsv") == "A=1,2,3"
        assert len(chart.getChart().series()) <= 2   # bar packs sets into one

    def test_malformed_csv_does_not_raise(self, qapp, name):
        """A bad property in a .ui must not abort loading the form."""
        chart = _chart(name)
        chart.setProperty("seriesCsv", "garbage;;=,,;A=notanumber")
        chart.setProperty("categoriesCsv", "")
        chart.setProperty("seriesCsv", "")

    def test_categories_round_trip(self, qapp, name):
        chart = _chart(name)
        chart.setProperty("categoriesCsv", "Jan, Feb ,Mar,")
        assert chart.property("categoriesCsv") == "Jan,Feb,Mar"


class TestDataReachesTheChart:
    def test_line_series_become_xy_points(self, qapp):
        chart = _chart("QCustomLineChart")
        chart.setProperty("seriesCsv", "Revenue=10,20,30;Costs=5,8,12")
        series = chart.getChart().series()
        assert [s.name() for s in series] == ["Revenue", "Costs"]
        points = series[0].points()
        assert [(p.x(), p.y()) for p in points] == [(0.0, 10.0), (1.0, 20.0), (2.0, 30.0)]

    def test_area_series_named(self, qapp):
        chart = _chart("QCustomAreaChart")
        chart.setProperty("seriesCsv", "Revenue=10,20,30")
        assert [s.name() for s in chart.getChart().series()] == ["Revenue"]

    def test_bar_sets_carry_names_and_values(self, qapp):
        chart = _chart("QCustomBarChart")
        chart.setProperty("categoriesCsv", "Jan,Feb,Mar")
        chart.setProperty("seriesCsv", "Revenue=10,20,30;Costs=5,8,12")
        series = chart.getChart().series()[0]
        got = [(bs.label(), [bs.at(i) for i in range(bs.count())])
               for bs in series.barSets()]
        assert got == [("Revenue", [10.0, 20.0, 30.0]),
                       ("Costs", [5.0, 8.0, 12.0])]

    def test_pie_slices_take_labels_from_categories(self, qapp):
        chart = _chart("QCustomPieChart")
        chart.setProperty("categoriesCsv", "Jan,Feb,Mar")
        chart.setProperty("seriesCsv", "Revenue=10,20,30")
        series = chart.getChart().series()[0]
        assert [s.value() for s in series.slices()] == [10.0, 20.0, 30.0]
        # the category name reaches the legend even when the slice label is
        # replaced by percentage formatting
        legend = [m.label() for m in chart.getChart().legend().markers()]
        assert legend == ["Jan", "Feb", "Mar"]

    def test_pie_falls_back_when_categories_are_short(self, qapp):
        chart = _chart("QCustomPieChart")
        chart.setProperty("categoriesCsv", "Jan")
        chart.setProperty("seriesCsv", "Revenue=10,20,30")
        legend = [m.label() for m in chart.getChart().legend().markers()]
        assert legend == ["Jan", "Slice 2", "Slice 3"]

    def test_categories_set_after_series_still_apply(self, qapp):
        """Order in a .ui is not guaranteed, so the later one must rebuild."""
        chart = _chart("QCustomPieChart")
        chart.setProperty("seriesCsv", "Revenue=10,20,30")
        chart.setProperty("categoriesCsv", "Jan,Feb,Mar")
        legend = [m.label() for m in chart.getChart().legend().markers()]
        assert legend == ["Jan", "Feb", "Mar"]


class TestNoQtChartsLeakIntoPaintedCharts:
    def test_painted_charts_stay_clean(self, qapp):
        """The painted charts must not acquire a QtCharts dependency.

        QtCharts is GPLv3-or-commercial with no LGPL option, so anything
        importing it cannot ship in a proprietary wheel.
        """
        import ast
        base = os.path.join(REPO, "Custom_Widgets", "widgets", "charts")
        offenders = []
        for filename in sorted(os.listdir(base)):
            if not filename.endswith(".py"):
                continue
            tree = ast.parse(open(os.path.join(base, filename),
                                  encoding="utf-8").read())
            for node in ast.walk(tree):
                mods = []
                if isinstance(node, ast.Import):
                    mods = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    mods = [node.module]
                if any("QtChart" in m for m in mods):
                    offenders.append(filename)
        assert not offenders, "QtCharts leaked into painted charts: %s" % offenders
