########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomBubbleChart - an interactive packed-circle (bubble) chart.
##
## The sentiment / share bubble cloud: one circle per item, AREA proportional to
## the value, coloured by category and labelled inside when big enough. Circles
## are packed by a small deterministic force relaxation (push overlaps apart +
## gravity to a per-category anchor when grouped), then scaled to fill the widget.
##
## INTERACTIVE (the reference has all of these):
##   * hover  -> a CUSTOM painted tooltip card (never the OS QToolTip), plus a
##               grow animation + glow on the hovered bubble.
##   * zoom   -> wheel zooms toward the cursor, a painted +/- control, drag to pan,
##               double-click to reset. zoomIn()/zoomOut()/resetView().
##   * search -> setSearchQuery(text) dims the non-matching bubbles; the painted
##               search button emits searchRequested().
##   * scale  -> optional category grouping (`groupByCategory`) + axis labels.
##
## setItems([{label, value, category}]) / itemsJson; colours via
## setCategoryColors({category: colour}). Signals: bubbleClicked(label),
## searchRequested(), zoomChanged(float).
########################################################################
import json
import math

from qtpy.QtCore import Qt, Property, Signal, QRectF, QPointF, QTimer
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont, QFontMetrics, QPainterPath
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomBubbleChart(QWidget):

    bubbleClicked = Signal(str)
    searchRequested = Signal()
    zoomChanged = Signal(float)

    WIDGET_ICON = "components/icons/bubble_chart.png"
    WIDGET_TOOLTIP = "An interactive packed-circle (bubble) chart"
    WIDGET_MODULE = "Custom_Widgets.QCustomBubbleChart"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomBubbleChart' name='customBubbleChart'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>360</width><height>320</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomBubbleChart",
        "props": {
            "itemsJson": {"type": "string", "default": ""},
            "categoriesJson": {"type": "string", "default": ""},
            "padding": {"type": "float", "default": 3.0},
            "showLabels": {"type": "bool", "default": True},
            "minLabelRadius": {"type": "float", "default": 16.0},
            "labelColor": {"type": "color", "default": "#ffffff"},
            "defaultColor": {"type": "color", "default": "#8b90a0"},
            "shadeVariation": {"type": "float", "default": 0.18},
            "hoverGlow": {"type": "bool", "default": True},
            "hoverScale": {"type": "float", "default": 1.16},
            "groupByCategory": {"type": "bool", "default": False},
            "zoomable": {"type": "bool", "default": True},
            "showControls": {"type": "bool", "default": True},
            "searchQuery": {"type": "string", "default": ""},
            "tooltips": {"type": "bool", "default": True},
            "tooltipBgColor": {"type": "color", "default": "#0e1016"},
            "controlColor": {"type": "color", "default": "#f4f6fb"},
        },
        "signals": ["bubbleClicked", "searchRequested", "zoomChanged"],
        "tokens_used": ["accent", "up", "down"],
    }

    _DEFAULT_CATS = {
        "positive": "#3fb27f", "negative": "#e0607e", "neutral": "#8b9cff",
        "up": "#3fb27f", "down": "#e0607e", "default": "#8b90a0",
    }

    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.setObjectName("QCustomBubbleChart")
        self._items = list(items) if items is not None else self._seed()
        self._cats = dict(self._DEFAULT_CATS)
        self._pad = 3.0
        self._show_labels = True
        self._min_label_r = 16.0
        self._label_color = QColor("#ffffff")
        self._default_color = QColor("#8b90a0")
        self._shade = 0.18
        self._hover_glow = True
        self._hover_scale = 1.16
        self._group = False
        self._zoomable = True
        self._show_controls = True
        self._search = ""
        self._tooltips = True
        self._tip_bg = QColor("#0e1016")
        self._ctrl_color = QColor("#f4f6fb")
        # view state
        self._zoom = 1.0
        self._pan = QPointF(0.0, 0.0)
        self._drag_from = None
        self._dragged = False
        # packed data + hit caches
        self._nodes = []
        self._bbox = (0.0, 0.0, 1.0, 1.0)
        self._screen = []             # (label, cx, cy, r, matches) for hit-testing
        self._hover = -1
        self._grow = 1.0
        self._hover_timer = None
        self._plus_rect = QRectF()
        self._minus_rect = QRectF()
        self._search_rect = QRectF()
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(140, 140)
        self._pack()

    @staticmethod
    def _seed():
        return [
            {"label": "Travel insurance", "value": 90, "category": "negative"},
            {"label": "Low commission", "value": 82, "category": "positive"},
            {"label": "Wait time", "value": 55, "category": "negative"},
            {"label": "Resolve issue", "value": 60, "category": "positive"},
            {"label": "Shipping price", "value": 48, "category": "negative"},
            {"label": "Leave review", "value": 44, "category": "positive"},
            {"label": "Link account", "value": 40, "category": "neutral"},
            {"label": "High price", "value": 36, "category": "negative"},
            {"label": "Low price", "value": 34, "category": "positive"},
            {"label": "Charge fee", "value": 30, "category": "neutral"},
            {"label": "Send email", "value": 26, "category": "negative"},
            {"label": "Debit card", "value": 24, "category": "positive"},
            {"label": "Coupon code", "value": 30, "category": "negative"},
            {"label": "Buy button", "value": 18, "category": "neutral"},
            {"label": "Ship item", "value": 16, "category": "negative"},
            {"label": "Open card", "value": 20, "category": "positive"},
            {"label": "Use app", "value": 14, "category": "neutral"},
            {"label": "Post item", "value": 22, "category": "negative"},
        ]

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    def setItems(self, items):
        self._items = [dict(it) for it in (items or [])]
        self._pack()
        self.update()

    def setCategoryColors(self, mapping):
        for k, v in (mapping or {}).items():
            self._cats[str(k)] = v if isinstance(v, str) else QColor(v).name()
        self.update()

    def setSearchQuery(self, text):
        self._search = str(text or "")
        self.update()

    def items(self):
        return list(self._items)

    def _cat_color(self, cat):
        return QColor(self._cats.get(cat, self._default_color.name()))

    # ------------------------------------------------------------------ #
    ## View controls
    # ------------------------------------------------------------------ #
    def zoomIn(self):
        self._zoom_to(self._zoom * 1.2, QPointF(self.width() / 2, self.height() / 2))

    def zoomOut(self):
        self._zoom_to(self._zoom / 1.2, QPointF(self.width() / 2, self.height() / 2))

    def resetView(self):
        self._zoom = 1.0
        self._pan = QPointF(0.0, 0.0)
        self.zoomChanged.emit(self._zoom)
        self.update()

    def _zoom_to(self, z, focus):
        z = max(0.5, min(6.0, z))
        c = QPointF(self.width() / 2.0, self.height() / 2.0)
        d = focus - c
        # keep the point under `focus` fixed while zooming
        self._pan = d - (d - self._pan) * (z / self._zoom)
        self._zoom = z
        self.zoomChanged.emit(self._zoom)
        self.update()

    # ------------------------------------------------------------------ #
    ## Packing (deterministic force relaxation, size-independent)
    # ------------------------------------------------------------------ #
    def _pack(self):
        items = self._items
        self._nodes = []
        if not items:
            self._bbox = (0.0, 0.0, 1.0, 1.0)
            return
        vals = [max(1e-6, float(it.get("value", 1))) for it in items]
        vmax = max(vals)
        # per-category anchors on a circle (used only when grouped)
        cats = []
        for it in items:
            c = it.get("category", "default")
            if c not in cats:
                cats.append(c)
        anchors = {}
        if self._group and len(cats) > 1:
            R = 60.0
            for i, c in enumerate(cats):
                a = -math.pi / 2 + 2 * math.pi * i / len(cats)
                anchors[c] = (R * math.cos(a), R * math.sin(a))
        golden = 2.399963229728653
        nodes = []
        for i, it in enumerate(items):
            r = 10.0 + 34.0 * math.sqrt(vals[i] / vmax)
            ang = i * golden
            rad = 6.0 * math.sqrt(i + 0.5)
            ax, ay = anchors.get(it.get("category", "default"), (0.0, 0.0))
            nodes.append({"label": str(it.get("label", "")),
                          "cat": it.get("category", "default"), "val": vals[i],
                          "x": ax + rad * math.cos(ang), "y": ay + rad * math.sin(ang),
                          "r": r, "ax": ax, "ay": ay})
        for _ in range(180):
            for a in range(len(nodes)):
                na = nodes[a]
                for b in range(a + 1, len(nodes)):
                    nb = nodes[b]
                    dx = nb["x"] - na["x"]; dy = nb["y"] - na["y"]
                    d = math.hypot(dx, dy)
                    mind = na["r"] + nb["r"] + self._pad
                    if 1e-6 < d < mind:
                        push = (mind - d) / 2.0
                        ux, uy = dx / d, dy / d
                        na["x"] -= ux * push; na["y"] -= uy * push
                        nb["x"] += ux * push; nb["y"] += uy * push
                    elif d <= 1e-6:
                        na["x"] -= 0.5; nb["x"] += 0.5
            for n in nodes:                       # gravity to the (category) anchor
                n["x"] += (n["ax"] - n["x"]) * 0.02
                n["y"] += (n["ay"] - n["y"]) * 0.02
        xs0 = min(n["x"] - n["r"] for n in nodes)
        ys0 = min(n["y"] - n["r"] for n in nodes)
        xs1 = max(n["x"] + n["r"] for n in nodes)
        ys1 = max(n["y"] + n["r"] for n in nodes)
        self._nodes = nodes
        self._bbox = (xs0, ys0, xs1 - xs0, ys1 - ys0)

    def _base_fit(self):
        m = 12.0
        bx, by, bw, bh = self._bbox
        bw = bw or 1.0; bh = bh or 1.0
        s = min((self.width() - 2 * m) / bw, (self.height() - 2 * m) / bh)
        ox = (self.width() - bw * s) / 2.0 - bx * s
        oy = (self.height() - bh * s) / 2.0 - by * s
        return s, ox, oy

    def _to_screen(self, n):
        s, ox, oy = self._base_fit()
        c = QPointF(self.width() / 2.0, self.height() / 2.0)
        fx = n["x"] * s + ox
        fy = n["y"] * s + oy
        cx = c.x() + (fx - c.x()) * self._zoom + self._pan.x()
        cy = c.y() + (fy - c.y()) * self._zoom + self._pan.y()
        return cx, cy, n["r"] * s * self._zoom

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._nodes:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        vmax = max((n["val"] for n in self._nodes), default=1.0)
        q = self._search.strip().lower()
        self._screen = []
        for i, n in enumerate(self._nodes):
            cx, cy, r = self._to_screen(n)
            matches = (not q) or (q in n["label"].lower())
            self._screen.append((n["label"], cx, cy, r, matches))
            if i == self._hover:
                continue
            self._draw_bubble(p, n, cx, cy, r, vmax, grow=1.0, glow=False,
                              dim=(not matches))
        if 0 <= self._hover < len(self._screen):
            _, cx, cy, r, matches = self._screen[self._hover]
            self._draw_bubble(p, self._nodes[self._hover], cx, cy, r, vmax,
                              grow=self._grow, glow=self._hover_glow,
                              dim=(not matches))
        if self._show_controls and self._zoomable:
            self._paint_controls(p)
        if self._tooltips and 0 <= self._hover < len(self._screen):
            self._paint_tooltip(p)
        p.end()

    def _draw_bubble(self, p, n, cx, cy, r, vmax, grow, glow, dim):
        col = self._cat_color(n["cat"])
        frac = n["val"] / vmax
        col = col.lighter(int(100 + self._shade * 100 * (1.0 - frac)))
        if dim:
            col.setAlpha(46)
        rr = r * grow
        if glow and grow > 1.001 and not dim:
            for k in range(3, 0, -1):
                t = k / 3.0
                gc = QColor(col); gc.setAlphaF(0.22 * (1.1 - t))
                p.setPen(Qt.NoPen); p.setBrush(QBrush(gc))
                p.drawEllipse(QPointF(cx, cy), rr + t * 10.0, rr + t * 10.0)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(col))
        p.drawEllipse(QPointF(cx, cy), rr, rr)
        if self._show_labels and rr >= self._min_label_r and n["label"] and not dim:
            self._paint_label(p, n["label"], cx, cy, rr)

    def _paint_label(self, p, text, cx, cy, r):
        f = QFont(self.font()); f.setPointSizeF(max(7.0, r * 0.26)); f.setBold(True)
        p.setFont(f)
        fm = p.fontMetrics()
        elided = fm.elidedText(text, Qt.ElideRight, int(r * 1.7))
        p.setPen(QPen(self._label_color))
        p.drawText(QRectF(cx - r, cy - fm.height() / 2.0, 2 * r, fm.height()),
                   Qt.AlignCenter, elided)

    def _paint_controls(self, p):
        w = 34.0
        x = self.width() - w - 12.0
        y = self.height() / 2.0 - w
        self._plus_rect = QRectF(x, y, w, w)
        self._minus_rect = QRectF(x, y + w, w, w)
        pill = QRectF(x, y, w, 2 * w)
        p.setPen(QPen(QColor(self._ctrl_color).darker(300)))
        bg = QColor(self._tip_bg); bg.setAlpha(210)
        p.setBrush(QBrush(bg))
        p.drawRoundedRect(pill, w / 2.0, w / 2.0)
        pen = QPen(self._ctrl_color, 2.0); pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        c1 = self._plus_rect.center(); c2 = self._minus_rect.center()
        p.drawLine(QPointF(c1.x() - 7, c1.y()), QPointF(c1.x() + 7, c1.y()))
        p.drawLine(QPointF(c1.x(), c1.y() - 7), QPointF(c1.x(), c1.y() + 7))
        p.drawLine(QPointF(c2.x() - 7, c2.y()), QPointF(c2.x() + 7, c2.y()))
        # search button below the zoom pill
        self._search_rect = QRectF(x, y + 2 * w + 10, w, w)
        p.setPen(QPen(QColor(self._ctrl_color).darker(300)))
        p.setBrush(QBrush(bg))
        p.drawEllipse(self._search_rect)
        sc = self._search_rect.center()
        pen2 = QPen(self._ctrl_color, 2.0); pen2.setCapStyle(Qt.RoundCap)
        p.setPen(pen2); p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(sc.x() - 2, sc.y() - 2), 5.5, 5.5)
        p.drawLine(QPointF(sc.x() + 2.2, sc.y() + 2.2), QPointF(sc.x() + 7, sc.y() + 7))

    def _paint_tooltip(self, p):
        _, cx, cy, r, _ = self._screen[self._hover]
        n = self._nodes[self._hover]
        tf = QFont(self.font()); tf.setBold(True); tf.setPointSizeF(max(9.0, self.font().pointSizeF()))
        sf = QFont(self.font()); sf.setPointSizeF(max(8.0, self.font().pointSizeF() * 0.86))
        fm, fms = QFontMetrics(tf), QFontMetrics(sf)
        cat = n.get("cat", "")
        sub = "%g%s" % (n["val"], "  ·  " + cat if cat and cat != "default" else "")
        padx, pady, dot = 12.0, 9.0, 9.0
        tw = max(fm.horizontalAdvance(n["label"]), fms.horizontalAdvance(sub))
        cw = dot + 8 + tw + 2 * padx
        ch = fm.height() + fms.height() + 2 * pady + 2
        tx = min(max(8.0, cx - cw / 2.0), self.width() - cw - 8.0)
        ty = cy - r - ch - 10.0
        if ty < 6:
            ty = cy + r + 10.0
        card = QRectF(tx, ty, cw, ch)
        path = QPainterPath(); path.addRoundedRect(card, 10, 10)
        p.setPen(QPen(QColor(255, 255, 255, 28)))
        p.setBrush(QBrush(self._tip_bg))
        p.drawPath(path)
        dcx = tx + padx + dot / 2.0
        p.setPen(Qt.NoPen); p.setBrush(QBrush(self._cat_color(cat)))
        p.drawEllipse(QPointF(dcx, ty + pady + fm.height() * 0.5), dot / 2.0, dot / 2.0)
        text_x = tx + padx + dot + 8
        p.setFont(tf); p.setPen(QPen(QColor("#ffffff")))
        p.drawText(QRectF(text_x, ty + pady, tw, fm.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, n["label"])
        p.setFont(sf); p.setPen(QPen(QColor("#aab2bd")))
        p.drawText(QRectF(text_x, ty + pady + fm.height() + 2, tw, fms.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, sub)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def _bubble_at(self, pos):
        for i in range(len(self._screen) - 1, -1, -1):
            _, cx, cy, r, _ = self._screen[i]
            if math.hypot(pos.x() - cx, pos.y() - cy) <= r:
                return i
        return -1

    def mousePressEvent(self, e):
        if e.button() != Qt.LeftButton:
            return super().mousePressEvent(e)
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        if self._show_controls and self._zoomable:
            if self._plus_rect.contains(pos):
                return self.zoomIn()
            if self._minus_rect.contains(pos):
                return self.zoomOut()
            if self._search_rect.contains(pos):
                return self.searchRequested.emit()
        self._drag_from = pos
        self._dragged = False
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        if self._drag_from is not None and (e.buttons() & Qt.LeftButton):
            delta = pos - self._drag_from
            if self._zoomable and (self._dragged or delta.manhattanLength() > 4):
                self._dragged = True
                self._pan += delta
                self._drag_from = pos
                self.update()
                return
        i = self._bubble_at(pos)
        if i != self._hover:
            self._hover = i
            self._grow = 1.0 if i >= 0 else self._grow
            self._start_hover_anim()
            self.update()
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
        if e.button() == Qt.LeftButton and self._drag_from is not None and not self._dragged:
            i = self._bubble_at(pos)
            if i >= 0:
                self.bubbleClicked.emit(self._screen[i][0])
        self._drag_from = None
        self._dragged = False
        super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self._zoomable:
            self.resetView()
        super().mouseDoubleClickEvent(e)

    def wheelEvent(self, e):
        if not self._zoomable:
            return super().wheelEvent(e)
        d = e.angleDelta().y()
        if d:
            pos = e.position() if hasattr(e, "position") else QPointF(e.pos())
            self._zoom_to(self._zoom * (1.15 if d > 0 else 1 / 1.15), pos)
            e.accept()

    def leaveEvent(self, e):
        if self._hover != -1:
            self._hover = -1
            self._start_hover_anim()
            self.update()
        super().leaveEvent(e)

    def _start_hover_anim(self):
        if self._hover_timer is None:
            self._hover_timer = QTimer(self)
            self._hover_timer.setInterval(16)
            self._hover_timer.timeout.connect(self._hover_tick)
        self._hover_timer.start()

    def _hover_tick(self):
        target = self._hover_scale if self._hover >= 0 else 1.0
        self._grow += (target - self._grow) * 0.28
        if abs(self._grow - target) < 0.004:
            self._grow = target
            if target == 1.0:
                self._hover_timer.stop()
        self.update()

    def resizeEvent(self, e):
        self.update()
        super().resizeEvent(e)

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

    @Property(str)
    def categoriesJson(self):
        return json.dumps(self._cats)

    @categoriesJson.setter
    def categoriesJson(self, text):
        try:
            data = json.loads(text) if str(text).strip() else {}
            if isinstance(data, dict):
                self.setCategoryColors(data)
        except Exception:
            pass

    @Property(float)
    def padding(self):
        return self._pad

    @padding.setter
    def padding(self, v):
        self._pad = max(0.0, float(v)); self._pack(); self.update()

    @Property(bool)
    def showLabels(self):
        return self._show_labels

    @showLabels.setter
    def showLabels(self, v):
        self._show_labels = bool(v); self.update()

    @Property(float)
    def minLabelRadius(self):
        return self._min_label_r

    @minLabelRadius.setter
    def minLabelRadius(self, v):
        self._min_label_r = max(0.0, float(v)); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._label_color

    @labelColor.setter
    def labelColor(self, c):
        self._label_color = QColor(c); self.update()

    @Property(QColor)
    def defaultColor(self):
        return self._default_color

    @defaultColor.setter
    def defaultColor(self, c):
        self._default_color = QColor(c); self.update()

    @Property(float)
    def shadeVariation(self):
        return self._shade

    @shadeVariation.setter
    def shadeVariation(self, v):
        self._shade = max(0.0, min(1.0, float(v))); self.update()

    @Property(bool)
    def hoverGlow(self):
        return self._hover_glow

    @hoverGlow.setter
    def hoverGlow(self, v):
        self._hover_glow = bool(v); self.update()

    @Property(float)
    def hoverScale(self):
        return self._hover_scale

    @hoverScale.setter
    def hoverScale(self, v):
        self._hover_scale = max(1.0, float(v))

    @Property(bool)
    def groupByCategory(self):
        return self._group

    @groupByCategory.setter
    def groupByCategory(self, v):
        self._group = bool(v); self._pack(); self.update()

    @Property(bool)
    def zoomable(self):
        return self._zoomable

    @zoomable.setter
    def zoomable(self, v):
        self._zoomable = bool(v); self.update()

    @Property(bool)
    def showControls(self):
        return self._show_controls

    @showControls.setter
    def showControls(self, v):
        self._show_controls = bool(v); self.update()

    @Property(str)
    def searchQuery(self):
        return self._search

    @searchQuery.setter
    def searchQuery(self, v):
        self.setSearchQuery(v)

    @Property(bool)
    def tooltips(self):
        return self._tooltips

    @tooltips.setter
    def tooltips(self, v):
        self._tooltips = bool(v); self.update()

    @Property(QColor)
    def tooltipBgColor(self):
        return self._tip_bg

    @tooltipBgColor.setter
    def tooltipBgColor(self, c):
        self._tip_bg = QColor(c); self.update()

    @Property(QColor)
    def controlColor(self):
        return self._ctrl_color

    @controlColor.setter
    def controlColor(self, c):
        self._ctrl_color = QColor(c); self.update()
