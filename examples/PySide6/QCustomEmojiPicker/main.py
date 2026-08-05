"""QCustomEmojiPicker example.

Two editors (a QLineEdit and a QTextEdit) each with a picker button; the
picker inserts the chosen emoji into its target editor. Chrome comes from
Qss/scss + json-styles; the picker buttons use a themed SVG icon."""

import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomEmojiPicker import QCustomEmojiPicker
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication, QGraphicsDropShadowEffect


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        if s.value("THEME") is None:
            # A stray QSettings file (written before QApplication got its real
            # names) strips every theme's default flag — seed explicitly.
            s.setValue("THEME", "Nightfall")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self.ui.lineEditBtn.clicked.connect(
            lambda: self.showEmojiPicker(self.ui.lineEdit))
        self.ui.textEditBtn.clicked.connect(
            lambda: self.showEmojiPicker(self.ui.textEdit))

    def showEmojiPicker(self, target_widget):
        emoji_picker = QCustomEmojiPicker(target=target_widget, parent=self,
                                          itemsPerRow=16)
        emoji_picker.show()

        # Soft shadow so the floating picker separates from the window
        # (matches the original demo).  # allow-shadow: floating popup depth
        effect = emoji_picker.graphicsEffect()
        if effect is None:
            effect = QGraphicsDropShadowEffect(emoji_picker)  # allow-shadow: floating popup depth
        effect.setColor(QColor(30, 30, 30, 200))
        effect.setBlurRadius(20)
        effect.setXOffset(0)
        effect.setYOffset(0)
        emoji_picker.setGraphicsEffect(effect)  # allow-shadow: floating popup depth


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
