########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomSocialButton - a brand-coloured sign-in / share button.
##
## "Continue with GitHub", "Share on X". The brand colour is the whole point,
## so the widget ships a small table of them and picks the readable foreground
## automatically rather than making every caller look up a hex value and then
## get the contrast wrong.
##
## The brand MARK is deliberately not drawn: reproducing a company logo is a
## trademark question, not a painting one, so the caller supplies an icon and
## the widget supplies the colour, shape and layout. `brandColor` is exposed so
## an unlisted brand still works.
##
## Emits clicked().
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QIcon, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


from Custom_Widgets.accessibility import set_accessibility, QAccessible


class QCustomSocialButton(QWidget):
    clicked = Signal()

    WIDGET_ICON = "components/icons/share.png"
    WIDGET_TOOLTIP = "A brand-coloured social sign-in / share button"
    WIDGET_MODULE = "Custom_Widgets.QCustomSocialButton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSocialButton' name='customSocialButton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>220</width><height>40</height></rect></property>
            <property name='brand'><string>github</string></property>
            <property name='text'><string>Continue with GitHub</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSocialButton",
        "props": {"brand": {"type": "string", "default": "github"},
                  "text": {"type": "string", "default": ""},
                  "iconPath": {"type": "string", "default": ""},
                  "variant": {"type": "enum", "values": ["solid", "outline", "soft"],
                              "default": "solid"},
                  "shape": {"type": "enum", "values": ["rounded", "pill", "square"],
                            "default": "rounded"},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"},
                  "iconOnly": {"type": "bool", "default": False},
                  "brandColor": {"type": "color", "default": "#24292f"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"}},
        "signals": ["clicked"],
        "tokens_used": ["surface", "on-surface"],
    }

    #: Brand -> (colour, default caption). Colours only; no marks are drawn.
    BRANDS = {
        "github": ("#24292f", "Continue with GitHub"),
        "google": ("#ea4335", "Continue with Google"),
        "x": ("#000000", "Share on X"),
        "twitter": ("#1da1f2", "Share on Twitter"),
        "facebook": ("#1877f2", "Continue with Facebook"),
        "linkedin": ("#0a66c2", "Share on LinkedIn"),
        "youtube": ("#ff0000", "Watch on YouTube"),
        "discord": ("#5865f2", "Join on Discord"),
        "slack": ("#4a154b", "Add to Slack"),
        "apple": ("#000000", "Continue with Apple"),
        "microsoft": ("#00a4ef", "Continue with Microsoft"),
        "patreon": ("#f96854", "Support on Patreon"),
        "whatsapp": ("#25d366", "Share on WhatsApp"),
        "telegram": ("#26a5e4", "Share on Telegram"),
        "reddit": ("#ff4500", "Share on Reddit"),
        "instagram": ("#e4405f", "Follow on Instagram"),
    }

    _HEIGHTS = {"sm": 32, "md": 40, "lg": 48}

    def __init__(self, parent=None, brand="github", text=None, icon=None):
        super().__init__(parent)
        self.setObjectName("QCustomSocialButton")
        self._brand = ""
        self._text = ""
        self._icon = QIcon(icon) if icon else QIcon()
        self._iconPath = str(icon) if isinstance(icon, str) else ""
        self._variant = "solid"
        self._shape = "rounded"
        self._sizeVariant = "md"
        self._iconOnly = False
        self._brandColor = QColor("#24292f")
        self._surface = QColor("#ffffff")
        self._hovered = False

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        self.setBrand(brand)
        if text is not None:
            self._text = str(text)
        set_accessibility(self, QAccessible.Button, self._text or self.toolTip() or "Social button")

    # ------------------------------------------------------------------ #
    ## Brand
    # ------------------------------------------------------------------ #
    def setBrand(self, brand):
        """Adopt a known brand's colour and default caption.

        An unknown brand is kept as the name and leaves the colour alone, so
        `brandColor` still lets a caller support anything not in the table.
        """
        brand = str(brand).strip().lower()
        self._brand = brand
        known = self.BRANDS.get(brand)
        if known is not None:
            colour, caption = known
            self._brandColor = QColor(colour)
            if not self._text:
                self._text = caption
        self.updateGeometry()
        self.update()

    def brandNames(self):
        return sorted(self.BRANDS)

    def isKnownBrand(self):
        return self._brand in self.BRANDS

    def foregroundColor(self):
        """Readable text colour for the current fill.

        Uses relative luminance rather than a fixed pairing: a caller can set
        any brandColor, and white-on-yellow is unreadable.
        """
        if self._variant != "solid":
            return QColor(self._brandColor)
        colour = self._brandColor
        luminance = (0.2126 * colour.redF() + 0.7152 * colour.greenF()
                     + 0.0722 * colour.blueF())
        return QColor("#0f172a") if luminance > 0.6 else QColor("#ffffff")

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _height(self):
        return self._HEIGHTS.get(self._sizeVariant, self._HEIGHTS["md"])

    def sizeHint(self):
        height = self._height()
        if self._iconOnly:
            return QSize(height, height)
        fm = QFontMetrics(self.font())
        return QSize(fm.horizontalAdvance(self._text) + height + 26, height)

    def minimumSizeHint(self):
        height = self._height()
        return QSize(height, height)

    def _radiusFor(self, rect):
        if self._shape == "pill":
            return rect.height() / 2.0
        if self._shape == "square":
            return 0.0
        return 8.0

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        radius = self._radiusFor(rect)
        foreground = self.foregroundColor()

        if self._variant == "solid":
            fill = self._brandColor.lighter(112) if self._hovered else self._brandColor
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(fill))
        elif self._variant == "soft":
            tint = QColor(self._brandColor)
            tint.setAlphaF(0.22 if self._hovered else 0.14)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(tint))
        else:
            p.setPen(QPen(self._brandColor, 1.4))
            p.setBrush(QBrush(self._surface))
        p.drawRoundedRect(rect, radius, radius)

        fm = QFontMetrics(self.font())
        iconSide = rect.height() * 0.45
        if self._iconOnly:
            self._paintIcon(p, rect.center().x(), rect.center().y(), iconSide,
                            foreground)
            return

        width = fm.horizontalAdvance(self._text)
        total = (iconSide + 10 if not self._icon.isNull() else 0) + width
        x = rect.center().x() - total / 2.0
        if not self._icon.isNull():
            self._paintIcon(p, x + iconSide / 2.0, rect.center().y(), iconSide,
                            foreground)
            x += iconSide + 10
        p.setPen(QPen(foreground))
        p.drawText(QRectF(x, rect.top(), width + 2, rect.height()),
                   int(Qt.AlignVCenter | Qt.AlignLeft), self._text)

    def _paintIcon(self, p, cx, cy, side, colour):
        if self._icon.isNull():
            return
        pixmap = self._icon.pixmap(int(side), int(side))
        if pixmap.isNull():
            return
        from qtpy.QtGui import QPixmap
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)
        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), colour)
        painter.end()
        p.drawPixmap(QRectF(cx - side / 2.0, cy - side / 2.0, side, side).toRect(),
                     tinted)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def enterEvent(self, e):
        self._hovered = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
            self.clicked.emit()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self.setBrand(value)

    @Property(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def iconPath(self):
        return self._iconPath

    @iconPath.setter
    def iconPath(self, path):
        self._iconPath = str(path)
        self._icon = QIcon(self._iconPath)
        self.update()

    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        value = str(value)
        self._variant = value if value in ("solid", "outline", "soft") else "solid"
        self.update()

    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value)
        self._shape = value if value in ("rounded", "pill", "square") else "rounded"
        self.update()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self.updateGeometry(); self.update()

    @Property(bool)
    def iconOnly(self):
        return self._iconOnly

    @iconOnly.setter
    def iconOnly(self, value):
        self._iconOnly = bool(value)
        self.updateGeometry(); self.update()

    @Property(QColor)
    def brandColor(self):
        return self._brandColor

    @brandColor.setter
    def brandColor(self, c):
        self._brandColor = QColor(c); self.update()

    @Property(QColor)
    def surfaceColor(self):
        return self._surface

    @surfaceColor.setter
    def surfaceColor(self, c):
        self._surface = QColor(c); self.update()
