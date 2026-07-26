########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCoverCard - an album / song COVER card.
##
## A rounded album-art tile: the cover image fills a rounded rectangle
## (centre-cropped, KeepAspectRatioByExpanding), a bottom gradient SCRIM
## darkens the lower third, and a bold TITLE over a muted ARTIST sit at the
## bottom-left. A translucent circular PLAY badge fades in on hover (or is
## pinned on with `showPlay`). Everything is painted with QPainter so it stays
## crisp at any size and recolours on a theme switch (all colours are
## qproperties). When no `coverPath` is set it paints a two-stop gradient from
## `accentColor` so it still previews in Designer / render_widget.
##
## It is a QAbstractButton, so it emits clicked() — drop it in a "Popular
## songs" / "Recently played" row or a coverflow. Give it `title`, `artist`
## and `coverPath` in code or Qt Designer.
########################################################################
import os

from qtpy.QtCore import Qt, Property, QRectF, QRect, QSize, QPointF, Signal
from qtpy.QtGui import (QColor, QPainter, QBrush, QPen, QFont, QFontMetrics,
                        QLinearGradient, QPixmap, QPainterPath, QPolygonF)
from qtpy.QtWidgets import QAbstractButton, QSizePolicy


class QCustomCoverCard(QAbstractButton):

    WIDGET_ICON = "components/icons/image.png"
    WIDGET_TOOLTIP = "An album / song cover card (art + title + artist + hover play)"
    WIDGET_MODULE = "Custom_Widgets.QCustomCoverCard"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCoverCard' name='customCoverCard'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>150</width><height>190</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCoverCard",
        "props": {"title": {"type": "string", "default": "Golden Days"},
                  "artist": {"type": "string", "default": "Felix Carter"},
                  "coverPath": {"type": "string", "default": ""},
                  "accentColor": {"type": "color", "default": "#e0592f"},
                  "titleColor": {"type": "color", "default": "#ffffff"},
                  "artistColor": {"type": "color", "default": "#d0d0d8"},
                  "cornerRadius": {"type": "int", "default": 22},
                  "scrimStrength": {"type": "float", "default": 0.85},
                  "scrimColor": {"type": "color", "default": "#06080e"},
                  "showPlay": {"type": "bool", "default": False},
                  "playOnHover": {"type": "bool", "default": True},
                  "titleScale": {"type": "float", "default": 1.0},
                  "textAlign": {"type": "enum", "values": ["left", "center"], "default": "left"}},
        "signals": ["clicked", "playClicked"],
        "tokens_used": ["accent", "on-surface"],
    }

    playClicked = Signal()

    def __init__(self, parent=None, title="Golden Days", artist="Felix Carter",
                 coverPath=""):
        super().__init__(parent)
        self.setObjectName("QCustomCoverCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self._title = title
        self._artist = artist
        self._cover_path = coverPath
        self._accent = QColor("#e0592f")
        self._title_color = QColor("#ffffff")
        self._artist_color = QColor("#d0d0d8")
        self._radius = 22
        self._scrim = 0.85
        self._scrim_color = QColor(6, 8, 14)    # bottom scrim tint (set to accent for a colour band)
        self._show_play = False
        self._play_on_hover = True
        self._title_scale = 1.0
        self._text_align = "left"   # "left" | "center"
        self._cover_pm = None       # a directly-loaded pixmap (e.g. from a URL)
        self._pix_cache = {}
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(120, 150)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setTitle(self, text):
        self._title = str(text)
        self.update()

    def setArtist(self, text):
        self._artist = str(text)
        self.update()

    def setCoverPath(self, path):
        path = str(path or "")
        self._cover_path = path
        self._pix_cache.clear()
        # an http(s) source is fetched + cached asynchronously, then painted
        if path.lower().startswith(("http://", "https://")):
            self._cover_pm = None
            from Custom_Widgets.ImageLoader import load_image
            load_image(path, self._onCoverLoaded)
        else:
            self._cover_pm = None
        self.update()

    def _onCoverLoaded(self, pm):
        self._cover_pm = pm if (pm is not None and not pm.isNull()) else None
        self._pix_cache.clear()
        self.update()

    def setData(self, title=None, artist=None, coverPath=None):
        if title is not None:
            self._title = str(title)
        if artist is not None:
            self._artist = str(artist)
        if coverPath is not None:
            self.setCoverPath(coverPath)   # routes http(s) sources through ImageLoader
        self.update()

    # ------------------------------------------------------------------ #
    ## Helpers
    # ------------------------------------------------------------------ #
    def _cover_pixmap(self, w, h):
        """Cover image scaled to FILL (w x h) at 2x, centre-cropped. Source is a
        directly-loaded pixmap (e.g. fetched from a URL) if present, else the
        local file path."""
        if self._cover_pm is not None and not self._cover_pm.isNull():
            src = self._cover_pm
            ckey = "pm"
        elif self._cover_path and os.path.exists(self._cover_path):
            src = QPixmap(self._cover_path)
            ckey = self._cover_path
        else:
            return None
        key = (ckey, w, h)
        if key in self._pix_cache:
            return self._pix_cache[key]
        if src.isNull():
            self._pix_cache[key] = None
            return None
        tw, th = int(w * 2), int(h * 2)
        scaled = src.scaled(tw, th, Qt.KeepAspectRatioByExpanding,
                            Qt.SmoothTransformation)
        # centre-crop
        x = max(0, (scaled.width() - tw) // 2)
        y = max(0, (scaled.height() - th) // 2)
        cropped = scaled.copy(x, y, tw, th)
        cropped.setDevicePixelRatio(2.0)
        self._pix_cache[key] = cropped
        return cropped

    def _play_visible(self):
        return self._show_play or (self._play_on_hover and self.underMouse())

    def _play_rect(self):
        d = max(30.0, min(self.width(), self.height()) * 0.24)
        cx = self.width() - d / 2.0 - self.height() * 0.06
        cy = self.height() - d / 2.0 - self.height() * 0.06
        return QRectF(cx - d / 2.0, cy - d / 2.0, d, d)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        w, h = self.width(), self.height()
        r = float(self._radius)

        rect = QRectF(0, 0, w, h)
        clip = QPainterPath()
        clip.addRoundedRect(rect, r, r)
        p.setClipPath(clip)

        # --- cover art or fallback gradient ---
        pm = self._cover_pixmap(w, h)
        if pm is not None:
            p.drawPixmap(rect, pm, QRectF(0, 0, pm.width(), pm.height()))
        else:
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, self._accent.lighter(118))
            grad.setColorAt(1.0, self._accent.darker(135))
            p.fillRect(rect, QBrush(grad))

        # hover lift: subtle brighten
        if self.underMouse():
            p.fillRect(rect, QColor(255, 255, 255, 18))

        # --- bottom scrim so text is legible (tinted by scrimColor) ---
        sc = self._scrim_color
        r0, g0, b0 = sc.red(), sc.green(), sc.blue()
        scrim = QLinearGradient(QPointF(0, h * 0.38), QPointF(0, h))
        a = int(max(0.0, min(1.0, self._scrim)) * 240)
        scrim.setColorAt(0.0, QColor(r0, g0, b0, 0))
        scrim.setColorAt(0.5, QColor(r0, g0, b0, int(a * 0.5)))
        scrim.setColorAt(1.0, QColor(r0, g0, b0, a))
        p.fillRect(QRectF(0, h * 0.38, w, h * 0.62), QBrush(scrim))

        # --- title + artist ---
        pad = max(10.0, w * 0.08)
        avail = w - pad * 2 - 6

        title_pt = max(9.0, min(h * 0.085, 15.0)) * self._title_scale
        tf = QFont(self.font())
        tf.setBold(True)
        tf.setPointSizeF(title_pt)
        tf = self._fit_font(tf, self._title, avail)
        artist_pt = max(8.0, min(h * 0.062, 12.0))
        af = QFont(self.font())
        af.setPointSizeF(artist_pt)
        af = self._fit_font(af, self._artist, avail)

        tfm, afm = QFontMetrics(tf), QFontMetrics(af)
        gap = 2.0
        block_h = tfm.height() + gap + afm.height()
        base_y = h - max(10.0, h * 0.07) - block_h

        halign = Qt.AlignHCenter if self._text_align == "center" else Qt.AlignLeft
        p.setFont(tf)
        p.setPen(QPen(self._title_color))
        p.drawText(QRectF(pad, base_y, avail, tfm.height()),
                   halign | Qt.AlignVCenter,
                   tfm.elidedText(self._title, Qt.ElideRight, int(avail)))
        p.setFont(af)
        p.setPen(QPen(self._artist_color))
        p.drawText(QRectF(pad, base_y + tfm.height() + gap, avail, afm.height()),
                   halign | Qt.AlignVCenter,
                   afm.elidedText(self._artist, Qt.ElideRight, int(avail)))

        # --- play badge ---
        if self._play_visible():
            pr = self._play_rect()
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 255, 255, 60))
            p.drawEllipse(pr)
            inner = pr.adjusted(pr.width() * 0.16, pr.height() * 0.16,
                                -pr.width() * 0.16, -pr.height() * 0.16)
            p.setBrush(QColor(255, 255, 255, 235))
            p.drawEllipse(inner)
            # triangle
            cx, cy = inner.center().x(), inner.center().y()
            s = inner.width() * 0.30
            tri = QPolygonF([QPointF(cx - s * 0.5, cy - s * 0.62),
                             QPointF(cx - s * 0.5, cy + s * 0.62),
                             QPointF(cx + s * 0.72, cy)])
            p.setBrush(QColor("#12131a"))
            p.drawPolygon(tri)
        p.end()

    def _fit_font(self, font, text, max_w):
        if max_w <= 0 or not text:
            return font
        fm = QFontMetrics(font)
        adv = fm.horizontalAdvance(text)
        if adv > max_w:
            pt = font.pointSizeF() * (max_w / adv)
            font.setPointSizeF(max(7.0, pt))
        return font

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mouseMoveEvent(self, e):
        self.update()
        super().mouseMoveEvent(e)

    def enterEvent(self, e):
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if self._play_visible() and self._play_rect().contains(QPointF(e.pos())):
            self.playClicked.emit()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        return QSize(150, 190)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def title(self):
        return self._title

    @title.setter
    def title(self, t):
        self.setTitle(t)

    @Property(str)
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, t):
        self.setArtist(t)

    @Property(str)
    def coverPath(self):
        return self._cover_path

    @coverPath.setter
    def coverPath(self, p):
        self.setCoverPath(p)

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self.update()

    @Property(QColor)
    def titleColor(self):
        return self._title_color

    @titleColor.setter
    def titleColor(self, c):
        self._title_color = QColor(c)
        self.update()

    @Property(QColor)
    def artistColor(self):
        return self._artist_color

    @artistColor.setter
    def artistColor(self, c):
        self._artist_color = QColor(c)
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(float)
    def scrimStrength(self):
        return self._scrim

    @scrimStrength.setter
    def scrimStrength(self, v):
        self._scrim = float(v)
        self.update()

    @Property(QColor)
    def scrimColor(self):
        return self._scrim_color

    @scrimColor.setter
    def scrimColor(self, c):
        self._scrim_color = QColor(c)
        self.update()

    @Property(bool)
    def showPlay(self):
        return self._show_play

    @showPlay.setter
    def showPlay(self, v):
        self._show_play = bool(v)
        self.update()

    @Property(bool)
    def playOnHover(self):
        return self._play_on_hover

    @playOnHover.setter
    def playOnHover(self, v):
        self._play_on_hover = bool(v)
        self.update()

    @Property(float)
    def titleScale(self):
        return self._title_scale

    @titleScale.setter
    def titleScale(self, v):
        self._title_scale = max(0.5, float(v))
        self.update()

    @Property(str)
    def textAlign(self):
        return self._text_align

    @textAlign.setter
    def textAlign(self, v):
        self._text_align = "center" if str(v).lower() == "center" else "left"
        self.update()
