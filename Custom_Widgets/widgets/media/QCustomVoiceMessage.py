########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomVoiceMessage - a voice / audio message with a scrubber waveform.
##
## The audio row seen inside a chat bubble: a circular play / pause button, a
## painted bar waveform (heights from `valuesCsv`), and a duration label. The
## played portion of the waveform fills with the accent colour up to
## `progress` (0..1), the rest stays muted, so it doubles as a scrubber. Bars
## are painted (crisp at any size, no assets); every colour is a qproperty so
## it tracks the theme. Clicking the button toggles playing and emits
## `playToggled(bool)`; clicking the waveform emits `seeked(float)`.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPolygonF
from qtpy.QtCore import QPointF
from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy


class _Waveform(QWidget):
    seeked = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._vals = []
        self._progress = 0.0
        self._played = QColor("#1b74e4")
        self._unplayed = QColor("#c7d0dc")
        self._bar_w = 3.0
        self._gap = 2.0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(60, 26)
        self.setCursor(Qt.PointingHandCursor)

    def setValues(self, vals):
        self._vals = [max(0.04, float(v)) for v in (vals or [])]
        self.update()

    def setProgress(self, p):
        self._progress = max(0.0, min(1.0, float(p)))
        self.update()

    def setColors(self, played, unplayed):
        self._played = QColor(played)
        self._unplayed = QColor(unplayed)
        self.update()

    def paintEvent(self, e):
        if not self._vals:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        n = len(self._vals)
        slot = self._bar_w + self._gap
        total = n * slot - self._gap
        # scale to fit available width if too wide
        if total > w:
            slot = w / n
            bw = max(1.5, slot - self._gap)
        else:
            bw = self._bar_w
        x = 0.0
        hi = max(self._vals) or 1.0
        cut = self._progress * w
        p.setPen(Qt.NoPen)
        for v in self._vals:
            bh = max(3.0, (v / hi) * (h - 4))
            y = (h - bh) / 2.0
            color = self._played if x <= cut else self._unplayed
            p.setBrush(QBrush(color))
            p.drawRoundedRect(QRectF(x, y, bw, bh), bw / 2.0, bw / 2.0)
            x += slot
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.width() > 0:
            self.seeked.emit(max(0.0, min(1.0, e.position().x() / self.width())))
        super().mousePressEvent(e)


class _PlayButton(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._playing = False
        self._bg = QColor("#1b74e4")
        self._fg = QColor("#ffffff")
        self._d = 34
        self.setFixedSize(self._d, self._d)
        self.setCursor(Qt.PointingHandCursor)

    def setPlaying(self, v):
        self._playing = bool(v)
        self.update()

    def setDiameter(self, d):
        self._d = max(20, int(d))
        self.setFixedSize(self._d, self._d)
        self.update()

    def setColors(self, bg, fg):
        self._bg = QColor(bg)
        self._fg = QColor(fg)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawEllipse(self.rect())
        p.setBrush(QBrush(self._fg))
        c = self._d / 2.0
        if self._playing:
            bw = self._d * 0.11
            gap = self._d * 0.10
            bh = self._d * 0.34
            p.drawRoundedRect(QRectF(c - gap - bw, c - bh / 2, bw, bh), bw / 3, bw / 3)
            p.drawRoundedRect(QRectF(c + gap, c - bh / 2, bw, bh), bw / 3, bw / 3)
        else:
            s = self._d * 0.30
            tri = QPolygonF([QPointF(c - s * 0.5, c - s * 0.62),
                             QPointF(c - s * 0.5, c + s * 0.62),
                             QPointF(c + s * 0.72, c)])
            p.drawPolygon(tri)
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)


