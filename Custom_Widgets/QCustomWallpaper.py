########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomWallpaper - a full-bleed backdrop image widget.
##
## The photo layer glass UIs sample: give it an `imageSource` (local path or
## http(s) URL - downloaded + cached async via Custom_Widgets.ImageLoader) and
## it paints the image COVER-FIT (fills, centre-cropped - never distorted like
## a scaledContents QLabel). Until the image arrives (or offline) it paints a
## three-stop diagonal gradient from `fallbackTop/Mid/Bottom` - qproperties,
## so the fallback THEMES from QSS. Glass frames watching it via
## backdropSource re-sample automatically when the photo lands.
########################################################################
from qtpy.QtCore import Qt, Property, QRectF, Signal
from qtpy.QtGui import QColor, QLinearGradient, QPainter, QPixmap
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomWallpaper(QWidget):

    imageLoaded = Signal()

    WIDGET_ICON = "components/icons/image.png"
    WIDGET_TOOLTIP = "A full-bleed cover-fit backdrop image with a themed gradient fallback"
    WIDGET_MODULE = "Custom_Widgets.QCustomWallpaper"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomWallpaper' name='wallpaper'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>400</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomWallpaper",
        "props": {"imageSource": {"type": "string", "default": ""},
                  "fallbackTop": {"type": "color", "default": "#2b3550"},
                  "fallbackMid": {"type": "color", "default": "#4c4668"},
                  "fallbackBottom": {"type": "color", "default": "#1a1e30"}},
        "signals": ["imageLoaded"],
        "tokens_used": [],
    }
    DESIGNER_CUSTOM_PROPS = [
        {"name": "imageSource", "kind": "str", "group": "Wallpaper"},
        {"name": "fallbackTop", "kind": "color", "group": "Wallpaper"},
        {"name": "fallbackMid", "kind": "color", "group": "Wallpaper"},
        {"name": "fallbackBottom", "kind": "color", "group": "Wallpaper"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomWallpaper")
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._source = ""
        self._pixmap = None
        self._fallback_top = QColor("#2b3550")
        self._fallback_mid = QColor("#4c4668")
        self._fallback_bottom = QColor("#1a1e30")

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setImageSource(self, source):
        source = str(source or "")
        self._source = source
        if not source:
            self._pixmap = None
            self.update()
            return
        from Custom_Widgets.ImageLoader import load_image
        load_image(source, self._on_loaded)

    def _on_loaded(self, pm):
        if pm is None or pm.isNull():
            return
        self._pixmap = pm
        self.update()
        self.imageLoaded.emit()

    def pixmap(self):
        return self._pixmap

    # ------------------------------------------------------------------ #
    ## painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        w, h = self.width(), self.height()
        if self._pixmap is not None and not self._pixmap.isNull():
            pm = self._pixmap
            # cover-fit: scale to fill, centre-crop the overflow
            scale = max(w / pm.width(), h / pm.height())
            sw, sh = pm.width() * scale, pm.height() * scale
            p.drawPixmap(QRectF((w - sw) / 2.0, (h - sh) / 2.0, sw, sh),
                         pm, QRectF(0, 0, pm.width(), pm.height()))
        else:
            grad = QLinearGradient(0, 0, w * 0.25, h)
            grad.setColorAt(0.0, self._fallback_top)
            grad.setColorAt(0.5, self._fallback_mid)
            grad.setColorAt(1.0, self._fallback_bottom)
            p.fillRect(self.rect(), grad)
        p.end()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def imageSource(self):
        return self._source

    @imageSource.setter
    def imageSource(self, v):
        self.setImageSource(v)

    def _mk_color(attr):
        def getter(self):
            return getattr(self, attr)

        def setter(self, v):
            setattr(self, attr, QColor(v))
            self.update()
        return Property(QColor, getter, setter)

    fallbackTop = _mk_color("_fallback_top")
    fallbackMid = _mk_color("_fallback_mid")
    fallbackBottom = _mk_color("_fallback_bottom")
