########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomNodeGraph - a node-based visual editor canvas.
##
## An infinite, pan/zoom canvas with a dotted-grid backdrop that hosts
## draggable NODE cards. Each node has a titled header (accent dot), a body of
## painted content (freeform text, label/value rows, an image thumbnail, or
## chips) and typed input/output PORTS (the socket dots). Drag from an output
## port to an input port to wire nodes together with a curved bezier CABLE.
##
## Everything is painted with QPainter (crisp at any zoom, no assets) and every
## colour is a qproperty, so the whole graph recolours on a theme switch. It is
## data-driven: build a graph declaratively with addNode()/addEdge() or
## setGraph({...}); read interaction back through nodeMoved / nodeSelected /
## connectionMade / nodeClicked / canvasClicked.
##
## This is the headline "flow builder / pipeline / AI graph" surface — the
## SETTINGS/IDEAS/REFERENCES/AI-MODELS canvas in node-based creative tools.
########################################################################
import os
import math

from qtpy.QtCore import Qt, Property, QRectF, QPointF, QByteArray, QSize, Signal, QTimer
from qtpy.QtGui import (QColor, QPainter, QBrush, QPen, QFont, QPainterPath,
                        QLinearGradient, QPixmap)
from qtpy.QtWidgets import QWidget, QSizePolicy

try:
    from qtpy.QtSvg import QSvgRenderer
except Exception:
    QSvgRenderer = None


class _Node:
    """Plain data holder for one node card (world coordinates)."""

    __slots__ = ("id", "title", "x", "y", "w", "h", "accent", "text",
                 "rows", "image", "chips", "inputs", "outputs")

    def __init__(self, nid, title="Node", x=0.0, y=0.0, w=200.0, h=120.0,
                 accent="#f2a63b", text="", rows=None, image="", chips=None,
                 inputs=None, outputs=None):
        self.id = nid
        self.title = title
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.accent = QColor(accent)
        self.text = text or ""
        self.rows = list(rows or [])      # [{"label":..,"value":..,"dot":color}]
        self.image = image or ""          # path to a thumbnail
        self.chips = list(chips or [])    # ["Gemini", "Seedance2"]
        self.inputs = list(inputs or [])  # port labels
        self.outputs = list(outputs or [])


class _Edge:
    __slots__ = ("src", "src_port", "dst", "dst_port", "color")

    def __init__(self, src, src_port, dst, dst_port, color=None):
        self.src = src
        self.src_port = int(src_port)
        self.dst = dst
        self.dst_port = int(dst_port)
        self.color = QColor(color) if color else None


