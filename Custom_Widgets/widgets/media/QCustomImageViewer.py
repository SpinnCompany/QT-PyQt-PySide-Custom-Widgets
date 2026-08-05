########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomImageViewer - a modal lightbox for a gallery of images.
##
## A frameless overlay that covers its host window with a dark scrim and
## shows one image centred (aspect-fit), with painted prev / next arrows, a
## close button and a "3 / 12" counter. Feed it images with setImages([...])
## (QPixmap / path) and open a given one with openAt(index, host); it parents
## itself to the host and resizes to cover it. Left / Right / Esc navigate and
## close; clicking the scrim closes. Emits indexChanged(int) and closed(). The
## scrim is intentionally dark in every theme (a lightbox convention); its
## colours are qproperties so a form can still retint them.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF, QPoint
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPolygonF, QPixmap, QFont
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QSizePolicy


class _NavButton(QWidget):
    """A painted circular button: kind = 'prev' | 'next' | 'close'."""
    clicked = Signal()

    def __init__(self, kind, parent=None):
        super().__init__(parent)
        self._kind = kind
        self._bg = QColor(255, 255, 255, 28)
        self._fg = QColor("#ffffff")
        self._hover = False
        self._d = 46 if kind != "close" else 40
        self.setFixedSize(self._d, self._d)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)

    def setColors(self, bg, fg):
        self._bg, self._fg = QColor(bg), QColor(fg)
        self.update()

    def enterEvent(self, e):
        self._hover = True
        self.update()

    def leaveEvent(self, e):
        self._hover = False
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        bg = QColor(self._bg)
        if self._hover:
            bg = bg.lighter(140)
            bg.setAlpha(min(255, self._bg.alpha() + 40))
        p.setBrush(QBrush(bg))
        p.drawEllipse(self.rect())
        c = self._d / 2.0
        pen = QPen(self._fg, max(2.0, self._d * 0.055))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        s = self._d * 0.17
        if self._kind == "close":
            p.drawLine(QPointF(c - s, c - s), QPointF(c + s, c + s))
            p.drawLine(QPointF(c - s, c + s), QPointF(c + s, c - s))
        elif self._kind == "prev":
            p.drawPolyline(QPolygonF([QPointF(c + s * 0.6, c - s),
                                      QPointF(c - s * 0.6, c),
                                      QPointF(c + s * 0.6, c + s)]))
        else:  # next
            p.drawPolyline(QPolygonF([QPointF(c - s * 0.6, c - s),
                                      QPointF(c + s * 0.6, c),
                                      QPointF(c - s * 0.6, c + s)]))
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        e.accept()


