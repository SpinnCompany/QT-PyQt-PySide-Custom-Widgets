########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomStepper - a step progress indicator.
##
## A row (or column) of numbered steps with connectors, showing progress:
## completed / active / pending. Tokenized via a `state` dynamic property on
## the circles and connectors.
########################################################################
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame


class QCustomStepper(QWidget):
    currentStepChanged = Signal(int)

    WIDGET_ICON = "components/icons/stepper.png"
    WIDGET_TOOLTIP = "A step progress indicator"
    WIDGET_MODULE = "Custom_Widgets.QCustomStepper"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomStepper' name='customStepper'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>400</width><height>72</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomStepper",
        "props": {"currentStep": {"type": "int", "default": 0}},
        "signals": ["currentStepChanged"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent=None, orientation=Qt.Horizontal):
        super().__init__(parent)
        self.setObjectName("QCustomStepper")
        self._orientation = orientation
        self._titles = []
        self._current = 0
        self._circles = []
        self._connectors = []
        self._box = (QHBoxLayout if orientation == Qt.Horizontal else QVBoxLayout)(self)
        self._box.setContentsMargins(8, 8, 8, 8)
        self._box.setSpacing(0)

    def setSteps(self, titles):
        self._clear()
        self._titles = list(titles or [])
        for i, title in enumerate(self._titles):
            if i > 0:
                line = QFrame(self)
                line.setObjectName("stepperConnector")
                line.setFrameShape(QFrame.HLine if self._orientation == Qt.Horizontal
                                   else QFrame.VLine)
                self._connectors.append(line)
                self._box.addWidget(line, 1)
            self._box.addWidget(self._makeStep(i, title))
        self.setCurrentStep(min(self._current, max(0, len(self._titles) - 1)))

    def _makeStep(self, index, title):
        cell = QWidget(self)
        lay = QVBoxLayout(cell)
        lay.setContentsMargins(6, 0, 6, 0)
        lay.setSpacing(4)
        circle = QLabel(str(index + 1), cell)
        circle.setObjectName("stepperCircle")
        circle.setAlignment(Qt.AlignCenter)
        circle.setFixedSize(28, 28)
        self._circles.append(circle)
        label = QLabel(title, cell)
        label.setObjectName("stepperLabel")
        label.setAlignment(Qt.AlignCenter)
        lay.addWidget(circle, 0, Qt.AlignHCenter)
        lay.addWidget(label, 0, Qt.AlignHCenter)
        return cell

    def _clear(self):
        while self._box.count():
            item = self._box.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self._circles = []
        self._connectors = []

    def _applyStates(self):
        for i, circle in enumerate(self._circles):
            state = "completed" if i < self._current else ("active" if i == self._current else "pending")
            circle.setText("✓" if state == "completed" else str(i + 1))
            self._setState(circle, state)
        for i, line in enumerate(self._connectors):
            # connector i sits between step i and i+1
            self._setState(line, "completed" if i < self._current else "pending")

    @staticmethod
    def _setState(widget, state):
        widget.setProperty("state", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def stepCount(self):
        return len(self._titles)

    def currentStep(self):
        return self._current

    def setCurrentStep(self, index):
        index = max(0, min(int(index), max(0, len(self._titles) - 1)))
        changed = index != self._current
        self._current = index
        self._applyStates()
        if changed:
            self.currentStepChanged.emit(index)

    def next(self):
        self.setCurrentStep(self._current + 1)

    def previous(self):
        self.setCurrentStep(self._current - 1)

    def isComplete(self):
        return self._current >= len(self._titles) - 1
