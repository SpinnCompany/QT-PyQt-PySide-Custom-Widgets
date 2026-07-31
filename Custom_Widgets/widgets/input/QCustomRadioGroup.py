########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRadioGroup - a labelled set of single-choice options.
##
## Owns a set of QCustomRadioButton children and the mutual exclusion between
## them, so the group - not the buttons - is the single source of truth for
## "what is selected". That matters in Qt Designer, where you cannot wire up
## sibling relationships by hand.
##
## Options are authored in code with setOptions([...]) or in Qt Designer with
## the optionsCsv property, following the valuesCsv convention used by the
## chart widgets:
##
##     optionsCsv = "Free,Pro,Studio"              labels double as values
##     optionsCsv = "free=Free,pro=Pro,studio=Studio"   explicit value=label
##
## Emits valueChanged(str) and currentIndexChanged(int).
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from Custom_Widgets.QCustomRadioButton import QCustomRadioButton


class QCustomRadioGroup(QWidget):
    valueChanged = Signal(str)
    currentIndexChanged = Signal(int)

    WIDGET_ICON = "components/icons/radio_button_checked.png"
    WIDGET_TOOLTIP = "A single-choice radio group"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadioGroup"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadioGroup' name='customRadioGroup'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>220</width><height>110</height></rect></property>
            <property name='optionsCsv'><string>Option one,Option two,Option three</string></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadioGroup",
        "props": {"optionsCsv": {"type": "string",
                                 "default": "Option one,Option two,Option three"},
                  "selectedValue": {"type": "string", "default": ""},
                  "title": {"type": "string", "default": ""},
                  "orientation": {"type": "enum",
                                  "values": ["vertical", "horizontal"],
                                  "default": "vertical"},
                  "spacingPx": {"type": "int", "default": 10},
                  "sizeVariant": {"type": "enum", "values": ["sm", "md", "lg"],
                                  "default": "md"}},
        "signals": ["valueChanged", "currentIndexChanged"],
        "tokens_used": ["accent", "outline", "on-surface"],
    }

    def __init__(self, parent=None, options=None, value=None,
                 orientation="vertical", title=""):
        super().__init__(parent)
        self.setObjectName("QCustomRadioGroup")
        self._options = []          # list of (value, label)
        self._buttons = []
        self._value = ""
        self._title = str(title)
        self._orientation = "horizontal" if orientation == "horizontal" else "vertical"
        self._spacing = 10
        self._sizeVariant = "md"
        self._titleColor = QColor("#0f172a")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._layout = self._makeLayout()
        self.setOptions(options if options is not None
                        else ["Option one", "Option two", "Option three"])
        if value is not None:
            self.setValue(value)

    # ------------------------------------------------------------------ #
    ## Layout
    # ------------------------------------------------------------------ #
    def _makeLayout(self):
        box = QHBoxLayout(self) if self._orientation == "horizontal" else QVBoxLayout(self)
        box.setContentsMargins(0, self._titleHeight(), 0, 0)
        box.setSpacing(self._spacing)
        return box

    def _titleHeight(self):
        return (self.fontMetrics().height() + 6) if self._title else 0

    def _rebuildLayout(self):
        """Swap the layout direction, keeping the existing buttons."""
        for btn in self._buttons:
            self._layout.removeWidget(btn)
        # A QWidget can only own one layout; reparent the old one to a temp
        # widget so Qt destroys it with that widget instead of leaking it.
        QWidget().setLayout(self._layout)
        self._layout = self._makeLayout()
        for btn in self._buttons:
            self._layout.addWidget(btn)
        if self._orientation == "horizontal":
            self._layout.addStretch(1)

    # ------------------------------------------------------------------ #
    ## Options
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalise(options):
        """Accept strings, "value=label" strings, (value, label) pairs or dicts."""
        out = []
        for opt in options or []:
            if isinstance(opt, dict):
                label = str(opt.get("label", opt.get("value", "")))
                value = str(opt.get("value", label))
            elif isinstance(opt, (tuple, list)) and len(opt) >= 2:
                value, label = str(opt[0]), str(opt[1])
            else:
                text = str(opt)
                if "=" in text:
                    value, label = text.split("=", 1)
                    value, label = value.strip(), label.strip()
                else:
                    value = label = text.strip()
            if label:
                out.append((value, label))
        return out

    def setOptions(self, options):
        """Replace every option. Selection is kept if its value survives."""
        previous = self._value
        for btn in self._buttons:
            self._layout.removeWidget(btn)
            btn.setParent(None)
            btn.deleteLater()
        self._buttons = []
        self._options = self._normalise(options)

        for value, label in self._options:
            btn = QCustomRadioButton(self, text=label, value=value)
            # The group owns exclusion, not the buttons: a button that cleared
            # its own siblings would bypass us and valueChanged would not fire.
            btn.autoExclusive = False
            btn.sizeVariant = self._sizeVariant
            btn.toggled.connect(lambda on, v=value: self._onButtonToggled(on, v))
            self._buttons.append(btn)
            self._layout.addWidget(btn)
        if self._orientation == "horizontal":
            self._layout.addStretch(1)

        self._value = ""
        if previous and any(v == previous for v, _ in self._options):
            self.setValue(previous)
        self.updateGeometry()
        self.update()

    def options(self):
        return list(self._options)

    def buttons(self):
        return list(self._buttons)

    def count(self):
        return len(self._options)

    # ------------------------------------------------------------------ #
    ## Selection
    # ------------------------------------------------------------------ #
    def _onButtonToggled(self, on, value):
        if on:
            self.setValue(value)

    def value(self):
        return self._value

    def setValue(self, value):
        value = str(value)
        if value == self._value:
            return
        if value and not any(v == value for v, _ in self._options):
            return                                  # unknown value: ignore
        self._value = value
        for btn, (v, _) in zip(self._buttons, self._options):
            btn.setChecked(v == value)
        self.valueChanged.emit(value)
        self.currentIndexChanged.emit(self.currentIndex())

    def currentIndex(self):
        for i, (v, _) in enumerate(self._options):
            if v == self._value:
                return i
        return -1

    def setCurrentIndex(self, index):
        if 0 <= index < len(self._options):
            self.setValue(self._options[index][0])

    def currentLabel(self):
        i = self.currentIndex()
        return self._options[i][1] if i >= 0 else ""

    def clearSelection(self):
        self._value = ""
        for btn in self._buttons:
            btn.setChecked(False)
        self.valueChanged.emit("")
        self.currentIndexChanged.emit(-1)

    # ------------------------------------------------------------------ #
    ## Painting (title only; the options paint themselves)
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if not self._title:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        f = self.font()
        f.setBold(True)
        p.setFont(f)
        p.setPen(QPen(self._titleColor))
        p.drawText(0, 0, self.width(), self.fontMetrics().height(),
                   int(Qt.AlignLeft | Qt.AlignVCenter), self._title)

    # ------------------------------------------------------------------ #
    ## Properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def optionsCsv(self):
        return ",".join(lbl if val == lbl else "%s=%s" % (val, lbl)
                        for val, lbl in self._options)

    @optionsCsv.setter
    def optionsCsv(self, text):
        self.setOptions([tok for tok in str(text).replace(";", ",").split(",")
                         if tok.strip()])

    # Named selectedValue rather than value: the value() / setValue() methods
    # already occupy that name, and Designer needs a settable property here so
    # an option can be preselected in the .ui file.
    @Property(str)
    def selectedValue(self):
        return self._value

    @selectedValue.setter
    def selectedValue(self, v):
        self.setValue(v)

    @Property(str)
    def title(self):
        return self._title

    @title.setter
    def title(self, text):
        self._title = str(text)
        self._layout.setContentsMargins(0, self._titleHeight(), 0, 0)
        self.updateGeometry()
        self.update()

    @Property(str)
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        value = "horizontal" if str(value) == "horizontal" else "vertical"
        if value == self._orientation:
            return
        self._orientation = value
        self._rebuildLayout()
        self.updateGeometry()
        self.update()

    @Property(int)
    def spacingPx(self):
        return self._spacing

    @spacingPx.setter
    def spacingPx(self, px):
        self._spacing = int(px)
        self._layout.setSpacing(self._spacing)
        self.updateGeometry()

    @Property(str)
    def sizeVariant(self):
        return self._sizeVariant

    @sizeVariant.setter
    def sizeVariant(self, value):
        self._sizeVariant = str(value)
        for btn in self._buttons:
            btn.sizeVariant = self._sizeVariant
        self.updateGeometry()
        self.update()

    @Property(QColor)
    def titleColor(self):
        return self._titleColor

    @titleColor.setter
    def titleColor(self, c):
        self._titleColor = QColor(c); self.update()
