########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomSankey - a painted Sankey flow diagram.
##
## Nodes in columns joined by ribbons whose thickness is the quantity flowing.
## Energy budgets, traffic sources to conversions, spend breakdowns - anything
## where the interesting thing is where the volume GOES, not just its size.
##
## The hardest of the painted charts, because nothing about the layout is
## given: node columns, vertical order, and the stacking of each ribbon at
## both ends all have to be derived from the link list alone.
##
## QPainter only, NO QtCharts (see docs/design/mui-charts-gap.md).
##
## Data goes in with setLinks([...]) in code, or linksCsv in Qt Designer:
##
##     linksCsv = "Search>Signup=120;Social>Signup=80;Signup>Paid=60"
##                 source > target = value, links separated by ";"
##
## Emits linkHovered(int), nodeHovered(str) and nodeClicked(str).
########################################################################
from qtpy.QtCore import Qt, Signal, Property, QRectF, QSize, QPointF
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QPainterPath,
                        QFontMetrics, QLinearGradient)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomSankey(QWidget):
    linkHovered = Signal(int)
    nodeHovered = Signal(str)
    nodeClicked = Signal(str)

    WIDGET_ICON = "components/icons/account_tree.png"
    WIDGET_TOOLTIP = "A painted Sankey flow diagram"
    WIDGET_MODULE = "Custom_Widgets.QCustomSankey"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSankey' name='customSankey'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>480</width><height>320</height></rect></property>
            <property name='linksCsv'><string>Search&gt;Signup=120;Social&gt;Signup=80;Signup&gt;Paid=60;Signup&gt;Churn=140</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSankey",
        "props": {"linksCsv": {"type": "string", "default": ""},
                  "nodeColorsCsv": {"type": "string", "default": ""},
                  "nodeWidth": {"type": "int", "default": 14},
                  "nodePadding": {"type": "int", "default": 12},
                  "linkOpacity": {"type": "float", "default": 0.4},
                  "curvature": {"type": "float", "default": 0.5},
                  "showLabels": {"type": "bool", "default": True},
                  "showValues": {"type": "bool", "default": False},
                  "labelColor": {"type": "color", "default": "#0f172a"}},
        "signals": ["linkHovered", "nodeHovered", "nodeClicked"],
        "tokens_used": ["accent", "on-surface", "outline"],
    }

    _DEFAULT_COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed",
                       "#0891b2", "#db2777", "#65a30d"]
    _PAD = 8.0

    def __init__(self, parent=None, links=None):
        super().__init__(parent)
        self.setObjectName("QCustomSankey")
        self._links = []            # list of (source, target, value)
        self._nodeColors = {}
        self._nodeWidth = 14
        self._nodePadding = 12
        self._linkOpacity = 0.4
        self._curvature = 0.5
        self._showLabels = True
        self._showValues = False
        self._hoverLink = -1
        self._hoverNode = ""
        self._nodeRects = {}        # name -> QRectF
        self._ribbons = []          # per-link QPainterPath

        self._labelColor = QColor("#0f172a")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        if links:
            self.setLinks(links)

    # ------------------------------------------------------------------ #
    ## Data
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(link):
        if isinstance(link, dict):
            source, target, value = (link.get("source"), link.get("target"),
                                     link.get("value"))
        elif isinstance(link, (tuple, list)) and len(link) >= 3:
            source, target, value = link[0], link[1], link[2]
        else:
            return None
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None
        source, target = str(source or ""), str(target or "")
        if not source or not target or source == target or value <= 0:
            return None
        return (source, target, value)

    def setLinks(self, links):
        """Replace every link. Self-loops, zero flows and unnamed ends are
        dropped: none of them can be laid out, and keeping them would put a
        ribbon of nowhere-to-nowhere in the diagram."""
        self._links = [l for l in (self._coerce(x) for x in (links or [])) if l]
        self._hoverLink = -1
        self._hoverNode = ""
        self.update()

    def links(self):
        return list(self._links)

    def linkCount(self):
        return len(self._links)

    def clearLinks(self):
        self._links = []
        self._hoverLink = -1
        self._hoverNode = ""
        self.update()

    def nodes(self):
        """Every node name, in first-seen order."""
        seen, out = set(), []
        for source, target, _v in self._links:
            for name in (source, target):
                if name not in seen:
                    seen.add(name)
                    out.append(name)
        return out

    def nodeDepth(self, name):
        """Column index: the longest path from any source-only node.

        Longest, not shortest — a node fed by both a 1-hop and a 3-hop path
        must sit after both, or its ribbons run backwards.
        """
        depths = self.nodeDepths()
        return depths.get(name, 0)

    def nodeDepths(self):
        names = self.nodes()
        depths = {name: 0 for name in names}
        # Relax repeatedly; bounded by node count so a cycle cannot spin.
        for _round in range(len(names)):
            changed = False
            for source, target, _v in self._links:
                candidate = depths[source] + 1
                if candidate > depths[target]:
                    depths[target] = candidate
                    changed = True
            if not changed:
                break
        return depths

    def nodeValue(self, name):
        """Throughput: the larger of what flows in and what flows out."""
        incoming = sum(v for _s, t, v in self._links if t == name)
        outgoing = sum(v for s, _t, v in self._links if s == name)
        return max(incoming, outgoing)

    def columns(self):
        """[[node, ...], ...] left to right."""
        depths = self.nodeDepths()
        if not depths:
            return []
        out = [[] for _ in range(max(depths.values()) + 1)]
        for name in self.nodes():
            out[depths[name]].append(name)
        return out

    def nodeColor(self, name):
        if name in self._nodeColors:
            return QColor(self._nodeColors[name])
        order = self.nodes()
        index = order.index(name) if name in order else 0
        return QColor(self._DEFAULT_COLORS[index % len(self._DEFAULT_COLORS)])

    # ------------------------------------------------------------------ #
    ## Layout
    # ------------------------------------------------------------------ #
    def sizeHint(self):
        return QSize(480, 320)

    def minimumSizeHint(self):
        return QSize(180, 140)

    def _plotRect(self):
        """Reserve label room on BOTH sides.

        Labels sit left of a node unless it is a sink, so insetting only the
        right edge pushed every left-column label off-screen — "Search"
        rendered as a stray "h".
        """
        inset = self._PAD
        if self._showLabels:
            fm = QFontMetrics(self.font())
            widest = max((fm.horizontalAdvance(self._labelTextFor(n))
                          for n in self.nodes()), default=0)
            inset += widest + 9
        return QRectF(inset, self._PAD,
                      max(1.0, self.width() - 2 * inset),
                      max(1.0, self.height() - 2 * self._PAD))

    def _labelTextFor(self, name):
        if self._showValues:
            return "%s  %g" % (name, self.nodeValue(name))
        return name

    def isSink(self, name):
        """True when nothing flows out of a node."""
        return not any(s == name for s, _t, _v in self._links)

    def _computeLayout(self):
        """Node rectangles, then ribbon paths stacked at both ends."""
        self._nodeRects = {}
        self._ribbons = []
        columns = self.columns()
        if not columns:
            return
        rect = self._plotRect()
        colCount = len(columns)
        gap = ((rect.width() - self._nodeWidth) / (colCount - 1)
               if colCount > 1 else 0.0)

        # Scale so the busiest column exactly fills the height.
        scale = None
        for column in columns:
            total = sum(self.nodeValue(n) for n in column)
            padding = self._nodePadding * max(0, len(column) - 1)
            usable = max(1.0, rect.height() - padding)
            if total > 0:
                candidate = usable / total
                scale = candidate if scale is None else min(scale, candidate)
        scale = scale or 1.0

        for ci, column in enumerate(columns):
            heights = [max(1.0, self.nodeValue(n) * scale) for n in column]
            used = sum(heights) + self._nodePadding * max(0, len(column) - 1)
            y = rect.top() + (rect.height() - used) / 2.0
            x = rect.left() + ci * gap
            for name, height in zip(column, heights):
                self._nodeRects[name] = QRectF(x, y, float(self._nodeWidth), height)
                y += height + self._nodePadding

        self._computeRibbons(scale)

    def _computeRibbons(self, scale):
        """Stack each node's links in a stable order at both ends.

        Sorting by the other end's vertical position keeps ribbons from
        crossing more than the data forces them to.
        """
        outOffsets = {name: 0.0 for name in self._nodeRects}
        inOffsets = {name: 0.0 for name in self._nodeRects}

        def targetY(link):
            rect = self._nodeRects.get(link[1])
            return rect.top() if rect else 0.0

        def sourceY(link):
            rect = self._nodeRects.get(link[0])
            return rect.top() if rect else 0.0

        order = sorted(range(len(self._links)),
                       key=lambda i: (sourceY(self._links[i]),
                                      targetY(self._links[i])))
        placement = {}
        for i in order:
            source, target, value = self._links[i]
            if source not in self._nodeRects or target not in self._nodeRects:
                continue
            thickness = max(1.0, value * scale)
            srcRect = self._nodeRects[source]
            dstRect = self._nodeRects[target]
            y0 = srcRect.top() + outOffsets[source]
            y1 = dstRect.top() + inOffsets[target]
            outOffsets[source] += thickness
            inOffsets[target] += thickness
            placement[i] = (srcRect.right(), y0, dstRect.left(), y1, thickness)

        self._ribbons = []
        for i in range(len(self._links)):
            if i not in placement:
                self._ribbons.append(QPainterPath())
                continue
            x0, y0, x1, y1, thickness = placement[i]
            self._ribbons.append(self._ribbonPath(x0, y0, x1, y1, thickness))

    def _ribbonPath(self, x0, y0, x1, y1, thickness):
        """A closed cubic band from (x0, y0) to (x1, y1)."""
        bend = (x1 - x0) * max(0.0, min(1.0, self._curvature))
        path = QPainterPath()
        path.moveTo(x0, y0)
        path.cubicTo(x0 + bend, y0, x1 - bend, y1, x1, y1)
        path.lineTo(x1, y1 + thickness)
        path.cubicTo(x1 - bend, y1 + thickness, x0 + bend, y0 + thickness,
                     x0, y0 + thickness)
        path.closeSubpath()
        return path

    def nodeRects(self):
        if not self._nodeRects:
            self._computeLayout()
        return dict(self._nodeRects)

    def ribbons(self):
        if not self._ribbons:
            self._computeLayout()
        return list(self._ribbons)

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(self.font())
        self._computeLayout()
        if not self._nodeRects:
            return

        for index, path in enumerate(self._ribbons):
            if path.isEmpty():
                continue
            source, target, _value = self._links[index]
            hovered = index == self._hoverLink or self._hoverNode in (source, target)
            gradient = QLinearGradient(self._nodeRects[source].right(), 0,
                                       self._nodeRects[target].left(), 0)
            start = QColor(self.nodeColor(source))
            stop = QColor(self.nodeColor(target))
            alpha = min(1.0, self._linkOpacity * (1.8 if hovered else 1.0))
            start.setAlphaF(alpha)
            stop.setAlphaF(alpha)
            gradient.setColorAt(0.0, start)
            gradient.setColorAt(1.0, stop)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(gradient))
            p.drawPath(path)

        for name, rect in self._nodeRects.items():
            colour = self.nodeColor(name)
            if name == self._hoverNode:
                colour = colour.lighter(115)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(colour))
            p.drawRect(rect)

        if self._showLabels:
            self._paintLabels(p)

    def _paintLabels(self, p):
        fm = QFontMetrics(self.font())
        p.setPen(QPen(self._labelColor))
        for name, rect in self._nodeRects.items():
            text = self._labelTextFor(name)
            width = fm.horizontalAdvance(text)
            # Sinks label to the right, everything else to the left, so a
            # label never sits on top of the ribbons leaving its node. Keyed
            # on "has no outgoing links", not on being in the last column: a
            # dead end partway through is still a sink.
            if self.isSink(name):
                box = QRectF(rect.right() + 5, rect.center().y() - fm.height() / 2.0,
                             width + 4, fm.height())
                align = Qt.AlignLeft
            else:
                box = QRectF(rect.left() - width - 9,
                             rect.center().y() - fm.height() / 2.0,
                             width + 4, fm.height())
                align = Qt.AlignRight
            p.drawText(box, int(align | Qt.AlignVCenter), text)

    # ------------------------------------------------------------------ #
    ## Interaction
    # ------------------------------------------------------------------ #
    def nodeAt(self, pos):
        point = QPointF(pos)
        for name, rect in self.nodeRects().items():
            if rect.adjusted(-2, -2, 2, 2).contains(point):
                return name
        return ""

    def linkAt(self, pos):
        point = QPointF(pos)
        for index in range(len(self._ribbons) - 1, -1, -1):
            if self._ribbons[index].contains(point):
                return index
        return -1

    def mouseMoveEvent(self, e):
        node = self.nodeAt(e.pos())
        link = -1 if node else self.linkAt(e.pos())
        if node != self._hoverNode:
            self._hoverNode = node
            self.nodeHovered.emit(node)
            self.update()
        if link != self._hoverLink:
            self._hoverLink = link
            self.linkHovered.emit(link)
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        if self._hoverNode:
            self._hoverNode = ""
            self.nodeHovered.emit("")
        if self._hoverLink != -1:
            self._hoverLink = -1
            self.linkHovered.emit(-1)
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            name = self.nodeAt(e.pos())
            if name:
                self.nodeClicked.emit(name)
        super().mouseReleaseEvent(e)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def linksCsv(self):
        return ";".join("%s>%s=%g" % (s, t, v) for s, t, v in self._links)

    @linksCsv.setter
    def linksCsv(self, text):
        links = []
        for chunk in str(text).replace("|", ";").split(";"):
            chunk = chunk.strip()
            if not chunk or ">" not in chunk or "=" not in chunk:
                continue
            pair, _, raw = chunk.partition("=")
            source, _, target = pair.partition(">")
            coerced = self._coerce((source.strip(), target.strip(), raw.strip()))
            if coerced:
                links.append(coerced)
        self.setLinks(links)

    @Property(str)
    def nodeColorsCsv(self):
        return ",".join("%s=%s" % (name, colour.name())
                        for name, colour in self._nodeColors.items())

    @nodeColorsCsv.setter
    def nodeColorsCsv(self, text):
        colors = {}
        for chunk in str(text).replace(";", ",").split(","):
            chunk = chunk.strip()
            if "=" not in chunk:
                continue
            name, _, raw = chunk.partition("=")
            colour = QColor(raw.strip())
            if name.strip() and colour.isValid():
                colors[name.strip()] = colour
        self._nodeColors = colors
        self.update()

    @Property(int)
    def nodeWidth(self):
        return self._nodeWidth

    @nodeWidth.setter
    def nodeWidth(self, value):
        self._nodeWidth = max(2, int(value)); self.update()

    @Property(int)
    def nodePadding(self):
        return self._nodePadding

    @nodePadding.setter
    def nodePadding(self, value):
        self._nodePadding = max(0, int(value)); self.update()

    @Property(float)
    def linkOpacity(self):
        return self._linkOpacity

    @linkOpacity.setter
    def linkOpacity(self, value):
        self._linkOpacity = max(0.0, min(1.0, float(value))); self.update()

    @Property(float)
    def curvature(self):
        return self._curvature

    @curvature.setter
    def curvature(self, value):
        self._curvature = max(0.0, min(1.0, float(value))); self.update()

    @Property(bool)
    def showLabels(self):
        return self._showLabels

    @showLabels.setter
    def showLabels(self, value):
        self._showLabels = bool(value); self.update()

    @Property(bool)
    def showValues(self):
        return self._showValues

    @showValues.setter
    def showValues(self, value):
        self._showValues = bool(value); self.update()

    @Property(QColor)
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, c):
        self._labelColor = QColor(c); self.update()
