########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomMediaTimeline - a horizontal multi-track clip / scrubber timeline.
##
## The bottom-of-a-video/animation-tool surface: a time RULER with labelled
## ticks (0:01 .. 0:09), a draggable PLAYHEAD, and one or more TRACK lanes.
## A track is either a lane of rounded CLIP blocks (move the body, trim from
## either edge) or a WAVEFORM lane (an audio waveform painted from sample
## values). Everything is painted with QPainter so it stays crisp at any size
## and every colour is a qproperty that tracks the theme.
##
## Drag on the ruler (or the playhead) to scrub -> positionChanged(seconds).
## Drag a clip body -> clipMoved(track, clip); drag a clip edge -> clipTrimmed.
## Build it declaratively: setDuration(), addTrack(), addClip()/setWaveform(),
## or setTimeline({...}).
########################################################################
import math

from qtpy.QtCore import Qt, Property, QRectF, QPointF, QSize, Signal, QTimer
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QFont, QPainterPath, QLinearGradient
from qtpy.QtWidgets import QWidget, QSizePolicy


class _Clip:
    __slots__ = ("start", "end", "color", "label")

    def __init__(self, start, end, color=None, label=""):
        self.start = float(start)
        self.end = float(end)
        self.color = QColor(color) if color else None
        self.label = label or ""


class _Track:
    __slots__ = ("name", "kind", "clips", "values", "color")

    def __init__(self, name="Track", kind="clips", color=None):
        self.name = name
        self.kind = kind          # "clips" | "wave"
        self.clips = []           # list[_Clip]
        self.values = []          # waveform samples (any range, auto-normalised)
        self.color = QColor(color) if color else None


