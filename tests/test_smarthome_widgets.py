"""Headless paint + API tests for the smart-home dashboard widgets:
QCustomTileButton (new) and the ring-gauge extensions on QCustomRadialGauge
(showHandle / centerIcon / innerColor)."""

from qtpy.QtGui import QColor


def _img(w, size=(120, 120)):
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


class TestTileButton:
    def test_construct_and_checkable(self, qapp):
        from Custom_Widgets.QCustomTileButton import QCustomTileButton
        w = QCustomTileButton(caption="Lights")
        assert w.isCheckable()
        assert w.caption == "Lights"

    def test_toggled_signal(self, qapp):
        from Custom_Widgets.QCustomTileButton import QCustomTileButton
        w = QCustomTileButton()
        seen = []
        w.toggled.connect(lambda v: seen.append(v))
        w.setChecked(True)
        assert seen and seen[-1] is True

    def test_active_gradient_renders(self, qapp):
        from Custom_Widgets.QCustomTileButton import QCustomTileButton
        w = QCustomTileButton(caption="Lights")
        w.setGradient("#a05cf0", "#f45c9c")
        w.setChecked(True)
        img = _img(w)
        assert _has_color(img, "#a05cf0") or _has_color(img, "#f45c9c")

    def test_inactive_bg_renders(self, qapp):
        from Custom_Widgets.QCustomTileButton import QCustomTileButton
        w = QCustomTileButton(caption="Heating")
        w.bgColor = QColor("#242850")
        w.setChecked(False)
        img = _img(w)
        assert _has_color(img, "#242850")

    def test_designer_props(self, qapp):
        from Custom_Widgets.QCustomTileButton import QCustomTileButton
        w = QCustomTileButton()
        w.caption = "Garden"
        w.cornerRadius = 20
        w.iconSize = 40
        assert w.caption == "Garden" and w.cornerRadius == 20 and w.iconSize == 40
        _img(w)


class TestRingGaugeExtensions:
    def test_handle_and_disc_props(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        g = QCustomRadialGauge(value=22, minimum=0, maximum=40)
        g.showNeedle = False
        g.showHandle = True
        g.innerColor = QColor("#ffffff")
        g.centerText = "22"
        g.centerSuffix = "C°"
        assert g.showHandle is True
        assert QColor(g.innerColor).name() == "#ffffff"
        img = _img(g, (220, 220))
        # the white inner disc should be visible
        assert _has_color(img, "#ffffff")

    def test_gradient_used_when_zones_cleared(self, qapp):
        from Custom_Widgets.QCustomRadialGauge import QCustomRadialGauge
        g = QCustomRadialGauge(value=30, minimum=0, maximum=40)
        g.showNeedle = False
        g.zonesCsv = ""                      # clear default zones -> use gradient
        g.setGradient("#4bc0ff", "#7ee0ff")
        g.arcWidth = 16
        img = _img(g, (220, 220))
        assert _has_color(img, "#4bc0ff") or _has_color(img, "#7ee0ff")
