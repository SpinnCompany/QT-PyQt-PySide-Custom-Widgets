"""QCustomFunnelChart — stages, band geometry, pyramid mode, Designer CSV."""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

STAGES = [("Visits", 1000), ("Signups", 420), ("Trials", 180), ("Paid", 64)]


def _chart(stages=STAGES, size=(360, 300)):
    from Custom_Widgets.QCustomFunnelChart import QCustomFunnelChart
    c = QCustomFunnelChart(stages=list(stages))
    c.resize(*size)
    return c


class TestFunnelData:
    def test_stages(self, qapp):
        c = _chart()
        assert c.stageCount() == 4
        assert c.stages()[0] == ("Visits", 1000.0)

    def test_accepts_dicts(self, qapp):
        c = _chart([{"label": "A", "value": 10}, ("B", 5)])
        assert c.stages() == [("A", 10.0), ("B", 5.0)]

    def test_malformed_stages_dropped(self, qapp):
        c = _chart([("A", 10), ("B",), None, ("C", "x"), "junk"])
        assert c.stageCount() == 1

    def test_negative_values_clamped(self, qapp):
        c = _chart([("A", -5)])
        assert c.stages()[0][1] == 0.0

    def test_maximum_never_zero(self, qapp):
        """Zero would divide by zero in the width mapping."""
        assert _chart([("A", 0), ("B", 0)]).maximum() == 1.0

    def test_empty_is_safe(self, qapp):
        c = _chart([])
        assert c.stageCount() == 0 and c.maximum() == 1.0
        c.grab()

    def test_clear(self, qapp):
        c = _chart()
        c.clearStages()
        assert c.stageCount() == 0


class TestFunnelPercent:
    def test_percent_of_first(self, qapp):
        c = _chart()
        assert c.percentFor(0) == 100.0
        assert round(c.percentFor(1), 1) == 42.0

    def test_percent_of_previous(self, qapp):
        c = _chart()
        c.percentOf = "previous"
        assert c.percentFor(0) == 100.0
        assert round(c.percentFor(1), 1) == 42.0
        assert round(c.percentFor(2), 1) == round(180 / 420 * 100, 1)

    def test_percent_out_of_range(self, qapp):
        assert _chart().percentFor(99) == 0.0

    def test_percent_with_zero_base(self, qapp):
        c = _chart([("A", 0), ("B", 5)])
        assert c.percentFor(1) == 0.0


class TestFunnelGeometry:
    def test_one_band_per_stage(self, qapp):
        c = _chart()
        c.grab()
        assert len(c.bands()) == 4

    def test_bands_are_continuous(self, qapp):
        """Each band's far edge must match the next band's near edge, or the
        funnel comes apart at every seam."""
        c = _chart()
        c.gapPx = 0
        c.grab()
        bands = c.bands()
        for i in range(len(bands) - 1):
            lower = bands[i]
            upper = bands[i + 1]
            assert abs(lower.at(3).x() - upper.at(0).x()) < 0.5
            assert abs(lower.at(2).x() - upper.at(1).x()) < 0.5

    def test_pyramid_is_continuous_too(self, qapp):
        """Mirroring keeps list order, so band 0 is still the largest value —
        it just moves to the bottom. Seams therefore run the other way."""
        c = _chart()
        c.shape = "pyramid"
        c.gapPx = 0
        c.grab()
        bands = c.bands()
        for i in range(len(bands) - 1):
            assert abs(bands[i].boundingRect().top()
                       - bands[i + 1].boundingRect().bottom()) < 0.5

    def test_pyramid_puts_the_widest_band_at_the_bottom(self, qapp):
        funnel = _chart()
        funnel.grab()
        pyramid = _chart()
        pyramid.shape = "pyramid"
        pyramid.grab()

        def widestTop(chart):
            bands = chart.bands()
            widest = max(bands, key=lambda b: b.boundingRect().width())
            return widest.boundingRect().top(), chart.height()

        funnelTop, height = widestTop(funnel)
        pyramidTop, _ = widestTop(pyramid)
        assert funnelTop < height / 2 < pyramidTop

    def test_band_width_tracks_value(self, qapp):
        c = _chart()
        c.grab()
        widths = [b.boundingRect().width() for b in c.bands()]
        assert widths == sorted(widths, reverse=True)

    def test_neck_ratio_floors_the_taper(self, qapp):
        pointed = _chart()
        pointed.grab()
        spouted = _chart()
        spouted.neckRatio = 0.5
        spouted.grab()
        assert spouted.bands()[-1].boundingRect().width() > \
            pointed.bands()[-1].boundingRect().width()

    def test_horizontal_bands_run_across(self, qapp):
        c = _chart()
        c.orientation = "horizontal"
        c.grab()
        boxes = [b.boundingRect() for b in c.bands()]
        assert boxes[1].left() > boxes[0].left()


