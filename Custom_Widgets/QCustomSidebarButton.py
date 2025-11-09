from qtpy.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve, Property, Signal, QSize, QPoint, QTimer, QCoreApplication
from qtpy.QtWidgets import QPushButton, QWidget, QLabel, QStyleOption, QStyle, QHBoxLayout, QVBoxLayout, QSizePolicy, QGraphicsOpacityEffect, QSpacerItem, QApplication, QGraphicsDropShadowEffect
from qtpy.QtGui import QPainter, QIcon, QPaintEvent, QEnterEvent, QMouseEvent, QHoverEvent, QColor, QCursor
import os

# Import your custom sidebar and utility functions
from Custom_Widgets.QCustomSidebar import QCustomSidebar 
from Custom_Widgets.Utils import replace_url_prefix, is_in_designer, get_icon_path

class QCustomSidebarButton(QPushButton):
    clicked = Signal()

    # Define XML for Qt Designer
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/new_button.png")
    WIDGET_TOOLTIP = "A custom button that interacts with the sidebar"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomSidebarButton' name='customSidebarButton'>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomSidebarButton"

    def __init__(self, parent=None, *args):
        super().__init__(parent)

        # Install event filter for the whole application
        app = QCoreApplication.instance()
        if app is not None:
            app.installEventFilter(self)
        elif self.parent():
            self.parent().installEventFilter(self)

        # Store original text and icon for resetting
        self.original_text = ""
        self.original_icon = self.icon()
        self._label_hidden = False
        self._hideOnCollapse = True
        self._text_prefix_spaces = 5

        self._fading_out = False

        self._is_hovered = False
        self._floating_widget = None
        self._hover_timer = QTimer(self)
        self._hover_timer.setSingleShot(True)
        self._hover_timer.timeout.connect(self._show_floating_button)
        self._float_position = None


    @Property(bool)
    def hideOnCollapse(self):
        """Whether to hide this label when the sidebar collapses."""
        return self._hideOnCollapse

    @hideOnCollapse.setter
    def hideOnCollapse(self, hide):
        self._hideOnCollapse = hide

    @Property(int)
    def textPrefixSpaces(self):
        """Get number of spaces to prepend to the text."""
        return self._text_prefix_spaces

    @textPrefixSpaces.setter
    def textPrefixSpaces(self, num_spaces):
        """Set number of spaces to prepend to the text."""
        self._text_prefix_spaces = num_spaces

        self.update()

    # Define the property for labelHidden state
    @Property(bool)
    def labelHidden(self, designable = False):
        return self._label_hidden

    @labelHidden.setter
    def labelHidden(self, state):
        self._label_hidden = state
        self.style().unpolish(self)  # Refresh style
        self.style().polish(self)
        self.update()

    @Property(str, designable=True)
    def labelText(self):
        """Returns the label text for the button (read-only)."""
        return self.original_text or ""

    @labelText.setter
    def labelText(self, text):
        """Sets the original label text for the button."""
        self.original_text = text
        self.update()

    @property
    def text(self):
        return super().text()

    @text.setter
    def text(self, value):
        super().setText(value or 'Sidebar Button')

    def paintEvent(self, event: QPaintEvent):
        """Custom paint event to draw the button with opacity."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawControl(QStyle.CE_PushButton, opt, painter, self)

        if self.original_text and not self.labelHidden:  
            self.setText(self.original_text) 

        elif self.labelHidden:
            self.setText("**clear")

        self.update()
        
        super().paintEvent(event) 

    def setText(self, text):
        # print(text)
        """Override setText to store the raw text and apply the prefix spaces."""
        if text == "**clear":
            super().setText("")

        else:

            if self.original_text != text:
                self.labelText = text
            super().setText(self.getPrefixedText(text))

    def update(self):
        if self.original_text and not self.labelHidden:  
            self.setText(self.original_text) 

        elif self.labelHidden:
            self.setText("**clear")

        super().update()


    def getPrefixedText(self, text):
        return " " * self._text_prefix_spaces + text.lstrip()

    def connect_to_parent(self):
        """Connect to the closest QCustomSidebar parent if necessary."""
        self.parent_sidebar = self.parent()  # Start with the direct parent
        while self.parent_sidebar and not isinstance(self.parent_sidebar, QCustomSidebar):
            self.parent_sidebar = self.parent_sidebar.parent()  # Move up the hierarchy

        if self.parent_sidebar:
            self.parent_sidebar.onCollapsed.connect(self.hideButtonLabel)
            self.parent_sidebar.onExpanded.connect(self.showButtonLabel)

            self.parent_sidebar.onCollapsing.connect(self.showButtonLabel)
            self.parent_sidebar.onExpanding.connect(self.showButtonLabel)

            if self.parent_sidebar and self.parent_sidebar.isCollapsed():
                self.hideButtonLabel()
            else:
                self.showButtonLabel()

    def hideButtonLabel(self):
        """Hide the button label by clearing the text."""
        if not self.original_text:
            self.original_text = self.text()
        
        if self.original_text:
            self.setText("**clear")  # Clear the button text
            self.labelHidden = True

        # Set the custom property for labelHidden state
        self.labelHidden = True

    def hideButtonIcon(self):
        """Hide the button icon by setting it to an empty QIcon."""
        self.original_icon = self.icon()
        self.setIcon(QIcon())  # Set an empty icon

    def showButtonLabel(self):
        """Show the button label by restoring the original text."""
        if self.original_text:  # Check if there is original text to show
            self.setText(self.original_text)  # Restore the original text
            self.labelHidden = False

        # Unset the custom property for labelHidden state
        self.labelHidden = False

        self._fade_out_floating_button()


    def showButtonIcon(self):
        """Show the button icon by restoring the original icon."""
        if not self.original_icon.isNull():  # Check if there is an original icon to show
            self.setIcon(self.original_icon)  # Restore the original icon

    def showEvent(self, e):
        super().showEvent(e)
        self.connect_to_parent()
        # Adjust size and update the widget
        self.adjustSize()
        self.update()

        try:
            if self.parent_sidebar and self.parent_sidebar.isCollapsed():
                if not self.labelHidden:
                    self.hideButtonLabel()
            if self.parent_sidebar and self.parent_sidebar.isExpanded():
                if self.labelHidden:
                    self.showButtonLabel()
        except Exception as e:
            print(e)

    def enterEvent(self, event: QEnterEvent):
        """Show the button label when the button is hovered, even if the sidebar is collapsed."""
        #FIXME: self.parent_sidebar.isCollapsed() and self.parent_sidebar.isExpanded() do not always return the expected bool
        # print(self.parent_sidebar.isCollapsed(), self.parent_sidebar.isExpanded())
        if self.parent_sidebar and (self.parent_sidebar.isCollapsed() or not self.parent_sidebar.isExpanded()):
            # Start a timer to avoid immediate hover effect
            self._hover_timer.start(2000)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event to set _is_hovered to False."""
        # self._fade_out_floating_button()
        super().leaveEvent(event)

    def _delete_floating_button(self, e):
        """Hide the button label when the hover ends, return to original collapsed state."""
        if self._floating_widget:
            self._fade_out_floating_button()  # Fade out the floating button
        self._hover_timer.stop()  # Cancel any hover event in progress

    def _show_floating_button(self):
        """Show the floating button only if the mouse is still over the main button."""
        if not self.labelHidden:
            return
        # Check if the mouse is still over the main button
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            return  # Mouse is no longer hovering over the button, so don't show the floating button

        # If mouse is still over the button, create and display the floating button
        if not self._floating_widget:
            self._create_floating_button()

            self._floating_widget.show()
            self._floating_widget.setMinimumSize(self._floating_widget.sizeHint())
            self._floating_button.adjustSize()
            self._floating_widget.adjustSize()
            self._floating_widget.move(self._calculate_floating_position())


    def _create_floating_button(self):
        """Create the floating version of the button."""
        # Create a QWidget as the container
        self._floating_widget = QWidget(self)
        self._floating_widget.setObjectName("floatingButtonWidget") #for css styling
        # self._floating_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Create the QPushButton
        self._floating_button = QCustomSidebarButton(" " * self._text_prefix_spaces + self.original_text, self._floating_widget)
        self._floating_widget.hideOnCollapse = False
        self._floating_button.setIcon(self.icon())
        self._floating_button.setObjectName(self.objectName())

        # Create the shadow effect
        shadow = QGraphicsDropShadowEffect(self._floating_button)
        shadow.setBlurRadius(10)  # Set the blur radius for the shadow
        shadow.setColor(QColor(0, 0, 0, 160))  # Set the shadow color (can be customized)
        shadow.setOffset(0, 0)  # Set the offset for the shadow (horizontal, vertical)

        # Apply the shadow effect to the widget
        self._floating_button.setGraphicsEffect(shadow)
        
        # Create a QVBoxLayout
        layout = QVBoxLayout(self._floating_widget)
        layout.addWidget(self._floating_button)
        
        # Set the layout margins and spacing to zero
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Set the widget's layout
        self._floating_widget.setLayout(layout)
        # Raise the widget to the front
        self._floating_widget.raise_()
        self._floating_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self._floating_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.Popup)

        # 
        self._floating_button.showEvent = self._fade_in_floating_button

        # Connect events from the floating button to the main button's event handlers
        self._floating_button.mousePressEvent = self.mousePressEvent
        self._floating_button.mouseReleaseEvent = self.mouseReleaseEvent
        self._floating_button.enterEvent = self.enterEvent
        self._floating_button.leaveEvent = self.leaveEvent

        self._fading_out = False

    def _pass_event_to_main_button(self, event):
        """Pass all events from the floating button to the main button."""
        # Forward the event to the main button
        return super(QPushButton, self._floating_button).event(event)

    def _fade_in_floating_button(self, e = None):
        """Fade in the floating button."""
        if self._floating_widget and not self._fading_out:
            # fade animation
            self._opacityAni = QPropertyAnimation(self._floating_widget, b'windowOpacity', self._floating_widget)
            self._opacityAni.setDuration(500)
            self._opacityAni.setStartValue(0)
            self._opacityAni.setEndValue(1)
            self._opacityAni.start()

    def _fade_out_floating_button(self):
        """Fade out the floating button."""
        if self._fading_out:
            return

        if self._floating_widget:
            self._fading_out = True
            # fade animation
            self._opacityAni = QPropertyAnimation(self._floating_widget, b'windowOpacity', self._floating_widget)
            self._opacityAni.setDuration(500)
            self._opacityAni.setStartValue(1)
            self._opacityAni.setEndValue(0)
            self._opacityAni.finished.connect(self._hide_floating_button)
            self._opacityAni.start()

    def _hide_floating_button(self):
        """Hide the floating button after the fade-out."""
        if self._floating_widget:
            self._floating_widget.hide()  # Hide the button
            self._floating_widget.deleteLater()  # Schedule for deletion
            self._floating_widget = None  # Clear reference

    def _calculate_floating_position(self):
        """Calculate the exact relative position for the floating button."""
        # Get the position of the main button relative to its parent 
        floating_button_pos = self.mapToGlobal(QPoint(-10, -10))
        return floating_button_pos

    def resizeEvent(self, event):
        """Update floating button position on window resize."""
        if self._floating_widget:
            self._floating_widget.move(self._calculate_floating_position())
        super().resizeEvent(event)

    def moveEvent(self, event):
        """Update floating button position on window move."""
        if self._floating_widget:
            self._floating_widget.move(self._calculate_floating_position())
        super().moveEvent(event)

    def eventFilter(self, obj, event: QEvent):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick, QEvent.MouseMove):
            # Handle the mouse event here
            local_pos = self.mapFromGlobal(event.globalPos())
            if hasattr(self, "_floating_widget") and self._floating_widget and not self._floating_button.rect().contains(local_pos):
                self._fade_out_floating_button()

        return super().eventFilter(obj, event)