class QCustomImageViewer(QWidget):

    indexChanged = Signal(int)
    closed = Signal()

    WIDGET_ICON = "components/icons/image_viewer.png"
    WIDGET_TOOLTIP = "A modal lightbox for a gallery of images"
    WIDGET_MODULE = "Custom_Widgets.QCustomImageViewer"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomImageViewer' name='customImageViewer'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>480</width><height>320</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomImageViewer",
        "props": {
            "scrimColor": {"type": "color", "default": "#e60a0e18"},
            "buttonColor": {"type": "color", "default": "#1cffffff"},
            "buttonIconColor": {"type": "color", "default": "#ffffff"},
            "textColor": {"type": "color", "default": "#eef1f6"},
            "imageRadius": {"type": "int", "default": 16},
        },
        "signals": ["indexChanged", "closed"],
        "tokens_used": [],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomImageViewer")
        self._pixmaps = []
        self._index = 0
        self._scrim = QColor(10, 12, 24, 230)
        self._text = QColor("#eef1f6")
        self._radius = 16
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._prev = _NavButton("prev", self)
        self._next = _NavButton("next", self)
        self._close = _NavButton("close", self)
        self._prev.clicked.connect(lambda: self.setIndex(self._index - 1))
        self._next.clicked.connect(lambda: self.setIndex(self._index + 1))
        self._close.clicked.connect(self.close)
        self.hide()

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setImages(self, images):
        self._pixmaps = [im if isinstance(im, QPixmap) else QPixmap(str(im))
                         for im in (images or [])]
        self.update()

    def setImageAt(self, index, pm):
        """Swap one image in place (e.g. the full-res photo arriving async)."""
        pm = pm if isinstance(pm, QPixmap) else QPixmap(str(pm))
        if 0 <= index < len(self._pixmaps):
            self._pixmaps[index] = pm
            if index == self._index:
                self.update()

    def count(self):
        return len(self._pixmaps)

    def index(self):
        return self._index

    def setIndex(self, i):
        if not self._pixmaps:
            return
        i = max(0, min(len(self._pixmaps) - 1, int(i)))
        if i != self._index:
            self._index = i
            self.indexChanged.emit(i)
        self._syncNav()
        self.update()

    def openAt(self, index, host=None):
        """Cover `host` (or the current parent) and show image `index`."""
        if host is not None and host is not self.parent():
            self.setParent(host)
        parent = self.parent()
        if parent is not None:
            self.setGeometry(parent.rect())
        self._index = max(0, min(max(0, len(self._pixmaps) - 1), int(index)))
        self._syncNav()
        self.raise_()
        self.show()
        self.setFocus(Qt.OtherFocusReason)
        self.update()

    # ------------------------------------------------------------------ #
    ## Layout / paint
    # ------------------------------------------------------------------ #
    def _syncNav(self):
        multi = len(self._pixmaps) > 1
        self._prev.setVisible(multi)
        self._next.setVisible(multi)

    def resizeEvent(self, e):
        w, h = self.width(), self.height()
        m = 22
        self._close.move(w - self._close.width() - m, m)
        self._prev.move(m, (h - self._prev.height()) // 2)
        self._next.move(w - self._next.width() - m, (h - self._next.height()) // 2)
        super().resizeEvent(e)

    def _imageRect(self):
        w, h = self.width(), self.height()
        avail_w, avail_h = w - 200, h - 150
        pm = self._pixmaps[self._index] if self._pixmaps else None
        if pm is None or pm.isNull() or avail_w <= 0 or avail_h <= 0:
            return QRectF(), None
        scaled = pm.size().scaled(avail_w, avail_h, Qt.KeepAspectRatio)
        x = (w - scaled.width()) / 2.0
        y = (h - scaled.height()) / 2.0
        return QRectF(x, y, scaled.width(), scaled.height()), pm

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        p.fillRect(self.rect(), self._scrim)
        rect, pm = self._imageRect()
        if pm is not None:
            from qtpy.QtGui import QPainterPath
            path = QPainterPath()
            path.addRoundedRect(rect, self._radius, self._radius)
            p.save()
            p.setClipPath(path)
            p.drawPixmap(rect.toRect(), pm)
            p.restore()
        # counter
        if len(self._pixmaps) > 1:
            f = QFont(self.font())
            f.setPointSizeF(11)
            f.setWeight(QFont.DemiBold)
            p.setFont(f)
            p.setPen(QPen(self._text))
            txt = "%d / %d" % (self._index + 1, len(self._pixmaps))
            p.drawText(QRectF(0, 20, self.width(), 30), Qt.AlignHCenter | Qt.AlignVCenter, txt)
        p.end()

    def mousePressEvent(self, e):
        # click on the scrim (not the image) closes
        rect, pm = self._imageRect()
        if pm is None or not rect.contains(e.position()):
            self.close()
        e.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() in (Qt.Key_Left, Qt.Key_Up):
            self.setIndex(self._index - 1)
        elif e.key() in (Qt.Key_Right, Qt.Key_Down):
            self.setIndex(self._index + 1)
        else:
            super().keyPressEvent(e)

    def closeEvent(self, e):
        self.closed.emit()
        super().closeEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(QColor)
    def scrimColor(self):
        return self._scrim

    @scrimColor.setter
    def scrimColor(self, c):
        self._scrim = QColor(c)
        self.update()

    @Property(QColor)
    def buttonColor(self):
        return self._prev._bg

    @buttonColor.setter
    def buttonColor(self, c):
        for b in (self._prev, self._next, self._close):
            b.setColors(QColor(c), b._fg)

    @Property(QColor)
    def buttonIconColor(self):
        return self._prev._fg

    @buttonIconColor.setter
    def buttonIconColor(self, c):
        for b in (self._prev, self._next, self._close):
            b.setColors(b._bg, QColor(c))

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c)
        self.update()

    @Property(int)
    def imageRadius(self):
        return self._radius

    @imageRadius.setter
    def imageRadius(self, v):
        self._radius = max(0, int(v))
        self.update()