class TestFunnelInteraction:
    def test_stage_at(self, qapp):
        c = _chart()
        c.grab()
        centre = c.bands()[0].boundingRect().center()
        assert c.stageAt(centre) == 0

    def test_stage_at_misses(self, qapp):
        c = _chart()
        c.grab()
        assert c.stageAt(QPointF(1, 1)) == -1

    def test_hover_signal(self, qapp):
        c = _chart()
        c.grab()
        seen = []
        c.stageHovered.connect(seen.append)
        c.mouseMoveEvent(QMouseEvent(
            QEvent.MouseMove, c.bands()[0].boundingRect().center(),
            Qt.NoButton, Qt.NoButton, Qt.NoModifier))
        assert seen == [0]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert seen == [0, -1]

    def test_click_signal(self, qapp):
        c = _chart()
        c.grab()
        seen = []
        c.stageClicked.connect(seen.append)
        c.mouseReleaseEvent(QMouseEvent(
            QEvent.MouseButtonRelease, c.bands()[1].boundingRect().center(),
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
        assert seen == [1]


class TestFunnelDesigner:
    def test_stages_csv_roundtrip(self, qapp):
        c = _chart([])
        c.stagesCsv = "Visits=1000,Signups=420"
        assert c.stageCount() == 2
        assert c.stagesCsv == "Visits=1000,Signups=420"

    def test_stages_csv_unnamed(self, qapp):
        c = _chart([])
        c.stagesCsv = "100,50"
        assert [l for l, _v in c.stages()] == ["Stage 1", "Stage 2"]

    def test_stages_csv_skips_junk(self, qapp):
        c = _chart([])
        c.stagesCsv = "A=10,,B=notanumber,C=5"
        assert [l for l, _v in c.stages()] == ["A", "C"]

    def test_colors_csv(self, qapp):
        c = _chart()
        c.colorsCsv = "#ff0000,#00ff00"
        assert c.stageColor(0).name() == "#ff0000"
        assert c.stageColor(1).name() == "#00ff00"
        assert c.stageColor(3).isValid()        # falls back to the palette

    def test_enums_fall_back(self, qapp):
        c = _chart()
        c.shape = "nonsense"
        c.orientation = "nonsense"
        c.percentOf = "nonsense"
        assert c.shape == "funnel"
        assert c.orientation == "vertical"
        assert c.percentOf == "first"

    def test_numeric_properties_clamp(self, qapp):
        c = _chart()
        c.gapPx = -5
        c.neckRatio = 5
        assert c.gapPx == 0 and c.neckRatio == 1.0


class TestFunnelPainting:
    def test_paints(self, qapp):
        c = _chart()
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 2

    def test_funnel_and_pyramid_render_differently(self, qapp):
        f = _chart()
        p = _chart()
        p.shape = "pyramid"
        assert f.grab().toImage() != p.grab().toImage()

    def test_orientation_changes_render(self, qapp):
        v = _chart()
        h = _chart()
        h.orientation = "horizontal"
        assert v.grab().toImage() != h.grab().toImage()

    def test_percent_labels_change_render(self, qapp):
        off = _chart()
        on = _chart()
        on.showPercent = True
        assert off.grab().toImage() != on.grab().toImage()

    def test_no_qtcharts_import(self, qapp):
        import ast
        import Custom_Widgets.QCustomFunnelChart as mod
        tree = ast.parse(open(mod.__file__, encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any("QtChart" in n for n in imported), imported

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = _chart()
        c.ensurePolished()
        assert c.outsideLabelColor.name().lower() == "#0f172a"
        qapp.setStyleSheet("")
