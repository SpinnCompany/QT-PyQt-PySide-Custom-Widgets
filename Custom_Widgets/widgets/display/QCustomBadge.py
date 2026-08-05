########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomBadge - a small status label / count / dot indicator.
##
## The modern, tokenized replacement for the legacy QBadgeWidget: a pill badge
## whose colour comes from a semantic `variant` (default / primary / secondary /
## success / warning / destructive / info / outline) via QSS attribute
## selectors, in three sizes (`sizeVariant`). Three modes:
##   * text  - setText("New")
##   * count - setCount(12, maxCount=99)  ->  "12" / "99+" (hidden at 0)
##   * dot   - setDot(True)               ->  a tiny coloured circle
## It can also float over another widget's corner via attachTo(). Emits clicked.
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QEvent
from qtpy.QtWidgets import QLabel, QSizePolicy, QWidget


class QCustomBadge(QLabel):
    clicked = Signal()

    WIDGET_ICON = "components/icons/badge.png"
    WIDGET_TOOLTIP = "A status / count / dot badge"
    WIDGET_MODULE = "Custom_Widgets.QCustomBadge"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomBadge' name='customBadge'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>48</width><height>22</height></rect></property>
            <property name='text'><string>Badge</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomBadge",
        "props": {"text": {"type": "string", "default": ""},
                  "variant": {"type": "enum",
                              "values": ["default", "primary", "secondary",
                                         "success", "warning", "destructive",
                                         "info", "outline"],
                              "default": "default"},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"},
                  "dot": {"type": "bool", "default": False}},
        "signals": ["clicked"],
        "tokens_used": ["surface-muted", "on-surface", "primary", "on-primary",
                        "secondary", "on-secondary", "success", "on-success",
                        "warning", "on-warning", "destructive", "on-destructive",
                        "info", "on-info", "outline"],
    }

    _VARIANTS = ("default", "primary", "secondary", "success", "warning",
                 "destructive", "info", "outline")
    _DOT_SIZE = {"sm": 8, "md": 10, "lg": 12}

    def __init__(self, text="", parent=None, variant="default"):
        # Qt Designer / uic instantiate custom widgets as ``Widget(parent)``.
        # ``text`` is the first positional arg, so a parent passed positionally
        # would be mistaken for the badge text (calling setText with a QWidget).
        # Detect a QWidget here and treat it as the parent instead.
        if isinstance(text, QWidget) and parent is None:
            text, parent = "", text
        super().__init__(parent)
        self.setObjectName("QCustomBadge")
        self._variant = variant if variant in self._VARIANTS else "default"
        self._sizeVariant = "md"
        self._dot = False
        self._count = None
        self._maxCount = 99
        self._showZero = False
        self._attachTarget = None
        self._attachCorner = "topright"
        self._attachOffset = (0, 0)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        super().setText(text or "")
        self._afterContent()

    # ------------------------------------------------------------------ #
    ## Content modes
    # ------------------------------------------------------------------ #
    def setText(self, text):
        """Plain-text badge (clears count / dot mode)."""
        self._count = None
        self._dot = False
        super().setText(text or "")
        self._afterContent()

    def setCount(self, count, maxCount=None):
        """Numeric badge. Shows ``maxCount+`` past the cap; hidden at 0 unless
        setShowZero(True)."""
        self._count = int(count)
        self._dot = False
        if maxCount is not None:
            self._maxCount = int(maxCount)
        self._renderCount()
        self._afterContent()

    def setDot(self, on=True):
        """Dot mode: a small coloured circle with no text."""
        self._dot = bool(on)
        if self._dot:
            self._count = None
            super().setText("")
        self._afterContent()

    def setShowZero(self, show):
        self._showZero = bool(show)
        if self._count is not None:
            self._renderCount()
            self._afterContent()

    def _renderCount(self):
        if self._count <= 0 and not self._showZero:
            super().setText("")
            self.setVisible(False)
            return
        self.setVisible(True)
        text = ("%d+" % self._maxCount) if self._count > self._maxCount else str(self._count)
        super().setText(text)

    def count(self):
        return self._count

    def isDot(self):
        return self._dot

    # ------------------------------------------------------------------ #
    ## Sizing / restyle
    # ------------------------------------------------------------------ #
    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)

    def _afterContent(self):
        self._repolish()
        if self._dot:
            d = self._DOT_SIZE.get(self._sizeVariant, 10)
            self.setFixedSize(d, d)
        else:
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
            self.adjustSize()
        self._reposition()

    # ------------------------------------------------------------------ #
    ## Overlay attachment
    # ------------------------------------------------------------------ #
    def attachTo(self, target, corner="topright", xOffset=0, yOffset=0):
        """Float this badge over ``target``'s corner (topright / topleft /
        bottomright / bottomleft), tracking its resize. Pass target=None to
        detach."""
        if self._attachTarget is not None:
            self._attachTarget.removeEventFilter(self)
        self._attachTarget = target
        self._attachCorner = corner
        self._attachOffset = (int(xOffset), int(yOffset))
        if target is not None:
            self.setParent(target)
            target.installEventFilter(self)
            self.show()
            self.raise_()
            self._reposition()

    def eventFilter(self, obj, event):
        if obj is getattr(self, "_attachTarget", None) and event.type() in (
                QEvent.Resize, QEvent.Show, QEvent.Move):
            self._reposition()
        return super().eventFilter(obj, event)

    def _reposition(self):
        t = self._attachTarget
        if t is None:
            return
        w, h = self.width(), self.height()
        tw, th = t.width(), t.height()
        dx, dy = self._attachOffset
        corner = self._attachCorner
        x = (tw - w - dx) if "right" in corner else dx
        y = (th - h - dy) if "bottom" in corner else dy
        self.move(x, y)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    # ------------------------------------------------------------------ #
    ## Designer properties (drive the QSS attribute selectors)
    # ------------------------------------------------------------------ #
    @Property(str)
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, value):
        value = str(value)
        self._variant = value if value in self._VARIANTS else "default"
        self._repolish()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        self._afterContent()

    @Property(bool)
    def dot(self):
        return self._dot

    @dot.setter
    def dot(self, value):
        self.setDot(value)
