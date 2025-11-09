from qtpy.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, Signal, QSize
from qtpy.QtWidgets import QWidget, QLabel, QStyleOption, QStyle, QHBoxLayout, QSizePolicy, QGraphicsOpacityEffect, QSpacerItem
from qtpy.QtGui import QPainter, QIcon, QPaintEvent

from Custom_Widgets.QCustomSidebar import QCustomSidebar 
from Custom_Widgets.Utils import replace_url_prefix, is_in_designer, get_icon_path

import os

class QCustomSidebarLabel(QWidget):  # Changed from QLabel to QWidget
    # Signal emitted when visibility changes
    visibilityChanged = Signal(bool)

    # Define XML for Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/new_label.png")
    WIDGET_TOOLTIP = "A custom widget that hides when its parent sidebar is collapsed"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebarLabel' name='customSidebarLabel'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebarLabel"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hideOnCollapse = True  # Default behavior to hide on collapse
        self._isVisible = True
        self._icon = None  # No icon set by default
        self._iconSize = QSize(24, 24)  # Default icon size

        # Initialize layout and QLabel for text and icon display
        layout = QHBoxLayout(self)  # Use QHBoxLayout for side-by-side icon and text
        # Create QLabel for the icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setWordWrap(True)
        layout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)

        # Create QLabel for text display
        self.label = QLabel("Default Text", self)  # Text will be shown if no icon
        layout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(self.verticalSpacer)

        # Set layout margins to 0
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # Set size policy
        self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Apply QGraphicsOpacityEffect to enable opacity animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # Animation
        self._animationDuration = 500
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Optional: smooth easing

        # Connect signals
        self.animation.finished.connect(self.on_animation_finished)

        # Connect signals
        self.animation.finished.connect(self.on_animation_finished)

        self.setStyleSheet("QLabel{ background-color: transparent;}")

    def start_show_animation(self):
        """Animate opacity from 0 to 1 and then show the widget."""
        self.setVisible(True)  # Make sure the widget is visible before animating
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def start_hide_animation(self):
        """Animate opacity from 1 to 0 and then hide the widget."""
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(self._animationDuration)
        self.animation.start()

    def on_animation_finished(self):
        """Handle the visibility of the widget after the animation finishes."""
        if self.animation.endValue() == 0.0:
            self.setVisible(False)

        # Ensure layout updates after animation
        self.adjustSize()
        self.updateGeometry()

        self.visibilityChanged.emit(self.isVisible())

    def hideLabel(self):
        """Start the hide animation."""
        if self._hideOnCollapse:
            self.start_hide_animation()

    def showLabel(self):
        """Start the show animation."""
        self.start_show_animation()

    def showEvent(self, e):
        """Validate and display the correct widget (icon or label) on show."""
        super().showEvent(e)
        
        # Check if the icon is valid and set visibility accordingly
        self.validateIconAndLabel()

        # Connect to parent's signals if a QCustomSidebar parent exists
        self.connect_to_parent()

        # Adjust size and update the widget
        self.adjustSize()
        self.update()

    def validateIconAndLabel(self):
        """Validate if the icon or label should be shown."""
        # Check if the icon is valid and set visibility accordingly
        if self._icon and not self._icon.isNull():
            # Icon is valid, show the iconLabel, hide the text label
            pixmap = self._icon.pixmap(self._iconSize)  # Get the scaled pixmap
            self.iconLabel.setPixmap(pixmap)
            self.iconLabel.setVisible(True)
        else:
            # No valid icon, hide the iconLabel, show the text label
            self.iconLabel.setVisible(False)

    @Property(str)
    def text(self):
        """Get the text of the label."""
        return self.label.text()

    @text.setter
    def text(self, text):
        self.setText(text)

    def setText(self, new_text: str):
        """Set the text of the label."""
        self.label.setText(new_text)
        self.adjustSize()
        self.update()
        self.label.setMinimumSize(self.label.sizeHint())

    @Property(QIcon)
    def icon(self):
        """Get the icon of the label."""
        return self._icon

    @icon.setter
    def icon(self, icon: QIcon):
        """Set the icon of the label."""
        self.setIcon(icon)

    def setIcon(self, icon: QIcon):
        """Set the icon in the QLabel and hide text if an icon is set."""
        if icon is not None and not icon.isNull():
            self._icon = icon
            # Set the icon into the QLabel using QIcon.pixmap for the appropriate size
            pixmap = icon.pixmap(self._iconSize)  # Use _iconSize for the pixmap size
            self.iconLabel.setPixmap(pixmap)
            self.iconLabel.setVisible(True)  # Show the icon label if an icon is set
        else:
            self.iconLabel.setVisible(False)  # Hide the icon label if no icon

        self.adjustSize()
        self.update()

        self.iconLabel.setMinimumSize(self.iconLabel.sizeHint())

    @Property(QSize)
    def iconSize(self):
        """Get the size of the icon."""
        return self._iconSize

    @iconSize.setter
    def iconSize(self, size: QSize):
        """Set the size of the icon."""
        if size != self._iconSize:
            self._iconSize = size
            # Update icon size if an icon is already set
            if self._icon and not self._icon.isNull():
                self.setIcon(self._icon)  # Reapply icon with new size
            self.adjustSize()
            self.update()

    @Property(bool)
    def hideOnCollapse(self):
        """Whether to hide this label when the sidebar collapses."""
        return self._hideOnCollapse

    @hideOnCollapse.setter
    def hideOnCollapse(self, hide):
        self._hideOnCollapse = hide

    def connect_to_parent(self):
        """Connect to the closest QCustomSidebar parent to listen for collapse/expand signals."""
        self.parent_sidebar = self.parent()  # Start with the direct parent
        while self.parent_sidebar and not isinstance(self.parent_sidebar, QCustomSidebar):
            self.parent_sidebar = self.parent_sidebar.parent()  # Move up the hierarchy

        if self.parent_sidebar:
            # Connect to signals emitted on collapse/expand
            self.parent_sidebar.onCollapsed.connect(self.hideLabel)
            self.parent_sidebar.onExpanded.connect(self.showLabel)

            self.parent_sidebar.onCollapsing.connect(self.hideLabel)
            self.parent_sidebar.onExpanding.connect(self.showLabel)

            self._animationDuration = self.parent_sidebar.animationDuration

            if self.parent_sidebar.isCollapsed():
                self.start_hide_animation()
            else:
                self.start_show_animation()
       

    def paintEvent(self, event: QPaintEvent):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


        self.validateIconAndLabel()
