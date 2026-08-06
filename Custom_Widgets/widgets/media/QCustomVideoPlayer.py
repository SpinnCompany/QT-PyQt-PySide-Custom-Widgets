########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomVideoPlayer - a poster-framed media/video player card.
##
## A rounded poster image with a big centred play button and a bottom control
## bar (play / pause, elapsed / total time, a seek track). Feed it a poster
## with setPoster(pm) and a length with `duration` ("mm:ss"); pressing play
## advances a simulated playhead (a QTimer) so it demos without any media
## backend, and clicking the track seeks. It emits playToggled(bool) and
## seeked(float 0..1). Everything is painted (crisp at any size, no assets) and
## every colour is a qproperty so it tracks the theme.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF, QTimer
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPolygonF, QPixmap, QFont, QLinearGradient, QPainterPath
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomVideoPlayer(QWidget):

    playToggled = Signal(bool)
    seeked = Signal(float)

    WIDGET_ICON = "components/icons/play_circle.png"
    WIDGET_TOOLTIP = "A poster-framed media / video player card"
    WIDGET_MODULE = "Custom_Widgets.QCustomVideoPlayer"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomVideoPlayer' name='customVideoPlayer'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>210</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomVideoPlayer",
        "props": {
            "duration": {"type": "string", "default": "02:45"},
            "progress": {"type": "float", "default": 0.0},
            "playing": {"type": "bool", "default": False},
            "radius": {"type": "int", "default": 18},
            "accentColor": {"type": "color", "default": "#1b74e4"},
            "posterColor": {"type": "color", "default": "#222838"},
            "barColor": {"type": "color", "default": "#e6ffffff"},
            "trackColor": {"type": "color", "default": "#4dffffff"},
            "textColor": {"type": "color", "default": "#ffffff"},
        },
        "signals": ["playToggled", "seeked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomVideoPlayer")
        self._poster = QPixmap()
        self._poster_color = QColor("#222838")
        self._accent = QColor("#1b74e4")
        self._bar = QColor(255, 255, 255, 230)
        self._track = QColor(255, 255, 255, 77)
        self._text = QColor("#ffffff")
        self._radius = 18
        self._duration = "02:45"
        self._total_ms = self._parse(self._duration)
        self._progress = 0.0
        self._playing = False
        self._bar_h = 40

        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._tick)

        self.setMinimumSize(220, 140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setPoster(self, pm):
        self._poster = pm if isinstance(pm, QPixmap) else QPixmap(str(pm))
        self.update()

    def setPlaying(self, v):
        v = bool(v)
        if v == self._playing:
            return
        self._playing = v
        if v:
            self._timer.start()
        else:
            self._timer.stop()
        self.playToggled.emit(v)
        self.update()

    def toggle(self):
        self.setPlaying(not self._playing)

    @staticmethod
    def _parse(text):
        try:
            parts = [int(x) for x in str(text).split(":")]
        except ValueError:
            return 0
        secs = 0
        for x in parts:
            secs = secs * 60 + x
        return secs * 1000

    @staticmethod
    def _fmt(ms):
        s = max(0, int(ms // 1000))
        return "%d:%02d" % (s // 60, s % 60)

    def _tick(self):
        if self._total_ms <= 0:
            return
        self._progress = min(1.0, self._progress + self._timer.interval() / self._total_ms)
        if self._progress >= 1.0:
            self.setPlaying(False)
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry helpers
    # ------------------------------------------------------------------ #
    def _barRect(self):
        return QRectF(0, self.height() - self._bar_h, self.width(), self._bar_h)

    def _trackRect(self):
        br = self._barRect()
        x0 = br.left() + 84
        x1 = br.right() - 16
        return QRectF(x0, br.center().y() - 2, max(1.0, x1 - x0), 4)

    def _centerBtnRect(self):
        d = min(self.width(), self.height()) * 0.26
        d = max(44, min(80, d))
        return QRectF((self.width() - d) / 2.0, (self.height() - self._bar_h - d) / 2.0, d, d)

    # ------------------------------------------------------------------ #
    ## Paint
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        full = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        path = QPainterPath()
        path.addRoundedRect(full, self._radius, self._radius)
        p.setClipPath(path)

        # poster (aspect-fill) or flat colour
        if not self._poster.isNull():
            scaled = self._poster.size().scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
            x = (self.width() - scaled.width()) / 2.0
            y = (self.height() - scaled.height()) / 2.0
            p.drawPixmap(QRectF(x, y, scaled.width(), scaled.height()).toRect(), self._poster)
        else:
            p.fillRect(full, self._poster_color)
        # subtle darken for control legibility
        p.fillRect(full, QColor(0, 0, 0, 40))

        # centre play/pause button
        cb = self._centerBtnRect()
        p.setPen(Qt.NoPen)
        halo = QColor(self._accent)
        p.setBrush(QBrush(halo))
        p.drawEllipse(cb)
        p.setBrush(QBrush(self._text))
        c = cb.center()
        d = cb.width()
        if self._playing:
            bw = d * 0.11
            gap = d * 0.10
            bh = d * 0.32
            p.drawRoundedRect(QRectF(c.x() - gap - bw, c.y() - bh / 2, bw, bh), bw / 3, bw / 3)
            p.drawRoundedRect(QRectF(c.x() + gap, c.y() - bh / 2, bw, bh), bw / 3, bw / 3)
        else:
            s = d * 0.28
            p.drawPolygon(QPolygonF([QPointF(c.x() - s * 0.45, c.y() - s * 0.62),
                                     QPointF(c.x() - s * 0.45, c.y() + s * 0.62),
                                     QPointF(c.x() + s * 0.68, c.y())]))

        # bottom control bar gradient
        br = self._barRect()
        g = QLinearGradient(0, br.top(), 0, br.bottom())
        g.setColorAt(0.0, QColor(0, 0, 0, 0))
        g.setColorAt(1.0, QColor(0, 0, 0, 150))
        p.fillRect(br, QBrush(g))

        # small play glyph on the bar
        p.setBrush(QBrush(self._bar))
        gx, gy = br.left() + 20, br.center().y()
        if self._playing:
            p.drawRoundedRect(QRectF(gx - 5, gy - 6, 3.4, 12), 1.4, 1.4)
            p.drawRoundedRect(QRectF(gx + 1.6, gy - 6, 3.4, 12), 1.4, 1.4)
        else:
            p.drawPolygon(QPolygonF([QPointF(gx - 4, gy - 6), QPointF(gx - 4, gy + 6), QPointF(gx + 6, gy)]))

        # time text
        f = QFont(self.font())
        f.setPointSizeF(9.5)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QPen(self._text))
        elapsed = self._fmt(self._progress * self._total_ms)
        total = self._fmt(self._total_ms)
        p.drawText(QRectF(br.left() + 38, br.top(), 60, br.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, elapsed)
        p.drawText(QRectF(br.right() - 54, br.top(), 42, br.height()),
                   Qt.AlignVCenter | Qt.AlignRight, total)

        # seek track
        tr = self._trackRect()
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._track))
        p.drawRoundedRect(tr, tr.height() / 2, tr.height() / 2)
        fill = QRectF(tr.left(), tr.top(), tr.width() * self._progress, tr.height())
        p.setBrush(QBrush(self._accent))
        p.drawRoundedRect(fill, tr.height() / 2, tr.height() / 2)
        # playhead knob
        kx = tr.left() + tr.width() * self._progress
        p.setBrush(QBrush(self._text))
        p.drawEllipse(QPointF(kx, tr.center().y()), 5, 5)
        p.end()

    def mousePressEvent(self, e):
        pos = e.position()
        tr = self._trackRect()
        hit = QRectF(tr.left() - 4, tr.top() - 10, tr.width() + 8, tr.height() + 20)
        if hit.contains(pos):
            frac = max(0.0, min(1.0, (pos.x() - tr.left()) / tr.width()))
            self._progress = frac
            self.seeked.emit(frac)
            self.update()
        else:
            self.toggle()
        e.accept()

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, v):
        self._duration = str(v)
        self._total_ms = self._parse(self._duration)
        self.update()

    @Property(float)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, v):
        self._progress = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(bool)
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, v):
        self.setPlaying(v)

    @Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self.update()

    @Property(QColor)
    def posterColor(self):
        return self._poster_color

    @posterColor.setter
    def posterColor(self, c):
        self._poster_color = QColor(c)
        self.update()

    @Property(QColor)
    def barColor(self):
        return self._bar

    @barColor.setter
    def barColor(self, c):
        self._bar = QColor(c)
        self.update()

    @Property(QColor)
    def trackColor(self):
        return self._track

    @trackColor.setter
    def trackColor(self, c):
        self._track = QColor(c)
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c)
        self.update()
