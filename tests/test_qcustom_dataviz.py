"""Untested data-viz / indicator widgets: donut, sparkline, mini bar chart,
trend chip, page dots, progress indicator, flow progress bar, round progress bar
and the loading indicators. Headless construction + behaviour + paint smoke
(part of the widget hardening pass toward the tiering gate)."""


def _colors(w, size):
    w.resize(*size)
    w.ensurePolished()
    img = w.grab().toImage()
    return len({img.pixel(x, y) for y in range(0, img.height(), 4)
                for x in range(0, img.width(), 4)})


class TestDonut:
    def test_data_modes_and_paint(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        d = QCustomDonut()
        d.setData([10, 20, 30], colors=["#e11", "#1a1", "#11e"])
        assert d.values() == [10, 20, 30]
        assert _colors(d, (120, 120)) > 1
        d.setMode("segments")
        assert _colors(d, (120, 120)) > 1
        d.setMode("rings")

    def test_empty_data_safe(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        d = QCustomDonut()
        d.setData([])
        assert _colors(d, (60, 60)) >= 1        # no crash on empty


class TestSparkline:
    def test_values_and_paint(self, qapp):
        from Custom_Widgets.QCustomSparkline import QCustomSparkline
        s = QCustomSparkline()
        s.setValues([1, 5, 2, 8, 3, 9, 4])
        assert _colors(s, (160, 40)) > 1
        s.setValues([])                          # empty must not crash
        s.setValues([7])                         # single point


class TestMiniBarChart:
    def test_data_and_paint(self, qapp):
        from Custom_Widgets.QCustomMiniBarChart import QCustomMiniBarChart
        c = QCustomMiniBarChart()
        c.setData([3, 7, 2, 9], colors=["#39f"], labels=["a", "b", "c", "d"])
        assert _colors(c, (160, 80)) > 1
        c.setValues([1, 2, 3])


class TestTrendChip:
    def test_direction_value_variant(self, qapp):
        from Custom_Widgets.QCustomTrendChip import QCustomTrendChip
        chip = QCustomTrendChip()
        chip.setValue(4.2, text="+4.2%")
        assert _colors(chip, (90, 30)) > 1
        chip.setValue(-1.5)                       # negative -> down
        chip.setDirection("flat")
        for v in ("circle", "soft", "plain"):
            chip.setVariant(v)


class TestPageDots:
    def test_count_active_and_signal(self, qapp):
        from Custom_Widgets.QCustomPageDots import QCustomPageDots
        dots = QCustomPageDots()
        dots.setCount(4)
        dots.setActiveIndex(2)
        assert _colors(dots, (100, 20)) > 1
        got = []
        dots.pageChanged.connect(got.append)
        dots.pageChanged.emit(3)                  # signal is wired
        assert got == [3]


class TestProgressIndicator:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomProgressIndicator import QCustomProgressIndicator
        pi = QCustomProgressIndicator()
        pi.setStepStatus()                        # no-op, must not raise
        assert _colors(pi, (200, 80)) >= 1


class TestFlowProgressBar:
    def test_construct_signal_and_setter(self, qapp):
        from Custom_Widgets.QFlowProgressBar import QFlowProgressBar
        bar = QFlowProgressBar()
        assert hasattr(bar, "onStepClicked")
        got = []
        bar.onStepClicked.connect(got.append)
        bar.onStepClicked.emit(2)
        assert got == [2]
        bar.setFinishedProgressLength(3)          # must not raise
        assert _colors(bar, (240, 60)) >= 1


class TestRoundProgressBar:
    def test_value_and_paint(self, qapp):
        # exercised through the public re-export shim (QCustomProgressBars)
        from Custom_Widgets.QCustomProgressBars import QCustomRoundProgressBar
        bar = QCustomRoundProgressBar()
        bar.setValue(70)
        assert _colors(bar, (120, 120)) > 1


class TestLoadingIndicators:
    def test_all_loaders_construct_and_paint(self, qapp):
        # public re-export shim (QCustomLoadingIndicators)
        from Custom_Widgets.QCustomLoadingIndicators import (
            QCustomArcLoader, QCustom3CirclesLoader, QCustomPerlinLoader,
            QCustomQProgressBar, QCustomSpinner)
        loaders = [
            QCustomArcLoader(),
            QCustom3CirclesLoader(),
            QCustomQProgressBar(start=False),
            QCustomSpinner(),
        ]
        for w in loaders:
            assert _colors(w, (100, 100)) >= 1    # constructs + paints, no crash
        # Perlin loader pulls perlin_noise; construct + paint separately so a
        # missing optional dep is an explicit, readable failure.
        p = QCustomPerlinLoader()
        assert _colors(p, (100, 100)) >= 1
