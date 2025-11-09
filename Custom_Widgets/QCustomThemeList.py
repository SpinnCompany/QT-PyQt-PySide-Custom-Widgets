from qtpy.QtWidgets import QComboBox, QMainWindow
from qtpy.QtCore import Qt, Signal

from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.QAppSettings import QAppSettings

import os

class QCustomThemeList(QComboBox):
    # Icon path for the widget
    script_dir = os.path.dirname(os.path.realpath(__file__))
    WIDGET_ICON = os.path.join(script_dir, "components/icons/airplay.png")
    
    # Tooltip for the widget
    WIDGET_TOOLTIP = "A custom QComboBox for selecting themes"
    
    # XML string for the widget
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class="QCustomThemeList" name="CustomThemeList">
        <property name="geometry">
        <rect>
            <x>0</x>
            <y>0</y>
            <width>200</width>
            <height>30</height>
        </rect>
        </property>
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

        self.themeEngine = QCustomTheme()
        self._app_themes = self.themeEngine.themes
        new_theme_names = sorted(set(theme.name for theme in self.themeEngine.themes))
        self.populate_themes(new_theme_names)

        self.currentIndexChanged.connect(self.on_theme_changed)

        self.old_theme_names = []
        self.new_theme_names = []

    def populate_themes(self, new_theme_names):
        try:
            self.blockSignals(True)
            self.clear()
            for theme in new_theme_names:
                # self.remove_item_by_text(theme.name)
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
        self.adjustSize()

        try:
            self.themeEngine = QCustomTheme()
            self._app_themes = self.themeEngine.themes

            # Extract and sort the names from the existing and new themes
            self.new_theme_names = sorted(set(theme.name for theme in self.themeEngine.themes))
            # Compare the sorted lists of names
            if self.old_theme_names != self.new_theme_names:
                self.populate_themes(self.new_theme_names)
                self.old_theme_names = self.new_theme_names
                
        except Exception as e:
            print(f"Error: {e}")

    def paintEvent(self, event):
        super(QCustomThemeList, self).paintEvent(event)
        
        self.check_theme_updates()