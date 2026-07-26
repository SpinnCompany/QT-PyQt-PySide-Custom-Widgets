########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomGlassFrame - a GLASSMORPHISM / "liquid glass" container.
##
## A rounded container that composites a BLURRED copy of the content behind
## it (the app's backdrop photo / wallpaper widget), then layers a tint, a
## film-grain noise pass, a hairline border and - opt-in - a "liquid" edge
## (refraction ring + specular rim) on top. Children laid out inside it sit
## on frosted glass, like CSS backdrop-filter or visionOS panels.
##
## Qt has no native backdrop-filter, so the frame renders a SOURCE widget
## into a pixmap, blurs it offscreen (downsample -> QGraphicsBlurEffect ->
## upsample) and paints that region under its own content:
##
##   * `backdropSource` (objectName) / setBackdropWidget(w): the widget to
##     sample - typically the full-window photo QLabel BELOW the glass
##     panels. Sampling a widget that does not contain the frame is cheap
##     and flicker-free, so `liveBackdrop` can re-sample continuously.
##   * With no source set, the frame samples its own top-level window
##     (hiding itself for the grab). That path is for static backdrops -
##     refresh happens on show/resize/move or an explicit refreshBackdrop().
##   * With nothing to sample (Designer palette preview, render_widget),
##     it paints a seeded placeholder gradient so it still previews.
##
## Every knob is a typed Designer property; colours are qproperties so QSS
## drives them per theme (qproperty-tintColor: ...). The live re-sampling
## "animation" is user-controllable via `liveBackdrop` + `refreshInterval`.
########################################################################
import random

from qtpy.QtCore import Qt, Property, QEvent, QPoint, QRect, QRectF, QSize, QTimer
from qtpy.QtGui import QBrush, QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap
from qtpy.QtWidgets import (QFrame, QGraphicsBlurEffect, QGraphicsPixmapItem,
                            QGraphicsScene, QSizePolicy, QWidget)


def _blur_image(img, radius):
    """Gaussian-blur a QImage offscreen via a throwaway QGraphicsScene."""
    if radius <= 0 or img.isNull():
        return img
    scene = QGraphicsScene()
    item = QGraphicsPixmapItem(QPixmap.fromImage(img))
    effect = QGraphicsBlurEffect()
    effect.setBlurRadius(float(radius))
    effect.setBlurHints(QGraphicsBlurEffect.QualityHint)
    item.setGraphicsEffect(effect)  # allow-shadow: offscreen QGraphicsBlurEffect IS the sanctioned pre-blurred-backdrop pipeline, not widget elevation
    scene.addItem(item)
    out = QImage(img.size(), QImage.Format_ARGB32_Premultiplied)
    out.fill(0)
    p = QPainter(out)
    p.setRenderHint(QPainter.SmoothPixmapTransform, True)
    scene.render(p, QRectF(out.rect()), QRectF(img.rect()))
    p.end()
    return out