class QCustomVoiceMessage(QWidget):

    playToggled = Signal(bool)
    seeked = Signal(float)

    WIDGET_ICON = "components/icons/voice_message.png"
    WIDGET_TOOLTIP = "A voice / audio message with a scrubber waveform"
    WIDGET_MODULE = "Custom_Widgets.QCustomVoiceMessage"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomVoiceMessage' name='customVoiceMessage'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>260</width><height>44</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomVoiceMessage",
        "props": {
            "valuesCsv": {"type": "string",
                          "default": "3,6,10,14,9,16,20,12,7,18,22,14,8,12,6,10,16,9,5,12,18,10,6,14,8"},
            "duration": {"type": "string", "default": "01:30"},
            "progress": {"type": "float", "default": 0.0},
            "playing": {"type": "bool", "default": False},
            "playedColor": {"type": "color", "default": "#1b74e4"},
            "unplayedColor": {"type": "color", "default": "#c7d0dc"},
            "buttonColor": {"type": "color", "default": "#1b74e4"},
            "buttonIconColor": {"type": "color", "default": "#ffffff"},
            "durationColor": {"type": "color", "default": "#5a6478"},
            "buttonDiameter": {"type": "int", "default": 34},
        },
        "signals": ["playToggled", "seeked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomVoiceMessage")
        self._dur_color = QColor("#5a6478")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        self._btn = _PlayButton(self)
        self._wave = _Waveform(self)
        self._dur = QLabel("01:30")
        self._dur.setObjectName("voiceDuration")
        self._dur.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        lay.addWidget(self._btn, 0)
        lay.addWidget(self._wave, 1)
        lay.addWidget(self._dur, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._wave.setValues([float(x) for x in
                              "3,6,10,14,9,16,20,12,7,18,22,14,8,12,6,10,16,9,5,12,18,10,6,14,8".split(",")])
        self._btn.clicked.connect(self._toggle)
        self._wave.seeked.connect(self.seeked)
        self._wave.seeked.connect(self._wave.setProgress)
        self._restyle()

    def _toggle(self):
        self._btn.setPlaying(not self._btn._playing)
        self.playToggled.emit(self._btn._playing)

    def _restyle(self):
        self._dur.setStyleSheet(
            "color:%s; background:transparent; font-size:12px; font-weight:600;"
            % self._dur_color.name())

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def valuesCsv(self):
        return ",".join("%g" % v for v in self._wave._vals)

    @valuesCsv.setter
    def valuesCsv(self, text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if not tok:
                continue
            try:
                out.append(float(tok))
            except ValueError:
                pass
        self._wave.setValues(out)

    @Property(str)
    def duration(self):
        return self._dur.text()

    @duration.setter
    def duration(self, v):
        self._dur.setText(str(v))

    @Property(float)
    def progress(self):
        return self._wave._progress

    @progress.setter
    def progress(self, v):
        self._wave.setProgress(v)

    @Property(bool)
    def playing(self):
        return self._btn._playing

    @playing.setter
    def playing(self, v):
        self._btn.setPlaying(v)

    @Property(QColor)
    def playedColor(self):
        return self._wave._played

    @playedColor.setter
    def playedColor(self, c):
        self._wave.setColors(QColor(c), self._wave._unplayed)

    @Property(QColor)
    def unplayedColor(self):
        return self._wave._unplayed

    @unplayedColor.setter
    def unplayedColor(self, c):
        self._wave.setColors(self._wave._played, QColor(c))

    @Property(QColor)
    def buttonColor(self):
        return self._btn._bg

    @buttonColor.setter
    def buttonColor(self, c):
        self._btn.setColors(QColor(c), self._btn._fg)

    @Property(QColor)
    def buttonIconColor(self):
        return self._btn._fg

    @buttonIconColor.setter
    def buttonIconColor(self, c):
        self._btn.setColors(self._btn._bg, QColor(c))

    @Property(QColor)
    def durationColor(self):
        return self._dur_color

    @durationColor.setter
    def durationColor(self, c):
        self._dur_color = QColor(c)
        self._restyle()

    @Property(int)
    def buttonDiameter(self):
        return self._btn._d

    @buttonDiameter.setter
    def buttonDiameter(self, v):
        self._btn.setDiameter(v)
