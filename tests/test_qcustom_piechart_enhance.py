"""QCustomPieChart enhancements — % callout labels + hatch fills. The QtCharts
pie already renders labels natively; here we verify the convenience %-toggle, the
hatch texture-brush and the CSV Designer props (opt-in, default unchanged)."""

from qtpy.QtGui import QColor


def _pie(qapp):
    from Custom_Widgets.QCustomCharts.QCustomPieChart import QCustomPieChart
    w = QCustomPieChart()
    w.addSeries("S", [("Product", 30), ("Bars", 23), ("Media", 18),
                      ("Pay", 17), ("Other", 12)],
                colors=["#8b5cf6", "#c3f53c", "#1f9bff", "#3a4150", "#5b6472"])
    return w


class TestPieChartEnhancements:
    def test_defaults_unchanged(self, qapp):
        w = _pie(qapp)
        assert w.hatchCsv == ""
        assert w.showPercentLabels is False   # default label layout, not the inside-% toggle
        w.resize(280, 280)
        w.grab()                              # renders

    def test_show_percent_labels_toggle(self, qapp):
        w = _pie(qapp)
        w.setShowPercentLabels(True)
        assert w.showPercentLabels is True
        assert w._show_percentages is True and w._show_values is False
        assert w._labels_position == w.LABELS_POSITION_INSIDE
        w.resize(280, 280); w.grab()

    def test_hatch_brush_is_texture(self, qapp):
        from qtpy.QtCore import Qt
        w = _pie(qapp)
        b = w._hatch_brush(QColor("#3a4150"))
        assert b.style() == Qt.TexturePattern
        assert not b.texture().isNull()

    def test_hatch_csv_roundtrip(self, qapp):
        w = _pie(qapp)
        w.hatchCsv = "3, 4"
        assert w._hatch_indices == {3, 4}
        assert w.hatchCsv == "3,4"
        w.hatchPattern = "cross"
        assert w.hatchPattern == "cross"
        w.resize(280, 280); w.grab()          # rebuilds + paints hatched slices

    def test_set_hatch_indices_api(self, qapp):
        w = _pie(qapp)
        w.setHatchIndices([1])
        w.setHatchPattern("fdiag")
        assert w._hatch_indices == {1}
        assert w._hatch_pattern == "fdiag"
        w.resize(280, 280); w.grab()
