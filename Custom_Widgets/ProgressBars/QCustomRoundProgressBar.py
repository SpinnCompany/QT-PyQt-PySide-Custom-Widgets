from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

import os


class ProgressBarArcLoader:
    def __init__(self, parent=None, progress=0, duration=2000):
        self.parent = parent
        self.progress = progress  # Current progress percentage
        self.duration = duration  # Animation duration in milliseconds

    def getProgressAnimation(self, start, end):
        animation = QVariantAnimation(self.parent)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.setDuration(self.duration)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.valueChanged.connect(self.updateProgress)
        return animation

    def updateProgress(self, newValue):
        self.progress = newValue
        self.parent.update()

class QCustomRoundProgressBar(QWidget):
    # Define XML for Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/new_label.png")
    WIDGET_TOOLTIP = "A custom round progress bar that shows animated progress."
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRoundProgressBar' name='customRoundProgressBar'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomProgressBars"

    def __init__(self, parent=None, progressColor=None, textColor=None, progressBarWidth=5):
        super().__init__(parent)

        # Set default colors from application palette if not specified
        appPalette = QApplication.palette()
        self._progressColor = progressColor if progressColor is not None else appPalette.highlight().color()  # Accent color
        self._progressBaseColor = QColor(255, 255, 255, 100)  # Translucent white
        self._textColor = textColor if textColor is not None else appPalette.text().color()  # Default text color

        self._min = 0
        self._max = 100
        self._value = 0
        self._textVisible = True
        self._clockwise = True  # Direction of progress bar (True for clockwise)
        self._animationDuration = 500  # Default animation duration
        self._progressBarWidth = progressBarWidth  # Store the progress bar width
        self.initPen(self._progressBarWidth)

        # Initialize the loader
        self.arcLoader = ProgressBarArcLoader(self, 0, self._animationDuration)
        self.currentProgress = 0

        # Set size policy to make it responsive
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(160, 160)

        # Start the initial progress animation to 0
        self.animateTo(0)

    # Set up properties to be editable in Qt Designer
    @Property(int)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.animateTo(val)

    def setValue(self, val):
        self.value = val

    @Property(int)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, val):
        self._min = val
        self.update()

    @Property(int)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, val):
        self._max = val
        self.update()

    @Property(bool)
    def textVisible(self):
        return self._textVisible

    @textVisible.setter
    def textVisible(self, visible):
        self._textVisible = visible
        self.update()

    @Property(bool)
    def clockwise(self):
        return self._clockwise

    @clockwise.setter
    def clockwise(self, val):
        self._clockwise = val
        self.update()

    @Property(int)
    def animationDuration(self):
        return self._animationDuration

    @animationDuration.setter
    def animationDuration(self, duration):
        self._animationDuration = duration
        self.arcLoader.duration = duration  # Update the animation loader's duration
        self.update()

    @Property(int)
    def progressBarWidth(self):
        return self._progressBarWidth

    @progressBarWidth.setter
    def progressBarWidth(self, width):
        self._progressBarWidth = width
        self.initPen(width)  # Reinitialize the pen with the new width
        self.update()  # Update the widget to reflect changes

    @Property(QColor)
    def progressColor(self):
        return self._progressColor

    @progressColor.setter
    def progressColor(self, color):
        self._progressColor = color
        self.initPen(self.pen.width())  # Re-initialize the pen with the new color
        self.update()

    @Property(QColor)
    def progressBaseColor(self):
        return self._progressBaseColor

    @progressBaseColor.setter
    def progressBaseColor(self, color):
        self._progressBaseColor = color
        self.initPen(self.pen.width())  # Re-initialize the pen with the new color
        self.update()

    @Property(QColor)
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, color):
        self._textColor = color
        self.update()

    def initPen(self, progressBarWidth):
        self.pen = QPen()
        self.pen.setColor(self._progressColor)  # Use the progress bar color property
        self.pen.setWidth(progressBarWidth)
        self.pen.setCapStyle(Qt.RoundCap)

    def animateTo(self, progress):
        """Animates the progress bar to the specified progress percentage."""
        startProgress = (self.arcLoader.progress / self.maximum) * 100
        endProgress = (progress / self.maximum) * 100
        animation = self.arcLoader.getProgressAnimation(startProgress, endProgress)
        self.currentProgress = progress
        animation.start()

    def calculateXR(self):
        x = self.pen.width() / 2
        r = min(self.width(), self.height()) - self.pen.width()
        return x, r

    def draw(self):
        # Calculate dimensions based on widget size
        x, r = self.calculateXR()
        progressArc = int((self.arcLoader.progress / 100) * 360)

        # Draw the base arc (translucent white background for the progress path)
        basePen = QPen(self._progressBaseColor) 
        basePen.setWidth(self.pen.width())
        basePen.setCapStyle(Qt.RoundCap)
        self.painter.setPen(basePen)
        self.painter.drawArc(x, x, r, r, 0, 360 * 16)  # Full circle for the base

        # Choose the direction of the arc based on the 'clockwise' property
        self.painter.setPen(self.pen)  # Use the progress bar pen
        if self._clockwise:
            self.painter.drawArc(x, x, r, r, 90 * 16, -progressArc * 16)  # Clockwise progress arc
        else:
            self.painter.drawArc(x, x, r, r, 90 * 16, progressArc * 16)  # Counterclockwise progress arc

        # Draw the progress text in the center
        if self.textVisible:
            self.drawText()


    def drawText(self):
        # Set the text font and color
        font = self.font()  # Adjust font size based on widget size
        self.painter.setFont(font)
        self.painter.setPen(QPen(self._textColor))  # Use the text color property
        text = f"{int(self.arcLoader.progress)}%"  # Progress percentage

        # Calculate the bounding rectangle to center the text
        textRect = self.rect()
        self.painter.drawText(textRect, Qt.AlignCenter, text)

    def paintEvent(self, e):
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(self.pen)
        self.draw()
        self.painter.end()
