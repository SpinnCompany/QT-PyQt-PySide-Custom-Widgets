"""Bar value labels must show the value, not the template.

QAbstractBarSeries does not speak Python format strings — it substitutes its
own "@value" token and prints everything else verbatim. Handing it "{:.1f}"
painted the literal characters "{:.1f}" on every bar, which shipped in the
documentation screenshot before anyone looked at it.
"""
import pytest

from Custom_Widgets.widgets.charts.qtcharts.QCustomChartConstants import (
    barLabelFormat)


class TestBarLabelFormat:
    def test_decimal_places_are_not_carried_across(self):
        """Qt's precision is SIGNIFICANT DIGITS, formatted with '%g'.

        Reading "{:.1f}" as precision 1 renders 12.4 as "2e+01", so decimal
        places are deliberately dropped in favour of Qt's default.
        """
        assert barLabelFormat("{:.1f}") == ("@value", 6)

    def test_significant_digits_are_carried_across(self):
        """'%g' means the same thing in both languages, so it survives."""
        assert barLabelFormat("{:.3g}") == ("@value", 3)

    def test_default_template_is_translated(self):
        """The shipped default. If this regresses, every bar reads '{:.1f}'."""
        template, _precision = barLabelFormat("{:.1f}")
        assert "{" not in template and "@value" in template

    def test_surrounding_text_is_kept(self):
        assert barLabelFormat("${:,.0f}")[0] == "$@value"
        assert barLabelFormat("{:.2f} kg")[0] == "@value kg"

    def test_qt_native_template_passes_through(self):
        assert barLabelFormat("@value kg")[0] == "@value kg"

    def test_named_and_bare_fields(self):
        assert barLabelFormat("{}")[0] == "@value"
        assert barLabelFormat("{value}")[0] == "@value"

    def test_integer_format_keeps_default_precision(self):
        template, precision = barLabelFormat("{:d}", defaultPrecision=6)
        assert template == "@value" and precision == 6

    def test_template_without_a_placeholder_still_shows_the_value(self):
        """A literal label on every bar is never what the caller meant."""
        assert barLabelFormat("Total")[0] == "@value"

    def test_empty_and_none_are_safe(self):
        assert barLabelFormat("")[0] == "@value"
        assert barLabelFormat(None)[0] == "@value"


class TestBarChartAppliesIt:
    def test_series_gets_a_qt_template_not_a_python_one(self, qapp):
        from Custom_Widgets.widgets.charts.qtcharts.QCustomBarChart import (
            QCustomBarChart)
        chart = QCustomBarChart()
        chart.categoriesCsv = "Jan,Feb,Mar"
        chart.seriesCsv = "Revenue=12.4,19,15"

        from qtpy.QtCharts import QBarSeries
        series = [s for s in chart._chart.series()
                  if isinstance(s, QBarSeries)]
        assert series, "no bar series was created"
        for one in series:
            assert "@value" in one.labelsFormat()
            assert "{" not in one.labelsFormat()
            # 6 significant digits renders 12.4 as "12.4", not "2e+01".
            assert one.labelsPrecision() == 6
