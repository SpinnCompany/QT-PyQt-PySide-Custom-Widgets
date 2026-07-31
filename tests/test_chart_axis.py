"""Shared cartesian axis maths — pure functions, no Qt needed.

Extracted from QCustomCandlestickChart when QCustomScatterChart became the
second consumer. Three divergent implementations of "nice ticks" is how charts
end up disagreeing about where round numbers fall.
"""
import pytest

from Custom_Widgets.widgets.charts._chart_axis import (
    formatTick, niceNumber, niceTicks, thinLabels, tickValues)


class TestNiceNumber:
    @pytest.mark.parametrize("value,expected", [
        (1.0, 1.0), (1.4, 1.0), (1.6, 2.0), (2.9, 2.0),
        (4.0, 5.0), (7.5, 10.0), (10.0, 10.0),
    ])
    def test_rounds_to_1_2_5_10(self, value, expected):
        assert niceNumber(value) == expected

    def test_scales_across_magnitudes(self):
        assert niceNumber(1400) == 1000.0
        assert niceNumber(0.014) == pytest.approx(0.01)

    def test_non_positive_is_zero(self):
        assert niceNumber(0) == 0.0
        assert niceNumber(-5) == 0.0


class TestNiceTicks:
    def test_range_covers_the_data(self):
        start, stop, step = niceTicks(3, 17)
        assert start <= 3 and stop >= 17 and step > 0

    def test_lands_on_round_numbers(self):
        start, stop, step = niceTicks(0, 97)
        assert step in (10.0, 20.0, 25.0)
        assert start % step == 0

    def test_reversed_input_is_normalised(self):
        assert niceTicks(17, 3) == niceTicks(3, 17)

    def test_flat_range_is_widened(self):
        """A zero-width range would divide by zero in every consumer."""
        start, stop, _step = niceTicks(5, 5)
        assert stop > start

    def test_flat_zero_range_is_widened(self):
        start, stop, _step = niceTicks(0, 0)
        assert stop > start

    def test_nan_falls_back(self):
        start, stop, _step = niceTicks(float("nan"), float("nan"))
        assert stop > start


class TestTickValues:
    def test_includes_both_ends(self):
        ticks = tickValues(0, 100, 5)
        assert ticks[0] <= 0 and ticks[-1] >= 100

    def test_evenly_spaced(self):
        ticks = tickValues(0, 100, 5)
        steps = {round(ticks[i + 1] - ticks[i], 9) for i in range(len(ticks) - 1)}
        assert len(steps) == 1

    def test_does_not_run_away_on_tiny_ranges(self):
        """Float drift in the accumulator must not spin forever."""
        assert len(tickValues(0, 1e-9, 5)) < 1000

    def test_last_tick_not_skipped_by_float_drift(self):
        ticks = tickValues(0, 0.3, 3)
        assert ticks[-1] >= 0.3 - 1e-9


class TestFormatTick:
    def test_integer_steps_have_no_decimals(self):
        assert formatTick(5.0, 1) == "5"
        assert formatTick(1000.0, 100) == "1000"

    def test_fractional_steps_keep_enough_decimals(self):
        assert formatTick(0.25, 0.25) == "0.25"
        assert formatTick(0.5, 0.1) == "0.5"


class TestThinLabels:
    def _width(self, text):
        return len(text) * 7

    def test_keeps_all_when_they_fit(self):
        labels = ["a", "b", "c"]
        assert thinLabels(labels, 600, self._width) == [0, 1, 2]

    def test_thins_when_cramped(self):
        labels = ["label%d" % i for i in range(20)]
        kept = thinLabels(labels, 200, self._width)
        assert 0 < len(kept) < 20

    def test_always_keeps_the_first(self):
        labels = ["long label %d" % i for i in range(40)]
        assert thinLabels(labels, 50, self._width)[0] == 0

    def test_empty_is_safe(self):
        assert thinLabels([], 100, self._width) == []
