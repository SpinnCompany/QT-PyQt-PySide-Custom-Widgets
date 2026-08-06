########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomAccordion - a stack of collapsible sections.
##
## Each section is a header button + an animated collapsible content area.
## Optional exclusive mode (only one section open at a time). Tokenized.
########################################################################
from qtpy.QtCore import Qt, Signal, QPropertyAnimation
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame


_MAX = 16777215


class _AccordionSection(QWidget):
    toggled = Signal(bool)

    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self._expanded = False
        col = QVBoxLayout(self)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(0)

        self._header = QPushButton(self)
        self._header.setObjectName("accordionHeader")
        self._header.setCheckable(True)
        self._header.setCursor(Qt.PointingHandCursor)
        self._title = title
        self._header.setText("▸  " + title)      # collapsed glyph
        self._header.clicked.connect(lambda: self.setExpanded(not self._expanded))
        col.addWidget(self._header)

        self._wrap = QFrame(self)
        self._wrap.setObjectName("accordionContent")
        inner = QVBoxLayout(self._wrap)
        inner.setContentsMargins(12, 10, 12, 10)
        self._content = content
        inner.addWidget(content)
        self._wrap.setMaximumHeight(0)                # start collapsed
        col.addWidget(self._wrap)

        self._anim = QPropertyAnimation(self._wrap, b"maximumHeight", self)
        self._anim.setDuration(180)
        self._anim.finished.connect(self._onAnimFinished)

    def title(self):
        return self._title

    def isExpanded(self):
        return self._expanded

    def contentWidget(self):
        return self._content

    def _fullHeight(self):
        return self._wrap.sizeHint().height()

    def setExpanded(self, expanded, animate=True):
        if expanded == self._expanded:
            return
        self._expanded = expanded
        self._header.setChecked(expanded)
        self._header.setText(("▾  " if expanded else "▸  ") + self._title)
        target = self._fullHeight() if expanded else 0
        if animate:
            self._anim.stop()
            self._anim.setStartValue(self._wrap.maximumHeight())
            self._anim.setEndValue(target)
            self._anim.start()
        else:
            self._wrap.setMaximumHeight(_MAX if expanded else 0)
        self.toggled.emit(expanded)

    def _onAnimFinished(self):
        if self._expanded:
            self._wrap.setMaximumHeight(_MAX)          # allow free resize when open


class QCustomAccordion(QWidget):
    # index, expanded
    sectionToggled = Signal(int, bool)

    WIDGET_ICON = "components/icons/view_stream.png"
    WIDGET_TOOLTIP = "A stack of collapsible sections"
    WIDGET_MODULE = "Custom_Widgets.QCustomAccordion"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomAccordion' name='customAccordion'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>240</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomAccordion",
        "props": {"exclusive": {"type": "bool", "default": False}},
        "signals": ["sectionToggled"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline", "accent"],
    }

    def __init__(self, parent=None, exclusive=False):
        super().__init__(parent)
        self.setObjectName("QCustomAccordion")
        self._exclusive = exclusive
        self._sections = []
        self._box = QVBoxLayout(self)
        self._box.setContentsMargins(0, 0, 0, 0)
        self._box.setSpacing(6)
        self._box.addStretch(1)

    def addSection(self, title, content):
        section = _AccordionSection(title, content, self)
        index = len(self._sections)
        self._sections.append(section)
        self._box.insertWidget(self._box.count() - 1, section)  # before the stretch
        section.toggled.connect(lambda expanded, i=index: self._onToggled(i, expanded))
        return index

    def _onToggled(self, index, expanded):
        if expanded and self._exclusive:
            for i, s in enumerate(self._sections):
                if i != index and s.isExpanded():
                    s.setExpanded(False)
        self.sectionToggled.emit(index, expanded)

    # -- API --
    def sectionCount(self):
        return len(self._sections)

    def section(self, index):
        return self._sections[index]

    def setExpanded(self, index, expanded, animate=True):
        if 0 <= index < len(self._sections):
            self._sections[index].setExpanded(expanded, animate=animate)

    def expandedIndices(self):
        return [i for i, s in enumerate(self._sections) if s.isExpanded()]

    def setExclusive(self, exclusive):
        self._exclusive = bool(exclusive)

    def isExclusive(self):
        return self._exclusive
