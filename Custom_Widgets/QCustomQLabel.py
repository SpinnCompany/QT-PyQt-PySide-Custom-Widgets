########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomQLabel - a QLabel that can show an SVG ICON recoloured from QSS.
##
## The icon FILE is set the normal way (a QLabel `pixmap` — in the .ui or from
## QSS with the path variable), and the label TINTS that pixmap to `iconColor`,
## so a decorative label icon tracks ANY token (a brand-orange logo, a muted
## glyph) with no Python and recolours on a theme switch:
##
##     QCustomQLabel#logoIcon   { qproperty-pixmap: url($PATH_RESOURCES+'feather/activity.svg');
##                                qproperty-iconColor: $logo; }
##     QCustomQLabel#searchIcon { qproperty-pixmap: url($PATH_RESOURCES+'feather/search.svg');
##                                qproperty-iconColor: $muted; }
##
## (Buttons use `qproperty-icon`; a QLabel has no icon property, so the file goes
## through `qproperty-pixmap`.) It renders at `iconSize` px, or at the widget
## size when iconSize is 0 (default). Leave iconColor unset and the pixmap shows
## as-is (an ordinary QLabel).
########################################################################
from qtpy.QtCore import Property, Qt, QTimer, QSize
from qtpy.QtGui import QColor, QPixmap, QPainter
from qtpy.QtWidgets import QLabel


class QCustomQLabel(QLabel):

    WIDGET_ICON = "components/icons/text_fields.png"
    WIDGET_TOOLTIP = "A label that tints its pixmap icon to a QSS iconColor"
    WIDGET_MODULE = "Custom_Widgets.QCustomQLabel"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQLabel' name='customLabel'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>20</width><height>20</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomQLabel",
        "props": {"iconColor": {"type": "color", "default": ""},
                  "iconSize": {"type": "int", "default": 0},
                  "imageSource": {"type": "string", "default": ""},
                  "imageCornerRadius": {"type": "int", "default": 0}},
        "signals": [],
        "tokens_used": ["on-surface"],
    }
    DESIGNER_CUSTOM_PROPS = [
        {"name": "iconColor", "kind": "color", "group": "Icon"},
        {"name": "iconSize", "kind": "int", "group": "Icon"},
        {"name": "imageSource", "kind": "str", "group": "Image"},
        {"name": "imageCornerRadius", "kind": "int", "group": "Image"},
    ]

    def __init__(self, parent=None, iconColor=""):
        super().__init__(parent)
        self.setObjectName("QCustomQLabel")
        self._icon_color = QColor(iconColor)   # invalid by default -> no tint
        self._icon_size = 0
        self._src = QPixmap()                  # the un-tinted source pixmap
        self._tinted_key = 0

    def _tintPixmap(self, pm, color, sz):
        scaled = (pm.scaled(sz, sz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                  if sz else pm)
        out = QPixmap(scaled.size())
        out.setDevicePixelRatio(scaled.devicePixelRatio())
        out.fill(Qt.transparent)
        p = QPainter(out)
        p.drawPixmap(0, 0, scaled)
        p.setCompositionMode(QPainter.CompositionMode_SourceIn)
        p.fillRect(out.rect(), QColor(color))
        p.end()
        return out

    def _applyTint(self):
        cur = self.pixmap()
        if cur is None or cur.isNull():
            return
        if cur.cacheKey() != self._tinted_key:
            self._src = cur                    # fresh source (qproperty-pixmap / setPixmap)
        sz = self._icon_size or min(self.width(), self.height()) or 18
        if self._icon_color.isValid():
            out = self._tintPixmap(self._src, self._icon_color, sz)
        else:
            out = (self._src.scaled(sz, sz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                   if sz else self._src)
        QLabel.setPixmap(self, out)
        cp = self.pixmap()
        self._tinted_key = cp.cacheKey() if cp else 0

    def _scheduleTint(self):
        QTimer.singleShot(0, self._applyTint)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if getattr(self, "_image_pm", None) is not None:
            self._applyImage()                 # re-fit the cover photo
        elif not self._icon_size:              # tracking the widget size
            self._applyTint()

    @Property(QColor)
    def iconColor(self):
        return self._icon_color

    @iconColor.setter
    def iconColor(self, c):
        self._icon_color = QColor(c)
        self._scheduleTint()

    @Property(int)
    def iconSize(self):
        return self._icon_size

    @iconSize.setter
    def iconSize(self, v):
        self._icon_size = max(0, int(v))
        self._applyTint()

    # ------------------------------------------------------------------ #
    ## Image mode (opt-in): async cover-fit photo with rounded corners.
    ## Orthogonal to the icon-tint path — set imageSource (path or http(s)
    ## url, loaded + cached async) and the label renders the photo COVER-FIT
    ## at its size, clipped to imageCornerRadius. No manager pixmap code.
    # ------------------------------------------------------------------ #
    def setImageSource(self, source):
        source = str(source or "")
        self._image_source = source
        if not source:
            return
        from Custom_Widgets.ImageLoader import load_image
        load_image(source, self._onImageLoaded)

    def _onImageLoaded(self, pm):
        if pm is None or pm.isNull():
            return
        self._image_pm = pm
        self._applyImage()

    def _applyImage(self):
        pm = getattr(self, "_image_pm", None)
        if pm is None or pm.isNull():
            return
        from qtpy.QtCore import QRectF
        from qtpy.QtGui import QPainterPath
        w = max(1, self.width())
        h = max(1, self.height())
        r = max(0, int(getattr(self, "_image_radius", 0)))
        out = QPixmap(w * 2, h * 2)
        out.fill(QColor(0, 0, 0, 0))
        p = QPainter(out)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if r > 0:
            path = QPainterPath()
            path.addRoundedRect(QRectF(0, 0, w * 2, h * 2), r * 2, r * 2)
            p.setClipPath(path)
        scaled = pm.scaled(w * 2, h * 2, Qt.KeepAspectRatioByExpanding,
                           Qt.SmoothTransformation)
        p.drawPixmap((w * 2 - scaled.width()) // 2, (h * 2 - scaled.height()) // 2, scaled)
        p.end()
        out.setDevicePixelRatio(2.0)
        QLabel.setPixmap(self, out)
        cp = self.pixmap()
        self._tinted_key = cp.cacheKey() if cp else 0   # don't re-tint the photo

    @Property(str)
    def imageSource(self):
        return getattr(self, "_image_source", "")

    @imageSource.setter
    def imageSource(self, v):
        self.setImageSource(v)

    @Property(int)
    def imageCornerRadius(self):
        return getattr(self, "_image_radius", 0)

    @imageCornerRadius.setter
    def imageCornerRadius(self, v):
        self._image_radius = max(0, int(v))
        self._applyImage()
