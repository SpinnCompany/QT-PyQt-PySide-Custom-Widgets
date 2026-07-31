########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomTileButton - a selectable device / action TILE.
##
## A rounded-rectangle button with a line ICON above a CAPTION — the classic
## smart-home / launcher tile. It is CHECKABLE: the selected tile paints a
## two-stop diagonal GRADIENT (e.g. purple->pink) with light icon+text, the
## rest paint a flat card fill with muted icon+text. Painted with QPainter so
## it stays crisp at any size and recolours on a theme switch (all colours are
## qproperties); the icon is a recoloured SVG so it flips light/muted with the
## selected state.
##
## Give it an icon with `iconPath` (an .svg) + a `caption` in code or Qt
## Designer. It is a QAbstractButton, so it emits clicked()/toggled(bool) and
## participates in a QButtonGroup for single-select device grids.
########################################################################
import os

from qtpy.QtCore import Qt, Property, QRectF, QByteArray
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QFont, QLinearGradient, QPixmap
from qtpy.QtWidgets import QAbstractButton, QSizePolicy

try:
    from qtpy.QtSvg import QSvgRenderer
except Exception:
    QSvgRenderer = None


class QCustomTileButton(QAbstractButton):

    WIDGET_ICON = "components/icons/view_quilt.png"
    WIDGET_TOOLTIP = "A selectable device / action tile (icon + caption, gradient when active)"
    WIDGET_MODULE = "Custom_Widgets.QCustomTileButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomTileButton' name='customTileButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>120</width><height>120</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomTileButton",
        "props": {"caption": {"type": "string", "default": "Lights"},
                  "iconPath": {"type": "string", "default": ""},
                  "gradientStart": {"type": "color", "default": "#a05cf0"},
                  "gradientEnd": {"type": "color", "default": "#f45c9c"},
                  "bgColor": {"type": "color", "default": "#242850"},
                  "iconColor": {"type": "color", "default": "#9aa0c6"},
                  "activeColor": {"type": "color", "default": "#ffffff"},
                  "cornerRadius": {"type": "int", "default": 16},
                  "iconSize": {"type": "int", "default": 34}},
        "signals": ["clicked", "toggled"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, caption="Lights", iconPath=""):
        super().__init__(parent)
        self.setObjectName("QCustomTileButton")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self._caption = caption
        self._icon_path = iconPath
        self._grad_start = QColor("#a05cf0")
        self._grad_end = QColor("#f45c9c")
        self._bg = QColor("#242850")
        self._icon_color = QColor("#9aa0c6")
        self._active_color = QColor("#ffffff")
        self._radius = 16
        self._icon_size = 34
        self._pix_cache = {}
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(84, 84)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setCaption(self, text):
        self._caption = str(text)
        self.update()

    def setIconPath(self, path):
        self._icon_path = str(path)
        self._pix_cache.clear()
        self.update()

    def setGradient(self, start, end):
        self._grad_start = QColor(start)
        self._grad_end = QColor(end)
        self.update()

    def _fg(self):
        return self._active_color if self.isChecked() else self._icon_color

    def _icon_pixmap(self, size, color):
        key = (self._icon_path, int(size), color.name())
        if key in self._pix_cache:
            return self._pix_cache[key]
        pm = QPixmap(int(size * 2), int(size * 2))
        pm.fill(QColor(0, 0, 0, 0))
        path = self._icon_path
        if path and os.path.exists(path):
            if path.lower().endswith(".svg") and QSvgRenderer is not None:
                svg = open(path, "r", encoding="utf-8").read()
                for old in ('stroke="#ffffff"', 'stroke="#000000"', 'stroke="currentColor"'):
                    svg = svg.replace(old, 'stroke="%s"' % color.name())
                svg = svg.replace('fill="currentColor"', 'fill="%s"' % color.name())
                rnd = QSvgRenderer(QByteArray(svg.encode("utf-8")))
                pr = QPainter(pm)
                pr.setRenderHint(QPainter.Antialiasing, True)
                rnd.render(pr)
                pr.end()
            else:
                src = QPixmap(path)
                if not src.isNull():
                    pm = src.scaled(int(size * 2), int(size * 2), Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        pm.setDevicePixelRatio(2.0)
        self._pix_cache[key] = pm
        return pm

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        rect = QRectF(0.5, 0.5, self.width() - 1.0, self.height() - 1.0)
        r = float(self._radius)

        p.setPen(Qt.NoPen)
        if self.isChecked():
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, self._grad_start)
            grad.setColorAt(1.0, self._grad_end)
            p.setBrush(QBrush(grad))
        else:
            bg = QColor(self._bg)
            if self.underMouse():
                bg = bg.lighter(118)
            p.setBrush(QBrush(bg))
        p.drawRoundedRect(rect, r, r)

        fg = self._fg()
        # icon in the upper-middle
        isz = float(self._icon_size)
        ipm = self._icon_pixmap(isz, fg)
        if not ipm.isNull():
            pr = ipm.devicePixelRatio() or 1.0
            iw, ih = ipm.width() / pr, ipm.height() / pr
            iy = self.height() * 0.40
            p.drawPixmap(QRectF(self.width() / 2.0 - iw / 2.0, iy - ih / 2.0, iw, ih),
                         ipm, QRectF(0, 0, ipm.width(), ipm.height()))

        # caption at the bottom (wraps for long names like "Air Conditioner")
        f = QFont(self.font())
        f.setPointSizeF(max(7.5, min(self.height() * 0.11, 13.0)))
        f.setBold(self.isChecked())
        p.setFont(f)
        p.setPen(QPen(fg))
        cap_rect = QRectF(6, self.height() * 0.62, self.width() - 12, self.height() * 0.34)
        p.drawText(cap_rect, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, self._caption)
        p.end()

    def sizeHint(self):
        from qtpy.QtCore import QSize
        return QSize(120, 120)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, t):
        self.setCaption(t)

    @Property(str)
    def iconPath(self):
        return self._icon_path

    @iconPath.setter
    def iconPath(self, p):
        self.setIconPath(p)

    @Property(QColor)
    def gradientStart(self):
        return self._grad_start

    @gradientStart.setter
    def gradientStart(self, c):
        self._grad_start = QColor(c)
        self.update()

    @Property(QColor)
    def gradientEnd(self):
        return self._grad_end

    @gradientEnd.setter
    def gradientEnd(self, c):
        self._grad_end = QColor(c)
        self.update()

    @Property(QColor)
    def bgColor(self):
        return self._bg

    @bgColor.setter
    def bgColor(self, c):
        self._bg = QColor(c)
        self.update()

    @Property(QColor)
    def iconColor(self):
        return self._icon_color

    @iconColor.setter
    def iconColor(self, c):
        self._icon_color = QColor(c)
        self._pix_cache.clear()
        self.update()

    @Property(QColor)
    def activeColor(self):
        return self._active_color

    @activeColor.setter
    def activeColor(self, c):
        self._active_color = QColor(c)
        self._pix_cache.clear()
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(int)
    def iconSize(self):
        return self._icon_size

    @iconSize.setter
    def iconSize(self, v):
        self._icon_size = max(8, int(v))
        self._pix_cache.clear()
        self.update()
