########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomSkeleton - a shimmering loading placeholder.
##
## A rounded shape (line / rect / circle) with a moving shimmer, shown while
## real content loads. Colours come from tokens via qproperty (baseColor /
## highlightColor set by skeleton_qss).
########################################################################
from qtpy.QtCore import Qt, QVariantAnimation, Property, QRectF
from qtpy.QtGui import QColor, QPainter, QLinearGradient, QBrush, QPainterPath
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomSkeleton(QWidget):
    WIDGET_ICON = "components/icons/skeleton.png"
    WIDGET_TOOLTIP = "A shimmering loading placeholder"
    WIDGET_MODULE = "Custom_Widgets.QCustomSkeleton"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSkeleton' name='customSkeleton'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>200</width><height>16</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomSkeleton",
        "props": {"shape": {"type": "enum", "values": ["line", "rect", "circle"],
                            "default": "line"}},
        "signals": [],
        "tokens_used": ["surface-muted", "surface"],
    }

    def __init__(self, parent=None, shape="line"):
        super().__init__(parent)
        self.setObjectName("QCustomSkeleton")
        self._shape = shape
        self._base = QColor("#e2e8f0")
        self._highlight = QColor("#f8fafc")
        self._t = 0.0
        self._applyShapeHints()

        self._anim = QVariantAnimation(self)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setDuration(1200)
        self._anim.setLoopCount(-1)
        self._anim.valueChanged.connect(self._onTick)
        self.start()

    def _applyShapeHints(self):
        if self._shape == "circle":
            self.setFixedSize(40, 40)
        elif self._shape == "line":
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.setFixedHeight(14)
        else:  # rect
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.setMinimumHeight(48)

    def _onTick(self, v):
        self._t = float(v)
        self.update()

    def start(self):
        self._anim.start()

    def stop(self):
        self._anim.stop()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        if self._shape == "circle":
            d = min(rect.width(), rect.height())
            c = rect.center()
            path.addEllipse(c, d / 2, d / 2)
        else:
            radius = min(7.0, rect.height() / 2) if self._shape == "line" else 8.0
            path.addRoundedRect(rect, radius, radius)

        grad = QLinearGradient(rect.left(), 0, rect.right(), 0)
        stops = []

        def add(at, col):
            at = min(1.0, max(0.0, at))
            if stops and at <= stops[-1][0]:
                at = min(1.0, stops[-1][0] + 0.0005)
            stops.append((at, col))

        add(0.0, self._base)
        add(self._t - 0.18, self._base)
        add(self._t, self._highlight)
        add(self._t + 0.18, self._base)
        add(1.0, self._base)
        for at, col in stops:
            grad.setColorAt(at, col)
        p.fillPath(path, QBrush(grad))

    # -- properties --
    @Property(str)
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = str(value)
        self._applyShapeHints()
        self.update()

    @Property(QColor)
    def baseColor(self):
        return self._base

    @baseColor.setter
    def baseColor(self, color):
        self._base = QColor(color)
        self.update()

    @Property(QColor)
    def highlightColor(self):
        return self._highlight

    @highlightColor.setter
    def highlightColor(self, color):
        self._highlight = QColor(color)
        self.update()
