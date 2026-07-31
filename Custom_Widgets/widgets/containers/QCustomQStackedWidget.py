## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com

## MODULE UPDATED TO USE QT.PY
from qtpy.QtCore import Qt, QEasingCurve, QPoint, Slot, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, QTimeLine, Property, QSequentialAnimationGroup, Signal
from qtpy.QtGui import QPainter, QPixmap
from qtpy.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect, QStyleOption, QStyle, QPushButton
import os

from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve, returnQtDirection, easingCurveToInt
from Custom_Widgets.Utils import is_in_designer
from Custom_Widgets._resources import packageDir

class QCustomQStackedWidget(QStackedWidget):
    """
    A custom QStackedWidget with animated transitions between pages.
    
    This widget extends QStackedWidget to provide smooth slide and fade transitions
    between different pages/widgets. It supports both slide animations (horizontal
    or vertical) and fade animations with customizable timing and easing curves.
    
    Features:
    - Slide transitions (horizontal or vertical)
    - Fade transitions with separate in/out animations
    - Customizable timing and easing curves
    - Optional delay between animations
    - Qt Designer integration
    
    Signals:
        transitionFinished: Emitted when a transition animation completes
    
    Properties:
        fadeTransition (bool): Enable/disable fade transitions
        slideTransition (bool): Enable/disable slide transitions
        transitionDirection (str): Direction of slide transitions ('horizontal' or 'vertical')
        transitionTime (int): Duration of slide transitions in milliseconds
        fadeTime (int): Total duration of fade transitions in milliseconds
        fadeDelay (int): Delay between fade out and fade in animations in milliseconds
        fadeInTime (int): Duration of fade in animation in milliseconds
        fadeOutTime (int): Duration of fade out animation in milliseconds
        fadeInCurve (str): Easing curve for fade in animation
        fadeOutCurve (str): Easing curve for fade out animation
        transitionEasingCurve (str): Easing curve for slide animations
        fadeEasingCurve (str): Legacy property for fade easing curve
    """
    
    # Define the XML metadata and icon for Qt Designer
    script_dir = packageDir()
    WIDGET_ICON = os.path.join(script_dir, "components/icons/layers.png")
    WIDGET_TOOLTIP = "A custom QStackedWidget with transitions"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomQStackedWidget' name='customQStackedWidget'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomQStackedWidget"

    # Rich editors for the Designer "Custom Properties" dock (see
    # DesignerTools.CustomPropertiesDock).
    DESIGNER_CUSTOM_PROPS = [
        {"name": "fadeTransition", "kind": "bool", "group": "Transition"},
        {"name": "slideTransition", "kind": "bool", "group": "Transition"},
        {"name": "transitionTime", "kind": "int", "group": "Transition"},
        {"name": "transitionEasingCurve", "kind": "easing", "group": "Transition"},
        {"name": "fadeTime", "kind": "int", "group": "Fade"},
        {"name": "fadeDelay", "kind": "int", "group": "Fade"},
        {"name": "fadeInTime", "kind": "int", "group": "Fade"},
        {"name": "fadeOutTime", "kind": "int", "group": "Fade"},
        {"name": "fadeEasingCurve", "kind": "easing", "group": "Fade"},
        {"name": "fadeInCurve", "kind": "easing", "group": "Fade"},
        {"name": "fadeOutCurve", "kind": "easing", "group": "Fade"},
    ]
    
    # Signal to indicate transition is complete
    transitionFinished = Signal()

    def __init__(self, parent=None):
        """
        Initialize the custom stacked widget.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super(QCustomQStackedWidget, self).__init__(parent)
        
        # Initialize private variables - store direction as string for Qt Designer
        self._fadeTransition = False
        self._slideTransition = False
        self._transitionDirection = 'horizontal'  # Store as string
        self._transitionTime = 500
        self._fadeTime = 500
        self._fadeDelay = 0  # New property for fade delay
        self._fadeInTime = 250  # Time for fade in portion
        self._fadeOutTime = 250  # Time for fade out portion
        self._fadeInCurve = "OutCubic"  # Easing curve for fade in
        self._fadeOutCurve = "InCubic"  # Easing curve for fade out
        self._transitionEasingCurve = "OutBack"
        self._fadeEasingCurve = "Linear"
        self._currentWidgetIndex = 0
        self._nextWidgetIndex = 0
        self._currentWidgetPosition = QPoint(0, 0)
        self._widgetActive = False
        
        # Store opacity effects to manage properly
        self._opacity_effects = {}
        
        # Animation group references
        self._anim_group = None
        self._fade_out_animation = None
        self._fade_in_animation = None

    # =========================================================================
    # PROPERTY GETTERS/SETTERS
    # =========================================================================
    
    @Property(bool)
    def fadeTransition(self):
        """Get the fade transition state."""
        return self._fadeTransition

    @fadeTransition.setter
    def fadeTransition(self, fadeState):
        """
        Set the fade transition state.
        
        Args:
            fadeState (bool): True to enable fade transitions, False to disable.
            
        Raises:
            Exception: If fadeState is not a boolean.
        """
        if isinstance(fadeState, bool):
            self._fadeTransition = fadeState
            # Initialize opacity for all widgets when fade transition is enabled
            if fadeState:
                self._initializeAllWidgetsOpacity()
        else:
            raise Exception("fadeTransition only accepts boolean variables")

    @Property(bool)
    def slideTransition(self):
        """Get the slide transition state."""
        return self._slideTransition

    @slideTransition.setter
    def slideTransition(self, slideState):
        """
        Set the slide transition state.
        
        Args:
            slideState (bool): True to enable slide transitions, False to disable.
            
        Raises:
            Exception: If slideState is not a boolean.
        """
        if isinstance(slideState, bool):
            self._slideTransition = slideState
        else:
            raise Exception("slideTransition only accepts boolean variables")

    @Property(Qt.Orientation)
    def transitionDirection(self):
        """Slide transition direction. Exposed as Qt.Orientation so Qt
        Designer shows a Horizontal/Vertical dropdown."""
        return Qt.Vertical if self._transitionDirection == 'vertical' else Qt.Horizontal

    @transitionDirection.setter
    def transitionDirection(self, direction):
        """Accepts Qt.Orientation (Qt.Horizontal/Qt.Vertical). Legacy string
        values ('horizontal'/'vertical'/'h'/'v') are still coerced so older
        .ui files keep loading."""
        if isinstance(direction, str):
            self._transitionDirection = 'vertical' \
                if direction.lower().strip() in ('vertical', 'v', 'vert') else 'horizontal'
        else:
            self._transitionDirection = 'vertical' if direction == Qt.Vertical else 'horizontal'

    @Property(int)
    def transitionTime(self):
        """Get the slide transition time in milliseconds."""
        return self._transitionTime

    @transitionTime.setter
    def transitionTime(self, time):
        """
        Set the slide transition time.
        
        Args:
            time (int): Duration in milliseconds.
        """
        self._transitionTime = time

    @Property(int)
    def fadeTime(self):
        """Get the total fade transition time in milliseconds."""
        return self._fadeTime

    @fadeTime.setter
    def fadeTime(self, time):
        """
        Set the total fade transition time.
        
        Args:
            time (int): Total duration in milliseconds.
        """
        self._fadeTime = time
        # Automatically split fade time between in and out if not manually set
        if not hasattr(self, '_fadeInTimeSet'):
            self._fadeInTime = time // 2
        if not hasattr(self, '_fadeOutTimeSet'):
            self._fadeOutTime = time // 2

    @Property(int)
    def fadeDelay(self):
        """Get the delay between fade out and fade in animations in milliseconds."""
        return self._fadeDelay

    @fadeDelay.setter
    def fadeDelay(self, delay):
        """
        Set the delay between fade out and fade in animations.
        
        Args:
            delay (int): Delay duration in milliseconds.
        """
        self._fadeDelay = delay

    @Property(int)
    def fadeInTime(self):
        """Get the fade in animation time in milliseconds."""
        return self._fadeInTime

    @fadeInTime.setter
    def fadeInTime(self, time):
        """
        Set the fade in animation time.
        
        Args:
            time (int): Duration in milliseconds.
        """
        self._fadeInTime = time
        self._fadeInTimeSet = True  # Mark as manually set

    @Property(int)
    def fadeOutTime(self):
        """Get the fade out animation time in milliseconds."""
        return self._fadeOutTime

    @fadeOutTime.setter
    def fadeOutTime(self, time):
        """
        Set the fade out animation time.
        
        Args:
            time (int): Duration in milliseconds.
        """
        self._fadeOutTime = time
        self._fadeOutTimeSet = True  # Mark as manually set

    # Easing curves are typed as int (a QEasingCurve.Type value) so Designer
    # shows a spin box; developers can pass QEasingCurve.OutQuad etc. Legacy
    # name strings are still accepted. The internal _*Curve values keep their
    # original form and are resolved via returnAnimationEasingCurve when used.
    @Property(int)
    def fadeInCurve(self):
        return easingCurveToInt(self._fadeInCurve)

    @fadeInCurve.setter
    def fadeInCurve(self, curve):
        self._fadeInCurve = curve

    @Property(int)
    def fadeOutCurve(self):
        return easingCurveToInt(self._fadeOutCurve)

    @fadeOutCurve.setter
    def fadeOutCurve(self, curve):
        self._fadeOutCurve = curve

    @Property(int)
    def transitionEasingCurve(self):
        return easingCurveToInt(self._transitionEasingCurve)

    @transitionEasingCurve.setter
    def transitionEasingCurve(self, curve):
        self._transitionEasingCurve = curve

    @Property(int)
    def fadeEasingCurve(self):
        return easingCurveToInt(self._fadeEasingCurve)

    @fadeEasingCurve.setter
    def fadeEasingCurve(self, curve):
        self._fadeEasingCurve = curve

    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _initializeAllWidgetsOpacity(self):
        """Initialize opacity for all widgets to 0 when fade transitions are enabled."""
        for i in range(self.count()):
            widget = self.widget(i)
            if widget:
                self._setWidgetOpacity(widget, 0.0)
    
    def _setWidgetOpacity(self, widget, opacity):
        """
        Set the opacity of a widget.
        
        Args:
            widget (QWidget): The widget to set opacity for.
            opacity (float): Opacity value between 0.0 and 1.0.
        """
        if widget.graphicsEffect():
            widget.graphicsEffect().deleteLater()
        
        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(opacity)
        widget.setGraphicsEffect(effect)
    
    def _cleanupAnimation(self):
        """Clean up current animation resources."""
        if self._anim_group:
            try:
                self._anim_group.stop()
                # Disconnect all signals first
                try:
                    self._anim_group.finished.disconnect()
                except (TypeError, RuntimeError):
                    pass
                self._anim_group.deleteLater()
            except RuntimeError:
                pass
            self._anim_group = None
        
        if self._fade_out_animation:
            try:
                self._fade_out_animation.deleteLater()
            except RuntimeError:
                pass
            self._fade_out_animation = None
        
        if self._fade_in_animation:
            try:
                self._fade_in_animation.deleteLater()
            except RuntimeError:
                pass
            self._fade_in_animation = None
    
    def _resetWidgetStates(self):
        """
        Reset all widget states to their default positions and opacity.
        This is called when interrupting an animation or when animation finishes.
        """
        # Reset all widget positions to (0, 0)
        for i in range(self.count()):
            widget = self.widget(i)
            if widget:
                # Reset position
                widget.move(0, 0)
                
                # Reset opacity based on whether it's the current widget
                if self._fadeTransition:
                    if i == self.currentIndex():
                        self._setWidgetOpacity(widget, 1.0)
                        widget.show()
                    else:
                        # Hide non-current widgets and set opacity to 0
                        self._setWidgetOpacity(widget, 0.0)
                        widget.hide()
                else:
                    # For non-fade transitions, ensure proper visibility
                    if i == self.currentIndex():
                        widget.show()
                    else:
                        widget.hide()
    
    # =========================================================================
    # PUBLIC METHODS
    # =========================================================================
    
    def setTransitionDirection(self, direction):
        """
        Set the transition direction.
        
        Args:
            direction (str): Either 'horizontal' or 'vertical'.
        """
        self.transitionDirection = direction  # Use the property setter
    
    def setTransitionSpeed(self, speed):
        """
        Set the slide transition speed.
        
        Args:
            speed (int): Duration in milliseconds.
        """
        self._transitionTime = speed

    def setFadeSpeed(self, speed):
        """
        Set the fade transition speed.
        
        Args:
            speed (int): Total duration in milliseconds.
        """
        self._fadeTime = speed
        self._fadeInTime = speed // 2
        self._fadeOutTime = speed // 2

    def setFadeDelay(self, delay):
        """
        Set the delay between fade out and fade in animations.
        
        Args:
            delay (int): Delay in milliseconds.
        """
        self._fadeDelay = delay

    def setFadeInOutTimes(self, fadeInTime, fadeOutTime):
        """
        Set fade in and fade out times separately.
        
        Args:
            fadeInTime (int): Fade in duration in milliseconds.
            fadeOutTime (int): Fade out duration in milliseconds.
        """
        self._fadeInTime = fadeInTime
        self._fadeOutTime = fadeOutTime
        self._fadeTime = fadeInTime + fadeOutTime
        self._fadeInTimeSet = True
        self._fadeOutTimeSet = True

    def setFadeInOutCurves(self, fadeInCurve, fadeOutCurve):
        """
        Set fade in and fade out easing curves separately.
        
        Args:
            fadeInCurve (str): Easing curve for fade in.
            fadeOutCurve (str): Easing curve for fade out.
        """
        self._fadeInCurve = fadeInCurve
        self._fadeOutCurve = fadeOutCurve

    def setTransitionEasingCurve(self, aesingCurve):
        """
        Set the easing curve for slide animations.
        
        Args:
            aesingCurve (str): Name of the easing curve.
        """
        self._transitionEasingCurve = aesingCurve

    def setFadeCurve(self, aesingCurve):
        """
        Legacy method to set fade easing curve.
        
        Args:
            aesingCurve (str): Name of the easing curve.
        """
        self._fadeEasingCurve = aesingCurve

    @Slot()
    def slideToPreviousWidget(self):
        """Transition to the previous widget with animation."""
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex > 0:
            self.slideToWidgetIndex(currentWidgetIndex - 1)

    @Slot()
    def slideToNextWidget(self):
        """Transition to the next widget with animation."""
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex < (self.count() - 1):
            self.slideToWidgetIndex(currentWidgetIndex + 1)

    def slideToWidgetIndex(self, index):
        """
        Transition to a specific widget index with animation.
        
        Args:
            index (int): Index of the widget to transition to.
        """
        if index > (self.count() - 1):
            index = index % self.count()
        elif index < 0:
            index = (index + self.count()) % self.count()
        
        if self._slideTransition or self._fadeTransition:
            self.slideToWidget(self.widget(index))
        else:
            self.setCurrentIndex(index)

    def slideToWidget(self, newWidget):
        """
        Transition to a specific widget with animation.
        
        This method handles the complete transition process with the following sequence:
        1. Stop and clean up any ongoing animation
        2. Reset all widget states to defaults
        3. Fade out current widget (if fade transition enabled)
        4. Set new widget as current
        5. Fade in new widget (if fade transition enabled)
        
        Args:
            newWidget (QWidget): The widget to transition to.
        """
        # Stop any ongoing animation immediately
        self._cleanupAnimation()
        
        # Reset all widget states to defaults
        self._resetWidgetStates()
        
        # If the widget is active from a previous incomplete animation, reset it
        if self._widgetActive:
            self._widgetActive = False
        
        # Get current and next widget indices
        currentIndex = self.currentIndex()
        nextIndex = self.indexOf(newWidget)

        # If already on the target widget, just emit signal and return
        if currentIndex == nextIndex:
            self.transitionFinished.emit()
            return

        # Update widget active state
        self._widgetActive = True
        self._nextWidgetIndex = nextIndex
        self._currentWidgetIndex = currentIndex

        # Get widget references
        current_widget = self.widget(currentIndex)
        next_widget = self.widget(nextIndex)

        # Prepare next widget
        next_widget.setGeometry(self.frameRect())
        
        # Initialize opacity for fade transition if enabled
        if self._fadeTransition:
            # Set current widget opacity to 1.0 and next widget to 0.0
            self._setWidgetOpacity(current_widget, 1.0)
            self._setWidgetOpacity(next_widget, 0.0)
        
        # Show and raise the next widget
        next_widget.show()
        next_widget.raise_()
        
        # Store current position for slide animation
        self._currentWidgetPosition = current_widget.pos()
        
        # Create parallel animation group for combined animations
        self._anim_group = QParallelAnimationGroup()
        
        # Add fade animation if enabled
        if self._fadeTransition:
            self._createFadeAnimation(current_widget, next_widget)
        
        # Add slide animation if enabled
        if self._slideTransition:
            self._createSlideAnimation(current_widget, next_widget, currentIndex, nextIndex)
        
        # Connect animation finished signal
        if self._anim_group.animationCount() > 0:
            self._anim_group.finished.connect(self._onAnimationFinished)
            self._anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        else:
            # If no animations, just switch immediately
            self.setCurrentIndex(self._nextWidgetIndex)
            old_widget = self.widget(self._currentWidgetIndex)
            if old_widget:
                old_widget.hide()
            self._widgetActive = False
            self.transitionFinished.emit()
    
    def _createFadeAnimation(self, current_widget, next_widget):
        """
        Create fade animations for both current and next widgets.
        
        Args:
            current_widget (QWidget): The current widget to fade out
            next_widget (QWidget): The next widget to fade in
        """
        # Create fade out animation for current widget
        if current_widget.graphicsEffect():
            current_widget.graphicsEffect().deleteLater()
        
        fade_out_effect = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(fade_out_effect)
        
        self._fade_out_animation = QPropertyAnimation(fade_out_effect, b'opacity')
        self._fade_out_animation.setStartValue(1.0)
        self._fade_out_animation.setEndValue(0.0)
        self._fade_out_animation.setDuration(self._fadeOutTime)
        self._fade_out_animation.setEasingCurve(returnAnimationEasingCurve(self._fadeOutCurve))
        
        # Create fade in animation for next widget
        if next_widget.graphicsEffect():
            next_widget.graphicsEffect().deleteLater()
        
        fade_in_effect = QGraphicsOpacityEffect(next_widget)
        next_widget.setGraphicsEffect(fade_in_effect)
        
        self._fade_in_animation = QPropertyAnimation(fade_in_effect, b'opacity')
        self._fade_in_animation.setStartValue(0.0)
        self._fade_in_animation.setEndValue(1.0)
        self._fade_in_animation.setDuration(self._fadeInTime)
        self._fade_in_animation.setEasingCurve(returnAnimationEasingCurve(self._fadeInCurve))
        
        # Add delay to fade in if specified
        if self._fadeDelay > 0:
            self._fade_in_animation.setStartDelay(self._fadeDelay)
        
        # Add animations to group
        self._anim_group.addAnimation(self._fade_out_animation)
        self._anim_group.addAnimation(self._fade_in_animation)
    
    def _createSlideAnimation(self, current_widget, next_widget, currentIndex, nextIndex):
        """
        Create slide animations for both current and next widgets.
        
        Args:
            current_widget (QWidget): The current widget
            next_widget (QWidget): The next widget
            currentIndex (int): Index of current widget
            nextIndex (int): Index of next widget
        """
        # Use the stored string direction
        direction_str = self._transitionDirection.lower()
        
        if direction_str == "horizontal":
            # Horizontal slide
            slide_offset = self.width()
            
            # Determine direction based on whether moving forward or backward
            if nextIndex > currentIndex:
                # Moving forward - slide in from right, out to left
                next_widget.move(slide_offset, 0)
                next_anim = QPropertyAnimation(next_widget, b'pos')
                next_anim.setStartValue(QPoint(slide_offset, 0))
                next_anim.setEndValue(QPoint(0, 0))
                next_anim.setDuration(self._transitionTime)
                next_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
                
                current_anim = QPropertyAnimation(current_widget, b'pos')
                current_anim.setStartValue(QPoint(0, 0))
                current_anim.setEndValue(QPoint(-slide_offset, 0))
                current_anim.setDuration(self._transitionTime)
                current_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
            else:
                # Moving backward - slide in from left, out to right
                next_widget.move(-slide_offset, 0)
                next_anim = QPropertyAnimation(next_widget, b'pos')
                next_anim.setStartValue(QPoint(-slide_offset, 0))
                next_anim.setEndValue(QPoint(0, 0))
                next_anim.setDuration(self._transitionTime)
                next_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
                
                current_anim = QPropertyAnimation(current_widget, b'pos')
                current_anim.setStartValue(QPoint(0, 0))
                current_anim.setEndValue(QPoint(slide_offset, 0))
                current_anim.setDuration(self._transitionTime)
                current_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
        else:
            # Vertical slide
            slide_offset = self.height()
            
            # Determine direction based on whether moving forward or backward
            if nextIndex > currentIndex:
                # Moving forward - slide in from bottom, out to top
                next_widget.move(0, slide_offset)
                next_anim = QPropertyAnimation(next_widget, b'pos')
                next_anim.setStartValue(QPoint(0, slide_offset))
                next_anim.setEndValue(QPoint(0, 0))
                next_anim.setDuration(self._transitionTime)
                next_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
                
                current_anim = QPropertyAnimation(current_widget, b'pos')
                current_anim.setStartValue(QPoint(0, 0))
                current_anim.setEndValue(QPoint(0, -slide_offset))
                current_anim.setDuration(self._transitionTime)
                current_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
            else:
                # Moving backward - slide in from top, out to bottom
                next_widget.move(0, -slide_offset)
                next_anim = QPropertyAnimation(next_widget, b'pos')
                next_anim.setStartValue(QPoint(0, -slide_offset))
                next_anim.setEndValue(QPoint(0, 0))
                next_anim.setDuration(self._transitionTime)
                next_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
                
                current_anim = QPropertyAnimation(current_widget, b'pos')
                current_anim.setStartValue(QPoint(0, 0))
                current_anim.setEndValue(QPoint(0, slide_offset))
                current_anim.setDuration(self._transitionTime)
                current_anim.setEasingCurve(returnAnimationEasingCurve(self._transitionEasingCurve))
        
        # Add slide animations to group
        self._anim_group.addAnimation(next_anim)
        self._anim_group.addAnimation(current_anim)
    
    def _onAnimationFinished(self):
        """Handle completion of all animations."""
        # Set the new widget as current
        self.setCurrentIndex(self._nextWidgetIndex)
        
        # Hide the old widget
        old_widget = self.widget(self._currentWidgetIndex)
        if old_widget:
            old_widget.hide()
        
        # Reset widget positions to (0, 0) for all widgets
        self._resetWidgetStates()
        
        # Clean up animation resources
        self._cleanupAnimation()
        
        # Reset state
        self._widgetActive = False
        
        # Emit completion signal
        self.transitionFinished.emit()
    
    @Slot()
    def setCurrentWidget(self, widget):
        """
        Set the current widget with animation if enabled.
        
        Args:
            widget (QWidget): The widget to set as current.
        """
        currentIndex = self.currentIndex()
        nextIndex = self.indexOf(widget)
        
        if currentIndex == nextIndex:
            return
        
        if self._slideTransition or self._fadeTransition:
            self.slideToWidget(widget)
        else:
            self.setCurrentIndex(nextIndex)
    
    def setCurrentIndex(self, index):
        """
        Set the current widget index with proper opacity handling.
        
        Args:
            index (int): The index of the widget to set as current.
        """
        # Clean up any ongoing animation when setting current index directly
        self._cleanupAnimation()
        
        # Reset opacity of all widgets if fade transitions are enabled
        if self._fadeTransition:
            for i in range(self.count()):
                widget = self.widget(i)
                if widget:
                    self._setWidgetOpacity(widget, 0.0)
        
        # Call parent method
        super().setCurrentIndex(index)
        
        # Set opacity of current widget to 1.0
        if self._fadeTransition:
            current_widget = self.widget(index)
            if current_widget:
                self._setWidgetOpacity(current_widget, 1.0)
        
        # Reset all widget states
        self._resetWidgetStates()
        
        # Reset active state
        self._widgetActive = False
    
    # =========================================================================
    # OVERRIDDEN METHODS
    # =========================================================================
    
    def paintEvent(self, event):
        """
        Override paintEvent to handle potential painting conflicts.
        
        Args:
            event (QPaintEvent): The paint event.
        """
        try:
            super().paintEvent(event)
        except RuntimeError as e:
            # Ignore painter conflicts during transitions
            if "painter" not in str(e).lower():
                raise
    
    def addWidget(self, widget):
        """
        Add a widget to the stacked widget with proper opacity initialization.
        
        Args:
            widget (QWidget): The widget to add.
            
        Returns:
            int: The index of the added widget.
        """
        index = super().addWidget(widget)
        # Initialize opacity to 0 if fade transitions are enabled
        if self._fadeTransition:
            self._setWidgetOpacity(widget, 0.0)
            # Set current widget to opacity 1.0
            if index == self.currentIndex():
                self._setWidgetOpacity(widget, 1.0)
        return index
    
    def __del__(self):
        """Clean up on destruction."""
        self._cleanupAnimation()