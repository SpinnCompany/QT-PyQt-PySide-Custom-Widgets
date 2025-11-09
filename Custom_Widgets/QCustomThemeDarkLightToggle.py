import re
from qtpy.QtWidgets import QPushButton
from qtpy.QtCore import Property
from qtpy.QtGui import QIcon

import os

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import get_icon_path

class QCustomThemeDarkLightToggle(QPushButton):
    # Icon path for the widget
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/theme_toggle.png")

    # Tooltip for the widget
    WIDGET_TOOLTIP = "Toggle between Dark and Light themes"
    
    # XML string for the widget
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomThemeDarkLightToggle" name="CustomThemeDarkLightToggle">
        <property name="geometry">
        <rect>
            <x>0</x>
            <y>0</y>
            <width>100</width>
            <height>30</height>
        </rect>
        </property>
        </widget>
    </ui>
    """
    WIDGET_MODULE = "Custom_Widgets.QCustomThemeDarkLightToggle"

    def __init__(self, parent=None, *args, **kwargs):
        super(QCustomThemeDarkLightToggle, self).__init__(parent)

        # Initialize button text and theme
        self._label_text = "Dark" if QCustomTheme.isAppDarkThemed() else "Light"
        self._update_label_text = True
        self._update_button_icon = True

        self._light_theme_icon = None
        self._dark_theme_icon = None

        self._light_theme_icon_file = None
        self._dark_theme_icon_file = None

        # Connect button click to toggle theme
        self.clicked.connect(self.toggle_theme)

        self.themeEngine = QCustomTheme() 

    def showEvent(self, event):
        super().showEvent(event)

        # Update button icon and text based
        self.update_button_icon()
        self.update_button_text()

    def toggle_theme(self):   
        self.themeEngine = QCustomTheme()      
        # Toggle theme based on current state
        new_theme = "Light" if QCustomTheme.isAppDarkThemed() else "Dark"
        self.themeEngine.theme = new_theme  # This updates the theme in QCustomTheme

        # Update button icon and text based on the new theme
        self.update_button_icon()
        self.update_button_text()
    
    def setText(self, text: str):
        # Override the setText method to only allow theme-based text changes
        if text in ["Dark", "Light"]:
            super().setText(text)  # Call the base class setText only for theme text

    def update_button_text(self):
        """Set the button text based on the current theme."""
        if not self._update_label_text:
            super().setText("")
            return
        # Update text based on the current theme
        if QCustomTheme.isAppDarkThemed():
            super().setText("Light")
        else:
            super().setText("Dark")
    
    def update_button_icon(self):
        """Update the button icon based on the current theme."""
        if not self._update_button_icon:
            return
        
        if QCustomTheme.isAppDarkThemed():
            if self._light_theme_icon is not None:
                self.setIcon(self._light_theme_icon)  # Light icon for dark theme
        else:
            if self._dark_theme_icon is not None:
                self.setIcon(self._dark_theme_icon)  # Dark icon for light theme
    
    @Property(bool)
    def updateLabelText(self):
        return self._update_label_text

    @updateLabelText.setter
    def updateLabelText(self, state: bool):
        self._update_label_text = state

    @Property(bool)
    def updateButtonIcon(self):
        return self._update_button_icon

    @updateButtonIcon.setter
    def updateButtonIcon(self, state: bool):
        self._update_button_icon = state
    
    @Property(QIcon)
    def darkThemeIcon(self):
        return self._dark_theme_icon

    @darkThemeIcon.setter
    def darkThemeIcon(self, icon: QIcon):
        self._dark_theme_icon = icon
        self.update_button_icon()

    @Property(QIcon)
    def lightThemeIcon(self):
        return self._light_theme_icon

    @lightThemeIcon.setter
    def lightThemeIcon(self, icon: QIcon):
        self._light_theme_icon = icon
        self.update_button_icon()