class QCustomGlassFrame(QFrame):

    WIDGET_ICON = "components/icons/filter_tilt_shift.png"
    WIDGET_TOOLTIP = "Glassmorphism container: blurred backdrop + tint + noise + liquid edge"
    WIDGET_MODULE = "Custom_Widgets.QCustomGlassFrame"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomGlassFrame' name='customGlassFrame'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>240</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomGlassFrame",
        "container": True,
        "props": {"backdropSource": {"type": "string", "default": ""},
                  "blurRadius": {"type": "int", "default": 28},
                  "downsample": {"type": "int", "default": 3},
                  "tintColor": {"type": "color", "default": "rgba(18,22,32,110)"},
                  "brightness": {"type": "float", "default": 1.0},
                  "noiseOpacity": {"type": "float", "default": 0.05},
                  "cornerRadius": {"type": "int", "default": 24},
                  "borderColor": {"type": "color", "default": "rgba(255,255,255,55)"},
                  "borderWidth": {"type": "float", "default": 1.0},
                  "liquidEdge": {"type": "bool", "default": False},
                  "edgeIntensity": {"type": "float", "default": 0.5},
                  "liveBackdrop": {"type": "bool", "default": False},
                  "refreshInterval": {"type": "int", "default": 120}},
        "signals": [],
        "tokens_used": [],
    }
    DESIGNER_CUSTOM_PROPS = [
        {"name": "backdropSource", "kind": "string", "group": "Glass"},
        {"name": "blurRadius", "kind": "int", "group": "Glass"},
        {"name": "downsample", "kind": "int", "group": "Glass"},
        {"name": "tintColor", "kind": "color", "group": "Glass"},
        {"name": "brightness", "kind": "float", "group": "Glass"},
        {"name": "noiseOpacity", "kind": "float", "group": "Glass"},
        {"name": "cornerRadius", "kind": "int", "group": "Glass"},
        {"name": "borderColor", "kind": "color", "group": "Glass"},
        {"name": "borderWidth", "kind": "float", "group": "Glass"},
        {"name": "liquidEdge", "kind": "bool", "group": "Liquid"},
        {"name": "edgeIntensity", "kind": "float", "group": "Liquid"},
        {"name": "liveBackdrop", "kind": "bool", "group": "Backdrop"},
        {"name": "refreshInterval", "kind": "int", "group": "Backdrop"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomGlassFrame")
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # The glass paints ONLY inside its rounded path — never let the frame's
        # own palette/stylesheet background fill the square corners behind it.
        # NB: QStyleSheetStyle::polish RE-ENABLES WA_StyledBackground whenever
        # an app stylesheet gives this widget a background (a base theme's
        # broad `QWidget { background-color: … }` is enough) — so the attribute
        # is re-cleared on every style change, not just here (see changeEvent).
        self._clear_bg_attrs()

        self._backdrop_source = ""
        self._backdrop_widget = None
        self._blur_radius = 28
        self._downsample = 3
        self._tint = QColor(18, 22, 32, 110)
        self._brightness = 1.0
        self._noise_opacity = 0.05
        self._radius = 24
        self._border_color = QColor(255, 255, 255, 55)
        self._border_width = 1.0
        self._liquid_edge = False
        self._edge_intensity = 0.5

        self._backdrop_pix = None
        self._noise_pm = None
        self._grabbing = False
        self._refresh_queued = False
        self._live = False

        self._live_timer = QTimer(self)
        self._live_timer.setInterval(120)
        self._live_timer.timeout.connect(self.refreshBackdrop)

    def _clear_bg_attrs(self):
        # Only touch attributes that are actually set — setAttribute itself
        # emits a StyleChange, so an unconditional clear inside changeEvent
        # recurses forever.
        if self.autoFillBackground():
            self.setAutoFillBackground(False)
        if self.testAttribute(Qt.WA_StyledBackground):
            self.setAttribute(Qt.WA_StyledBackground, False)

    def changeEvent(self, e):
        super().changeEvent(e)
        if e.type() in (QEvent.StyleChange, QEvent.PaletteChange):
            self._clear_bg_attrs()

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setBackdropWidget(self, widget):
        """Point the frame at the widget to sample (overrides backdropSource)."""
        self._backdrop_widget = widget
        self._backdrop_pix = None
        self._schedule_refresh()

    def refreshBackdrop(self):
        """Re-sample and re-blur the backdrop now."""
        if self._grabbing:
            return
        self._refresh_queued = False
        src = self._resolve_source()
        self._watch_source(src)
        if src is None or src.width() <= 0 or src.height() <= 0:
            self._backdrop_pix = None
            self.update()
            return
        inside = src is self or src.isAncestorOf(self)
        self._grabbing = True
        try:
            pm = QPixmap(src.size())
            pm.fill(Qt.transparent)
            if inside:
                self.hide()
                src.render(pm)
                self.show()
            else:
                src.render(pm)
        finally:
            self._grabbing = False
        img = pm.toImage()
        # src may be a sibling (not an ancestor), so route through global coords
        top_left = src.mapFromGlobal(self.mapToGlobal(QPoint(0, 0)))
        region = QRect(top_left, self.size())
        clipped = region.intersected(img.rect())
        if clipped.isEmpty():
            self._backdrop_pix = None
            self.update()
            return
        # paste the visible part at its offset so partly-outside frames align
        base = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        base.fill(0)
        p = QPainter(base)
        p.drawImage(clipped.topLeft() - region.topLeft(), img.copy(clipped))
        p.end()
        ds = max(1, int(self._downsample))
        if ds > 1:
            small = base.scaled(max(1, base.width() // ds), max(1, base.height() // ds),
                                Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            small = _blur_image(small, max(1.0, float(self._blur_radius) / ds))
            blurred = small.scaled(base.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            blurred = _blur_image(base, float(self._blur_radius))
        self._backdrop_pix = QPixmap.fromImage(blurred)
        self.update()

    # ------------------------------------------------------------------ #
    ## internals
    # ------------------------------------------------------------------ #
    def _resolve_source(self):
        if self._backdrop_widget is not None:
            return self._backdrop_widget
        win = self.window()
        if self._backdrop_source and win is not None:
            w = win.findChild(QWidget, self._backdrop_source)
            if w is not None and w is not self and not self.isAncestorOf(w):
                return w
        if win is not None and win is not self:
            return win
        return None

    def _schedule_refresh(self):
        if self._refresh_queued or self._grabbing:
            return
        self._refresh_queued = True
        QTimer.singleShot(0, self.refreshBackdrop)

    def _watch_source(self, src):
        """Auto-refresh when the backdrop SOURCE changes (async photo arrival,
        resize) — apps no longer fan refreshBackdrop() out by hand. The whole
        window is never watched (its repaints include our own — feedback)."""
        current = getattr(self, "_watched_source", None)
        if src is current:
            return
        if current is not None:
            try:
                current.removeEventFilter(self)
            except RuntimeError:
                pass
        self._watched_source = None
        if src is not None and src is not self.window():
            src.installEventFilter(self)
            self._watched_source = src

    def eventFilter(self, obj, e):
        # NB: render() during our own grab paints the source synchronously and
        # emits no UpdateRequest, so sampling can't re-trigger this.
        if obj is getattr(self, "_watched_source", None) and not self._grabbing:
            if e.type() in (QEvent.UpdateRequest, QEvent.Resize, QEvent.Move):
                self._schedule_refresh()
        return super().eventFilter(obj, e)

    def _noise_tile(self):
        if self._noise_pm is None:
            rnd = random.Random(7)  # deterministic so pixel probes stay stable
            img = QImage(64, 64, QImage.Format_ARGB32)
            for y in range(64):
                for x in range(64):
                    v = rnd.randint(0, 255)
                    img.setPixelColor(x, y, QColor(v, v, v, 255))
            self._noise_pm = QPixmap.fromImage(img)
        return self._noise_pm

    def _outer_path(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            float(self._radius), float(self._radius))
        return path

    # ------------------------------------------------------------------ #
    ## events
    # ------------------------------------------------------------------ #
    def showEvent(self, e):
        super().showEvent(e)
        self._schedule_refresh()
        if self._live and not self._live_timer.isActive():
            self._live_timer.start()

    def hideEvent(self, e):
        super().hideEvent(e)
        self._live_timer.stop()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._schedule_refresh()

    def moveEvent(self, e):
        super().moveEvent(e)
        self._schedule_refresh()

    # ------------------------------------------------------------------ #
    ## painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if self._grabbing:
            return
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        # Compose the full glass stack (backdrop + scrims + tint + noise) into
        # an UNROUNDED offscreen pixmap, then fill the rounded path with it as
        # a texture brush. QPainter clipping is not antialiased — the old
        # setClipPath approach left hard, stair-stepped corners over whatever
        # sat behind the frame.
        dpr = self.devicePixelRatioF()
        composed = QPixmap(max(1, int(w * dpr)), max(1, int(h * dpr)))
        composed.setDevicePixelRatio(dpr)
        composed.fill(Qt.transparent)
        cp = QPainter(composed)
        cp.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self._backdrop_pix is not None and not self._backdrop_pix.isNull():
            cp.drawPixmap(0, 0, self._backdrop_pix)
        else:
            # seeded placeholder so the frame previews with no backdrop around
            grad = QLinearGradient(0, 0, 0, h)
            grad.setColorAt(0.0, QColor(64, 74, 104))
            grad.setColorAt(1.0, QColor(28, 32, 48))
            cp.fillRect(self.rect(), grad)

        b = float(self._brightness)
        if b > 1.0:
            cp.fillRect(self.rect(), QColor(255, 255, 255, min(255, int((b - 1.0) * 255))))
        elif b < 1.0:
            cp.fillRect(self.rect(), QColor(0, 0, 0, min(255, int((1.0 - b) * 255))))

        if self._tint.alpha() > 0:
            cp.fillRect(self.rect(), self._tint)

        if self._noise_opacity > 0.0:
            cp.setOpacity(min(1.0, float(self._noise_opacity)))
            tile = self._noise_tile()
            for ty in range(0, h, tile.height()):
                for tx in range(0, w, tile.width()):
                    cp.drawPixmap(tx, ty, tile)
            cp.setOpacity(1.0)
        cp.end()

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        outer = self._outer_path()
        p.setPen(Qt.NoPen)
        p.fillPath(outer, QBrush(composed))

        if self._liquid_edge:
            self._paint_liquid_edge(p, outer)

        p.setClipping(False)
        if self._border_width > 0.0 and self._border_color.alpha() > 0:
            inset = self._border_width / 2.0
            p.setPen(QPen(self._border_color, self._border_width))
            p.setBrush(Qt.NoBrush)
            r = max(0.0, float(self._radius) - inset)
            p.drawRoundedRect(QRectF(inset, inset, w - 2 * inset,
                                     h - 2 * inset), r, r)
        p.end()

    def _paint_liquid_edge(self, p, outer):
        k = max(0.0, min(1.0, float(self._edge_intensity)))
        band = max(8.0, min(22.0, min(self.width(), self.height()) * 0.06))
        inner = QPainterPath()
        inner.addRoundedRect(QRectF(band, band, self.width() - 2 * band,
                                    self.height() - 2 * band),
                             max(2.0, self._radius - band), max(2.0, self._radius - band))
        ring = outer.subtracted(inner)

        # refraction: the backdrop drawn slightly zoomed, only in the edge ring
        if self._backdrop_pix is not None and not self._backdrop_pix.isNull():
            p.save()
            p.setClipPath(ring, Qt.IntersectClip)
            p.setOpacity(0.4 * k)
            zoom = 1.05
            zw, zh = self.width() * zoom, self.height() * zoom
            p.drawPixmap(QRectF(-(zw - self.width()) / 2.0, -(zh - self.height()) / 2.0, zw, zh),
                         self._backdrop_pix,
                         QRectF(0, 0, self._backdrop_pix.width(), self._backdrop_pix.height()))
            p.restore()

        # specular rim: bright top edge fading out, dark seat at the bottom
        rim = QLinearGradient(0, 0, 0, self.height())
        rim.setColorAt(0.0, QColor(255, 255, 255, int(150 * k)))
        rim.setColorAt(0.25, QColor(255, 255, 255, int(28 * k)))
        rim.setColorAt(0.85, QColor(255, 255, 255, 0))
        rim.setColorAt(1.0, QColor(0, 0, 0, int(70 * k)))
        p.setPen(QPen(rim, 1.6))
        p.setBrush(Qt.NoBrush)
        r = max(0.0, float(self._radius) - 1.0)
        p.drawRoundedRect(QRectF(1.0, 1.0, self.width() - 2.0, self.height() - 2.0), r, r)

    def sizeHint(self):
        return QSize(360, 240)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def backdropSource(self):
        return self._backdrop_source

    @backdropSource.setter
    def backdropSource(self, name):
        self._backdrop_source = str(name)
        self._backdrop_widget = None
        self._backdrop_pix = None
        self._schedule_refresh()

    @Property(int)
    def blurRadius(self):
        return self._blur_radius

    @blurRadius.setter
    def blurRadius(self, r):
        self._blur_radius = max(0, int(r))
        self._schedule_refresh()

    @Property(int)
    def downsample(self):
        return self._downsample

    @downsample.setter
    def downsample(self, d):
        self._downsample = max(1, int(d))
        self._schedule_refresh()

    @Property(QColor)
    def tintColor(self):
        return self._tint

    @tintColor.setter
    def tintColor(self, c):
        self._tint = QColor(c)
        self.update()

    @Property(float)
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, b):
        self._brightness = max(0.0, min(2.0, float(b)))
        self.update()

    @Property(float)
    def noiseOpacity(self):
        return self._noise_opacity

    @noiseOpacity.setter
    def noiseOpacity(self, o):
        self._noise_opacity = max(0.0, min(1.0, float(o)))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, r):
        self._radius = max(0, int(r))
        self.update()

    @Property(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, c):
        self._border_color = QColor(c)
        self.update()

    @Property(float)
    def borderWidth(self):
        return self._border_width

    @borderWidth.setter
    def borderWidth(self, w):
        self._border_width = max(0.0, float(w))
        self.update()

    @Property(bool)
    def liquidEdge(self):
        return self._liquid_edge

    @liquidEdge.setter
    def liquidEdge(self, on):
        self._liquid_edge = bool(on)
        self.update()

    @Property(float)
    def edgeIntensity(self):
        return self._edge_intensity

    @edgeIntensity.setter
    def edgeIntensity(self, k):
        self._edge_intensity = max(0.0, min(1.0, float(k)))
        self.update()

    @Property(bool)
    def liveBackdrop(self):
        return self._live

    @liveBackdrop.setter
    def liveBackdrop(self, on):
        self._live = bool(on)
        if self._live and self.isVisible():
            self._live_timer.start()
        elif not self._live:
            self._live_timer.stop()

    @Property(int)
    def refreshInterval(self):
        return self._live_timer.interval()

    @refreshInterval.setter
    def refreshInterval(self, ms):
        self._live_timer.setInterval(max(30, int(ms)))
