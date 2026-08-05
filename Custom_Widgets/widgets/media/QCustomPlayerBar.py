########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomPlayerBar - a NOW-PLAYING transport bar.
##
## The signature music-app footer: a rounded bar with, left-to-right, the
## current track's COVER + TITLE/ARTIST, a transport cluster (PREV, a big
## circular PLAY/PAUSE, NEXT), an elapsed/total SEEK slider you can click and
## drag, and a right cluster of FAVOURITE, SHUFFLE, REPEAT and VOLUME toggles.
## Every glyph is PAINTED as a vector (no font/unicode icons) so it recolours
## on a theme switch and stays crisp at any DPI. Seek + toggles are live and
## emit Qt signals — wire them to a real QMediaPlayer.
##
## Signals: playToggled(bool), nextClicked(), prevClicked(), seeked(float 0..1),
## favoriteToggled(bool), shuffleToggled(bool), repeatToggled(bool),
## volumeClicked(). Configure via `title`, `artist`, `coverPath`, `position`,
## `elapsedText`, `totalText`, `playing`, `favorite`, `shuffle`, `repeat`.
########################################################################
import os

from qtpy.QtCore import Qt, Property, QRectF, QRect, QSize, QPointF, Signal
from qtpy.QtGui import (QColor, QPainter, QBrush, QPen, QFont, QFontMetrics,
                        QPixmap, QPainterPath, QPolygonF)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomPlayerBar(QWidget):

    WIDGET_ICON = "components/icons/play_circle.png"
    WIDGET_TOOLTIP = "A now-playing transport bar (cover, transport, seek, volume)"
    WIDGET_MODULE = "Custom_Widgets.QCustomPlayerBar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomPlayerBar' name='customPlayerBar'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>900</width><height>92</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomPlayerBar",
        "props": {"title": {"type": "string", "default": "Echoes of Midnight"},
                  "artist": {"type": "string", "default": "Jon Hickman"},
                  "coverPath": {"type": "string", "default": ""},
                  "position": {"type": "float", "default": 0.22},
                  "elapsedText": {"type": "string", "default": "0:53"},
                  "totalText": {"type": "string", "default": "3:58"},
                  "playing": {"type": "bool", "default": False},
                  "favorite": {"type": "bool", "default": False},
                  "shuffle": {"type": "bool", "default": False},
                  "repeat": {"type": "bool", "default": False},
                  "barColor": {"type": "color", "default": "#171923"},
                  "accentColor": {"type": "color", "default": "#26c99e"},
                  "trackColor": {"type": "color", "default": "#33ffffff"},
                  "textColor": {"type": "color", "default": "#ffffff"},
                  "subTextColor": {"type": "color", "default": "#8b90a3"},
                  "iconColor": {"type": "color", "default": "#c7ccdb"},
                  "playBtnColor": {"type": "color", "default": "#e9ebf2"},
                  "cornerRadius": {"type": "int", "default": 20},
                  "compactMode": {"type": "bool", "default": False}},
        "signals": ["playToggled", "nextClicked", "prevClicked", "seeked",
                    "favoriteToggled", "shuffleToggled", "repeatToggled",
                    "volumeClicked"],
        "tokens_used": ["accent", "surface", "on-surface"],
    }

    playToggled = Signal(bool)
    nextClicked = Signal()
    prevClicked = Signal()
    seeked = Signal(float)
    favoriteToggled = Signal(bool)
    shuffleToggled = Signal(bool)
    repeatToggled = Signal(bool)
    volumeClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomPlayerBar")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(76)
        self.setMouseTracking(True)
        self.setCursor(Qt.ArrowCursor)

        self._title = "Echoes of Midnight"
        self._artist = "Jon Hickman"
        self._cover_path = ""
        self._pos = 0.22
        self._elapsed = "0:53"
        self._total = "3:58"
        self._playing = False
        self._favorite = False
        self._shuffle = False
        self._repeat = False

        self._bar = QColor("#171923")
        self._accent = QColor("#26c99e")
        self._track = QColor("#33ffffff")
        self._text = QColor("#ffffff")
        self._subtext = QColor("#8b90a3")
        self._icon = QColor("#c7ccdb")
        self._playbtn = QColor("#e9ebf2")
        self._radius = 20

        self._compact = False     # opt-in stacked card layout for narrow panels

        self._cover_pm = None     # directly-loaded cover pixmap (e.g. from a URL)
        self._pix_cache = {}
        self._hit = {}        # name -> QRectF
        self._seek_rect = QRectF()
        self._seeking = False
        self._hover = None

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setTrack(self, title=None, artist=None, coverPath=None,
                 elapsed=None, total=None, position=None):
        if title is not None:
            self._title = str(title)
        if artist is not None:
            self._artist = str(artist)
        if coverPath is not None:
            self.setCoverSource(coverPath)
        if elapsed is not None:
            self._elapsed = str(elapsed)
        if total is not None:
            self._total = str(total)
        if position is not None:
            self._pos = max(0.0, min(1.0, float(position)))
        self.update()

    def setPlaying(self, on):
        self._playing = bool(on)
        self.update()

    def setCoverSource(self, source):
        """Set the track cover from a local PATH or an http(s) URL (URL is
        downloaded + disk-cached async via Custom_Widgets.ImageLoader)."""
        source = str(source or "")
        self._cover_path = source
        self._pix_cache.clear()
        if source.lower().startswith(("http://", "https://")):
            self._cover_pm = None
            from Custom_Widgets.ImageLoader import load_image
            load_image(source, self._onCoverLoaded)
        else:
            self._cover_pm = None
        self.update()

    def _onCoverLoaded(self, pm):
        self._cover_pm = pm if (pm is not None and not pm.isNull()) else None
        self._pix_cache.clear()
        self.update()

    # ------------------------------------------------------------------ #
    ## Layout
    # ------------------------------------------------------------------ #
    def _layout(self):
        w, h = self.width(), self.height()
        pad = 16.0
        cover = h - pad * 2 + 6
        cover = min(cover, 68.0)
        cover_rect = QRectF(pad, (h - cover) / 2.0, cover, cover)
        left_text_x = cover_rect.right() + 12
        left_block_right = left_text_x + 184

        # right cluster: heart, shuffle, repeat, volume
        ibox = 30.0
        gap = 8.0
        n_right = 4
        right_w = n_right * ibox + (n_right - 1) * gap
        rx = w - pad - right_w
        cy = h / 2.0
        right = {}
        names = ["favorite", "shuffle", "repeat", "volume"]
        for i, nm in enumerate(names):
            x = rx + i * (ibox + gap)
            right[nm] = QRectF(x, cy - ibox / 2.0, ibox, ibox)

        # transport cluster (prev, play, next) — sits after the left block
        play_d = min(46.0, h - 20)
        prev_d = 26.0
        tgap = 16.0
        tw = prev_d + tgap + play_d + tgap + prev_d
        tx = max(left_block_right + 20, w * 0.30)
        prev_rect = QRectF(tx, cy - prev_d / 2.0, prev_d, prev_d)
        play_rect = QRectF(prev_rect.right() + tgap, cy - play_d / 2.0, play_d, play_d)
        next_rect = QRectF(play_rect.right() + tgap, cy - prev_d / 2.0, prev_d, prev_d)

        # seek zone between transport and right cluster
        seek_left = next_rect.right() + 26
        seek_right = rx - 26
        elapsed_w = 40.0
        track_x0 = seek_left + elapsed_w + 8
        track_x1 = seek_right - elapsed_w - 8
        track = QRectF(track_x0, cy - 3, max(20.0, track_x1 - track_x0), 6)

        return dict(cover=cover_rect, left_text_x=left_text_x,
                    left_block_right=left_block_right,
                    prev=prev_rect, play=play_rect, next=next_rect,
                    right=right, track=track,
                    elapsed_rect=QRectF(seek_left, cy - 10, elapsed_w, 20),
                    total_rect=QRectF(seek_right - elapsed_w, cy - 10, elapsed_w, 20))

    def _layout_compact(self):
        """Stacked card layout for narrow panels (compactMode=True):
        cover + title/artist row, seek row, centred transport row."""
        w, h = self.width(), self.height()
        pad = 14.0
        off = QRectF(-1000, -1000, 0, 0)     # parked (undrawn) hit zones

        cover = 44.0
        cover_rect = QRectF(pad, pad, cover, cover)
        left_text_x = cover_rect.right() + 10
        left_block_right = w - pad
        text_cy = cover_rect.center().y()

        # seek row between cover row and transport row
        seek_cy = cover_rect.bottom() + (h - pad - 40 - cover_rect.bottom()) / 2.0
        elapsed_w = 34.0
        track = QRectF(pad + elapsed_w + 8, seek_cy - 3,
                       max(20.0, w - 2 * pad - 2 * (elapsed_w + 8)), 6)

        # transport row: repeat · prev · play · next · volume (centred)
        play_d = min(44.0, h * 0.30)
        small = 24.0
        ibox = 26.0
        gaps = (16.0, 12.0, 12.0, 16.0)
        total_w = ibox + gaps[0] + small + gaps[1] + play_d + gaps[2] + small + gaps[3] + ibox
        x = (w - total_w) / 2.0
        t_cy = h - pad - play_d / 2.0
        repeat_rect = QRectF(x, t_cy - ibox / 2.0, ibox, ibox); x += ibox + gaps[0]
        prev_rect = QRectF(x, t_cy - small / 2.0, small, small); x += small + gaps[1]
        play_rect = QRectF(x, t_cy - play_d / 2.0, play_d, play_d); x += play_d + gaps[2]
        next_rect = QRectF(x, t_cy - small / 2.0, small, small); x += small + gaps[3]
        volume_rect = QRectF(x, t_cy - ibox / 2.0, ibox, ibox)

        return dict(cover=cover_rect, left_text_x=left_text_x,
                    left_block_right=left_block_right, text_cy=text_cy,
                    prev=prev_rect, play=play_rect, next=next_rect,
                    right=dict(favorite=off, shuffle=off,
                               repeat=repeat_rect, volume=volume_rect),
                    track=track,
                    elapsed_rect=QRectF(pad, seek_cy - 10, elapsed_w, 20),
                    total_rect=QRectF(w - pad - elapsed_w, seek_cy - 10, elapsed_w, 20))

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        w, h = self.width(), self.height()
        L = self._layout_compact() if self._compact else self._layout()
        self._hit = {}

        # bar background
        p.setPen(Qt.NoPen)
        p.setBrush(self._bar)
        p.drawRoundedRect(QRectF(0, 0, w, h), self._radius, self._radius)

        # --- cover ---
        cr = L["cover"]
        path = QPainterPath()
        path.addRoundedRect(cr, 12, 12)
        p.save()
        p.setClipPath(path)
        pm = self._cover_pixmap(cr.width(), cr.height())
        if pm is not None:
            p.drawPixmap(cr, pm, QRectF(0, 0, pm.width(), pm.height()))
        else:
            p.fillRect(cr, self._accent.darker(140))
        p.restore()

        # --- title / artist ---
        tx = L["left_text_x"]
        tw = L["left_block_right"] - tx
        tf = QFont(self.font())
        tf.setBold(True)
        tf.setPointSizeF(max(9.5, min(h * 0.15, 12.5)))
        af = QFont(self.font())
        af.setPointSizeF(max(8.0, min(h * 0.12, 10.5)))
        tfm, afm = QFontMetrics(tf), QFontMetrics(af)
        gap = 3.0
        block = tfm.height() + gap + afm.height()
        ty = L.get("text_cy", h / 2.0) - block / 2.0
        p.setFont(tf)
        p.setPen(self._text)
        p.drawText(QRectF(tx, ty, tw, tfm.height()), Qt.AlignLeft | Qt.AlignVCenter,
                   tfm.elidedText(self._title, Qt.ElideRight, int(tw)))
        p.setFont(af)
        p.setPen(self._subtext)
        p.drawText(QRectF(tx, ty + tfm.height() + gap, tw, afm.height()),
                   Qt.AlignLeft | Qt.AlignVCenter,
                   afm.elidedText(self._artist, Qt.ElideRight, int(tw)))

        # --- transport ---
        self._draw_prev(p, L["prev"]); self._hit["prev"] = L["prev"]
        self._draw_play_button(p, L["play"]); self._hit["play"] = L["play"]
        self._draw_next(p, L["next"]); self._hit["next"] = L["next"]

        # --- seek ---
        self._draw_seek(p, L)

        # --- right cluster (compact keeps only repeat + volume, flanking) ---
        r = L["right"]
        if not self._compact:
            self._draw_heart(p, r["favorite"], self._favorite); self._hit["favorite"] = r["favorite"]
            self._draw_shuffle(p, r["shuffle"], self._shuffle); self._hit["shuffle"] = r["shuffle"]
        self._draw_repeat(p, r["repeat"], self._repeat); self._hit["repeat"] = r["repeat"]
        self._draw_volume(p, r["volume"]); self._hit["volume"] = r["volume"]
        p.end()

    def _cover_pixmap(self, w, h):
        if self._cover_pm is not None and not self._cover_pm.isNull():
            src = self._cover_pm
            ckey = "pm"
        elif self._cover_path and os.path.exists(self._cover_path):
            src = QPixmap(self._cover_path)
            ckey = self._cover_path
        else:
            return None
        key = (ckey, int(w), int(h))
        if key in self._pix_cache:
            return self._pix_cache[key]
        if src.isNull():
            self._pix_cache[key] = None
            return None
        tw, th = int(w * 2), int(h * 2)
        sc = src.scaled(tw, th, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = max(0, (sc.width() - tw) // 2)
        y = max(0, (sc.height() - th) // 2)
        pm = sc.copy(x, y, tw, th)
        pm.setDevicePixelRatio(2.0)
        self._pix_cache[key] = pm
        return pm

    # -- transport glyphs --
    def _icon_color(self, name, active=False):
        if active:
            return self._accent
        if self._hover == name:
            return self._text
        return self._icon

    def _draw_play_button(self, p, rect):
        p.setPen(Qt.NoPen)
        p.setBrush(self._playbtn if not self._hover == "play" else self._playbtn.lighter(108))
        p.drawEllipse(rect)
        c = rect.center()
        s = rect.width()
        p.setBrush(QColor("#12131a"))
        if self._playing:
            bw = s * 0.09
            bh = s * 0.30
            off = s * 0.10
            p.drawRoundedRect(QRectF(c.x() - off - bw, c.y() - bh / 2, bw, bh), 1.5, 1.5)
            p.drawRoundedRect(QRectF(c.x() + off, c.y() - bh / 2, bw, bh), 1.5, 1.5)
        else:
            t = s * 0.17
            tri = QPolygonF([QPointF(c.x() - t * 0.55, c.y() - t),
                             QPointF(c.x() - t * 0.55, c.y() + t),
                             QPointF(c.x() + t * 0.9, c.y())])
            p.drawPolygon(tri)

    def _draw_prev(self, p, rect):
        col = self._icon_color("prev")
        p.setPen(Qt.NoPen)
        p.setBrush(col)
        c = rect.center()
        s = rect.width() * 0.30
        for dx in (0.15, -0.55):
            cx = c.x() + s * dx * 1.7
            tri = QPolygonF([QPointF(cx + s * 0.55, c.y() - s),
                             QPointF(cx + s * 0.55, c.y() + s),
                             QPointF(cx - s * 0.5, c.y())])
            p.drawPolygon(tri)
        p.setPen(QPen(col, max(1.6, rect.width() * 0.07)))
        x = c.x() - s * 1.35
        p.drawLine(QPointF(x, c.y() - s), QPointF(x, c.y() + s))

    def _draw_next(self, p, rect):
        col = self._icon_color("next")
        p.setPen(Qt.NoPen)
        p.setBrush(col)
        c = rect.center()
        s = rect.width() * 0.30
        for dx in (-0.15, 0.55):
            cx = c.x() + s * dx * 1.7
            tri = QPolygonF([QPointF(cx - s * 0.55, c.y() - s),
                             QPointF(cx - s * 0.55, c.y() + s),
                             QPointF(cx + s * 0.5, c.y())])
            p.drawPolygon(tri)
        p.setPen(QPen(col, max(1.6, rect.width() * 0.07)))
        x = c.x() + s * 1.35
        p.drawLine(QPointF(x, c.y() - s), QPointF(x, c.y() + s))

    def _draw_seek(self, p, L):
        tr = L["track"]
        self._seek_rect = tr
        p.setPen(Qt.NoPen)
        p.setBrush(self._track)
        p.drawRoundedRect(tr, tr.height() / 2, tr.height() / 2)
        fillw = tr.width() * max(0.0, min(1.0, self._pos))
        fr = QRectF(tr.left(), tr.top(), fillw, tr.height())
        p.setBrush(self._accent)
        p.drawRoundedRect(fr, tr.height() / 2, tr.height() / 2)
        # knob
        kx = tr.left() + fillw
        kr = tr.height() * 1.6
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(QPointF(kx, tr.center().y()), kr, kr)
        # times
        f = QFont(self.font())
        f.setPointSizeF(max(7.5, min(self.height() * 0.11, 9.5)))
        p.setFont(f)
        p.setPen(self._subtext)
        p.drawText(L["elapsed_rect"], Qt.AlignVCenter | Qt.AlignLeft, self._elapsed)
        p.drawText(L["total_rect"], Qt.AlignVCenter | Qt.AlignRight, self._total)

    def _draw_heart(self, p, rect, active):
        col = self._accent if active else self._icon_color("favorite")
        c = rect.center()
        s = rect.width() * 0.30
        path = QPainterPath()
        path.moveTo(c.x(), c.y() + s * 0.9)
        path.cubicTo(c.x() - s * 1.7, c.y() - s * 0.3,
                     c.x() - s * 0.6, c.y() - s * 1.25, c.x(), c.y() - s * 0.35)
        path.cubicTo(c.x() + s * 0.6, c.y() - s * 1.25,
                     c.x() + s * 1.7, c.y() - s * 0.3, c.x(), c.y() + s * 0.9)
        if active:
            p.setPen(Qt.NoPen); p.setBrush(col); p.drawPath(path)
        else:
            p.setPen(QPen(col, max(1.5, rect.width() * 0.06))); p.setBrush(Qt.NoBrush)
            p.drawPath(path)

    def _draw_shuffle(self, p, rect, active):
        col = self._icon_color("shuffle", active)
        p.setPen(QPen(col, max(1.6, rect.width() * 0.065), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(Qt.NoBrush)
        c = rect.center()
        s = rect.width() * 0.32
        # two crossing arrows
        p.drawLine(QPointF(c.x() - s, c.y() - s * 0.7), QPointF(c.x() + s, c.y() + s * 0.7))
        p.drawLine(QPointF(c.x() - s, c.y() + s * 0.7), QPointF(c.x() + s, c.y() - s * 0.7))
        p.setPen(Qt.NoPen); p.setBrush(col)
        for sy in (-0.7, 0.7):
            ax, ay = c.x() + s, c.y() + s * sy
            p.drawPolygon(QPolygonF([QPointF(ax, ay), QPointF(ax - s * 0.5, ay - s * 0.14 * (1 if sy < 0 else -1) - s * 0.28),
                                     QPointF(ax - s * 0.5, ay)]))

    def _draw_repeat(self, p, rect, active):
        col = self._icon_color("repeat", active)
        p.setPen(QPen(col, max(1.6, rect.width() * 0.065), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(Qt.NoBrush)
        c = rect.center()
        s = rect.width() * 0.30
        rr = QRectF(c.x() - s, c.y() - s, s * 2, s * 2)
        p.drawArc(rr, 40 * 16, 280 * 16)
        p.setPen(Qt.NoPen); p.setBrush(col)
        # arrowhead at arc end (top-right)
        ax, ay = c.x() + s * 0.75, c.y() - s * 0.62
        p.drawPolygon(QPolygonF([QPointF(ax + s * 0.35, ay - s * 0.05),
                                 QPointF(ax - s * 0.2, ay - s * 0.5),
                                 QPointF(ax - s * 0.1, ay + s * 0.35)]))

    def _draw_volume(self, p, rect):
        col = self._icon_color("volume")
        c = rect.center()
        s = rect.width() * 0.30
        p.setPen(Qt.NoPen); p.setBrush(col)
        body = QPolygonF([QPointF(c.x() - s, c.y() - s * 0.35),
                          QPointF(c.x() - s * 0.35, c.y() - s * 0.35),
                          QPointF(c.x() + s * 0.2, c.y() - s * 0.85),
                          QPointF(c.x() + s * 0.2, c.y() + s * 0.85),
                          QPointF(c.x() - s * 0.35, c.y() + s * 0.35),
                          QPointF(c.x() - s, c.y() + s * 0.35)])
        p.drawPolygon(body)
        p.setPen(QPen(col, max(1.4, rect.width() * 0.05))); p.setBrush(Qt.NoBrush)
        for rad in (s * 0.7, s * 1.15):
            p.drawArc(QRectF(c.x() + s * 0.2 - rad, c.y() - rad, rad * 2, rad * 2),
                      -55 * 16, 110 * 16)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _seek_from_x(self, x):
        tr = self._seek_rect
        if tr.width() <= 0:
            return
        self._pos = max(0.0, min(1.0, (x - tr.left()) / tr.width()))
        self.update()
        self.seeked.emit(self._pos)

    def mousePressEvent(self, e):
        pt = QPointF(e.pos())
        seek_hot = self._seek_rect.adjusted(-6, -14, 6, 14)
        if seek_hot.contains(pt):
            self._seeking = True
            self._seek_from_x(pt.x())
            return
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        pt = QPointF(e.pos())
        if self._seeking:
            self._seek_from_x(pt.x())
            return
        prev_hover = self._hover
        self._hover = None
        for nm, r in self._hit.items():
            if r.contains(pt):
                self._hover = nm
                break
        self.setCursor(Qt.PointingHandCursor if self._hover else Qt.ArrowCursor)
        if prev_hover != self._hover:
            self.update()
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if self._seeking:
            self._seeking = False
            return
        pt = QPointF(e.pos())
        for nm, r in self._hit.items():
            if r.contains(pt):
                self._activate(nm)
                break
        super().mouseReleaseEvent(e)

    def leaveEvent(self, e):
        if self._hover:
            self._hover = None
            self.update()
        super().leaveEvent(e)

    def _activate(self, name):
        if name == "play":
            self._playing = not self._playing
            self.playToggled.emit(self._playing)
        elif name == "next":
            self.nextClicked.emit()
        elif name == "prev":
            self.prevClicked.emit()
        elif name == "favorite":
            self._favorite = not self._favorite
            self.favoriteToggled.emit(self._favorite)
        elif name == "shuffle":
            self._shuffle = not self._shuffle
            self.shuffleToggled.emit(self._shuffle)
        elif name == "repeat":
            self._repeat = not self._repeat
            self.repeatToggled.emit(self._repeat)
        elif name == "volume":
            self.volumeClicked.emit()
        self.update()

    def sizeHint(self):
        return QSize(300, 150) if self._compact else QSize(900, 88)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    def _mk_str(attr):
        def getter(self): return getattr(self, attr)
        def setter(self, v):
            setattr(self, attr, str(v))
            if attr == "_cover_path":
                self._pix_cache.clear()
            self.update()
        return Property(str, getter, setter)

    def _mk_color(attr):
        def getter(self): return getattr(self, attr)
        def setter(self, v):
            setattr(self, attr, QColor(v)); self.update()
        return Property(QColor, getter, setter)

    def _mk_bool(attr):
        def getter(self): return getattr(self, attr)
        def setter(self, v):
            setattr(self, attr, bool(v)); self.update()
        return Property(bool, getter, setter)

    title = _mk_str("_title")
    artist = _mk_str("_artist")
    elapsedText = _mk_str("_elapsed")
    totalText = _mk_str("_total")

    playing = _mk_bool("_playing")
    favorite = _mk_bool("_favorite")
    shuffle = _mk_bool("_shuffle")
    repeat = _mk_bool("_repeat")

    barColor = _mk_color("_bar")
    accentColor = _mk_color("_accent")
    trackColor = _mk_color("_track")
    textColor = _mk_color("_text")
    subTextColor = _mk_color("_subtext")
    iconColor = _mk_color("_icon")
    playBtnColor = _mk_color("_playbtn")

    @Property(str)
    def coverPath(self):
        return self._cover_path

    @coverPath.setter
    def coverPath(self, v):
        self.setCoverSource(v)

    @Property(float)
    def position(self):
        return self._pos

    @position.setter
    def position(self, v):
        self._pos = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    # Numeric time API — the bar formats m:ss and derives `position` itself,
    # so managers feed SECONDS instead of hand-formatting display strings.
    @staticmethod
    def _fmt(seconds):
        m, s = divmod(max(0, int(seconds)), 60)
        return "%d:%02d" % (m, s)

    @Property(float)
    def durationSeconds(self):
        return getattr(self, "_duration_s", 0.0)

    @durationSeconds.setter
    def durationSeconds(self, secs):
        self._duration_s = max(0.0, float(secs))
        if self._duration_s > 0:
            self._total = self._fmt(self._duration_s)
        self.update()

    @Property(float)
    def elapsedSeconds(self):
        return getattr(self, "_elapsed_s", 0.0)

    @elapsedSeconds.setter
    def elapsedSeconds(self, secs):
        self._elapsed_s = max(0.0, float(secs))
        self._elapsed = self._fmt(self._elapsed_s)
        dur = getattr(self, "_duration_s", 0.0)
        if dur > 0:
            self._pos = max(0.0, min(1.0, self._elapsed_s / dur))
        self.update()

    @Property(bool)
    def compactMode(self):
        """Opt-in stacked layout (cover+titles / seek / centred transport) for
        a narrow now-playing CARD; the default wide bar is unchanged."""
        return self._compact

    @compactMode.setter
    def compactMode(self, v):
        self._compact = bool(v)
        pol = self.sizePolicy()
        pol.setVerticalPolicy(QSizePolicy.Expanding if self._compact else QSizePolicy.Fixed)
        self.setSizePolicy(pol)
        self.updateGeometry()
        self.update()
