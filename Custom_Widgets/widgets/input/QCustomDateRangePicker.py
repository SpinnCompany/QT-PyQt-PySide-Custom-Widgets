########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomDateRangePicker - an INLINE dual-month range calendar.
##
## The travel-dates / booking range picker: N month grids side by side, a painted
## in-range BAND between the two chosen days (rounded at the range ends and each
## week wrap), green endpoint circles, a "today" marker and month nav arrows.
## Click a day to set the start (clears the end); click a later day to set the
## end. This is the piece the compact popup QCustomDateRangeEdit lacks.
##
## Painted with QPainter; the month panels flex to the widget and stack vertically
## when it is too narrow. Colours are qproperties so they flip with the theme.
## API: setStartDate/setEndDate/setRange(QDate...), monthsVisible; navigation
## arrows; signal rangeChanged(QDate start, QDate end).
########################################################################
import calendar

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QDate
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont, QPainterPath, QFontMetrics
from qtpy.QtWidgets import QWidget, QSizePolicy

_WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
_MONTHS = ["", "January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


class QCustomDateRangePicker(QWidget):

    rangeChanged = Signal(QDate, QDate)

    WIDGET_ICON = "components/icons/calendar.png"
    WIDGET_TOOLTIP = "An inline dual-month date range calendar"
    WIDGET_MODULE = "Custom_Widgets.QCustomDateRangePicker"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomDateRangePicker' name='customDateRangePicker'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>560</width><height>300</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomDateRangePicker",
        "props": {
            "monthsVisible": {"type": "int", "default": 2},
            "accentColor": {"type": "color", "default": "#2f8f5b"},
            "rangeBandColor": {"type": "color", "default": "#e9edf0"},
            "todayColor": {"type": "color", "default": "#2f8f5b"},
            "textColor": {"type": "color", "default": "#1c2430"},
            "mutedColor": {"type": "color", "default": "#aab2bd"},
            "headerColor": {"type": "color", "default": "#1c2430"},
            "selectedTextColor": {"type": "color", "default": "#ffffff"},
        },
        "signals": ["rangeChanged"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, start=None, end=None, monthsVisible=2):
        super().__init__(parent)
        self.setObjectName("QCustomDateRangePicker")
        self._start = start if isinstance(start, QDate) else QDate(2025, 6, 23)
        self._end = end if isinstance(end, QDate) else QDate(2025, 7, 9)
        self._min = QDate()
        self._max = QDate()
        self._months = max(1, int(monthsVisible))
        self._first = QDate(self._start.year(), self._start.month(), 1)
        self._accent = QColor("#2f8f5b")
        self._band = QColor("#e9edf0")
        self._today_color = QColor("#2f8f5b")
        self._text = QColor("#1c2430")
        self._muted = QColor("#aab2bd")
        self._header = QColor("#1c2430")
        self._sel_text = QColor("#ffffff")
        self._cal = calendar.Calendar(firstweekday=6)   # Sunday-first
        self._day_rects = {}          # QDate -> QRectF (hit-test)
        self._prev_rect = QRectF()
        self._next_rect = QRectF()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(240, 220)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setStartDate(self, d):
        self._start = QDate(d)
        if self._end.isValid() and self._end < self._start:
            self._end = QDate()
        self._emit()
        self.update()

    def setEndDate(self, d):
        self._end = QDate(d)
        if self._start.isValid() and self._end < self._start:
            self._start, self._end = self._end, self._start
        self._emit()
        self.update()

    def setRange(self, start, end):
        self._start, self._end = QDate(start), QDate(end)
        if self._start.isValid():
            self._first = QDate(self._start.year(), self._start.month(), 1)
        self._emit()
        self.update()

    def setSelectableRange(self, minimum, maximum):
        self._min, self._max = QDate(minimum), QDate(maximum)
        self.update()

    def setMonthsVisible(self, n):
        self._months = max(1, int(n))
        self.updateGeometry()
        self.update()

    def startDate(self):
        return self._start

    def endDate(self):
        return self._end

    def showMonth(self, year, month):
        self._first = QDate(year, month, 1)
        self.update()

    def _emit(self):
        self.rangeChanged.emit(self._start, self._end)

    def _selectable(self, d):
        if self._min.isValid() and d < self._min:
            return False
        if self._max.isValid() and d > self._max:
            return False
        return True

    # ------------------------------------------------------------------ #
    ## Layout
    # ------------------------------------------------------------------ #
    def _panels(self):
        w, h = self.width(), self.height()
        pad, gap = 10.0, 18.0
        n = self._months
        stacked = w < n * 250 and n > 1
        cols = 1 if stacked else n
        rows = n if stacked else 1
        pw = (w - 2 * pad - (cols - 1) * gap) / cols
        ph = (h - 2 * pad - (rows - 1) * gap) / rows
        out = []
        for i in range(n):
            c, r = (0, i) if stacked else (i, 0)
            x = pad + c * (pw + gap)
            y = pad + r * (ph + gap)
            d = self._first.addMonths(i)
            out.append((d.year(), d.month(), QRectF(x, y, pw, ph)))
        return out

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def _f(self, size, bold=False):
        f = QFont(self.font())
        f.setPointSizeF(size)
        f.setBold(bold)
        return f

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        self._day_rects = {}
        panels = self._panels()
        for idx, (year, month, rect) in enumerate(panels):
            self._paint_month(p, year, month, rect,
                              first=(idx == 0), last=(idx == len(panels) - 1))
        p.end()

    def _paint_month(self, p, year, month, rect, first, last):
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        title_h = min(38.0, h * 0.16)
        wk_h = min(24.0, h * 0.10)
        base = 11.0
        # ---- title + nav arrows ----
        p.setFont(self._f(min(15.0, w * 0.05), bold=True))
        p.setPen(QPen(self._header))
        p.drawText(QRectF(x, y, w, title_h), Qt.AlignCenter,
                   "%s %d" % (_MONTHS[month], year))
        ar = title_h * 0.5
        if first:
            self._prev_rect = QRectF(x + 2, y + (title_h - ar) / 2, ar, ar)
            self._chevron(p, self._prev_rect, "left")
        if last:
            self._next_rect = QRectF(x + w - ar - 2, y + (title_h - ar) / 2, ar, ar)
            self._chevron(p, self._next_rect, "right")
        # ---- weekday header ----
        cell = min(w / 7.0, (h - title_h - wk_h) / 6.0)
        gx = x + (w - 7 * cell) / 2.0
        gy = y + title_h + wk_h
        p.setFont(self._f(min(10.0, cell * 0.30)))
        p.setPen(QPen(self._muted))
        for c in range(7):
            p.drawText(QRectF(gx + c * cell, y + title_h, cell, wk_h),
                       Qt.AlignCenter, _WEEKDAYS[c])
        # ---- day cells: band, then endpoints, then text ----
        weeks = self._cal.monthdayscalendar(year, month)
        dfont = self._f(min(11.0, cell * 0.34))
        today = QDate.currentDate()
        for wi, week in enumerate(weeks):
            for c, day in enumerate(week):
                if day == 0:
                    continue
                d = QDate(year, month, day)
                cr = QRectF(gx + c * cell, gy + wi * cell, cell, cell)
                self._day_rects[d] = cr
                self._paint_band(p, d, c, cr, cell)
        for wi, week in enumerate(weeks):
            for c, day in enumerate(week):
                if day == 0:
                    continue
                d = QDate(year, month, day)
                cr = self._day_rects[d]
                self._paint_day(p, d, cr, cell, dfont, today)

    def _in_range(self, d):
        return (self._start.isValid() and self._end.isValid()
                and self._start < d < self._end)

    def _is_end(self, d):
        return d == self._start or d == self._end

    def _paint_band(self, p, d, col, cr, cell):
        if not (self._in_range(d) or (self._is_end(d) and self._start.isValid()
                                      and self._end.isValid())):
            return
        band_h = cell * 0.78
        rr = QRectF(cr.x(), cr.center().y() - band_h / 2, cr.width(), band_h)
        round_l = (col == 0) or (d == self._start)
        round_r = (col == 6) or (d == self._end)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._band))
        p.drawPath(self._selective_round(rr, round_l, round_r, band_h / 2))

    @staticmethod
    def _selective_round(r, left, right, rad):
        rad = min(rad, r.height() / 2.0, r.width() / 2.0)
        path = QPainterPath()
        x0, y0, x1, y1 = r.left(), r.top(), r.right(), r.bottom()
        path.moveTo(x0 + (rad if left else 0), y0)
        path.lineTo(x1 - (rad if right else 0), y0)
        if right:
            path.arcTo(x1 - 2 * rad, y0, 2 * rad, 2 * rad, 90, -90)
            path.lineTo(x1, y1 - rad)
            path.arcTo(x1 - 2 * rad, y1 - 2 * rad, 2 * rad, 2 * rad, 0, -90)
        else:
            path.lineTo(x1, y1)
        path.lineTo(x0 + (rad if left else 0), y1)
        if left:
            path.arcTo(x0, y1 - 2 * rad, 2 * rad, 2 * rad, -90, -90)
            path.lineTo(x0, y0 + rad)
            path.arcTo(x0, y0, 2 * rad, 2 * rad, 180, -90)
        else:
            path.lineTo(x0, y0)
        path.closeSubpath()
        return path

    def _paint_day(self, p, d, cr, cell, dfont, today):
        p.setFont(dfont)
        endpoint = self._is_end(d) and self._start.isValid()
        selectable = self._selectable(d)
        if endpoint:
            dia = cell * 0.74
            circ = QRectF(cr.center().x() - dia / 2, cr.center().y() - dia / 2, dia, dia)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._accent))
            p.drawEllipse(circ)
            p.setPen(QPen(self._sel_text))
        elif d == today:
            p.setPen(QPen(self._today_color))
            f = QFont(dfont); f.setBold(True); p.setFont(f)
        elif not selectable:
            faded = QColor(self._muted); faded.setAlpha(120)
            p.setPen(QPen(faded))
        else:
            p.setPen(QPen(self._text))
        p.drawText(cr, Qt.AlignCenter, str(d.day()))

    def _chevron(self, p, rect, direction):
        pen = QPen(self._header, max(1.6, rect.width() * 0.12))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        cx, cy = rect.center().x(), rect.center().y()
        wx = rect.width() * 0.22
        wy = rect.height() * 0.26
        if direction == "left":
            p.drawLine(QPointF(cx + wx, cy - wy), QPointF(cx - wx, cy))
            p.drawLine(QPointF(cx - wx, cy), QPointF(cx + wx, cy + wy))
        else:
            p.drawLine(QPointF(cx - wx, cy - wy), QPointF(cx + wx, cy))
            p.drawLine(QPointF(cx + wx, cy), QPointF(cx - wx, cy + wy))

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return super().mousePressEvent(e)
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        if self._prev_rect.adjusted(-6, -6, 6, 6).contains(pos):
            self._first = self._first.addMonths(-1)
            self.update()
            return
        if self._next_rect.adjusted(-6, -6, 6, 6).contains(pos):
            self._first = self._first.addMonths(1)
            self.update()
            return
        for d, r in self._day_rects.items():
            if r.contains(pos):
                if self._selectable(d):
                    self._pick(d)
                return
        super().mousePressEvent(e)

    def _pick(self, d):
        # first click (or restart) sets start + clears end; a later click sets end
        if not self._start.isValid() or self._end.isValid():
            self._start, self._end = QDate(d), QDate()
        elif d < self._start:
            self._start = QDate(d)
        else:
            self._end = QDate(d)
        self._emit()
        self.update()

    def sizeHint(self):
        from qtpy.QtCore import QSize
        return QSize(280 * self._months, 300)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(int)
    def monthsVisible(self):
        return self._months

    @monthsVisible.setter
    def monthsVisible(self, n):
        self.setMonthsVisible(n)

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self.update()

    @Property(QColor)
    def rangeBandColor(self):
        return self._band

    @rangeBandColor.setter
    def rangeBandColor(self, c):
        self._band = QColor(c)
        self.update()

    @Property(QColor)
    def todayColor(self):
        return self._today_color

    @todayColor.setter
    def todayColor(self, c):
        self._today_color = QColor(c)
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c)
        self.update()

    @Property(QColor)
    def mutedColor(self):
        return self._muted

    @mutedColor.setter
    def mutedColor(self, c):
        self._muted = QColor(c)
        self.update()

    @Property(QColor)
    def headerColor(self):
        return self._header

    @headerColor.setter
    def headerColor(self, c):
        self._header = QColor(c)
        self.update()

    @Property(QColor)
    def selectedTextColor(self):
        return self._sel_text

    @selectedTextColor.setter
    def selectedTextColor(self, c):
        self._sel_text = QColor(c)
        self.update()
