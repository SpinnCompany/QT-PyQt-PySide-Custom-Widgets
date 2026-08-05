"""QCustomGradientPicker — stops, interpolation, editing, Designer CSV."""
from qtpy.QtCore import Qt, QEvent, QPointF
from qtpy.QtGui import QColor, QKeyEvent, QMouseEvent


def _press(widget, x, y):
    widget.mousePressEvent(QMouseEvent(
        QEvent.MouseButtonPress, QPointF(x, y),
        Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))


def _key(widget, key):
    widget.keyPressEvent(QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier, ""))


class TestGradientStops:
    def test_default_two_stops(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.count() == 2
        assert g.stopPosition(0) == 0.0 and g.stopPosition(1) == 1.0

    def test_stops_are_kept_sorted(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(1.0, "#ff0000"), (0.0, "#0000ff"),
                                         (0.5, "#00ff00")])
        assert [p for p, _ in g.stops()] == [0.0, 0.5, 1.0]

    def test_fewer_than_two_stops_rejected(self, qapp):
        """A one-stop gradient is a fill; allowing it burdens every consumer."""
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.setStops([(0.0, "#ff0000")]) is False
        assert g.count() == 2

    def test_invalid_stops_dropped(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.setStops([(0.0, "#ff0000"), (0.5, "not-a-colour"),
                           ("x", "#00ff00"), (1.0, "#0000ff")]) is True
        assert g.count() == 2

    def test_positions_clamped(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(-5, "#ff0000"), (9, "#0000ff")])
        assert g.stopPosition(0) == 0.0 and g.stopPosition(1) == 1.0

    def test_add_stop_defaults_to_the_colour_there(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.0, "#000000"), (1.0, "#ffffff")])
        idx = g.addStop(0.5)
        assert g.count() == 3
        mid = g.stopColor(idx)
        assert 120 <= mid.red() <= 135          # halfway between 0 and 255

    def test_remove_stop_respects_the_minimum(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.addStop(0.5, "#ff0000")
        assert g.removeStop(1) is True and g.count() == 2
        assert g.removeStop(0) is False and g.count() == 2

    def test_remove_out_of_range(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.removeStop(99) is False

    def test_set_stop_color(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.setStopColor(0, "#123456") is True
        assert g.stopColor(0).name() == "#123456"
        assert g.setStopColor(0, "nonsense") is False
        assert g.setStopColor(99, "#123456") is False

    def test_set_stop_position_resorts_and_tracks_selection(self, qapp):
        """Dragging a stop past its neighbour must not select a different one."""
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.0, "#ff0000"), (0.5, "#00ff00"),
                                         (1.0, "#0000ff")])
        g.setSelectedIndex(1)
        g.setStopPosition(1, 0.95)              # drag green past blue? no, to 0.95
        assert g.selectedIndex() == 1
        assert g.stopColor(g.selectedIndex()).name() == "#00ff00"
        g.setStopPosition(g.selectedIndex(), 0.0)
        assert g.stopColor(g.selectedIndex()).name() == "#00ff00"


