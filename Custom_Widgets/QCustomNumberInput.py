########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomNumberInput - a number stepper (spin box).
##
## A numeric field flanked by - / + step buttons. Range-clamped, integer or
## fixed-decimal (set decimals > 0 for floats), with a configurable step.
## Editing the field commits on Enter / focus-out. Tokenized. Emits
## valueChanged(value) - an int when decimals == 0, else a float.
########################################################################
from qtpy.QtCore import Qt, Signal, Property
from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class QCustomNumberInput(QWidget):
    valueChanged = Signal(object)          # int or float

    WIDGET_ICON = "components/icons/numberinput.png"
    WIDGET_TOOLTIP = "A number stepper / spin box"
    WIDGET_MODULE = "Custom_Widgets.QCustomNumberInput"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomNumberInput' name='customNumberInput'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>140</width><height>32</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomNumberInput",
        "props": {"minimum": {"type": "double", "default": 0},
                  "maximum": {"type": "double", "default": 100},
                  "singleStep": {"type": "double", "default": 1},
                  "decimals": {"type": "int", "default": 0}},
        "signals": ["valueChanged"],
        "tokens_used": ["surface", "on-surface", "outline", "accent", "on-primary"],
    }

    def __init__(self, parent=None, minimum=0, maximum=100, value=0, step=1,
                 decimals=0):
        super().__init__(parent)
        self.setObjectName("QCustomNumberInput")
        self._min = float(minimum)
        self._max = float(maximum)
        self._step = float(step)
        self._decimals = int(decimals)
        self._value = 0.0

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._down = QPushButton("−", self)      # minus sign
        self._down.setObjectName("numberDown")
        self._down.setFocusPolicy(Qt.NoFocus)
        self._down.setAutoRepeat(True)
        self._down.clicked.connect(self.stepDown)

        self._field = QLineEdit(self)
        self._field.setObjectName("numberField")
        self._field.setAlignment(Qt.AlignCenter)
        self._field.editingFinished.connect(self._onEdited)

        self._up = QPushButton("+", self)
        self._up.setObjectName("numberUp")
        self._up.setFocusPolicy(Qt.NoFocus)
        self._up.setAutoRepeat(True)
        self._up.clicked.connect(self.stepUp)

        for w in (self._down, self._field, self._up):
            row.addWidget(w)
        row.setStretch(1, 1)

        self._applyValidator()
        self.setValue(value)

    # ------------------------------------------------------------------ #
    ## Helpers
    # ------------------------------------------------------------------ #
    def _applyValidator(self):
        v = QDoubleValidator(self._min, self._max, max(0, self._decimals), self)
        v.setNotation(QDoubleValidator.StandardNotation)
        self._field.setValidator(v)

    def _cast(self, value):
        return int(round(value)) if self._decimals <= 0 else round(float(value),
                                                                    self._decimals)

    def _format(self, value):
        if self._decimals <= 0:
            return str(int(round(value)))
        return "{:.{}f}".format(value, self._decimals)

    def _clamp(self, value):
        return max(self._min, min(float(value), self._max))

    def _onEdited(self):
        text = self._field.text().strip()
        try:
            parsed = float(text) if text not in ("", "-", "+") else self._value
        except ValueError:
            parsed = self._value
        self.setValue(parsed)

    # ------------------------------------------------------------------ #
    ## Public API
    # ------------------------------------------------------------------ #
    def value(self):
        return self._cast(self._value)

    def setValue(self, value):
        clamped = self._clamp(value)
        cast = self._cast(clamped)
        changed = cast != self._cast(self._value)
        self._value = float(cast)
        self._field.setText(self._format(self._value))
        self._syncButtons()
        if changed:
            self.valueChanged.emit(self.value())

    def stepUp(self):
        self.setValue(self._value + self._step)

    def stepDown(self):
        self.setValue(self._value - self._step)

    def setRange(self, minimum, maximum):
        self._min, self._max = float(minimum), float(maximum)
        if self._min > self._max:
            self._min, self._max = self._max, self._min
        self._applyValidator()
        self.setValue(self._value)

    def setMinimum(self, minimum):
        self.setRange(minimum, self._max)

    def setMaximum(self, maximum):
        self.setRange(self._min, maximum)

    def setSingleStep(self, step):
        self._step = float(step)

    def setDecimals(self, decimals):
        self._decimals = int(decimals)
        self._applyValidator()
        self.setValue(self._value)

    def _syncButtons(self):
        self._down.setEnabled(self._value > self._min)
        self._up.setEnabled(self._value < self._max)

    def lineEdit(self):
        return self._field

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    # NB: no `value` Q_PROPERTY - it would collide with the value() method
    # (Qt-idiomatic getter). Set the value in code via setValue(); Designer
    # exposes range/step/decimals below.
    @Property(float)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, v):
        self.setMinimum(v)

    @Property(float)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, v):
        self.setMaximum(v)

    @Property(float)
    def singleStep(self):
        return self._step

    @singleStep.setter
    def singleStep(self, v):
        self.setSingleStep(v)

    @Property(int)
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, v):
        self.setDecimals(v)