class QCustomMediaTimeline(QWidget):

    WIDGET_ICON = "components/icons/video_settings.png"
    WIDGET_TOOLTIP = "A horizontal multi-track clip / scrubber timeline (ruler, playhead, clips, waveform)"
    WIDGET_MODULE = "Custom_Widgets.QCustomMediaTimeline"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomMediaTimeline' name='customMediaTimeline'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>620</width><height>150</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomMediaTimeline",
        "props": {"duration": {"type": "double", "default": 10.0},
                  "position": {"type": "double", "default": 1.0},
                  "bgColor": {"type": "color", "default": "#12141c"},
                  "rulerColor": {"type": "color", "default": "#8b90a6"},
                  "playheadColor": {"type": "color", "default": "#e7e9f3"},
                  "trackBgColor": {"type": "color", "default": "#1b1e2a"},
                  "clipColor": {"type": "color", "default": "#c17ce0"},
                  "waveColor": {"type": "color", "default": "#8b90a6"},
                  "textColor": {"type": "color", "default": "#e7e9f3"},
                  "cornerRadius": {"type": "int", "default": 10},
                  "playing": {"type": "bool", "default": False},
                  "loop": {"type": "bool", "default": True}},
        "signals": ["positionChanged", "clipMoved", "clipTrimmed", "clipClicked"],
        "tokens_used": ["accent", "background"],
    }
    # Every configurable property is exposed to Qt Designer.
    DESIGNER_CUSTOM_PROPS = [
        {"name": "duration", "kind": "double", "group": "Timeline"},
        {"name": "position", "kind": "double", "group": "Timeline"},
        {"name": "cornerRadius", "kind": "int", "group": "Timeline"},
        {"name": "playing", "kind": "bool", "group": "Timeline"},
        {"name": "loop", "kind": "bool", "group": "Timeline"},
        {"name": "bgColor", "kind": "color", "group": "Colours"},
        {"name": "rulerColor", "kind": "color", "group": "Colours"},
        {"name": "playheadColor", "kind": "color", "group": "Colours"},
        {"name": "trackBgColor", "kind": "color", "group": "Colours"},
        {"name": "clipColor", "kind": "color", "group": "Colours"},
        {"name": "waveColor", "kind": "color", "group": "Colours"},
        {"name": "textColor", "kind": "color", "group": "Colours"},
    ]

    positionChanged = Signal(float)
    clipMoved = Signal(int, int)
    clipTrimmed = Signal(int, int)
    clipClicked = Signal(int, int)
    playToggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomMediaTimeline")
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumHeight(96)

        self._duration = 10.0
        self._position = 1.0
        self._tracks = []

        self._bg = QColor("#12141c")
        self._ruler = QColor("#8b90a6")
        self._playhead = QColor("#e7e9f3")
        self._track_bg = QColor("#1b1e2a")
        self._clip = QColor("#c17ce0")
        self._wave = QColor("#8b90a6")
        self._text = QColor("#e7e9f3")
        self._radius = 10

        # layout metrics
        self._ruler_h = 26.0
        self._track_gap = 8.0
        self._pad = 14.0

        # interaction
        self._drag = None   # ("scrub",) | ("move", ti, ci, grabOffset) | ("trim", ti, ci, edge)
        self._hover_clip = None    # (track, clip) under the cursor

        # animation: a self-driven playhead so the widget animates on its own
        # (play()/pause()); clips also glow on hover.
        self._playing = False
        self._loop = True
        self._play_timer = QTimer(self)
        self._play_timer.setInterval(33)
        self._play_timer.timeout.connect(self._advance)

    # ------------------------------------------------------------------ #
    ## Playback (self-animating playhead)
    # ------------------------------------------------------------------ #
    def setPlaying(self, on):
        on = bool(on)
        if on == self._playing:
            return
        self._playing = on
        if on:
            self._play_timer.start()
        else:
            self._play_timer.stop()
        self.playToggled.emit(on)

    def play(self):
        self.setPlaying(True)

    def pause(self):
        self.setPlaying(False)

    def togglePlay(self):
        self.setPlaying(not self._playing)

    def isPlaying(self):
        return self._playing

    def _advance(self):
        step = self._play_timer.interval() / 1000.0
        nxt = self._position + step
        if nxt >= self._duration:
            if self._loop:
                nxt = 0.0
            else:
                nxt = self._duration
                self.setPlaying(False)
        self.setPosition(nxt)

    # ------------------------------------------------------------------ #
    ## Public data API
    # ------------------------------------------------------------------ #
    def setDuration(self, seconds):
        self._duration = max(0.1, float(seconds))
        self.update()

    def setPosition(self, seconds):
        s = max(0.0, min(self._duration, float(seconds)))
        if s != self._position:
            self._position = s
            self.positionChanged.emit(s)
            self.update()

    def positionSeconds(self):
        return self._position

    def addTrack(self, name="Track", kind="clips", color=None):
        t = _Track(name, kind, color)
        self._tracks.append(t)
        self.update()
        return len(self._tracks) - 1

    def addClip(self, track, start, end, color=None, label=""):
        if 0 <= track < len(self._tracks):
            self._tracks[track].clips.append(_Clip(start, end, color, label))
            self.update()

    def setWaveform(self, track, values):
        if 0 <= track < len(self._tracks):
            self._tracks[track].values = [float(v) for v in values]
            self.update()

    def clear(self):
        self._tracks = []
        self.update()

    def setTimeline(self, data):
        """data = {"duration":10, "position":1,
                    "tracks":[{"name","kind","color",
                               "clips":[{start,end,color,label}], "values":[...]}]}."""
        data = data or {}
        self.clear()
        if "duration" in data:
            self._duration = max(0.1, float(data["duration"]))
        for t in data.get("tracks", []):
            ti = self.addTrack(t.get("name", "Track"), t.get("kind", "clips"),
                               t.get("color"))
            for c in t.get("clips", []):
                self.addClip(ti, c.get("start", 0), c.get("end", 1),
                             c.get("color"), c.get("label", ""))
            if t.get("values"):
                self.setWaveform(ti, t["values"])
        if "position" in data:
            self._position = max(0.0, min(self._duration, float(data["position"])))
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _content_rect(self):
        return QRectF(self._pad, 0, max(1.0, self.width() - 2 * self._pad),
                      self.height())

    def _t2x(self, t):
        cr = self._content_rect()
        return cr.x() + (t / self._duration) * cr.width()

    def _x2t(self, x):
        cr = self._content_rect()
        return max(0.0, min(self._duration,
                            (x - cr.x()) / cr.width() * self._duration))

    def _tracks_top(self):
        return self._ruler_h + 6.0

    def _track_h(self):
        n = max(1, len(self._tracks))
        avail = self.height() - self._tracks_top() - self._pad
        return max(18.0, (avail - (n - 1) * self._track_gap) / n)

    def _track_rect(self, i):
        th = self._track_h()
        y = self._tracks_top() + i * (th + self._track_gap)
        cr = self._content_rect()
        return QRectF(cr.x(), y, cr.width(), th)

    def _clip_rect(self, ti, clip):
        tr = self._track_rect(ti)
        x0 = self._t2x(clip.start)
        x1 = self._t2x(clip.end)
        return QRectF(x0, tr.y(), max(6.0, x1 - x0), tr.height())

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), self._bg)
        self._paint_ruler(p)
        for i, t in enumerate(self._tracks):
            self._paint_track(p, i, t)
        self._paint_playhead(p)
        p.end()

    def _fmt_time(self, secs):
        m = int(secs) // 60
        s = int(secs) % 60
        return "%d:%02d" % (m, s)

    def _paint_ruler(self, p):
        cr = self._content_rect()
        f = QFont(self.font())
        f.setPointSizeF(8.0)
        p.setFont(f)
        # choose a tick step that yields ~1s where it fits, else spread out
        step = 1.0
        while (cr.width() / (self._duration / step)) < 42 and step < self._duration:
            step += 1.0
        p.setPen(QPen(QColor(self._ruler.red(), self._ruler.green(),
                             self._ruler.blue(), 120), 1.0))
        t = 0.0
        while t <= self._duration + 1e-6:
            x = self._t2x(t)
            p.setPen(QPen(QColor(self._ruler.red(), self._ruler.green(),
                                 self._ruler.blue(), 90), 1.0))
            p.drawLine(QPointF(x, self._ruler_h - 6), QPointF(x, self._ruler_h - 1))
            p.setPen(QPen(self._ruler))
            p.drawText(QRectF(x - 20, 2, 40, 14), Qt.AlignCenter, self._fmt_time(t))
            t += step

    def _paint_track(self, p, ti, track):
        tr = self._track_rect(ti)
        r = float(self._radius)
        # lane background
        p.setPen(Qt.NoPen)
        p.setBrush(self._track_bg)
        p.drawRoundedRect(tr, r, r)

        if track.kind == "wave":
            self._paint_waveform(p, tr, track)
        else:
            for ci, clip in enumerate(track.clips):
                self._paint_clip(p, ti, ci, clip)

    def _paint_clip(self, p, ti, ci, clip):
        rect = self._clip_rect(ti, clip)
        r = float(self._radius)
        col = clip.color or self._clip
        hovered = (self._hover_clip == (ti, ci))
        top = col.lighter(140 if hovered else 118)
        grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        grad.setColorAt(0.0, top)
        grad.setColorAt(1.0, col.lighter(112) if hovered else col)
        p.setPen(QPen(QColor(255, 255, 255, 150), 1.0) if hovered else Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawRoundedRect(rect, r, r)
        # trim handles
        p.setBrush(QColor(255, 255, 255, 150))
        hw = 3.0
        for hx in (rect.left() + 5, rect.right() - 5 - hw):
            p.drawRoundedRect(QRectF(hx, rect.center().y() - 7, hw, 14), 1.5, 1.5)
        # label
        if clip.label and rect.width() > 46:
            f = QFont(self.font())
            f.setPointSizeF(8.0)
            f.setBold(True)
            p.setFont(f)
            p.setPen(QPen(QColor("#ffffff")))
            p.drawText(rect.adjusted(12, 0, -12, 0),
                       Qt.AlignVCenter | Qt.AlignLeft, clip.label)

    def _paint_waveform(self, p, tr, track):
        vals = track.values
        col = track.color or self._wave
        inner = tr.adjusted(10, 6, -10, -6)
        mid = inner.center().y()
        if not vals:
            p.setPen(QPen(QColor(col.red(), col.green(), col.blue(), 120), 1.0))
            p.drawLine(QPointF(inner.left(), mid), QPointF(inner.right(), mid))
            return
        n = len(vals)
        peak = max(1e-6, max(abs(v) for v in vals))
        bw = inner.width() / n
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(col.red(), col.green(), col.blue(), 200))
        for i, v in enumerate(vals):
            h = (abs(v) / peak) * (inner.height() / 2)
            x = inner.left() + i * bw
            bar = QRectF(x, mid - h, max(1.0, bw * 0.6), h * 2)
            p.drawRoundedRect(bar, bar.width() / 2, bar.width() / 2)

    def _paint_playhead(self, p):
        x = self._t2x(self._position)
        top = 2.0
        p.setPen(QPen(self._playhead, 1.6))
        p.drawLine(QPointF(x, top + 10), QPointF(x, self.height() - self._pad + 4))
        # handle triangle
        p.setPen(Qt.NoPen)
        p.setBrush(self._playhead)
        path = QPainterPath()
        path.moveTo(x - 5, top)
        path.lineTo(x + 5, top)
        path.lineTo(x, top + 8)
        path.closeSubpath()
        p.drawPath(path)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _pos(self, e):
        return QPointF(e.position()) if hasattr(e, "position") else QPointF(e.pos())

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return super().mousePressEvent(e)
        pt = self._pos(e)
        # ruler / above tracks -> scrub
        if pt.y() <= self._tracks_top():
            self._drag = ("scrub",)
            self.setPosition(self._x2t(pt.x()))
            return
        # clip hit?
        for ti, track in enumerate(self._tracks):
            if track.kind != "clips":
                continue
            for ci, clip in enumerate(track.clips):
                rect = self._clip_rect(ti, clip)
                if not rect.contains(pt):
                    continue
                edge = 9.0
                if pt.x() - rect.left() <= edge:
                    self._drag = ("trim", ti, ci, "start")
                elif rect.right() - pt.x() <= edge:
                    self._drag = ("trim", ti, ci, "end")
                else:
                    self._drag = ("move", ti, ci, self._x2t(pt.x()) - clip.start)
                self.clipClicked.emit(ti, ci)
                return
        # empty track area -> scrub too
        self._drag = ("scrub",)
        self.setPosition(self._x2t(pt.x()))

    def mouseMoveEvent(self, e):
        pt = self._pos(e)
        if self._drag is None:
            # cursor feedback + track the hovered clip (for its glow)
            cur = Qt.ArrowCursor
            hover = None
            if pt.y() <= self._tracks_top():
                cur = Qt.SizeHorCursor
            else:
                for ti, track in enumerate(self._tracks):
                    if track.kind != "clips":
                        continue
                    for ci, clip in enumerate(track.clips):
                        rect = self._clip_rect(ti, clip)
                        if rect.contains(pt):
                            hover = (ti, ci)
                            if (pt.x() - rect.left() <= 9.0) or (rect.right() - pt.x() <= 9.0):
                                cur = Qt.SizeHorCursor
                            else:
                                cur = Qt.OpenHandCursor
            if hover != self._hover_clip:
                self._hover_clip = hover
                self.update()
            self.setCursor(cur)
            return super().mouseMoveEvent(e)

        kind = self._drag[0]
        if kind == "scrub":
            self.setPosition(self._x2t(pt.x()))
            return
        t = self._x2t(pt.x())
        ti = self._drag[1]
        ci = self._drag[2]
        clip = self._tracks[ti].clips[ci]
        if kind == "trim":
            edge = self._drag[3]
            if edge == "start":
                clip.start = max(0.0, min(clip.end - 0.2, t))
            else:
                clip.end = min(self._duration, max(clip.start + 0.2, t))
            self.clipTrimmed.emit(ti, ci)
            self.update()
        elif kind == "move":
            grab = self._drag[3]
            length = clip.end - clip.start
            new_start = max(0.0, min(self._duration - length, t - grab))
            clip.start = new_start
            clip.end = new_start + length
            self.clipMoved.emit(ti, ci)
            self.update()

    def mouseReleaseEvent(self, e):
        self._drag = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(e)

    def leaveEvent(self, e):
        if self._hover_clip is not None:
            self._hover_clip = None
            self.update()
        super().leaveEvent(e)

    def sizeHint(self):
        return QSize(620, 150)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, v):
        self.setDuration(v)

    @Property(float)
    def position(self):  # noqa: F811 - Qt property alongside position() method
        return self._position

    @position.setter
    def position(self, v):
        self.setPosition(v)

    @Property(bool)
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, v):
        self.setPlaying(v)

    @Property(bool)
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, v):
        self._loop = bool(v)

    @Property(QColor)
    def bgColor(self):
        return self._bg

    @bgColor.setter
    def bgColor(self, c):
        self._bg = QColor(c)
        self.update()

    @Property(QColor)
    def rulerColor(self):
        return self._ruler

    @rulerColor.setter
    def rulerColor(self, c):
        self._ruler = QColor(c)
        self.update()

    @Property(QColor)
    def playheadColor(self):
        return self._playhead

    @playheadColor.setter
    def playheadColor(self, c):
        self._playhead = QColor(c)
        self.update()

    @Property(QColor)
    def trackBgColor(self):
        return self._track_bg

    @trackBgColor.setter
    def trackBgColor(self, c):
        self._track_bg = QColor(c)
        self.update()

    @Property(QColor)
    def clipColor(self):
        return self._clip

    @clipColor.setter
    def clipColor(self, c):
        self._clip = QColor(c)
        self.update()

    @Property(QColor)
    def waveColor(self):
        return self._wave

    @waveColor.setter
    def waveColor(self, c):
        self._wave = QColor(c)
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._text

    @textColor.setter
    def textColor(self, c):
        self._text = QColor(c)
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()