class TestGradientInterpolation:
    def test_color_at_endpoints(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.0, "#ff0000"), (1.0, "#0000ff")])
        assert g.colorAt(0.0).name() == "#ff0000"
        assert g.colorAt(1.0).name() == "#0000ff"

    def test_color_at_midpoint(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.0, "#000000"), (1.0, "#ffffff")])
        mid = g.colorAt(0.5)
        assert 125 <= mid.red() <= 130

    def test_color_at_clamps_outside_range(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.25, "#ff0000"), (0.75, "#0000ff")])
        assert g.colorAt(0.0).name() == "#ff0000"
        assert g.colorAt(1.0).name() == "#0000ff"

    def test_alpha_is_interpolated(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        transparent = QColor(255, 0, 0, 0)
        opaque = QColor(255, 0, 0, 255)
        g.setStops([(0.0, transparent), (1.0, opaque)])
        assert 120 <= g.colorAt(0.5).alpha() <= 135

    def test_gradient_object_matches_type(self, qapp):
        from qtpy.QtGui import QGradient
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        assert g.gradient().type() == QGradient.LinearGradient
        g.gradientType = "radial"
        assert g.gradient().type() == QGradient.RadialGradient


class TestGradientInteraction:
    def test_clicking_the_bar_adds_a_stop(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.resize(280, 72)
        bar = g._barRect()
        _press(g, bar.center().x(), bar.center().y())
        assert g.count() == 3

    def test_clicking_a_handle_selects_it(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.resize(280, 72)
        seen = []
        g.stopSelected.connect(seen.append)
        centre = g._handleCenter(1)
        _press(g, centre.x(), centre.y())
        assert g.selectedIndex() == 1 and seen == [1]
        assert g.count() == 2                  # selecting must not add a stop

    def test_handle_at_misses_return_minus_one(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.resize(280, 72)
        assert g.handleAt(QPointF(140, 0)) == -1

    def test_delete_removes_selected_stop(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.addStop(0.5, "#ff0000")
        g.setSelectedIndex(1)
        _key(g, Qt.Key_Delete)
        assert g.count() == 2

    def test_arrow_keys_nudge_position(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.5, "#ff0000"), (1.0, "#0000ff")])
        g.setSelectedIndex(0)
        before = g.stopPosition(0)
        _key(g, Qt.Key_Right)
        assert g.stopPosition(g.selectedIndex()) > before

    def test_read_only_blocks_editing(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.resize(280, 72)
        g.readOnly = True
        bar = g._barRect()
        _press(g, bar.center().x(), bar.center().y())
        _key(g, Qt.Key_Delete)
        assert g.count() == 2


class TestGradientDesigner:
    def test_stops_csv_roundtrip(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.stopsCsv = "0:#ff0000,0.5:#00ff00,1:#0000ff"
        assert g.count() == 3
        assert g.stopsCsv == "0:#ff0000,0.5:#00ff00,1:#0000ff"

    def test_stops_csv_preserves_alpha(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.stopsCsv = "0:#80ff0000,1:#0000ff"
        assert g.stopColor(0).alpha() == 0x80
        assert "#80ff0000" in g.stopsCsv

    def test_stops_csv_ignores_junk(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.stopsCsv = "0:#ff0000,garbage,,1:#0000ff"
        assert g.count() == 2

    def test_stops_csv_below_minimum_is_ignored(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker(stops=[(0.0, "#111111"), (1.0, "#222222")])
        g.stopsCsv = "0:#ff0000"
        assert g.count() == 2 and g.stopColor(0).name() == "#111111"

    def test_gradient_changed_emits_on_edits(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        seen = []
        g.gradientChanged.connect(seen.append)
        g.addStop(0.5, "#ff0000")
        g.setStopColor(0, "#123456")
        g.removeStop(1)
        assert len(seen) == 3 and seen[-1] == g.stopsCsv

    def test_numeric_properties_clamp(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.barHeight = -10
        g.handleRadius = 0
        g.angle = 450
        assert g.barHeight >= 6 and g.handleRadius >= 3 and g.angle == 90

    def test_type_falls_back(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        g = QCustomGradientPicker()
        g.gradientType = "nonsense"
        assert g.gradientType == "linear"

    def test_paints_and_reflects_stops(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        a = QCustomGradientPicker(stops=[(0.0, "#ff0000"), (1.0, "#0000ff")])
        a.resize(280, 72)
        b = QCustomGradientPicker(stops=[(0.0, "#00ff00"), (1.0, "#ffff00")])
        b.resize(280, 72)
        assert a.grab().toImage() != b.grab().toImage()

    def test_radial_and_linear_render_differently(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        linear = QCustomGradientPicker()
        linear.resize(280, 72)
        radial = QCustomGradientPicker()
        radial.gradientType = "radial"
        radial.resize(280, 72)
        assert linear.grab().toImage() != radial.grab().toImage()

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomGradientPicker import QCustomGradientPicker
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        g = QCustomGradientPicker()
        g.ensurePolished()
        assert g.borderErrorColor.name().lower() == "#dc2626"     # destructive
        assert g.handleColor.name().lower() == "#ffffff"          # surface
        qapp.setStyleSheet("")