class QCustomNodeGraph(QWidget):

    WIDGET_ICON = "components/icons/account_tree.png"
    WIDGET_TOOLTIP = "A node-based visual editor canvas (pan/zoom, draggable nodes, bezier wires)"
    WIDGET_MODULE = "Custom_Widgets.QCustomNodeGraph"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomNodeGraph' name='customNodeGraph'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>640</width><height>420</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomNodeGraph",
        "props": {"bgColor": {"type": "color", "default": "#12141c"},
                  "gridColor": {"type": "color", "default": "#26ffffff"},
                  "gridSpacing": {"type": "int", "default": 26},
                  "nodeColor": {"type": "color", "default": "#1b1e2a"},
                  "nodeHeaderColor": {"type": "color", "default": "#232634"},
                  "nodeBorderColor": {"type": "color", "default": "#33ffffff"},
                  "textColor": {"type": "color", "default": "#e7e9f3"},
                  "mutedColor": {"type": "color", "default": "#8b90a6"},
                  "portColor": {"type": "color", "default": "#f2a63b"},
                  "edgeColor": {"type": "color", "default": "#c98a3a"},
                  "selectedColor": {"type": "color", "default": "#6c7bff"},
                  "cornerRadius": {"type": "int", "default": 14},
                  "animated": {"type": "bool", "default": True}},
        "signals": ["nodeMoved", "nodeSelected", "nodeClicked",
                    "connectionMade", "canvasClicked", "rowClicked"],
        "tokens_used": ["accent", "background"],
    }
    # Every configurable property is exposed to Qt Designer (the @Property below
    # auto-appears in the property editor; these give the Custom-Properties dock
    # its typed editors, grouped).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "bgColor", "kind": "color", "group": "Canvas"},
        {"name": "gridColor", "kind": "color", "group": "Canvas"},
        {"name": "gridSpacing", "kind": "int", "group": "Canvas"},
        {"name": "nodeColor", "kind": "color", "group": "Node"},
        {"name": "nodeHeaderColor", "kind": "color", "group": "Node"},
        {"name": "nodeBorderColor", "kind": "color", "group": "Node"},
        {"name": "textColor", "kind": "color", "group": "Node"},
        {"name": "mutedColor", "kind": "color", "group": "Node"},
        {"name": "cornerRadius", "kind": "int", "group": "Node"},
        {"name": "portColor", "kind": "color", "group": "Wiring"},
        {"name": "edgeColor", "kind": "color", "group": "Wiring"},
        {"name": "selectedColor", "kind": "color", "group": "Wiring"},
        {"name": "animated", "kind": "bool", "group": "Canvas"},
    ]

    nodeMoved = Signal(str)
    nodeSelected = Signal(str)
    nodeClicked = Signal(str)
    connectionMade = Signal(str, int, str, int)
    canvasClicked = Signal()
    rowClicked = Signal(str, int)     # (node_id, row_index) — a settings row tap

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomNodeGraph")
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(240, 180)

        # colours
        self._bg = QColor("#12141c")
        self._grid = QColor(255, 255, 255, 38)
        self._grid_spacing = 26
        self._node = QColor("#1b1e2a")
        self._node_header = QColor("#232634")
        self._node_border = QColor(255, 255, 255, 51)
        self._text = QColor("#e7e9f3")
        self._muted = QColor("#8b90a6")
        self._port = QColor("#f2a63b")
        self._edge = QColor("#c98a3a")
        self._selected = QColor("#6c7bff")
        self._radius = 14

        # model
        self._nodes = []          # list[_Node]
        self._edges = []          # list[_Edge]
        self._auto = 0            # auto id counter
        self._pix_cache = {}

        # view transform (world -> screen: p*scale + offset)
        self._scale = 1.0
        self._offset = QPointF(0.0, 0.0)

        # interaction state
        self._sel = None          # selected node id
        self._drag_node = None    # node being dragged
        self._drag_dx = 0.0
        self._drag_dy = 0.0
        self._panning = False
        self._pan_start = QPointF()
        self._pan_off0 = QPointF()
        self._connect_from = None  # (node_id, port_index) while wiring
        self._cursor = QPointF()
        self._press_node = None    # node id pressed (for click-vs-drag)
        self._press_row = None     # row index under the press, if any
        self._did_move = False     # became a drag?
        self._hover = None         # node id currently hovered

        # animation: a phase drives a bright pulse flowing along each cable, and
        # hovered/selected nodes get an animated glow (animated content).
        self._phase = 0.0
        self._animated = True
        self._anim = QTimer(self)
        self._anim.setInterval(40)
        self._anim.timeout.connect(self._tick)
        self._anim.start()

    def _tick(self):
        if not self._animated or not self.isVisible():
            return
        self._phase = (self._phase + 0.012) % 1.0
        if self._edges or self._hover or self._sel:
            self.update()

    # ------------------------------------------------------------------ #
    ## Public data API
    # ------------------------------------------------------------------ #
    def addNode(self, title="Node", x=0.0, y=0.0, w=200.0, h=120.0,
                accent="#f2a63b", text="", rows=None, image="", chips=None,
                inputs=None, outputs=None, nid=None):
        if nid is None:
            self._auto += 1
            nid = "node%d" % self._auto
        node = _Node(nid, title, x, y, w, h, accent, text, rows, image,
                     chips, inputs, outputs)
        self._nodes.append(node)
        self.update()
        return nid

    def addEdge(self, src, src_port, dst, dst_port, color=None):
        self._edges.append(_Edge(src, src_port, dst, dst_port, color))
        self.update()

    def clear(self):
        self._nodes = []
        self._edges = []
        self._sel = None
        self._auto = 0
        self.update()

    def setGraph(self, data):
        """data = {"nodes":[{...}], "edges":[{"src","srcPort","dst","dstPort","color"}]}."""
        self.clear()
        for n in (data or {}).get("nodes", []):
            self.addNode(**n)
        for e in (data or {}).get("edges", []):
            self.addEdge(e.get("src"), e.get("srcPort", 0),
                         e.get("dst"), e.get("dstPort", 0), e.get("color"))

    def nodeById(self, nid):
        for n in self._nodes:
            if n.id == nid:
                return n
        return None

    def setNodePosition(self, nid, x, y):
        n = self.nodeById(nid)
        if n:
            n.x, n.y = float(x), float(y)
            self.update()

    def nodeRows(self, nid):
        n = self.nodeById(nid)
        return list(n.rows) if n else []

    def setRowValue(self, nid, idx, value):
        n = self.nodeById(nid)
        if n and 0 <= idx < len(n.rows):
            n.rows[idx]["value"] = str(value)
            self.update()

    def fitToView(self, margin=40):
        if not self._nodes:
            return
        xs0 = min(n.x for n in self._nodes)
        ys0 = min(n.y for n in self._nodes)
        xs1 = max(n.x + n.w for n in self._nodes)
        ys1 = max(n.y + n.h for n in self._nodes)
        bw, bh = max(1.0, xs1 - xs0), max(1.0, ys1 - ys0)
        sx = (self.width() - 2 * margin) / bw
        sy = (self.height() - 2 * margin) / bh
        self._scale = max(0.25, min(2.0, min(sx, sy)))
        self._offset = QPointF(
            (self.width() - bw * self._scale) / 2.0 - xs0 * self._scale,
            (self.height() - bh * self._scale) / 2.0 - ys0 * self._scale)
        self.update()

    # ------------------------------------------------------------------ #
    ## Geometry helpers
    # ------------------------------------------------------------------ #
    def _w2s(self, x, y):
        return QPointF(x * self._scale + self._offset.x(),
                       y * self._scale + self._offset.y())

    def _s2w(self, pt):
        return QPointF((pt.x() - self._offset.x()) / self._scale,
                       (pt.y() - self._offset.y()) / self._scale)

    def _node_rect_screen(self, n):
        tl = self._w2s(n.x, n.y)
        return QRectF(tl.x(), tl.y(), n.w * self._scale, n.h * self._scale)

    def _port_pos(self, n, is_input, idx):
        """World-space centre of a port dot."""
        names = n.inputs if is_input else n.outputs
        count = max(1, len(names))
        header = 34.0
        avail = n.h - header
        gy = n.y + header + avail * (idx + 0.5) / count
        gx = n.x if is_input else n.x + n.w
        return QPointF(gx, gy)

    def _hit_port(self, screen_pt):
        """Return (node_id, is_input, idx) if a port is under the screen point."""
        r = 9.0
        for n in reversed(self._nodes):
            for is_in, names in ((True, n.inputs), (False, n.outputs)):
                for i in range(len(names)):
                    wp = self._port_pos(n, is_in, i)
                    sp = self._w2s(wp.x(), wp.y())
                    if (sp.x() - screen_pt.x()) ** 2 + (sp.y() - screen_pt.y()) ** 2 <= r * r:
                        return (n.id, is_in, i)
        return None

    def _hit_node(self, screen_pt):
        for n in reversed(self._nodes):
            if self._node_rect_screen(n).contains(screen_pt):
                return n
        return None

    def _row_at(self, node, screen_pt):
        """Index of the label/value row under the point, or None (rows nodes)."""
        if not node.rows:
            return None
        rect = self._node_rect_screen(node)
        sc = self._scale
        by = rect.y() + 34.0 * sc + 8 * sc
        rh = 30.0 * sc
        if screen_pt.x() < rect.left() or screen_pt.x() > rect.right():
            return None
        for i in range(len(node.rows)):
            ry = by + i * rh
            if ry <= screen_pt.y() <= ry + rh:
                return i
        return None

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), self._bg)
        self._paint_grid(p)
        for edge in self._edges:
            self._paint_edge(p, edge)
        if self._connect_from is not None:
            self._paint_pending_edge(p)
        for n in self._nodes:
            self._paint_node(p, n)
        p.end()

    def _paint_grid(self, p):
        step = self._grid_spacing * self._scale
        if step < 6:
            return
        p.setPen(Qt.NoPen)
        p.setBrush(self._grid)
        ox = self._offset.x() % step
        oy = self._offset.y() % step
        r = 1.3
        y = oy
        while y < self.height():
            x = ox
            while x < self.width():
                p.drawEllipse(QPointF(x, y), r, r)
                x += step
            y += step

    def _cable_path(self, a, b):
        dx = max(40.0, abs(b.x() - a.x()) * 0.5)
        path = QPainterPath(a)
        path.cubicTo(QPointF(a.x() + dx, a.y()),
                     QPointF(b.x() - dx, b.y()), b)
        return path

    def _paint_edge(self, p, edge):
        ns = self.nodeById(edge.src)
        nd = self.nodeById(edge.dst)
        if ns is None or nd is None:
            return
        aw = self._port_pos(ns, False, edge.src_port)
        bw = self._port_pos(nd, True, edge.dst_port)
        a = self._w2s(aw.x(), aw.y())
        b = self._w2s(bw.x(), bw.y())
        col = edge.color or self._edge
        pen = QPen(col, max(1.6, 2.2 * self._scale))
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        path = self._cable_path(a, b)
        p.drawPath(path)
        # a bright pulse flowing along the cable (animated "energy")
        if self._animated:
            off = (self._phase + 0.13 * (hash(edge.src) % 7)) % 1.0
            pt = path.pointAtPercent(off)
            glow = QColor(col).lighter(170)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(glow.red(), glow.green(), glow.blue(), 80))
            p.drawEllipse(pt, 5 * self._scale, 5 * self._scale)
            p.setBrush(glow)
            p.drawEllipse(pt, 2.3 * self._scale, 2.3 * self._scale)

    def _paint_pending_edge(self, p):
        nid, is_in, idx = self._connect_from
        n = self.nodeById(nid)
        if n is None:
            return
        aw = self._port_pos(n, is_in, idx)
        a = self._w2s(aw.x(), aw.y())
        b = self._cursor
        pen = QPen(self._port, 2.0, Qt.DashLine)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        if is_in:
            a, b = b, a
        p.drawPath(self._cable_path(a, b))

    def _paint_node(self, p, n):
        rect = self._node_rect_screen(n)
        r = self._radius * self._scale
        selected = (n.id == self._sel)

        # animated glow ring on the hovered / selected node
        if self._animated and (selected or n.id == self._hover):
            pulse = 0.5 + 0.5 * math.sin(self._phase * 2 * math.pi)
            g = self._selected if selected else self._port
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(g.red(), g.green(), g.blue(), int(34 + 46 * pulse)))
            p.drawRoundedRect(rect.adjusted(-5, -5, 5, 6), r + 5, r + 5)

        # drop shadow
        sh = QColor(0, 0, 0, 90)
        p.setPen(Qt.NoPen)
        p.setBrush(sh)
        p.drawRoundedRect(rect.adjusted(0, 3, 0, 5), r, r)

        # body
        p.setBrush(self._node)
        pen = QPen(self._selected if selected else self._node_border,
                   2.0 if selected else 1.0)
        p.setPen(pen)
        p.drawRoundedRect(rect, r, r)

        # header strip
        hh = 34.0 * self._scale
        header = QRectF(rect.x(), rect.y(), rect.width(), hh)
        hp = QPainterPath()
        hp.addRoundedRect(header, r, r)
        hp.addRect(QRectF(rect.x(), rect.y() + hh - r, rect.width(), r))
        p.setPen(Qt.NoPen)
        p.setBrush(self._node_header)
        p.drawPath(hp.simplified())

        sc = self._scale
        # accent dot + title
        p.setBrush(n.accent)
        p.drawEllipse(QPointF(rect.x() + 15 * sc, rect.y() + hh / 2), 4 * sc, 4 * sc)
        f = QFont(self.font())
        f.setPointSizeF(max(6.0, 8.5 * sc))
        f.setBold(True)
        f.setCapitalization(QFont.AllUppercase)
        f.setLetterSpacing(QFont.PercentageSpacing, 108)
        p.setFont(f)
        p.setPen(QPen(self._muted))
        p.drawText(QRectF(rect.x() + 26 * sc, rect.y(), rect.width() - 40 * sc, hh),
                   Qt.AlignVCenter | Qt.AlignLeft, n.title)

        # body content
        p.setClipRect(rect)
        by = rect.y() + hh + 8 * sc
        bx = rect.x() + 14 * sc
        bw = rect.width() - 28 * sc

        if n.image:
            self._paint_node_image(p, n, QRectF(bx, by, bw, rect.bottom() - by - 12 * sc))
        elif n.text:
            tf = QFont(self.font())
            tf.setPointSizeF(max(6.0, 9.0 * sc))
            p.setFont(tf)
            p.setPen(QPen(self._text))
            p.drawText(QRectF(bx, by, bw, rect.bottom() - by - 8 * sc),
                       Qt.AlignTop | Qt.TextWordWrap, n.text)
        elif n.rows:
            self._paint_node_rows(p, n, rect, bx, by, bw, sc)
        elif n.chips:
            self._paint_node_chips(p, n, bx, by, bw, sc)
        p.setClipping(False)

        # ports
        self._paint_ports(p, n, sc)

    def _paint_node_rows(self, p, n, rect, bx, by, bw, sc):
        rh = 30.0 * sc
        f = QFont(self.font())
        f.setPointSizeF(max(6.0, 8.5 * sc))
        for i, row in enumerate(n.rows):
            ry = by + i * rh
            if ry > rect.bottom() - 6 * sc:
                break
            dot = row.get("dot")
            tx = bx
            if dot:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(dot))
                p.drawEllipse(QPointF(bx + 5 * sc, ry + rh / 2 - 2 * sc), 4 * sc, 4 * sc)
                tx = bx + 18 * sc
            p.setFont(f)
            p.setPen(QPen(self._muted))
            p.drawText(QRectF(tx, ry, bw * 0.5, rh - 6 * sc),
                       Qt.AlignVCenter | Qt.AlignLeft, str(row.get("label", "")))
            val = str(row.get("value", ""))
            if val:
                # value pill on the right
                vf = QFont(f)
                fm_w = p.fontMetrics().horizontalAdvance(val) + 22 * sc
                pill = QRectF(rect.right() - 14 * sc - fm_w, ry + 2 * sc,
                              fm_w, rh - 10 * sc)
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(255, 255, 255, 18))
                p.drawRoundedRect(pill, pill.height() / 2, pill.height() / 2)
                p.setFont(vf)
                p.setPen(QPen(self._text))
                p.drawText(pill, Qt.AlignCenter, val)

    def _paint_node_chips(self, p, n, bx, by, bw, sc):
        f = QFont(self.font())
        f.setPointSizeF(max(6.0, 8.5 * sc))
        f.setBold(True)
        p.setFont(f)
        x = bx
        y = by
        for label in n.chips:
            w = p.fontMetrics().horizontalAdvance(label) + 26 * sc
            h = 26 * sc
            if x + w > bx + bw:
                x = bx
                y += h + 8 * sc
            chip = QRectF(x, y, w, h)
            p.setPen(QPen(n.accent, 1.4))
            p.setBrush(QColor(n.accent.red(), n.accent.green(), n.accent.blue(), 30))
            p.drawRoundedRect(chip, h / 2, h / 2)
            p.setPen(QPen(self._text))
            p.drawText(chip, Qt.AlignCenter, label)
            x += w + 8 * sc

    def _paint_node_image(self, p, n, box):
        pm = self._image_pixmap(n.image)
        radius = 10 * self._scale
        path = QPainterPath()
        path.addRoundedRect(box, radius, radius)
        p.save()
        p.setClipPath(path)
        if pm is not None and not pm.isNull():
            scaled = pm.scaled(box.size().toSize(), Qt.KeepAspectRatioByExpanding,
                               Qt.SmoothTransformation)
            sx = (scaled.width() - box.width()) / 2
            sy = (scaled.height() - box.height()) / 2
            p.drawPixmap(box, scaled, QRectF(sx, sy, box.width(), box.height()))
        else:
            grad = QLinearGradient(box.topLeft(), box.bottomRight())
            grad.setColorAt(0.0, QColor("#2a2f45"))
            grad.setColorAt(1.0, QColor("#1a1d29"))
            p.fillRect(box, QBrush(grad))
        p.restore()
        p.setPen(QPen(self._node_border, 1.0))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

    def _paint_ports(self, p, n, sc):
        rr = 4.5 * sc
        for is_in, names in ((True, n.inputs), (False, n.outputs)):
            for i in range(len(names)):
                wp = self._port_pos(n, is_in, i)
                sp = self._w2s(wp.x(), wp.y())
                p.setPen(QPen(self._bg, 2.0))
                p.setBrush(self._port)
                p.drawEllipse(sp, rr, rr)

    def _image_pixmap(self, path):
        if path in self._pix_cache:
            return self._pix_cache[path]
        pm = None
        if path and os.path.exists(path):
            if path.lower().endswith(".svg") and QSvgRenderer is not None:
                pm = QPixmap(400, 400)
                pm.fill(QColor(0, 0, 0, 0))
                rnd = QSvgRenderer(path)
                pr = QPainter(pm)
                rnd.render(pr)
                pr.end()
            else:
                pm = QPixmap(path)
        self._pix_cache[path] = pm
        return pm

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def mousePressEvent(self, e):
        pt = QPointF(e.position()) if hasattr(e, "position") else QPointF(e.pos())
        self._cursor = pt
        if e.button() == Qt.LeftButton:
            hit = self._hit_port(pt)
            if hit is not None:
                self._connect_from = hit
                self.update()
                return
            n = self._hit_node(pt)
            if n is not None:
                # raise to top + select + start drag
                self._nodes.remove(n)
                self._nodes.append(n)
                self._sel = n.id
                self._drag_node = n
                wp = self._s2w(pt)
                self._drag_dx = wp.x() - n.x
                self._drag_dy = wp.y() - n.y
                self._press_node = n.id
                self._press_row = self._row_at(n, pt)
                self._did_move = False
                self.nodeSelected.emit(n.id)
                self.nodeClicked.emit(n.id)
                self.update()
                return
            # empty canvas -> pan
            self._sel = None
            self._panning = True
            self._pan_start = pt
            self._pan_off0 = QPointF(self._offset)
            self.canvasClicked.emit()
            self.setCursor(Qt.ClosedHandCursor)
            self.update()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        pt = QPointF(e.position()) if hasattr(e, "position") else QPointF(e.pos())
        self._cursor = pt
        if self._drag_node is not None:
            wp = self._s2w(pt)
            nx = wp.x() - self._drag_dx
            ny = wp.y() - self._drag_dy
            if abs(nx - self._drag_node.x) > 2 or abs(ny - self._drag_node.y) > 2:
                self._did_move = True
            self._drag_node.x = nx
            self._drag_node.y = ny
            self.update()
            return
        if self._panning:
            d = pt - self._pan_start
            self._offset = self._pan_off0 + d
            self.update()
            return
        if self._connect_from is not None:
            self.update()
            return
        # hover cursor feedback over ports + track hovered node for the glow
        hn = self._hit_node(pt)
        new_hover = hn.id if hn is not None else None
        if new_hover != self._hover:
            self._hover = new_hover
            self.update()
        if self._hit_port(pt) is not None:
            self.setCursor(Qt.CrossCursor)
        elif hn is not None:
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hover is not None:
            self._hover = None
            self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        pt = QPointF(e.position()) if hasattr(e, "position") else QPointF(e.pos())
        if self._drag_node is not None:
            if self._did_move:
                self.nodeMoved.emit(self._drag_node.id)
            elif self._press_row is not None:
                self.rowClicked.emit(self._press_node, self._press_row)
            self._drag_node = None
            self._press_row = None
        if self._panning:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        if self._connect_from is not None:
            target = self._hit_port(pt)
            if target is not None:
                (n0, in0, i0) = self._connect_from
                (n1, in1, i1) = target
                # connect an output to an input (either drag direction)
                if in0 != in1 and n0 != n1:
                    if in0:  # started on an input -> the other is the source
                        src, sp, dst, dp = n1, i1, n0, i0
                    else:
                        src, sp, dst, dp = n0, i0, n1, i1
                    self.addEdge(src, sp, dst, dp)
                    self.connectionMade.emit(src, sp, dst, dp)
            self._connect_from = None
            self.update()
        super().mouseReleaseEvent(e)

    def wheelEvent(self, e):
        delta = e.angleDelta().y()
        if delta == 0:
            return
        factor = 1.12 if delta > 0 else 1.0 / 1.12
        new_scale = max(0.3, min(2.5, self._scale * factor))
        # zoom about the cursor
        pt = QPointF(e.position()) if hasattr(e, "position") else QPointF(e.pos())
        before = self._s2w(pt)
        self._scale = new_scale
        after = self._w2s(before.x(), before.y())
        self._offset += (pt - after)
        self.update()

    def sizeHint(self):
        return QSize(640, 420)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(QColor)
    def bgColor(self):
        return self._bg

    @bgColor.setter
    def bgColor(self, c):
        self._bg = QColor(c)
        self.update()

    @Property(QColor)
    def gridColor(self):
        return self._grid

    @gridColor.setter
    def gridColor(self, c):
        self._grid = QColor(c)
        self.update()

    @Property(int)
    def gridSpacing(self):
        return self._grid_spacing

    @gridSpacing.setter
    def gridSpacing(self, v):
        self._grid_spacing = max(6, int(v))
        self.update()

    @Property(QColor)
    def nodeColor(self):
        return self._node

    @nodeColor.setter
    def nodeColor(self, c):
        self._node = QColor(c)
        self.update()

    @Property(QColor)
    def nodeHeaderColor(self):
        return self._node_header

    @nodeHeaderColor.setter
    def nodeHeaderColor(self, c):
        self._node_header = QColor(c)
        self.update()

    @Property(QColor)
    def nodeBorderColor(self):
        return self._node_border

    @nodeBorderColor.setter
    def nodeBorderColor(self, c):
        self._node_border = QColor(c)
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
    def portColor(self):
        return self._port

    @portColor.setter
    def portColor(self, c):
        self._port = QColor(c)
        self.update()

    @Property(QColor)
    def edgeColor(self):
        return self._edge

    @edgeColor.setter
    def edgeColor(self, c):
        self._edge = QColor(c)
        self.update()

    @Property(QColor)
    def selectedColor(self):
        return self._selected

    @selectedColor.setter
    def selectedColor(self, c):
        self._selected = QColor(c)
        self.update()

    @Property(int)
    def cornerRadius(self):
        return self._radius

    @cornerRadius.setter
    def cornerRadius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        self._animated = bool(v)
        if self._animated:
            self._anim.start()
        else:
            self._anim.stop()
        self.update()
