########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomAvatarGroup - a row of overlapping avatars with overflow.
##
## Circular initials-avatars overlap; beyond `maxVisible` a "+N" chip shows
## the remainder. Each avatar's colour is derived deterministically from its
## name. The separating ring colour comes from tokens (qproperty ringColor).
########################################################################
from qtpy.QtCore import Qt, Property
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel


_PALETTE = ["#ef4444", "#f59e0b", "#22c55e", "#14b8a6", "#3b82f6",
            "#6366f1", "#8b5cf6", "#ec4899", "#64748b", "#0ea5e9"]


def _initials(name):
    parts = [p for p in str(name).split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def _color_for(name):
    return _PALETTE[sum(ord(c) for c in str(name)) % len(_PALETTE)]


class QCustomAvatarGroup(QWidget):
    WIDGET_ICON = "components/icons/group.png"
    WIDGET_TOOLTIP = "A row of overlapping avatars with overflow"
    WIDGET_MODULE = "Custom_Widgets.QCustomAvatarGroup"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomAvatarGroup' name='customAvatarGroup'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>160</width><height>40</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomAvatarGroup",
        "props": {"maxVisible": {"type": "int", "default": 4},
                  "avatarSize": {"type": "int", "default": 34}},
        "signals": [],
        "tokens_used": ["surface", "surface-muted", "on-surface"],
    }

    def __init__(self, parent=None, maxVisible=4, size=34):
        super().__init__(parent)
        self.setObjectName("QCustomAvatarGroup")
        self._max = max(1, int(maxVisible))
        self._size = int(size)
        self._names = []
        self._ring = QColor("#ffffff")
        # Overflow ("+N") chip colours - token-driven (surface-muted / on-surface)
        # via the qproperties below; these literals are just first-paint fallbacks.
        self._overflow_bg = QColor("#94a3b8")
        self._overflow_text = QColor("#ffffff")
        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, 0, 0, 0)
        self._row.setSpacing(-self._size // 3)     # overlap
        self._row.addStretch(1)

    def setAvatars(self, names):
        self._names = list(names or [])
        self._rebuild()

    def _rebuild(self):
        while self._row.count() > 1:
            w = self._row.takeAt(0).widget()
            if w is not None:
                w.deleteLater()
        visible = self._names[:self._max]
        overflow = len(self._names) - len(visible)
        for name in visible:
            self._row.insertWidget(self._row.count() - 1,
                                   self._circle(_initials(name), _color_for(name), name))
        if overflow > 0:
            self._row.insertWidget(self._row.count() - 1,
                                   self._circle("+%d" % overflow, None, "%d more" % overflow))
        # left-most on top
        for i in range(self._row.count() - 1):
            w = self._row.itemAt(i).widget()
            if w is not None:
                w.raise_()

    def _circle(self, text, bg, tooltip):
        lbl = QLabel(text, self)
        lbl.setObjectName("avatarOverflow" if bg is None else "avatarCircle")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedSize(self._size, self._size)
        lbl.setToolTip(tooltip)
        if bg is None:
            lbl.setStyleSheet(
                "border-radius: %dpx; border: 2px solid %s; background-color: %s;"
                " color: %s; font-weight: 600;"
                % (self._size // 2, self._ring.name(),
                   self._overflow_bg.name(), self._overflow_text.name()))
        else:
            lbl.setStyleSheet(
                "border-radius: %dpx; border: 2px solid %s; background-color: %s;"
                " color: white; font-weight: 600;"
                % (self._size // 2, self._ring.name(), bg))
        return lbl

    # -- properties --
    @Property(int)
    def maxVisible(self):
        return self._max

    @maxVisible.setter
    def maxVisible(self, value):
        self._max = max(1, int(value))
        self._rebuild()

    @Property(QColor)
    def ringColor(self):
        return self._ring

    @ringColor.setter
    def ringColor(self, color):
        self._ring = QColor(color)

    @Property(QColor)
    def overflowBg(self):
        return self._overflow_bg

    @overflowBg.setter
    def overflowBg(self, color):
        self._overflow_bg = QColor(color)

    @Property(QColor)
    def overflowText(self):
        return self._overflow_text

    @overflowText.setter
    def overflowText(self, color):
        self._overflow_text = QColor(color)
        self._rebuild()

    def names(self):
        return list(self._names)
