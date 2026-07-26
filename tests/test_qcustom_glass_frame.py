"""QCustomGlassFrame — headless paint smoke + pixel probes that the backdrop
really gets sampled and BLURRED, the tint/border/liquid-edge knobs paint, and
props clamp/roundtrip."""

from qtpy.QtCore import QPoint, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLabel, QWidget


def _wallpaper(parent, w=400, h=300):
    """A half-red / half-blue backdrop label the glass frame can sample."""
    from qtpy.QtGui import QImage, QPixmap, QPainter
    img = QImage(w, h, QImage.Format_ARGB32)
    p = QPainter(img)
    p.fillRect(0, 0, w // 2, h, QColor(220, 30, 30))
    p.fillRect(w // 2, 0, w - w // 2, h, QColor(30, 30, 220))
    p.end()
    lbl = QLabel(parent)
    lbl.setObjectName("wallpaper")
    lbl.setPixmap(QPixmap.fromImage(img))
    lbl.setGeometry(0, 0, w, h)
    return lbl


def _make(qapp, **props):
    from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
    host = QWidget()
    host.resize(400, 300)
    _wallpaper(host)
    glass = QCustomGlassFrame(host)
    glass.setGeometry(100, 50, 200, 200)  # straddles the red/blue boundary
    glass.backdropSource = "wallpaper"
    glass.noiseOpacity = 0.0
    glass.tintColor = QColor(0, 0, 0, 0)
    glass.borderWidth = 0.0
    for k, v in props.items():
        setattr(glass, k, v)
    host.show()
    qapp.processEvents()
    glass.refreshBackdrop()
    qapp.processEvents()
    return host, glass


def _px(glass, x, y):
    img = glass.grab().toImage()
    return QColor(img.pixel(x, y))


class TestGlassFrame:
    def test_construct_and_paint_smoke(self, qapp):
        from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
        w = QCustomGlassFrame()
        w.resize(300, 200)
        img = w.grab().toImage()
        assert not img.isNull()

    def test_backdrop_sampled_and_blurred(self, qapp):
        host, glass = _make(qapp, blurRadius=40, downsample=2)
        # frame spans x=100..300 over a boundary at x=200 (frame-local x=100).
        # With a strong blur the colours at the boundary MIX; far edges stay
        # nearly pure. Sample mid-height.
        edge = _px(glass, 100, 100)
        assert edge.red() > 40 and edge.blue() > 40, \
            f"boundary should blend red+blue, got {edge.red()},{edge.green()},{edge.blue()}"
        left = _px(glass, 8, 100)
        assert left.red() > left.blue(), "left of glass should stay red-dominant"
        right = _px(glass, 191, 100)
        assert right.blue() > right.red(), "right of glass should stay blue-dominant"

    def test_no_blur_keeps_edge_sharp(self, qapp):
        host, glass = _make(qapp, blurRadius=0, downsample=1)
        just_left = _px(glass, 95, 100)
        just_right = _px(glass, 105, 100)
        assert just_left.red() > 150 and just_left.blue() < 100
        assert just_right.blue() > 150 and just_right.red() < 100

    def test_tint_composites(self, qapp):
        host, glass = _make(qapp, tintColor=QColor(0, 255, 0, 255))
        c = _px(glass, 100, 100)
        assert c.green() > 200 and c.red() < 60 and c.blue() < 60

    def test_border_paints(self, qapp):
        host, glass = _make(qapp, borderWidth=4.0,
                            borderColor=QColor(255, 255, 0, 255), cornerRadius=0)
        c = _px(glass, 100, 1)  # top edge, mid-width
        assert c.red() > 180 and c.green() > 180 and c.blue() < 90, \
            f"border colour missing at top edge: {c.red()},{c.green()},{c.blue()}"

    def test_placeholder_paints_without_backdrop(self, qapp):
        from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
        w = QCustomGlassFrame()
        w.resize(200, 150)
        img = w.grab().toImage()
        seen = {img.pixel(x, y) for y in range(0, 150, 5) for x in range(0, 200, 5)}
        assert len(seen) > 3, "placeholder gradient should paint multiple shades"

    def test_liquid_edge_smoke_and_rim(self, qapp):
        host, glass = _make(qapp, liquidEdge=True, edgeIntensity=1.0, cornerRadius=0)
        plain_host, plain = _make(qapp, liquidEdge=False, cornerRadius=0)
        def top_brightness(w):
            img = w.grab().toImage()
            return max(sum(QColor(img.pixel(100, y)).getRgb()[:3]) for y in range(0, 4))

        # specular rim brightens the very top edge vs the plain glass
        assert top_brightness(glass) > top_brightness(plain), \
            "liquid edge should paint a brighter specular rim at the top"

    def test_window_grab_fallback(self, qapp):
        """No backdropSource: samples the top-level window without recursing."""
        from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
        host = QWidget()
        host.resize(400, 300)
        _wallpaper(host)
        glass = QCustomGlassFrame(host)
        glass.setGeometry(100, 50, 200, 200)
        glass.noiseOpacity = 0.0
        glass.tintColor = QColor(0, 0, 0, 0)
        glass.borderWidth = 0.0
        host.show()
        qapp.processEvents()
        glass.refreshBackdrop()
        qapp.processEvents()
        c = _px(glass, 8, 100)
        assert c.red() > 100, "window-grab backdrop should sample the red half"
        assert glass.isVisible(), "frame must be re-shown after the guarded grab"

    def test_props_clamp_and_roundtrip(self, qapp):
        from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
        w = QCustomGlassFrame()
        w.blurRadius = -5
        assert w.blurRadius == 0
        w.downsample = 0
        assert w.downsample == 1
        w.noiseOpacity = 3.0
        assert w.noiseOpacity == 1.0
        w.edgeIntensity = -1.0
        assert w.edgeIntensity == 0.0
        w.brightness = 5.0
        assert w.brightness == 2.0
        w.refreshInterval = 5
        assert w.refreshInterval == 30
        w.cornerRadius = 40
        assert w.cornerRadius == 40

    def test_live_backdrop_toggle(self, qapp):
        from Custom_Widgets.QCustomGlassFrame import QCustomGlassFrame
        host = QWidget()
        host.resize(300, 200)
        w = QCustomGlassFrame(host)
        host.show()
        qapp.processEvents()
        w.liveBackdrop = True
        assert w._live_timer.isActive(), "live mode should start the refresh timer"
        w.liveBackdrop = False
        assert not w._live_timer.isActive(), "user can always turn the animation off"
        host.hide()
