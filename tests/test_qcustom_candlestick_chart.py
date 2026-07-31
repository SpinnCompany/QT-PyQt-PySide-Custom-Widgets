"""QCustomCandlestickChart — OHLC data, painting, hit-testing, Designer CSV."""

OHLC = [(26, 28, 25, 27),        # up
        (27, 30, 26, 29),        # up
        (29, 29.5, 27, 27.5),    # down
        (27.5, 31, 27, 30.5),    # up
        (30.5, 32, 30, 31)]      # up


class TestCandlestickData:
    def test_set_data(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        assert c.count() == 5
        assert c.data()[0] == (26.0, 28.0, 25.0, 27.0)

    def test_price_range_spans_wicks_not_bodies(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        lo, hi = c.priceRange()
        assert lo == 25.0 and hi == 32.0

    def test_empty_range_is_safe(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart()
        assert c.priceRange() == (0.0, 1.0)
        c.resize(300, 160)
        c.grab()                      # must not raise on an empty series

    def test_flat_series_gets_drawable_range(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=[(10, 10, 10, 10), (10, 10, 10, 10)])
        lo, hi = c.priceRange()
        assert lo < hi                # zero span would divide by zero

    def test_dict_and_list_candles(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=[
            {"open": 1, "high": 3, "low": 0.5, "close": 2},
            [2, 4, 1.5, 3],
        ])
        assert c.count() == 2
        assert c.data()[0] == (1.0, 3.0, 0.5, 2.0)

    def test_malformed_candles_dropped(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=[(1, 2, 0, 1), (1, 2), "junk",
                                          (1, 2, 0, "x"), None])
        assert c.count() == 1

    def test_swapped_high_low_is_normalised(self, qapp):
        """A feed that swaps high/low should still render, not vanish."""
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=[(10, 5, 20, 15)])   # high<low
        o, h, l, cl = c.data()[0]
        assert h == 20.0 and l == 5.0


class TestCandlestickPainting:
    def test_paints_something(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        c.resize(520, 280)
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2

    def test_up_and_down_paint_differently(self, qapp):
        """Direction colouring is the entire point of a candlestick."""
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        up = QCustomCandlestickChart(data=[(10, 12, 9, 11)])
        up.resize(200, 140)
        down = QCustomCandlestickChart(data=[(11, 12, 9, 10)])
        down.resize(200, 140)
        assert up.grab().toImage() != down.grab().toImage()

    def test_doji_still_visible(self, qapp):
        """open == close is a zero-height body; it must not disappear."""
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        doji = QCustomCandlestickChart(data=[(10, 12, 8, 10)])
        doji.resize(200, 140)
        blank = QCustomCandlestickChart()
        blank.resize(200, 140)
        assert doji.grab().toImage() != blank.grab().toImage()

    def test_hollow_up_candles_differ(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        solid = QCustomCandlestickChart(data=OHLC)
        solid.resize(400, 200)
        hollow = QCustomCandlestickChart(data=OHLC)
        hollow.hollowUpCandles = True
        hollow.resize(400, 200)
        assert solid.grab().toImage() != hollow.grab().toImage()

    def test_grid_toggle_changes_render(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        on = QCustomCandlestickChart(data=OHLC)
        on.resize(400, 200)
        off = QCustomCandlestickChart(data=OHLC)
        off.showGrid = False
        off.showPriceAxis = False
        off.resize(400, 200)
        assert on.grab().toImage() != off.grab().toImage()


class TestCandlestickInteraction:
    def test_candle_at_maps_x_to_index(self, qapp):
        from qtpy.QtCore import QPoint
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        c.resize(520, 280)
        c.grab()                                  # populate hit rects
        plot_mid_y = c.height() // 2
        first = c.candleAt(QPoint(int(c._plotRect().left()) + 4, plot_mid_y))
        last = c.candleAt(QPoint(int(c._plotRect().right()) - 4, plot_mid_y))
        assert first == 0 and last == len(OHLC) - 1

    def test_candle_at_outside_plot_is_minus_one(self, qapp):
        from qtpy.QtCore import QPoint
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        c.resize(520, 280)
        c.grab()
        assert c.candleAt(QPoint(0, 0)) == -1     # left of the plot, above it

    def test_hover_signal(self, qapp):
        from qtpy.QtCore import QPoint, QEvent, QPointF
        from qtpy.QtGui import QMouseEvent
        from qtpy.QtCore import Qt
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        c.resize(520, 280)
        c.grab()
        seen = []
        c.candleHovered.connect(seen.append)
        x = c._plotRect().left() + 4
        ev = QMouseEvent(QEvent.MouseMove, QPointF(x, c.height() / 2),
                         Qt.NoButton, Qt.NoButton, Qt.NoModifier)
        c.mouseMoveEvent(ev)
        assert seen == [0]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert seen == [0, -1]


class TestCandlestickDesigner:
    def test_ohlc_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart()
        c.ohlcCsv = "1,3,0.5,2;2,4,1.5,3"
        assert c.count() == 2
        assert c.data()[1] == (2.0, 4.0, 1.5, 3.0)
        assert c.ohlcCsv == "1,3,0.5,2;2,4,1.5,3"

    def test_ohlc_csv_skips_short_and_bad_chunks(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart()
        c.ohlcCsv = "1,3,0.5,2;bad;1,2;4,5,6,x;5,7,4,6"
        assert c.count() == 2

    def test_labels_csv(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart(data=OHLC)
        c.labelsCsv = "Mon,Tue,Wed,Thu,Fri"
        assert c.labels() == ["Mon", "Tue", "Wed", "Thu", "Fri"]
        assert c.labelsCsv == "Mon,Tue,Wed,Thu,Fri"

    def test_numeric_designer_properties_clamp(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        c = QCustomCandlestickChart()
        c.candleWidthRatio = 5.0
        assert c.candleWidthRatio == 1.0
        c.candleWidthRatio = -1
        assert c.candleWidthRatio == 0.05
        c.gridLines = 0
        assert c.gridLines == 1
        c.pricePrecision = -3
        assert c.pricePrecision == 0

    def test_no_qtcharts_dependency(self, qapp):
        """Load-bearing: QtCharts is GPLv3-only, so a Pro wheel cannot use it.

        Checks the import graph, not the text — the module docstring explains
        the constraint and would trip a naive substring search.
        """
        import ast
        import Custom_Widgets.QCustomCandlestickChart as mod
        tree = ast.parse(open(mod.__file__).read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any("QtChart" in name for name in imported), imported

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomCandlestickChart import QCustomCandlestickChart
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = QCustomCandlestickChart(data=OHLC)
        c.ensurePolished()
        assert c.upColor.name().lower() == "#16a34a"      # success
        assert c.downColor.name().lower() == "#dc2626"    # destructive
        qapp.setStyleSheet("")
