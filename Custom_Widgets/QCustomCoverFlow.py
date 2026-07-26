########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomCoverFlow - a 3D COVER-FLOW carousel.
##
## The signature music/media hero: the ACTIVE cover sits large and centred
## with a bottom scrim, TITLE + ARTIST and a circular PLAY badge; its
## neighbours PEEK out on either side, progressively SCALED DOWN, DIMMED and
## slid behind it to fake depth. Click a side cover (or drag / wheel / arrow
## keys) to rotate it to the centre — the motion EASES smoothly. Fully
## painted with QPainter so it is crisp at any size and needs no images to
## preview (covers with no `coverPath` fall back to a per-item accent
## gradient).
##
## Data-driven: feed it items with setItems([...]) (each: title, artist,
## coverPath, accent) or the `itemsJson` Designer property. Emits
## currentChanged(int), itemClicked(int) and playClicked(int).
########################################################################
import os
import json

from qtpy.QtCore import (Qt, Property, QRectF, QRect, QSize, QPointF, QTimer,
                         Signal)
from qtpy.QtGui import (QColor, QPainter, QBrush, QPen, QFont, QFontMetrics,
                        QLinearGradient, QPixmap, QPainterPath, QPolygonF)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomCoverFlow(QWidget):

    WIDGET_ICON = "components/icons/view_carousel.png"
    WIDGET_TOOLTIP = "A 3D cover-flow carousel (active cover centred, neighbours peek)"
    WIDGET_MODULE = "Custom_Widgets.QCustomCoverFlow"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomCoverFlow' name='customCoverFlow'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>640</width><height>320</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomCoverFlow",
        "props": {"itemsJson": {"type": "string", "default": "[]"},
                  "currentIndex": {"type": "int", "default": 0},
                  "activeRatio": {"type": "float", "default": 0.9},
                  "aspect": {"type": "float", "default": 1.05},
                  "sideScale": {"type": "float", "default": 0.72},
                  "sideOpacity": {"type": "float", "default": 0.55},
                  "sideSpacing": {"type": "float", "default": 0.42},
                  "cornerRadius": {"type": "int", "default": 24},
                  "showText": {"type": "bool", "default": True},
                  "showPlay": {"type": "bool", "default": True},
                  "titleColor": {"type": "color", "default": "#ffffff"},
                  "artistColor": {"type": "color", "default": "#c8c8d4"},
                  "playColor": {"type": "color", "default": "#ffffff"}},
        "signals": ["currentChanged", "itemClicked", "playClicked"],
        "tokens_used": ["accent", "on-surface"],
    }

    currentChanged = Signal(int)
    itemClicked = Signal(int)
    playClicked = Signal(int)

    _DEMO = [
        {"title": "Sunset Drive", "artist": "Leah Cole", "accent": "#c0432a"},
        {"title": "Neon Bloom", "artist": "Ivy Sound", "accent": "#2f6f8f"},
        {"title": "Echoes of Midnight", "artist": "Jon Hickman", "accent": "#1f7a5a"},
        {"title": "Golden Hour", "artist": "Mia Lowell", "accent": "#d79a2b"},
        {"title": "Crimson Bass", "artist": "The Verge", "accent": "#a12f4b"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomCoverFlow")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(360, 220)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self._items = list(self._DEMO)
        self._index = 2
        self._pos = 2.0            # animated fractional position
        self._target = 2.0
        self._active_ratio = 0.9
        self._aspect = 1.05        # width / height of a cover
        self._side_scale = 0.72
        self._side_opacity = 0.55
        self._side_spacing = 0.42  # centre-to-centre step, in active-widths
        self._radius = 24
        self._show_text = True
        self._show_play = True
        self._title_color = QColor("#ffffff")
        self._artist_color = QColor("#c8c8d4")
        self._play_color = QColor("#ffffff")

        self._pix_cache = {}
        self._item_rects = []      # [(i, QRectF)] nearest-last
        self._play_hit = None      # QRectF of active play badge
        self._drag_x = None
        self._drag_pos0 = 0.0
        self._dragging = False

        self._anim = QTimer(self)
        self._anim.setInterval(16)
        self._anim.timeout.connect(self._tick)

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def setItems(self, items):
        self._items = list(items or [])
        self._pix_cache.clear()
        self._index = max(0, min(self._index, len(self._items) - 1))
        self._pos = self._target = float(self._index)
        self._loadCovers()
        self.update()

    def _loadCovers(self):
        """Any item whose `coverPath` (or `coverUrl`) is an http(s) URL is
        fetched + disk-cached asynchronously; the pixmap lands on the item as
        `_pm` and repaints. Local paths are read straight from disk in paint."""
        from Custom_Widgets.ImageLoader import load_image
        for item in self._items:
            src = item.get("coverUrl") or item.get("coverPath") or ""
            if isinstance(src, str) and src.lower().startswith(("http://", "https://")):
                def _cb(pm, it=item):
                    if pm is not None and not pm.isNull():
                        it["_pm"] = pm
                        self._pix_cache.clear()
                        self.update()
                load_image(src, _cb)

    def count(self):
        return len(self._items)

    def setCurrentIndex(self, i, animate=True):
        if not self._items:
            return
        i = max(0, min(int(i), len(self._items) - 1))
        if i == self._index and abs(self._pos - i) < 1e-3:
            return
        self._index = i
        self._target = float(i)
        if animate:
            if not self._anim.isActive():
                self._anim.start()
        else:
            self._pos = float(i)
            self.update()
        self.currentChanged.emit(i)

    def next(self):
        self.setCurrentIndex(self._index + 1)

    def previous(self):
        self.setCurrentIndex(self._index - 1)

    # ------------------------------------------------------------------ #
    ## Animation
    # ------------------------------------------------------------------ #
    def _tick(self):
        d = self._target - self._pos
        if abs(d) < 0.004:
            self._pos = self._target
            self._anim.stop()
        else:
            self._pos += d * 0.22
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry
    # ------------------------------------------------------------------ #
    def _active_size(self):
        w, h = self.width(), self.height()
        text_reserve = 0.0  # text is painted ON the cover scrim
        ah = h * self._active_ratio
        aw = ah * self._aspect
        if aw > w * 0.5:
            aw = w * 0.5
            ah = aw / self._aspect
        return aw, ah

    def _cover_pixmap(self, item, w, h):
        w, h = int(w), int(h)
        if w <= 0 or h <= 0:
            return None
        loaded = item.get("_pm")
        path = item.get("coverPath", "")
        if loaded is not None and not loaded.isNull():
            src, ckey = loaded, "pm"
        elif path and os.path.exists(path):
            src, ckey = QPixmap(path), path
        else:
            return None
        key = (id(item), ckey, w, h)
        if key in self._pix_cache:
            return self._pix_cache[key]
        pm = None
        if not src.isNull():
            tw, th = w * 2, h * 2
            scaled = src.scaled(tw, th, Qt.KeepAspectRatioByExpanding,
                                Qt.SmoothTransformation)
            x = max(0, (scaled.width() - tw) // 2)
            y = max(0, (scaled.height() - th) // 2)
            pm = scaled.copy(x, y, tw, th)
            pm.setDevicePixelRatio(2.0)
        self._pix_cache[key] = pm
        return pm

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self._item_rects = []
        self._play_hit = None
        if not self._items:
            return

        w, h = self.width(), self.height()
        aw, ah = self._active_size()
        cx, cy = w / 2.0, h / 2.0
        step = aw * self._side_spacing

        n = len(self._items)
        # farthest first so the centre cover ends up on top
        order = sorted(range(n), key=lambda i: -abs(i - self._pos))
        for i in order:
            off = i - self._pos
            aoff = abs(off)
            if aoff > 3.2:
                continue
            scale = self._side_scale ** min(aoff, 3.0)
            iw, ih = aw * scale, ah * scale
            # cluster far covers closer together (perspective)
            xoff = step * (off if aoff <= 1 else (off / aoff) * (1 + (aoff - 1) * 0.62))
            rect = QRectF(cx + xoff - iw / 2.0, cy - ih / 2.0, iw, ih)
            opacity = 1.0 if aoff < 0.5 else max(self._side_opacity,
                                                 1.0 - aoff * (1.0 - self._side_opacity) * 0.9)
            self._paint_cover(p, self._items[i], rect, opacity, aoff < 0.5)
            self._item_rects.append((i, rect))
        # nearest-last for hit testing
        self._item_rects.sort(key=lambda t: -abs(t[0] - self._pos))
        p.end()

    def _paint_cover(self, p, item, rect, opacity, active):
        p.save()
        p.setOpacity(opacity)
        r = float(self._radius) * (rect.height() / (self._active_size()[1] or 1))
        r = max(8.0, r)
        clip = QPainterPath()
        clip.addRoundedRect(rect, r, r)
        p.setClipPath(clip)

        pm = self._cover_pixmap(item, rect.width(), rect.height())
        if pm is not None:
            p.drawPixmap(rect, pm, QRectF(0, 0, pm.width(), pm.height()))
        else:
            acc = QColor(item.get("accent", "#2f6f8f"))
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0.0, acc.lighter(120))
            grad.setColorAt(1.0, acc.darker(140))
            p.fillRect(rect, QBrush(grad))

        if not active:
            # darken non-active covers so the centre pops
            p.fillRect(rect, QColor(4, 6, 12, 90))

        if active and (self._show_text or self._show_play):
            self._paint_active_overlay(p, item, rect)
        p.restore()

        # crisp rim on the active cover
        if active:
            p.save()
            p.setOpacity(opacity)
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(255, 255, 255, 34), 1.2))
            p.drawRoundedRect(rect.adjusted(0.6, 0.6, -0.6, -0.6), r, r)
            p.restore()

    def _paint_active_overlay(self, p, item, rect):
        h = rect.height()
        scrim = QLinearGradient(QPointF(0, rect.top() + h * 0.42),
                                QPointF(0, rect.bottom()))
        scrim.setColorAt(0.0, QColor(6, 8, 14, 0))
        scrim.setColorAt(1.0, QColor(6, 8, 14, 220))
        p.fillRect(QRectF(rect.left(), rect.top() + h * 0.42,
                          rect.width(), h * 0.58), QBrush(scrim))

        pad = max(12.0, rect.width() * 0.07)
        play_d = max(34.0, rect.height() * 0.16)
        # play badge is vertically CENTRED on the right, so the bottom title
        # row can use the full width without colliding with it.
        text_w = rect.width() - pad * 2

        if self._show_text:
            tf = QFont(self.font())
            tf.setBold(True)
            tf.setPointSizeF(max(11.0, rect.height() * 0.072))
            tf = self._fit(tf, item.get("title", ""), text_w)
            af = QFont(self.font())
            af.setPointSizeF(max(9.0, rect.height() * 0.05))
            tfm, afm = QFontMetrics(tf), QFontMetrics(af)
            gap = 3.0
            block = tfm.height() + gap + afm.height()
            by = rect.bottom() - max(14.0, h * 0.08) - block
            p.setFont(tf)
            p.setPen(QPen(self._title_color))
            p.drawText(QRectF(rect.left() + pad, by, text_w, tfm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter,
                       tfm.elidedText(item.get("title", ""), Qt.ElideRight, int(text_w)))
            p.setFont(af)
            p.setPen(QPen(self._artist_color))
            p.drawText(QRectF(rect.left() + pad, by + tfm.height() + gap,
                              text_w, afm.height()),
                       Qt.AlignLeft | Qt.AlignVCenter,
                       afm.elidedText(item.get("artist", ""), Qt.ElideRight, int(text_w)))

        if self._show_play:
            d = play_d
            pcx = rect.right() - pad - d / 2.0
            pcy = rect.center().y() + rect.height() * 0.06
            pr = QRectF(pcx - d / 2.0, pcy - d / 2.0, d, d)
            p.setPen(QPen(QColor(255, 255, 255, 150), 1.4))
            p.setBrush(QColor(255, 255, 255, 40))
            p.drawEllipse(pr)
            s = d * 0.24
            tri = QPolygonF([QPointF(pcx - s * 0.45, pcy - s * 0.62),
                             QPointF(pcx - s * 0.45, pcy + s * 0.62),
                             QPointF(pcx + s * 0.8, pcy)])
            p.setPen(Qt.NoPen)
            p.setBrush(self._play_color)
            p.drawPolygon(tri)
            self._play_hit = pr

    def _fit(self, font, text, max_w):
        if max_w <= 0 or not text:
            return font
        fm = QFontMetrics(font)
        adv = fm.horizontalAdvance(text)
        if adv > max_w:
            font.setPointSizeF(max(8.0, font.pointSizeF() * (max_w / adv)))
        return font

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _item_at(self, pos):
        pt = QPointF(pos)
        for i, rect in reversed(self._item_rects):  # nearest last -> check first
            if rect.contains(pt):
                return i
        return -1

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_x = e.pos().x()
            self._drag_pos0 = self._pos
            self._dragging = False
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._drag_x is not None:
            dx = e.pos().x() - self._drag_x
            if abs(dx) > 4:
                self._dragging = True
            aw, _ = self._active_size()
            step = aw * self._side_spacing
            if step > 0:
                self._pos = self._drag_pos0 - dx / step
                self._pos = max(0.0, min(self._pos, len(self._items) - 1))
                self.update()
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if self._drag_x is not None:
            if self._dragging:
                self.setCurrentIndex(int(round(self._pos)))
            else:
                if self._play_hit is not None and self._play_hit.contains(QPointF(e.pos())):
                    self.playClicked.emit(self._index)
                else:
                    i = self._item_at(e.pos())
                    if i >= 0 and i != self._index:
                        self.setCurrentIndex(i)
                        self.itemClicked.emit(i)
                    elif i == self._index:
                        self.itemClicked.emit(i)
        self._drag_x = None
        self._dragging = False
        super().mouseReleaseEvent(e)

    def wheelEvent(self, e):
        self.setCurrentIndex(self._index + (1 if e.angleDelta().y() < 0 else -1))
        e.accept()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Right, Qt.Key_Down):
            self.next()
        elif e.key() in (Qt.Key_Left, Qt.Key_Up):
            self.previous()
        else:
            super().keyPressEvent(e)

    def sizeHint(self):
        return QSize(640, 320)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def itemsJson(self):
        return json.dumps(self._items)

    @itemsJson.setter
    def itemsJson(self, s):
        try:
            data = json.loads(s) if s else []
            if isinstance(data, list):
                self.setItems(data)
        except Exception:
            pass

    @Property(int)
    def currentIndex(self):
        return self._index

    @currentIndex.setter
    def currentIndex(self, i):
        self.setCurrentIndex(i, animate=False)

    @Property(float)
    def activeRatio(self):
        return self._active_ratio

    @activeRatio.setter
    def activeRatio(self, v):
        self._active_ratio = max(0.4, min(1.0, float(v)))
        self._pix_cache.clear()
        self.update()

    @Property(float)
    def aspect(self):
        return self._aspect

    @aspect.setter
    def aspect(self, v):
        self._aspect = max(0.5, float(v))
        self._pix_cache.clear()
        self.update()

    @Property(float)
    def sideScale(self):
        return self._side_scale

    @sideScale.setter
    def sideScale(self, v):
        self._side_scale = max(0.3, min(1.0, float(v)))
        self.update()

    @Property(float)
    def sideOpacity(self):
        return self._side_opacity

    @sideOpacity.setter
    def sideOpacity(self, v):
        self._side_opacity = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(float)
    def sideSpacing(self):
        return self._side_spacing

    @sideSpacing.setter
    def sideSpacing(self, v):
        self._side_spacing = max(0.2, float(v))
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(bool)
    def showText(self):
        return self._show_text

    @showText.setter
    def showText(self, v):
        self._show_text = bool(v)
        self.update()

    @Property(bool)
    def showPlay(self):
        return self._show_play

    @showPlay.setter
    def showPlay(self, v):
        self._show_play = bool(v)
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

    @Property(QColor)
    def playColor(self):
        return self._play_color

    @playColor.setter
    def playColor(self, c):
        self._play_color = QColor(c)
        self.update()
