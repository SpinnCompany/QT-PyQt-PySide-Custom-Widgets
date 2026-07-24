########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomAgendaList - a schedule / event timeline list.
##
## The day-plan card (Running / Cycling / Gym / Swimming): each row has a left
## CONNECTOR RAIL with a per-item status marker, a time range, a bold title and a
## muted subtitle (location). Status is done / active / pending (colour + painted
## marker: a check, a filled dot, a hollow ring - no glyph fonts). The active row
## gets a highlighted rounded background.
##
## Feed rows with setItems([{time, endTime, title, subtitle, status, color}]) or
## the `itemsJson` Designer property. Painted with QPainter; rows FLEX to a row
## height that fits the text, so it sits happily inside a QScrollArea. Colours are
## qproperties so they flip with the theme. Signal: itemClicked(index).
########################################################################
import json

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QSize
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomAgendaList(QWidget):

    itemClicked = Signal(int)

    WIDGET_ICON = "components/icons/agenda.png"
    WIDGET_TOOLTIP = "A schedule / event timeline list (rail + status rows)"
    WIDGET_MODULE = "Custom_Widgets.QCustomAgendaList"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomAgendaList' name='customAgendaList'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>320</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomAgendaList",
        "props": {
            "itemsJson": {"type": "string", "default": ""},
            "rowHeight": {"type": "int", "default": 0},
            "railColor": {"type": "color", "default": "#2b3040"},
            "doneColor": {"type": "color", "default": "#22c07e"},
            "activeColor": {"type": "color", "default": "#f59e0b"},
            "pendingColor": {"type": "color", "default": "#8b90a0"},
            "titleColor": {"type": "color", "default": "#f4f6fb"},
            "subtitleColor": {"type": "color", "default": "#8b90a0"},
            "timeColor": {"type": "color", "default": "#aab2bd"},
            "activeBgColor": {"type": "color", "default": "#1e2330"},
            "showRail": {"type": "bool", "default": True},
        },
        "signals": ["itemClicked"],
        "tokens_used": ["accent", "up"],
    }

    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.setObjectName("QCustomAgendaList")
        self._items = list(items) if items is not None else self._seed()
        self._row_h = 0                # 0 -> auto
        self._rail = QColor("#2b3040")
        self._done = QColor("#22c07e")
        self._active = QColor("#f59e0b")
        self._pending = QColor("#8b90a0")
        self._title_c = QColor("#f4f6fb")
        self._sub_c = QColor("#8b90a0")
        self._time_c = QColor("#aab2bd")
        self._active_bg = QColor("#1e2330")
        self._show_rail = True
        self._hover = -1
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _seed():
        return [
            {"time": "08:00", "endTime": "08:30", "title": "Running",
             "subtitle": "Central park", "status": "done", "color": "#f97316"},
            {"time": "09:00", "endTime": "09:45", "title": "Cycling",
             "subtitle": "Central park", "status": "done", "color": "#8b5cf6"},
            {"time": "11:00", "endTime": "12:30", "title": "Gym",
             "subtitle": "Sport club “Gladiator”", "status": "active",
             "color": "#ef4444"},
            {"time": "16:00", "endTime": "16:30", "title": "Swimming",
             "subtitle": "Swimming pool “Ariel”", "status": "pending",
             "color": "#3aa0ff"},
        ]

    def setItems(self, items):
        self._items = [dict(it) for it in (items or [])]
        self.updateGeometry()
        self.update()

    def items(self):
        return list(self._items)

    def _status_color(self, status):
        return {"done": self._done, "active": self._active,
                "pending": self._pending}.get(status, self._pending)

    # ------------------------------------------------------------------ #
    ## Sizing (flex row height that fits the text)
    # ------------------------------------------------------------------ #
    def _fonts(self):
        time_f = QFont(self.font()); time_f.setPointSizeF(max(8.0, self.font().pointSizeF() * 0.86))
        title_f = QFont(self.font()); title_f.setBold(True)
        title_f.setPointSizeF(max(10.5, self.font().pointSizeF() * 1.06))
        sub_f = QFont(self.font()); sub_f.setPointSizeF(max(8.5, self.font().pointSizeF() * 0.92))
        return time_f, title_f, sub_f

    def _row_height(self):
        if self._row_h > 0:
            return float(self._row_h)
        tf, tif, sf = self._fonts()
        h = (QFontMetrics(tf).height() + QFontMetrics(tif).height()
             + QFontMetrics(sf).height())
        return h + 26.0                # padding + inter-line gaps

    def sizeHint(self):
        return QSize(300, int(max(1, len(self._items)) * self._row_height()))

    def minimumSizeHint(self):
        return QSize(160, int(self._row_height()))

    def heightForWidth(self, w):
        return int(len(self._items) * self._row_height())

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._items:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        rh = self._row_height()
        rail_w = 46.0
        rx = rail_w / 2.0
        marker_r = min(13.0, rh * 0.18)
        time_f, title_f, sub_f = self._fonts()
        n = len(self._items)

        # rail line behind the markers
        if self._show_rail and n > 1:
            p.setPen(QPen(self._rail, 2.0))
            p.drawLine(QPointF(rx, rh * 0.5), QPointF(rx, (n - 0.5) * rh))

        for i, it in enumerate(self._items):
            y = i * rh
            cy = y + rh / 2.0
            status = it.get("status", "pending")
            sc = self._status_color(status)

            if status == "active":
                bg = QRectF(rail_w - 2, y + 4, self.width() - rail_w - 2, rh - 8)
                p.setPen(Qt.NoPen)
                p.setBrush(QBrush(self._active_bg))
                p.drawRoundedRect(bg, 12, 12)
            if i == self._hover and status != "active":
                bg = QRectF(rail_w - 2, y + 4, self.width() - rail_w - 2, rh - 8)
                hc = QColor(self._active_bg); hc.setAlpha(120)
                p.setPen(Qt.NoPen); p.setBrush(QBrush(hc))
                p.drawRoundedRect(bg, 12, 12)

            self._paint_marker(p, QPointF(rx, cy), marker_r, status, sc,
                               QColor(it.get("color", sc.name())))

            # text block: time / title / subtitle
            tx = rail_w + 8
            tw = self.width() - tx - 12
            p.setFont(time_f)
            p.setPen(QPen(self._time_c))
            th = QFontMetrics(time_f).height()
            tr = it.get("time", "")
            if it.get("endTime"):
                tr = "%s — %s" % (tr, it["endTime"])
            top = y + (rh - (th + QFontMetrics(title_f).height()
                             + QFontMetrics(sub_f).height() + 4)) / 2.0
            p.drawText(QRectF(tx, top, tw, th), Qt.AlignVCenter | Qt.AlignLeft, tr)
            p.setFont(title_f)
            p.setPen(QPen(self._title_c))
            tih = QFontMetrics(title_f).height()
            p.drawText(QRectF(tx, top + th + 2, tw, tih),
                       Qt.AlignVCenter | Qt.AlignLeft, it.get("title", ""))
            p.setFont(sub_f)
            p.setPen(QPen(self._sub_c))
            sh = QFontMetrics(sub_f).height()
            p.drawText(QRectF(tx, top + th + tih + 4, tw, sh),
                       Qt.AlignVCenter | Qt.AlignLeft, it.get("subtitle", ""))
        p.end()

    def _paint_marker(self, p, c, r, status, sc, item_color):
        if status == "done":
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(sc))
            p.drawEllipse(c, r, r)
            # painted check (no glyph)
            pen = QPen(QColor("#0e1016"), max(1.6, r * 0.22))
            pen.setCapStyle(Qt.RoundCap); pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.drawPolyline([QPointF(c.x() - r * 0.42, c.y() + r * 0.02),
                            QPointF(c.x() - r * 0.08, c.y() + r * 0.36),
                            QPointF(c.x() + r * 0.46, c.y() - r * 0.34)])
        elif status == "active":
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(sc))
            p.drawEllipse(c, r, r)
            p.setBrush(QBrush(QColor("#ffffff")))
            p.drawEllipse(c, r * 0.34, r * 0.34)
        else:                            # pending: hollow ring
            pen = QPen(sc, max(1.6, r * 0.20))
            p.setPen(pen)
            p.setBrush(QBrush(QColor(self._active_bg)))
            p.drawEllipse(c, r * 0.82, r * 0.82)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _row_at(self, pos):
        rh = self._row_height()
        i = int(pos.y() // rh)
        return i if 0 <= i < len(self._items) else -1

    def mouseMoveEvent(self, e):
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        i = self._row_at(pos)
        if i != self._hover:
            self._hover = i
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return super().mousePressEvent(e)
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        i = self._row_at(pos)
        if i >= 0:
            self.itemClicked.emit(i)
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def itemsJson(self):
        try:
            return json.dumps(self._items)
        except Exception:
            return "[]"

    @itemsJson.setter
    def itemsJson(self, text):
        try:
            data = json.loads(text) if str(text).strip() else []
            if isinstance(data, list):
                self.setItems(data)
        except Exception:
            pass

    @Property(int)
    def rowHeight(self):
        return self._row_h

    @rowHeight.setter
    def rowHeight(self, v):
        self._row_h = max(0, int(v))
        self.updateGeometry()
        self.update()

    @Property(QColor)
    def railColor(self):
        return self._rail

    @railColor.setter
    def railColor(self, c):
        self._rail = QColor(c)
        self.update()

    @Property(QColor)
    def doneColor(self):
        return self._done

    @doneColor.setter
    def doneColor(self, c):
        self._done = QColor(c)
        self.update()

    @Property(QColor)
    def activeColor(self):
        return self._active

    @activeColor.setter
    def activeColor(self, c):
        self._active = QColor(c)
        self.update()

    @Property(QColor)
    def pendingColor(self):
        return self._pending

    @pendingColor.setter
    def pendingColor(self, c):
        self._pending = QColor(c)
        self.update()

    @Property(QColor)
    def titleColor(self):
        return self._title_c

    @titleColor.setter
    def titleColor(self, c):
        self._title_c = QColor(c)
        self.update()

    @Property(QColor)
    def subtitleColor(self):
        return self._sub_c

    @subtitleColor.setter
    def subtitleColor(self, c):
        self._sub_c = QColor(c)
        self.update()

    @Property(QColor)
    def timeColor(self):
        return self._time_c

    @timeColor.setter
    def timeColor(self, c):
        self._time_c = QColor(c)
        self.update()

    @Property(QColor)
    def activeBgColor(self):
        return self._active_bg

    @activeBgColor.setter
    def activeBgColor(self, c):
        self._active_bg = QColor(c)
        self.update()

    @Property(bool)
    def showRail(self):
        return self._show_rail

    @showRail.setter
    def showRail(self, v):
        self._show_rail = bool(v)
        self.update()
