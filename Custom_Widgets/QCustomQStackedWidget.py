
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com

## MODULE UPDATED TO USE QT.PY
from qtpy.QtCore import Qt, QEasingCurve, QPoint, Slot, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, QTimeLine, Property
from qtpy.QtGui import QPainter, QPixmap
from qtpy.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect, QStyleOption, QStyle, QPushButton
import os

from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve, returnQtDirection

class QCustomQStackedWidget(QStackedWidget):
    # Define the XML metadata and icon for Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/stacked_widget.png")
    WIDGET_TOOLTIP = "A custom QStackedWidget with transitions"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQStackedWidget' name='customQStackedWidget'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomQStackedWidget"

    def __init__(self, parent=None):
        super(QCustomQStackedWidget, self).__init__(parent)
        # Initialize Default Values
        self.fadeTransition = False
        self.slideTransition = False
        self.transitionDirection = Qt.Vertical
        self.transitionTime = 500
        self.fadeTime = 500
        self.transitionEasingCurve = "OutBack"
        self.fadeEasingCurve = "Linear"
        self.currentWidget = 0
        self.nextWidget = 0
        self._currentWidgetPosition = QPoint(0, 0)
        self.widgetActive = False

    ## Define properties for Qt Designer integration
    @Property(bool)
    def fadeTransition(self):
        return self._fadeTransition

    @fadeTransition.setter
    def fadeTransition(self, fadeState):
        if isinstance(fadeState, bool):
            self._fadeTransition = fadeState
        else:
            raise Exception("setFadeTransition() only accepts boolean variables")

    @Property(bool)
    def slideTransition(self):
        return self._slideTransition

    @slideTransition.setter
    def slideTransition(self, slideState):
        if isinstance(slideState, bool):
            self._slideTransition = slideState
        else:
            raise Exception("setSlideTransition() only accepts boolean variables")

    @Property(int)
    def transitionTime(self):
        return self._transitionTime

    @transitionTime.setter
    def transitionTime(self, time):
        self._transitionTime = time

    @Property(int)
    def fadeTime(self):
        return self._fadeTime

    @fadeTime.setter
    def fadeTime(self, time):
        self._fadeTime = time

    @Property(str)
    def transitionEasingCurve(self):
        return self._transitionEasingCurve

    @transitionEasingCurve.setter
    def transitionEasingCurve(self, curve):
        self._transitionEasingCurve = curve

    @Property(str)
    def fadeEasingCurve(self):
        return self._fadeEasingCurve

    @fadeEasingCurve.setter
    def fadeEasingCurve(self, curve):
        self._fadeEasingCurve = curve

    
    ## Function to update transition direction
    def setTransitionDirection(self, direction):
        self.transitionDirection = direction
    
    ## Function to update transition speed
    def setTransitionSpeed(self, speed):
        self.transitionTime = speed

    
    ## Function to update fade speed
    def setFadeSpeed(self, speed):
        self.fadeTime = speed

    
    ## Function to update transition easing curve
    def setTransitionEasingCurve(self, aesingCurve):
        self.transitionEasingCurve = aesingCurve

    
    ## Function to update fade easing curve
    def setFadeCurve(self, aesingCurve):
        self.fadeEasingCurve = aesingCurve

    
    ## Function to transition to previous widget
    @Slot()
    def slideToPreviousWidget(self):
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex > 0:
            self.slideToWidgetIndex(currentWidgetIndex - 1)

    
    ## Function to transition to next widget
    @Slot()
    def slideToNextWidget(self):
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex < (self.count() - 1):
            self.slideToWidgetIndex(currentWidgetIndex + 1)


    
    ## Function to transition to a given widget index
    def slideToWidgetIndex(self, index):
        if index > (self.count() - 1):
            index = index % self.count()
        elif index < 0:
            index = (index + self.count()) % self.count()
        if self.slideTransition:
            self.slideToWidget(self.widget(index))
        else:
            self.setCurrentIndex(index)

    
    ## Function to transition to a given widget
    def slideToWidget(self, newWidget):
        # If the widget is active, exit the function
        if self.widgetActive:
            return

        # Update widget active bool
        self.widgetActive = True

        # Get current and next widget index
        _currentWidgetIndex = self.currentIndex()
        _nextWidgetIndex = self.indexOf(newWidget)

        # If current widget index is equal to next widget index, exit function
        if _currentWidgetIndex == _nextWidgetIndex:
            self.widgetActive = False
            return

        anim_group = QParallelAnimationGroup(
            self, finished=self.animationDoneSlot
        )

        # Get X and Y position of QStackedWidget
        offsetX, offsetY = self.frameRect().width(), self.frameRect().height()
        # Set the next widget geometry
        self.widget(_nextWidgetIndex).setGeometry(self.frameRect())

        self.widget(_nextWidgetIndex).show()
        self.widget(_nextWidgetIndex).raise_()

        if self.slideTransition:
            # Animate transition
            # Set left right(horizontal) or up down(vertical) transition
            if not self.transitionDirection == Qt.Horizontal:
                if _currentWidgetIndex < _nextWidgetIndex:
                    # Down up transition
                    offsetX, offsetY = 0, -offsetY
                else:
                    # Up down transition
                    offsetX = 0
            else:
                # Right left transition
                if _currentWidgetIndex < _nextWidgetIndex:
                    offsetX, offsetY = -offsetX, 0
                else:
                    # Left right transition
                    offsetY = 0

            nextWidgetPosition = self.widget(_nextWidgetIndex).pos()
            currentWidgetPosition = self.widget(_currentWidgetIndex).pos()
            self._currentWidgetPosition = currentWidgetPosition

            offset = QPoint(offsetX, offsetY)
            self.widget(_nextWidgetIndex).move(nextWidgetPosition - offset)
            
            for index, start, end in zip(
                (_currentWidgetIndex, _nextWidgetIndex),
                (currentWidgetPosition, nextWidgetPosition - offset),
                (currentWidgetPosition + offset, nextWidgetPosition)
            ):
                animation = QPropertyAnimation(
                    self.widget(index),
                    b"pos",
                    duration=self.transitionTime,
                    easingCurve=returnAnimationEasingCurve(self.transitionEasingCurve),
                    startValue=start,
                    endValue=end,
                )
                anim_group.addAnimation(animation)

        # Play fade animation
        if self.fadeTransition:
            opacityEffect = QGraphicsOpacityEffect(self.widget(self.currentWidget))
            self.setGraphicsEffect(opacityEffect)
            opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self.widget(self.currentWidget))
            opacityAni.setStartValue(0)
            opacityAni.setEndValue(1)
            opacityAni.setDuration(self.fadeTime)
            opacityAni.setEasingCurve(returnAnimationEasingCurve(self.fadeEasingCurve))
            opacityAni.finished.connect(opacityEffect.deleteLater)
            # opacityAni.start()

            anim_group.addAnimation(opacityAni)

        self.nextWidget = _nextWidgetIndex
        self.currentWidget = _currentWidgetIndex
        
        self.widgetActive = True
        # self.setCurrentIndex(self.nextWidget)
        anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    
    ## Function to hide old widget and show new widget after animation is done
    @Slot()
    def animationDoneSlot(self):
        # self.widget(self.currentWidget).hide()
        self.setCurrentIndex(self.nextWidget)
        self.widget(self.currentWidget).move(self._currentWidgetPosition)
        self.widgetActive = False

    
    ## Function extending the QStackedWidget setCurrentWidget to animate transition
    @Slot()
    def setCurrentWidget(self, widget):
        currentIndex = self.currentIndex()
        nextIndex = self.indexOf(widget)
        if currentIndex == nextIndex and self.currentWidget == currentIndex:
            return
        
        # FadeWidgetTransition(self, self.widget(self.currentIndex()), self.widget(self.indexOf(widget)))
        self.slideToWidget(widget)
        # if not self.slideTransition:
        #     self.setCurrentIndex(0)
            
        if not self.slideTransition and not self.fadeTransition:
            self.setCurrentIndex(nextIndex)

