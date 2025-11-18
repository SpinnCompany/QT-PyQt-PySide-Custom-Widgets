from qtpy.QtWidgets import QComboBox, QMainWindow
from qtpy.QtCore import Qt, Signal, Property

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.QAppSettings import QAppSettings

import os

class QCustomThemeList(QComboBox):
    # Icon path for the widget
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/palette.png")
    
    # Tooltip for the widget
    WIDGET_TOOLTIP = "A custom QComboBox for selecting themes"
    
    # XML string for the widget
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomThemeList" name="CustomThemeList">
        <property name="windowTitle">
        <string>Custom Theme List</string>
        </property>
        </widget>
    </ui>
    """

    WIDGET_MODULE="Custom_Widgets.QCustomThemeList"

    themeChanged = Signal(str)  # Custom signal for theme change

    def __init__(self, parent = None, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super(QCustomThemeList, self).__init__(parent)

        self.setDuplicatesEnabled(False)

        self._loadPredefinedThemes = False  # Default value
        self.themeEngine = QCustomTheme()
        self._app_themes = self.themeEngine.themes
        
        # Get initial themes based on loadPredefinedThemes setting
        new_theme_names = self.get_filtered_themes()
        self.populate_themes(new_theme_names)

        self.currentIndexChanged.connect(self.on_theme_changed)

        self.old_theme_names = []
        self.new_theme_names = []

    @Property(bool)
    def loadPredefinedThemes(self):
        """Get the loadPredefinedThemes property value"""
        return self._loadPredefinedThemes

    @loadPredefinedThemes.setter
    def loadPredefinedThemes(self, value):
        """Set the loadPredefinedThemes property value and refresh themes"""
        if self._loadPredefinedThemes != value:
            self._loadPredefinedThemes = value
            # Refresh the theme list when this property changes
            new_theme_names = self.get_filtered_themes()
            self.populate_themes(new_theme_names)

    def get_filtered_themes(self):
        """Get themes filtered based on loadPredefinedThemes setting"""
        if not self._loadPredefinedThemes:
            # Filter out predefined themes (where theme.predefined is True)
            filtered_themes = [theme.name for theme in self.themeEngine.themes 
                            if not theme.predefined]
            return sorted(filtered_themes)
        else:
            # Return all theme names
            all_theme_names = [theme.name for theme in self.themeEngine.themes]
            return sorted(all_theme_names)

    def populate_themes(self, new_theme_names):
        try:
            self.blockSignals(True)
            self.clear()
            for theme in new_theme_names:
                self.addItem(theme)
                
                if theme == self.themeEngine.theme:
                    # Select the matching theme
                    self.setCurrentText(theme)
            
            self.blockSignals(False)
                    
        except Exception as e:
            # print(e)
            pass

    def on_theme_changed(self, index):
        selected_theme = self.currentText()
        self.themeEngine.theme = selected_theme
        self.themeChanged.emit(selected_theme)  

    def check_theme_updates(self):
        # Use maximum available size
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        
        try:
            self.themeEngine = QCustomTheme()
            self._app_themes = self.themeEngine.themes

            # Get filtered themes based on loadPredefinedThemes setting
            self.new_theme_names = self.get_filtered_themes()
            
            # Compare the sorted lists of names
            if self.old_theme_names != self.new_theme_names:
                self.populate_themes(self.new_theme_names)
                self.old_theme_names = self.new_theme_names
                
        except Exception as e:
            print(f"Error: {e}")

    def showEvent(self, event):
        """Handle show event to adjust size and refresh themes"""
        super().showEvent(event)
        self.adjustSize()
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.check_theme_updates()

    def resizeEvent(self, event):
        """Handle resize event to use maximum available size"""
        super().resizeEvent(event)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def paintEvent(self, event):
        super(QCustomThemeList, self).paintEvent(event)
        
        self.check_theme_updates()