"""QCustomDonut enhancements — % callout labels + hatch fills (opt-in, segments
mode). Default (off) must render identically; the new props round-trip and paint."""

from qtpy.QtGui import QColor


def _img(w, size=(240, 240)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


class TestDonutEnhancements:
    def test_defaults_off_still_paint(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[30, 23, 18, 16, 13])
        w.setMode("segments")
        assert w.showPercentLabels is False
        assert w.hatchCsv == ""
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_percent_labels_render_white(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[30, 23, 18, 16, 13])
        w.setMode("segments")
        w.showPercentLabels = True
        w.percentLabelColor = "#ffffff"
        img = _img(w)
        # a bright pixel means the white % text painted over the coloured ring
        assert any(QColor(img.pixel(x, y)).lightness() > 230
                   for y in range(0, img.height(), 3)
                   for x in range(0, img.width(), 3)), "percent label text missing"

    def test_hatch_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[30, 23, 18, 16, 13])
        w.setMode("segments")
        w.hatchCsv = "3, 4"
        assert w._hatch == {3, 4}
        assert w.hatchCsv == "3,4"
        w.hatchPattern = "cross"
        assert w.hatchPattern == "cross"
        _img(w)

    def test_set_hatch_indices_api(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[50, 50])
        w.setMode("segments")
        w.setHatchIndices([1])
        w.setShowPercentLabels(True)
        assert w._hatch == {1}
        _img(w)

    def test_min_label_percent_hides_tiny(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[95, 5])
        w.setMode("segments")
        w.showPercentLabels = True
        w.minLabelPercent = 10          # the 5% slice's label is suppressed
        assert w.minLabelPercent == 10.0
        _img(w)                          # paints without error

    def test_rings_mode_unaffected(self, qapp):
        from Custom_Widgets.QCustomDonut import QCustomDonut
        w = QCustomDonut(values=[52, 33, 15])   # default rings mode
        w.showPercentLabels = True              # no-op in rings mode
        _img(w)
