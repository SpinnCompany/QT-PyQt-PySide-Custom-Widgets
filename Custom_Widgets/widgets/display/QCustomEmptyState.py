########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomEmptyState - a centered "nothing here yet" placeholder.
##
## A mark + title + description + an optional action button. Tokenized.
## Emits actionClicked.
##
## The default mark is PAINTED, not a glyph. An emoji does not tint with the
## theme, does not scale cleanly, and renders as a different picture on every
## platform - the same reasoning as QCustomSparklesText's drawn star. setIcon()
## still accepts a string for anyone who wants one.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QPen, QPixmap
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton


def _emptyMarkPixmap(size, color, ratio=1.0):
    """An outlined sheet with two ruled lines - reads as "nothing in here".

    Drawn rather than shipped as an asset so it tints from the theme and stays
    crisp at any device pixel ratio.
    """
    pixmap = QPixmap(int(size * ratio), int(size * ratio))
    pixmap.setDevicePixelRatio(ratio)
    pixmap.fill(Qt.transparent)

    stroke = max(1.5, size / 24.0)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(color), stroke)
    pen.setJoinStyle(Qt.RoundJoin)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)

    inset = stroke + size * 0.12
    body = QRectF(inset, inset * 0.75, size - inset * 2, size - inset * 1.5)
    painter.drawRoundedRect(body, size * 0.09, size * 0.09)

    # Two ruled lines, the second deliberately short: a page that trails off.
    left = body.left() + body.width() * 0.18
    for index, width in enumerate((0.64, 0.40)):
        y = body.top() + body.height() * (0.40 + index * 0.24)
        painter.drawLine(int(left), int(y),
                         int(left + body.width() * width), int(y))
    painter.end()
    return pixmap


class QCustomEmptyState(QWidget):
    actionClicked = Signal()

    WIDGET_ICON = "components/icons/inbox.png"
    WIDGET_TOOLTIP = "An empty-state placeholder"
    WIDGET_MODULE = "Custom_Widgets.QCustomEmptyState"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomEmptyState' name='customEmptyState'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>220</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomEmptyState",
        "props": {"markSize": {"type": "int", "default": 56},
                  "markColor": {"type": "color", "default": "#cbd5e1"}},
        "signals": ["actionClicked"],
        "tokens_used": ["on-surface", "outline", "surface-muted", "accent"],
    }

    def __init__(self, parent=None, icon=None, title="Nothing here yet",
                 description=""):
        super().__init__(parent)
        self.setObjectName("QCustomEmptyState")
        col = QVBoxLayout(self)
        col.setAlignment(Qt.AlignCenter)
        col.setSpacing(8)

        self._markSize = 56
        self._markColor = QColor("#cbd5e1")     # outline role

        self._icon = QLabel(self)
        self._icon.setObjectName("emptyIcon")
        self._icon.setAlignment(Qt.AlignCenter)
        col.addWidget(self._icon, 0, Qt.AlignHCenter)
        # `icon=None` means the painted default; a string is still honoured.
        if icon is None:
            self._paintMark()
        else:
            self.setIcon(icon)

        self._title = QLabel(title, self)
        self._title.setObjectName("emptyTitle")
        self._title.setAlignment(Qt.AlignCenter)
        col.addWidget(self._title)

        self._desc = QLabel(description, self)
        self._desc.setObjectName("emptyDesc")
        self._desc.setAlignment(Qt.AlignCenter)
        self._desc.setWordWrap(True)
        self._desc.setVisible(bool(description))
        col.addWidget(self._desc)

        self._action = QCustomQPushButton(self)
        self._action.variant = "primary"
        self._action.setVisible(False)
        self._action.clicked.connect(self.actionClicked)
        col.addWidget(self._action, 0, Qt.AlignHCenter)

    # -- API --
    def _paintMark(self):
        """Redraw the default mark at the current size and colour."""
        ratio = float(self.devicePixelRatioF() or 1.0)
        self._icon.setText("")
        self._icon.setPixmap(
            _emptyMarkPixmap(self._markSize, self._markColor, ratio))

    def setIcon(self, glyph_or_pixmap):
        """A string, a pixmap, or None to go back to the painted default."""
        if glyph_or_pixmap is None:
            self._paintMark()
        elif isinstance(glyph_or_pixmap, str):
            self._icon.setPixmap(QPixmap())
            self._icon.setText(glyph_or_pixmap)
        else:
            self._icon.setText("")
            self._icon.setPixmap(glyph_or_pixmap)

    def setTitle(self, title):
        self._title.setText(title)

    def setDescription(self, description):
        self._desc.setText(description)
        self._desc.setVisible(bool(description))

    def setActionText(self, text):
        self._action.setText(text)
        self._action.setVisible(bool(text))

    def actionButton(self):
        return self._action

    # ------------------------------------------------------------------ #
    ## Designer properties
    #
    # The mark is themed through these rather than hardcoded, so it flips
    # with light/dark like every other painted widget in the library.
    # ------------------------------------------------------------------ #
    @Property(int)
    def markSize(self):
        return self._markSize

    @markSize.setter
    def markSize(self, value):
        self._markSize = max(16, int(value))
        if not self._icon.text():
            self._paintMark()

    @Property(QColor)
    def markColor(self):
        return self._markColor

    @markColor.setter
    def markColor(self, value):
        self._markColor = QColor(value)
        if not self._icon.text():
            self._paintMark()
