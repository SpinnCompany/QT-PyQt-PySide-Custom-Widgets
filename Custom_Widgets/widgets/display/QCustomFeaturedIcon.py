########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomFeaturedIcon - an icon in a decorative container.
##
## The little coloured tile that sits above a feature headline or beside an
## empty state: an icon on a shaped, tinted background. Trivial to draw and
## tedious to redo by hand in every layout, which is exactly why it belongs in
## the catalog.
##
## Painted with QPainter; the icon itself is a QIcon so it themes and scales
## like every other icon in the library.
##
## Emits clicked() so it can double as a soft button.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QIcon, QLinearGradient
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomFeaturedIcon(QWidget):
    clicked = Signal()

    WIDGET_ICON = "components/icons/auto_awesome.png"
    WIDGET_TOOLTIP = "An icon in a decorative, tinted container"
    WIDGET_MODULE = "Custom_Widgets.QCustomFeaturedIcon"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFeaturedIcon' name='customFeaturedIcon'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>56</width><height>56</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomFeaturedIcon",
        "props": {"iconPath": {"type": "string", "default": ""},
                  "shape": {"type": "enum",
                            "values": ["circle", "rounded", "square"],
                            "default": "rounded"},
                  "variant": {"type": "enum",
                              "values": ["tinted", "filled", "outline", "gradient"],
                              "default": "tinted"},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg", "xl"],
                                  "default": "md"},
                  "cornerRadius": {"type": "int", "default": 12},
                  "accentColor": {"type": "color", "default": "#2563eb"},
                  "iconColor": {"type": "color", "default": "#2563eb"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"}},
        "signals": ["clicked"],
        "tokens_used": ["accent", "surface", "on-primary"],
    }

    _SIZES = {"sm": 36, "md": 48, "lg": 56, "xl": 72}
    _ICON_RATIO = 0.5

    def __init__(self, parent=None, icon=None, variant="tinted", shape="rounded"):
        super().__init__(parent)
        self.setObjectName("QCustomFeaturedIcon")
        self._icon = QIcon(icon) if icon else QIcon()
        self._iconPath = str(icon) if isinstance(icon, str) else ""
        self._shape = shape if shape in ("circle", "rounded", "square") else "rounded"
        self._variant = variant if variant in ("tinted", "filled", "outline",
                                               "gradient") else "tinted"
        self._sizeVariant = "md"
        self._radius = 12
        self._accent = QColor("#2563eb")
        self._iconColor = QColor("#2563eb")
        self._surface = QColor("#ffffff")

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)

    # ------------------------------------------------------------------ #
    ## Content
    # ------------------------------------------------------------------ #
    def setIcon(self, icon):
        self._icon = icon if isinstance(icon, QIcon) else QIcon(icon)
        self._iconPath = icon if isinstance(icon, str) else ""
        self.update()

    def icon(self):
        return self._icon

    def hasIcon(self):
        return not self._icon.isNull()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _side(self):
        return self._SIZES.get(self._sizeVariant, self._SIZES["md"])

    def sizeHint(self):
        side = self._side()
        return QSize(side, side)

    minimumSizeHint = sizeHint

    def _radiusFor(self, rect):
        if self._shape == "circle":
            return min(rect.width(), rect.height()) / 2.0
        if self._shape == "square":
            return 0.0
        return float(self._radius)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        radius = self._radiusFor(rect)

        if self._variant == "filled":
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._accent))
        elif self._variant == "outline":
            p.setPen(QPen(self._accent, 1.5))
            p.setBrush(QBrush(self._surface))
        elif self._variant == "gradient":
            gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
            gradient.setColorAt(0.0, self._accent.lighter(125))
            gradient.setColorAt(1.0, self._accent)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(gradient))
        else:
            tint = QColor(self._accent)
            tint.setAlphaF(0.14)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(tint))
        p.drawRoundedRect(rect, radius, radius)

        if self._icon.isNull():
            return
        side = min(rect.width(), rect.height()) * self._ICON_RATIO
        target = QRectF(rect.center().x() - side / 2.0,
                        rect.center().y() - side / 2.0, side, side)
        # A filled or gradient tile needs the icon in the on-primary colour or
        # it disappears into its own background.
        colour = (self._surface if self._variant in ("filled", "gradient")
                  else self._iconColor)
        pixmap = self._icon.pixmap(int(side), int(side))
        if not pixmap.isNull():
            tinted = self._tint(pixmap, colour)
            p.drawPixmap(target.toRect(), tinted)

    @staticmethod
    def _tint(pixmap, colour):
        """Recolour a pixmap, keeping its alpha."""
        from qtpy.QtGui import QPixmap
        result = QPixmap(pixmap.size())
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(result.rect(), colour)
        painter.end()
        return result

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def iconPath(self):
        return self._iconPath

    @iconPath.setter
    def iconPath(self, path):
        self.setIcon(str(path))

    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value)
        self._shape = value if value in ("circle", "rounded", "square") else "rounded"
        self.update()

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        value = str(value)
        self._variant = value if value in ("tinted", "filled", "outline",
                                           "gradient") else "tinted"
        self.update()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry(); self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, value):
        self._radius = max(0, int(value)); self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c); self.update()

    @Property(QColor)
    def iconColor(self):
        return self._iconColor

    @iconColor.setter
    def iconColor(self, c):
        self._iconColor = QColor(c); self.update()

    @Property(QColor)
    def surfaceColor(self):
        return self._surface

    @surfaceColor.setter
    def surfaceColor(self, c):
        self._surface = QColor(c); self.update()
