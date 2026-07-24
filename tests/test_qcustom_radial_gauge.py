"""QCustomRadialGauge — headless construction + paint smoke + pixel probes that
the value arc, zones, tick gradient and needle actually render, plus the value
clamping / countdown / CSV-Designer-prop behaviour."""

from qtpy.QtGui import QColor


def _img(w, size=(240, 200)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=48):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestRadialGauge:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=55)
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 4          # it actually painted something non-trivial

    def test_active_zone_colours_the_arc(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=75)
        w.setZones([(0, 33, "#33d17a"), (33, 66, "#f4c44e"), (66, 100, "#f2704e")])
        img = _img(w)
        assert _has_color(img, "#f2704e"), "top (red) zone colour missing at 75%"
        # a value in the green band recolours the arc + badge
        w.setValue(20)
        assert w._active_zone_color().name() == "#33d17a"

    def test_tick_gradient_renders(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=17, minimum=0, maximum=20, gaugeStyle="tick")
        w.spanAngle = -270
        w.startAngle = 225
        w.setZones([])                       # gradient, not zones
        w.setGradient("#7c5cff", "#ff5c8a")
        img = _img(w)
        assert _has_color(img, "#7c5cff") or _has_color(img, "#ff5c8a"), \
            "tick gradient colour missing"

    def test_value_is_clamped_to_range(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(minimum=0, maximum=100)
        w.setValue(250)
        assert w.value == 100.0
        w.setValue(-40)
        assert w.value == 0.0

    def test_value_changed_signal(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=10)
        seen = []
        w.valueChanged.connect(seen.append)
        w.setValue(42)
        assert seen == [42.0]

    def test_zones_csv_designer_prop(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge()
        w.zonesCsv = "0:50:#112233, 50:100:#445566"
        assert len(w._zones) == 2
        assert w._zones[0][2].name() == "#112233"
        assert w.zonesCsv.startswith("0:50:#112233")

    def test_gauge_style_switch(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge()
        w.gaugeStyle = "tick"
        assert w.gaugeStyle == "tick"
        _img(w)
        w.gaugeStyle = "needle"
        assert w.gaugeStyle == "needle"
        _img(w)

    def test_full_circle_and_scale_labels(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=70, gaugeStyle="tick")
        w.startAngle = 90
        w.spanAngle = -360                 # full circle
        w.scaleLabelEvery = 25             # numeric scale labels
        w.showGuide = True                 # dotted inner scale ring
        assert w.spanAngle == -360.0
        assert w.scaleLabelEvery == 25.0
        _img(w)                            # paints a full-circle dial + labels

    def test_full_circle_tick_timer(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=13, minimum=0, maximum=20, gaugeStyle="tick")
        w.startAngle = 90
        w.spanAngle = -360                 # full-circle tick timer
        w.scaleLabelEvery = 5
        w.showGuide = True
        assert w.spanAngle == -360.0
        _img(w, (240, 240))

    def test_active_tick_extend_and_scale_radius(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=10, minimum=0, maximum=20, gaugeStyle="tick")
        w.activeTickExtend = "outward"
        assert w.activeTickExtend == "outward"
        w.activeTickExtend = "bogus"       # invalid falls back to inward
        assert w.activeTickExtend == "inward"
        w.scaleLabelEvery = 5
        w.scaleLabelRadius = 0.9
        assert w.scaleLabelRadius == 0.9
        _img(w, (240, 240))

    def test_rounded_caps_toggle(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=55)
        assert w.roundedCaps is True
        w.roundedCaps = False
        assert w.roundedCaps is False
        _img(w)

    def test_animation_keeps_target_value(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(value=10)
        w.animated = True
        w.animationDuration = 0            # snap, so the test is deterministic
        w.setValue(80)
        assert w.value == 80.0             # logical target updates immediately
        _img(w)

    def test_glow_paints_without_error(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        # needle + glow
        g = QCustomRadialGauge(value=70)
        g.glow = True
        g.glowStrength = 0.8
        g.glowRadius = 18
        assert g.glow is True and g.glowStrength == 0.8 and g.glowRadius == 18
        _img(g)
        # tick + glow
        t = QCustomRadialGauge(value=15, minimum=0, maximum=20, gaugeStyle="tick")
        t.glow = True
        _img(t, (240, 240))

    def test_countdown_finishes(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        w = QCustomRadialGauge(gaugeStyle="tick")
        done = []
        w.finished.connect(lambda: done.append(True))
        w.start(seconds=2, interval_ms=1)
        # drive the timer manually so the test stays deterministic + fast
        w._tick_down()      # 2 -> 1
        w._tick_down()      # 1 -> 0  => finished
        assert w.value == 0.0
        assert done == [True]
