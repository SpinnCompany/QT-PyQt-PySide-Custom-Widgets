########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomHeaderNav - a horizontal top navigation bar.
##
## The gap this fills: every navigation widget in the catalog is vertical
## (QCustomSidebar) or an overlay (QCustomSlideMenu, QCustomDrawer). A plain
## horizontal header - brand on the left, links in the middle, actions on the
## right - had to be assembled by hand every time.
##
## Painted rather than assembled from buttons so the active-item indicator can
## slide between items, and so overflow can collapse cleanly at narrow widths
## instead of clipping links off the edge.
##
## Items are authored with setItems([...]) or the itemsCsv property:
##
##     itemsCsv = "Home,Docs,Pricing,Blog"
##     itemsCsv = "home=Home,docs=Docs"       explicit key=label
##
## Emits itemSelected(str) with the item key, and brandClicked().
########################################################################
from qtpy.QtCore import (Qt, Signal, Property, QRectF, QSize, QPropertyAnimation,
                         QEasingCurve)
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomHeaderNav(QWidget):
    itemSelected = Signal(str)
    brandClicked = Signal()
    overflowClicked = Signal()

    WIDGET_ICON = "components/icons/menu.png"
    WIDGET_TOOLTIP = "A horizontal top navigation bar"
    WIDGET_MODULE = "Custom_Widgets.QCustomHeaderNav"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomHeaderNav' name='customHeaderNav'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>640</width><height>56</height></rect></property>
            <property name='itemsCsv'><string>Home,Docs,Pricing,Blog</string></property>
            <property name='brandText'><string>Spinn UI</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomHeaderNav",
        "props": {"itemsCsv": {"type": "string", "default": ""},
                  "brandText": {"type": "string", "default": ""},
                  "currentKey": {"type": "string", "default": ""},
                  "indicator": {"type": "enum",
                                "values": ["underline", "pill", "none"],
                                "default": "underline"},
                  "alignment": {"type": "enum",
                                "values": ["left", "center", "right"],
                                "default": "left"},
                  "itemSpacing": {"type": "int", "default": 8},
                  "barHeight": {"type": "int", "default": 56},
                  "animated": {"type": "bool", "default": True},
                  "showDivider": {"type": "bool", "default": True},
                  "accentColor": {"type": "color", "default": "#2563eb"},
                  "textColor": {"type": "color", "default": "#64748b"},
                  "activeTextColor": {"type": "color", "default": "#0f172a"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"},
                  "dividerColor": {"type": "color", "default": "#e2e8f0"}},
        "signals": ["itemSelected", "brandClicked", "overflowClicked"],
        "tokens_used": ["surface", "on-surface", "outline", "accent"],
    }

    _PAD = 16.0
    _ITEM_PAD = 14.0
    _OVERFLOW_W = 34.0

    def __init__(self, parent=None, items=None, brand=""):
        super().__init__(parent)
        self.setObjectName("QCustomHeaderNav")
        self._items = []            # list of (key, label)
        self._current = ""
        self._brand = str(brand)
        self._indicator = "underline"
        self._alignment = "left"
        self._spacing = 8
        self._barHeight = 56
        self._animated = True
        self._showDivider = True
        self._hover = -1
        self._rects = []
        self._brandRect = QRectF()
        self._overflowRect = QRectF()
        self._hiddenCount = 0
        self._indicatorX = 0.0
        self._indicatorW = 0.0

        self._accent = QColor("#2563eb")
        self._textColor = QColor("#64748b")
        self._activeTextColor = QColor("#0f172a")
        self._surface = QColor("#ffffff")
        self._dividerColor = QColor("#e2e8f0")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMouseTracking(True)

        self._anim = QPropertyAnimation(self, b"indicatorPos", self)
        self._anim.setDuration(180)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        if items:
            self.setItems(items)

    # ------------------------------------------------------------------ #
    ## Items
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalise(items):
        out = []
        for item in items or []:
            if isinstance(item, dict):
                label = str(item.get("label", item.get("key", "")))
                key = str(item.get("key", label))
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                key, label = str(item[0]), str(item[1])
            else:
                text = str(item)
                if "=" in text:
                    key, label = text.split("=", 1)
                    key, label = key.strip(), label.strip()
                else:
                    key = label = text.strip()
            if label:
                out.append((key, label))
        return out

    def setItems(self, items):
        """Replace the items, keeping the selection if its key survives."""
        previous = self._current
        self._items = self._normalise(items)
        self._current = ""
        self._hover = -1
        if previous and any(k == previous for k, _l in self._items):
            self.setCurrentKey(previous, animate=False)
        elif self._items:
            self.setCurrentKey(self._items[0][0], animate=False)
        self.updateGeometry()
        self.update()

    def items(self):
        return list(self._items)

    def count(self):
        return len(self._items)

    def labelFor(self, key):
        for k, label in self._items:
            if k == key:
                return label
        return ""

    def currentIndex(self):
        for i, (key, _l) in enumerate(self._items):
            if key == self._current:
                return i
        return -1

    def setCurrentIndex(self, index, animate=True):
        if 0 <= index < len(self._items):
            self.setCurrentKey(self._items[index][0], animate)

    def setCurrentKey(self, key, animate=True):
        key = str(key)
        if key == self._current or not any(k == key for k, _l in self._items):
            return False
        self._current = key
        self._moveIndicator(animate)
        self.update()
        self.itemSelected.emit(key)
        return True

    def currentKeyValue(self):
        return self._current

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(640, self._barHeight)

    def minimumSizeHint(self):
        return QSize(120, self._barHeight)

    def _brandWidth(self):
        if not self._brand:
            return 0.0
        fm = QFontMetrics(self._brandFont())
        return fm.horizontalAdvance(self._brand) + self._PAD

    def _brandFont(self):
        font = self.font()
        font.setBold(True)
        return font

    def _computeRects(self):
        """Lay items out, collapsing any that will not fit into an overflow.

        Items are dropped from the END rather than being squeezed: half a link
        is unreadable, and a "+2" affordance is honest about what is hidden.
        """
        fm = QFontMetrics(self.font())
        self._rects = []
        self._hiddenCount = 0
        top = (self.height() - self._barHeight) / 2.0
        self._brandRect = QRectF(self._PAD, top, self._brandWidth(),
                                 self._barHeight) if self._brand else QRectF()

        widths = [fm.horizontalAdvance(label) + self._ITEM_PAD * 2
                  for _k, label in self._items]
        available = self.width() - self._PAD * 2 - self._brandWidth()
        total = sum(widths) + self._spacing * max(0, len(widths) - 1)

        visible = len(widths)
        while visible > 0 and total > available - (self._OVERFLOW_W
                                                   if visible < len(widths) else 0):
            visible -= 1
            total = (sum(widths[:visible])
                     + self._spacing * max(0, visible - 1))
        self._hiddenCount = len(widths) - visible

        start = self._PAD + self._brandWidth()
        if self._alignment == "center" and visible:
            start = max(start, (self.width() - total) / 2.0)
        elif self._alignment == "right" and visible:
            start = max(start, self.width() - self._PAD - total
                        - (self._OVERFLOW_W if self._hiddenCount else 0))

        x = start
        for index in range(visible):
            self._rects.append(QRectF(x, top, widths[index], self._barHeight))
            x += widths[index] + self._spacing

        self._overflowRect = (QRectF(x, top, self._OVERFLOW_W, self._barHeight)
                              if self._hiddenCount else QRectF())

    def itemRects(self):
        """Always recomputed. Caching these meant a caller that resized without
        triggering a repaint read the layout from the previous width."""
        self._computeRects()
        return list(self._rects)

    def hiddenCount(self):
        self._computeRects()
        return self._hiddenCount

    def _moveIndicator(self, animate=True):
        self._computeRects()
        index = self.currentIndex()
        if not (0 <= index < len(self._rects)):
            self._indicatorW = 0.0
            return
        rect = self._rects[index]
        target = rect.left()
        self._indicatorW = rect.width()
        if animate and self._animated and self._indicatorX:
            self._anim.stop()
            self._anim.setStartValue(self._indicatorX)
            self._anim.setEndValue(target)
            self._anim.start()
        else:
            self._indicatorX = target

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._moveIndicator(animate=False)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self._computeRects()

        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._surface))
        p.drawRect(self.rect())

        if self._showDivider:
            p.setPen(QPen(self._dividerColor, 1))
            p.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

        if self._brand:
            p.setPen(QPen(self._activeTextColor))
            p.setFont(self._brandFont())
            p.drawText(self._brandRect, int(Qt.AlignVCenter | Qt.AlignLeft),
                       self._brand)

        p.setFont(self.font())
        index = self.currentIndex()
        if self._indicator != "none" and 0 <= index < len(self._rects):
            self._paintIndicator(p)

        for i, rect in enumerate(self._rects):
            key, label = self._items[i]
            active = key == self._current
            colour = self._activeTextColor if active else self._textColor
            if i == self._hover and not active:
                colour = self._activeTextColor
            p.setPen(QPen(colour))
            p.drawText(rect, int(Qt.AlignCenter), label)

        if self._hiddenCount:
            p.setPen(QPen(self._textColor))
            p.drawText(self._overflowRect, int(Qt.AlignCenter),
                       "+%d" % self._hiddenCount)

    def _paintIndicator(self, p):
        rect = self._rects[self.currentIndex()]
        x = self._indicatorX or rect.left()
        width = self._indicatorW or rect.width()
        if self._indicator == "pill":
            tint = QColor(self._accent)
            tint.setAlphaF(0.14)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(tint))
            p.drawRoundedRect(QRectF(x, rect.top() + 8, width,
                                     rect.height() - 16), 8, 8)
        else:
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._accent))
            p.drawRoundedRect(QRectF(x + 4, rect.bottom() - 4, width - 8, 3),
                              1.5, 1.5)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def itemAt(self, pos):
        from qtpy.QtCore import QPointF
        point = QPointF(pos)
        for index, rect in enumerate(self.itemRects()):
            if rect.contains(point):
                return index
        return -1

    def mouseMoveEvent(self, e):
        index = self.itemAt(e.pos())
        if index != self._hover:
            self._hover = index
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            from qtpy.QtCore import QPointF
            point = QPointF(e.pos())
            if self._brand and self._brandRect.contains(point):
                self.brandClicked.emit()
            elif self._hiddenCount and self._overflowRect.contains(point):
                self.overflowClicked.emit()
            else:
                index = self.itemAt(e.pos())
                if index >= 0:
                    self.setCurrentKey(self._items[index][0])
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def indicatorPos(self):
        return self._indicatorX

    @indicatorPos.setter
    def indicatorPos(self, value):
        self._indicatorX = float(value)
        self.update()

    @Property(str)
    def itemsCsv(self):
        return ",".join(label if key == label else "%s=%s" % (key, label)
                        for key, label in self._items)

    @itemsCsv.setter
    def itemsCsv(self, text):
        self.setItems([t for t in str(text).replace(";", ",").split(",")
                       if t.strip()])

    @Property(str)
    def brandText(self):
        return self._brand

    @brandText.setter
    def brandText(self, value):
        self._brand = str(value)
        self.updateGeometry(); self.update()

    @Property(str)
    def currentKey(self):
        return self._current

    @currentKey.setter
    def currentKey(self, value):
        self.setCurrentKey(value, animate=False)

    @Property(str)
    def indicator(self):
        return self._indicator

    @indicator.setter
    def indicator(self, value):
        value = str(value)
        self._indicator = value if value in ("underline", "pill", "none") else "underline"
        self.update()

    @Property(str)
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        value = str(value)
        self._alignment = value if value in ("left", "center", "right") else "left"
        self._moveIndicator(animate=False)
        self.update()

    @Property(int)
    def itemSpacing(self):
        return self._spacing

    @itemSpacing.setter
    def itemSpacing(self, value):
        self._spacing = max(0, int(value))
        self._moveIndicator(animate=False)
        self.update()

    @Property(int)
    def barHeight(self):
        return self._barHeight

    @barHeight.setter
    def barHeight(self, value):
        self._barHeight = max(24, int(value))
        self.updateGeometry(); self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, value):
        self._animated = bool(value)

    @Property(bool)
    def showDivider(self):
        return self._showDivider

    @showDivider.setter
    def showDivider(self, value):
        self._showDivider = bool(value); self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c); self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, c):
        self._textColor = QColor(c); self.update()

    @Property(QColor)
    def activeTextColor(self):
        return self._activeTextColor

    @activeTextColor.setter
    def activeTextColor(self, c):
        self._activeTextColor = QColor(c); self.update()

    @Property(QColor)
    def surfaceColor(self):
        return self._surface

    @surfaceColor.setter
    def surfaceColor(self, c):
        self._surface = QColor(c); self.update()

    @Property(QColor)
    def dividerColor(self):
        return self._dividerColor

    @dividerColor.setter
    def dividerColor(self, c):
        self._dividerColor = QColor(c); self.update()
