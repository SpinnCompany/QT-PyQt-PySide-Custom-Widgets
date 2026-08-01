"""QtCharts must follow the design tokens.

A QChart paints into a QGraphicsScene, so the token QSS that styles every other
widget in the library cannot reach it. Its "App Theme" instead read QCustomTheme
— a separate system that reports dark whenever no theme JSON is loaded — so an
app calling applyDesignTokens(app, theme="light") got a black chart on a white
page. Every generated chart screenshot shipped that way.
"""
import pytest

from Custom_Widgets.JSonStyles.tokens import (
    DesignTokens, activeDesignTokens, applyDesignTokens)


@pytest.fixture
def lineChart(qapp):
    from Custom_Widgets.widgets.charts.qtcharts.QCustomLineChart import (
        QCustomLineChart)

    def build():
        chart = QCustomLineChart()
        chart.categoriesCsv = "Jan,Feb,Mar"
        chart.seriesCsv = "Revenue=12,19,15"
        return chart
    return build


class TestActiveTokens:
    def test_apply_records_what_is_live(self, qapp):
        applyDesignTokens(qapp, theme="dark")
        assert activeDesignTokens().theme == "dark"
        applyDesignTokens(qapp, theme="light")
        assert activeDesignTokens().theme == "light"
        qapp.setStyleSheet("")


class TestChartFollowsTokens:
    @pytest.mark.parametrize("theme", ["light", "dark"])
    def test_app_theme_paints_the_token_surface(self, qapp, lineChart, theme):
        applyDesignTokens(qapp, theme=theme)
        chart = lineChart()
        assert chart.theme == 0, "should still be on App Theme"

        expected = DesignTokens(theme=theme).role("surface").lower()
        assert chart._chart.backgroundBrush().color().name().lower() == expected
        assert (chart._chart.plotAreaBackgroundBrush().color().name().lower()
                == expected)
        qapp.setStyleSheet("")

    def test_light_and_dark_actually_differ(self, qapp, lineChart):
        """Guards the failure this replaced: both themes painting the same."""
        applyDesignTokens(qapp, theme="light")
        light = lineChart()._chart.backgroundBrush().color().name()
        applyDesignTokens(qapp, theme="dark")
        dark = lineChart()._chart.backgroundBrush().color().name()
        assert light != dark
        qapp.setStyleSheet("")

    def test_text_is_readable_on_the_surface(self, qapp, lineChart):
        """on-surface, not a hardcoded black that vanishes in dark."""
        applyDesignTokens(qapp, theme="dark")
        chart = lineChart()
        surface = chart._chart.backgroundBrush().color()
        for axis in chart._chart.axes():
            label = axis.labelsColor()
            assert abs(label.lightness() - surface.lightness()) > 60, (
                "axis labels are invisible against the plot background")
        qapp.setStyleSheet("")


class TestPresentationSurvivesData:
    """Applying data must not discard explicitly-set presentation."""

    def test_titles_set_before_data_survive(self, qapp):
        from Custom_Widgets.widgets.charts.qtcharts.QCustomLineChart import (
            QCustomLineChart)
        chart = QCustomLineChart()
        chart.xAxisTitle = "Month"
        chart.yAxisTitle = "$k"
        chart.categoriesCsv = "Jan,Feb,Mar"
        chart.seriesCsv = "Revenue=12,19,15"
        assert chart.xAxisTitle == "Month"
        assert chart._axis_x.titleText() == "Month"
        assert chart.yAxisTitle == "$k"

    def test_titles_set_after_data_survive(self, qapp):
        from Custom_Widgets.widgets.charts.qtcharts.QCustomLineChart import (
            QCustomLineChart)
        chart = QCustomLineChart()
        chart.categoriesCsv = "Jan,Feb,Mar"
        chart.seriesCsv = "Revenue=12,19,15"
        chart.xAxisTitle = "Month"
        assert chart._axis_x.titleText() == "Month"
