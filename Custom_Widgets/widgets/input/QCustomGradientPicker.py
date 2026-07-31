########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomGradientPicker - an editable multi-stop gradient control.
##
## A gradient preview with draggable colour stops beneath it. Click the bar to
## add a stop, drag a handle to move it, double-click a handle to recolour it,
## Delete to remove it. Qt ships a colour dialog but nothing that edits a
## gradient, so anything needing one has had to hand-roll it.
##
## Stops are held sorted by position and always number at least two - a
## "gradient" with one stop is a fill, and allowing it would make every
## consumer handle a degenerate case that has no reason to exist.
##
## Alpha is preserved throughout and the preview is drawn over a checkerboard,
## so a translucent stop is visible as translucent rather than silently
## composited against whatever is behind the widget.
##
## Emits gradientChanged(str) carrying the CSS-ish stop list, and
## stopSelected(int).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QLinearGradient,
                        QRadialGradient)
from qtpy.QtWidgets import QWidget, QSizePolicy, QColorDialog


class QCustomGradientPicker(QWidget):
    gradientChanged = Signal(str)
    stopSelected = Signal(int)

    WIDGET_ICON = "components/icons/gradient.png"
    WIDGET_TOOLTIP = "An editable multi-stop gradient picker"
    WIDGET_MODULE = "Custom_Widgets.QCustomGradientPicker"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomGradientPicker' name='customGradientPicker'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>280</width><height>72</height></rect></property>
            <property name='stopsCsv'><string>0:#2563eb,1:#16a34a</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomGradientPicker",
        "props": {"stopsCsv": {"type": "string", "default": "0:#2563eb,1:#16a34a"},
                  "gradientType": {"type": "enum", "values": ["linear", "radial"],
                                   "default": "linear"},
                  "angle": {"type": "int", "default": 0},
                  "barHeight": {"type": "int", "default": 28},
                  "handleRadius": {"type": "int", "default": 7},
                  "readOnly": {"type": "bool", "default": False},
                  "state": {"type": "enum", "values": ["default", "error"],
                            "default": "default"}},
        "signals": ["gradientChanged", "stopSelected"],
        "tokens_used": ["surface", "on-surface", "outline", "focus-ring",
                        "destructive"],
    }

    MIN_STOPS = 2
    _CHECKER = 6            # checkerboard square size, px

    def __init__(self, parent=None, stops=None, gradientType="linear"):
        super().__init__(parent)
        self.setObjectName("QCustomGradientPicker")
        self._stops = []            # list of [position float, QColor]
        self._selected = 0
        self._dragging = -1
        self._type = "radial" if gradientType == "radial" else "linear"
        self._angle = 0
        self._barHeight = 28
        self._handleRadius = 7
        self._readOnly = False
        self._state = "default"

        self._borderColor = QColor("#cbd5e1")
        self._borderActiveColor = QColor("#2563eb")
        self._borderErrorColor = QColor("#dc2626")
        self._handleColor = QColor("#ffffff")
        self._handleBorderColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.setStops(stops if stops is not None
                      else [(0.0, "#2563eb"), (1.0, "#16a34a")])

    # ------------------------------------------------------------------ #
    ## Stops
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(stop):
        """Accept (pos, colour) in most spellings; None if unusable."""
        if isinstance(stop, dict):
            pos, colour = stop.get("position"), stop.get("color")
        elif isinstance(stop, (tuple, list)) and len(stop) >= 2:
            pos, colour = stop[0], stop[1]
        else:
            return None
        try:
            pos = float(pos)
        except (TypeError, ValueError):
            return None
        colour = QColor(colour)
        if not colour.isValid():
            return None
        return [min(1.0, max(0.0, pos)), colour]

    def setStops(self, stops):
        """Replace every stop. Fewer than two valid stops is rejected."""
        parsed = [s for s in (self._coerce(x) for x in (stops or [])) if s]
        if len(parsed) < self.MIN_STOPS:
            return False
        parsed.sort(key=lambda s: s[0])
        self._stops = parsed
        self._selected = min(self._selected, len(self._stops) - 1)
        self.update()
        self.gradientChanged.emit(self.stopsCsv)
        return True

    def stops(self):
        """[(position, QColor), ...] sorted by position."""
        return [(pos, QColor(colour)) for pos, colour in self._stops]

    def count(self):
        return len(self._stops)

    def addStop(self, position, colour=None):
        """Insert a stop. Colour defaults to the gradient's colour there."""
        position = min(1.0, max(0.0, float(position)))
        colour = QColor(colour) if colour is not None else self.colorAt(position)
        self._stops.append([position, colour])
        self._stops.sort(key=lambda s: s[0])
        self._selected = next(i for i, s in enumerate(self._stops)
                              if s[0] == position and s[1] == colour)
        self.update()
        self.gradientChanged.emit(self.stopsCsv)
        self.stopSelected.emit(self._selected)
        return self._selected

    def removeStop(self, index):
        """Remove a stop. Refuses to go below MIN_STOPS."""
        if not (0 <= index < len(self._stops)):
            return False
        if len(self._stops) <= self.MIN_STOPS:
            return False
        del self._stops[index]
        self._selected = min(self._selected, len(self._stops) - 1)
        self.update()
        self.gradientChanged.emit(self.stopsCsv)
        return True

    def setStopColor(self, index, colour):
        if not (0 <= index < len(self._stops)):
            return False
        colour = QColor(colour)
        if not colour.isValid():
            return False
        self._stops[index][1] = colour
        self.update()
        self.gradientChanged.emit(self.stopsCsv)
        return True

    def setStopPosition(self, index, position):
        if not (0 <= index < len(self._stops)):
            return False
        target = self._stops[index]
        target[0] = min(1.0, max(0.0, float(position)))
        # Keep the list sorted and the selection pointing at the same stop.
        self._stops.sort(key=lambda s: s[0])
        self._selected = self._stops.index(target)
        self.update()
        self.gradientChanged.emit(self.stopsCsv)
        return True

    def stopColor(self, index):
        if 0 <= index < len(self._stops):
            return QColor(self._stops[index][1])
        return QColor()

    def stopPosition(self, index):
        if 0 <= index < len(self._stops):
            return self._stops[index][0]
        return -1.0

    def selectedIndex(self):
        return self._selected

    def setSelectedIndex(self, index):
        if 0 <= index < len(self._stops) and index != self._selected:
            self._selected = index
            self.update()
            self.stopSelected.emit(index)

    def colorAt(self, position):
        """Interpolated colour at a position, matching what the bar paints."""
        position = min(1.0, max(0.0, float(position)))
        if not self._stops:
            return QColor()
        if position <= self._stops[0][0]:
            return QColor(self._stops[0][1])
        if position >= self._stops[-1][0]:
            return QColor(self._stops[-1][1])
        for i in range(len(self._stops) - 1):
            p0, c0 = self._stops[i]
            p1, c1 = self._stops[i + 1]
            if p0 <= position <= p1:
                span = (p1 - p0) or 1.0
                t = (position - p0) / span
                return QColor(
                    int(c0.red() + (c1.red() - c0.red()) * t),
                    int(c0.green() + (c1.green() - c0.green()) * t),
                    int(c0.blue() + (c1.blue() - c0.blue()) * t),
                    int(c0.alpha() + (c1.alpha() - c0.alpha()) * t))
        return QColor(self._stops[-1][1])

    def gradient(self, rect=None):
        """A QGradient over `rect` (defaults to the preview bar)."""
        rect = rect if rect is not None else self._barRect()
        if self._type == "radial":
            grad = QRadialGradient(rect.center(),
                                   max(rect.width(), rect.height()) / 2.0)
        else:
            import math
            radians = math.radians(self._angle)
            dx, dy = math.cos(radians), math.sin(radians)
            cx, cy = rect.center().x(), rect.center().y()
            half_w, half_h = rect.width() / 2.0, rect.height() / 2.0
            grad = QLinearGradient(QPointF(cx - dx * half_w, cy - dy * half_h),
                                   QPointF(cx + dx * half_w, cy + dy * half_h))
        for pos, colour in self._stops:
            grad.setColorAt(pos, colour)
        return grad

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _handleStrip(self):
        return self._handleRadius * 2 + 6

    def sizeHint(self):
        return QSize(280, self._barHeight + self._handleStrip() + 6)

    minimumSizeHint = sizeHint

    def _barRect(self):
        inset = float(self._handleRadius)
        return QRectF(inset, 2, max(1.0, self.width() - 2 * inset), self._barHeight)

    def _handleCenter(self, index):
        bar = self._barRect()
        pos = self._stops[index][0]
        return QPointF(bar.left() + pos * bar.width(),
                       bar.bottom() + 4 + self._handleRadius)

    def handleAt(self, point):
        """Index of the stop handle under a point, or -1. Topmost wins."""
        point = QPointF(point)
        best, best_dist = -1, None
        for i in range(len(self._stops)):
            centre = self._handleCenter(i)
            dx, dy = point.x() - centre.x(), point.y() - centre.y()
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= self._handleRadius + 2 and (best_dist is None or dist < best_dist):
                best, best_dist = i, dist
        return best

    def _positionFor(self, x):
        bar = self._barRect()
        if bar.width() <= 0:
            return 0.0
        return min(1.0, max(0.0, (float(x) - bar.left()) / bar.width()))

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        bar = self._barRect()

        self._paintChecker(p, bar)
        p.setBrush(QBrush(self.gradient(bar)))
        if self._state == "error":
            border = self._borderErrorColor
        elif self.hasFocus():
            border = self._borderActiveColor
        else:
            border = self._borderColor
        p.setPen(QPen(border, 1))
        p.drawRoundedRect(bar, 6, 6)

        for i in range(len(self._stops)):
            self._paintHandle(p, i, i == self._selected)

    def _paintChecker(self, p, rect):
        """Checkerboard behind the bar so alpha reads as alpha."""
        p.save()
        p.setClipRect(rect)
        p.fillRect(rect, QBrush(QColor("#ffffff")))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor("#e2e8f0")))
        size = self._CHECKER
        rows = int(rect.height() // size) + 1
        cols = int(rect.width() // size) + 1
        for row in range(rows):
            for col in range(cols):
                if (row + col) % 2:
                    p.drawRect(QRectF(rect.left() + col * size,
                                      rect.top() + row * size, size, size))
        p.restore()

    def _paintHandle(self, p, index, selected):
        centre = self._handleCenter(index)
        radius = float(self._handleRadius)
        colour = self._stops[index][1]

        p.setPen(QPen(self._handleBorderColor, 2 if selected else 1))
        p.setBrush(QBrush(self._handleColor))
        p.drawEllipse(centre, radius, radius)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(colour))
        p.drawEllipse(centre, radius - 3, radius - 3)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, e):
        if self._readOnly or e.button() != Qt.LeftButton:
            super().mousePressEvent(e)
            return
        index = self.handleAt(e.pos())
        if index >= 0:
            self._dragging = index
            self.setSelectedIndex(index)
            return
        if self._barRect().contains(QPointF(e.pos())):
            self.addStop(self._positionFor(e.pos().x()))
            return
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._dragging >= 0 and not self._readOnly:
            self.setStopPosition(self._dragging, self._positionFor(e.pos().x()))
            self._dragging = self._selected      # sorting may have reindexed it
            return
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self._dragging = -1
        super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self._readOnly:
            return
        index = self.handleAt(e.pos())
        if index >= 0:
            self.editStopColor(index)
            return
        super().mouseDoubleClickEvent(e)

    def editStopColor(self, index=None):
        """Open a colour dialog for a stop. Returns True if it changed."""
        if self._readOnly:
            return False
        index = self._selected if index is None else index
        if not (0 <= index < len(self._stops)):
            return False
        chosen = QColorDialog.getColor(
            self._stops[index][1], self, "Stop colour",
            QColorDialog.ShowAlphaChannel)
        if not chosen.isValid():
            return False
        return self.setStopColor(index, chosen)

    def keyPressEvent(self, e):
        if self._readOnly:
            super().keyPressEvent(e)
            return
        key = e.key()
        if key in (Qt.Key_Delete, Qt.Key_Backspace):
            self.removeStop(self._selected)
            return
        if key == Qt.Key_Left:
            self.setStopPosition(self._selected,
                                 self.stopPosition(self._selected) - 0.01)
            return
        if key == Qt.Key_Right:
            self.setStopPosition(self._selected,
                                 self.stopPosition(self._selected) + 0.01)
            return
        if key == Qt.Key_Tab and self._stops:
            self.setSelectedIndex((self._selected + 1) % len(self._stops))
            return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self.editStopColor()
            return
        super().keyPressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def stopsCsv(self):
        out = []
        for pos, colour in self._stops:
            name = colour.name(QColor.HexArgb) if colour.alpha() < 255 else colour.name()
            out.append("%g:%s" % (pos, name))
        return ",".join(out)

    @stopsCsv.setter
    def stopsCsv(self, text):
        parsed = []
        for token in str(text).replace(";", ",").split(","):
            token = token.strip()
            if not token or ":" not in token:
                continue
            pos, _, colour = token.partition(":")
            parsed.append((pos.strip(), colour.strip()))
        self.setStops(parsed)

    @Property(str)
    def gradientType(self):
        return self._type

    @gradientType.setter
    def gradientType(self, value):
        self._type = "radial" if str(value) == "radial" else "linear"
        self.update()

    @Property(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = int(value) % 360
        self.update()

    @Property(int)
    def barHeight(self):
        return self._barHeight

    @barHeight.setter
    def barHeight(self, value):
        self._barHeight = max(6, int(value))
        self.updateGeometry(); self.update()

    @Property(int)
    def handleRadius(self):
        return self._handleRadius

    @handleRadius.setter
    def handleRadius(self, value):
        self._handleRadius = max(3, int(value))
        self.updateGeometry(); self.update()

    @Property(bool)
    def readOnly(self):
        return self._readOnly

    @readOnly.setter
    def readOnly(self, value):
        self._readOnly = bool(value)
        self.setCursor(Qt.ArrowCursor if self._readOnly else Qt.PointingHandCursor)

    @Property(str)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = "error" if str(value) == "error" else "default"
        self.update()

    # -- colours (from tokens via qproperty) --
    @Property(QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, c):
        self._borderColor = QColor(c); self.update()

    @Property(QColor)
    def borderActiveColor(self):
        return self._borderActiveColor

    @borderActiveColor.setter
    def borderActiveColor(self, c):
        self._borderActiveColor = QColor(c); self.update()

    @Property(QColor)
    def borderErrorColor(self):
        return self._borderErrorColor

    @borderErrorColor.setter
    def borderErrorColor(self, c):
        self._borderErrorColor = QColor(c); self.update()

    @Property(QColor)
    def handleColor(self):
        return self._handleColor

    @handleColor.setter
    def handleColor(self, c):
        self._handleColor = QColor(c); self.update()

    @Property(QColor)
    def handleBorderColor(self):
        return self._handleBorderColor

    @handleBorderColor.setter
    def handleBorderColor(self, c):
        self._handleBorderColor = QColor(c); self.update()
