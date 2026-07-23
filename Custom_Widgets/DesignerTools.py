########################################################################
## DESIGNER TOOLS
##
## Dock panels installed into Qt Designer's main window when Designer is
## launched with the Custom_Widgets plugins - the Python counterpart of
## the tool plugins from https://github.com/PyQt5/QtDesignerPlugins:
##
##   - Log View     : library + Qt messages, live
##   - UI Workspace : the project's .ui files, double-click to open
##   - QSS Editor   : syntax highlighting, property autocomplete, basic
##                    checks, apply-to-open-forms (live preview styling)
##   - Custom Properties : selection-following rich editors (dropdowns,
##                    pickers) for custom widget properties, driven by
##                    each widget class's DESIGNER_CUSTOM_PROPS spec
##
## Everything is best-effort and must never break Designer startup.
########################################################################
import logging
import os
import re
import sys

from qtpy.QtCore import Qt, QObject, QTimer, Signal, QStringListModel
from qtpy.QtGui import (QAction, QColor, QFont, QSyntaxHighlighter,
                        QTextCharFormat, QTextCursor)
from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                            QDockWidget, QFileDialog, QHBoxLayout, QLabel,
                            QLineEdit, QListWidget, QListWidgetItem,
                            QMainWindow, QMenu, QPlainTextEdit, QPushButton,
                            QSizePolicy, QToolBar, QToolButton, QVBoxLayout,
                            QWidget)

from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import *


def _checkbox(text, checked):
    box = QCheckBox(text)
    box.setChecked(checked)
    return box

_tools = {}  # keep references alive inside Designer

QSS_PROPERTIES = [
    "alternate-background-color", "background", "background-color",
    "background-image", "background-repeat", "background-position",
    "border", "border-color", "border-image", "border-radius",
    "border-style", "border-width", "border-top", "border-right",
    "border-bottom", "border-left", "bottom", "color", "font",
    "font-family", "font-size", "font-style", "font-weight", "height",
    "icon-size", "image", "left", "margin", "margin-top", "margin-right",
    "margin-bottom", "margin-left", "max-height", "max-width",
    "min-height", "min-width", "outline", "padding", "padding-top",
    "padding-right", "padding-bottom", "padding-left", "position",
    "right", "selection-background-color", "selection-color", "spacing",
    "subcontrol-origin", "subcontrol-position", "text-align",
    "text-decoration", "top", "width",
]


########################################################################
## LOG VIEW
########################################################################
class _DockLogHandler(logging.Handler):
    """Feeds python logging records into the dock (thread-safe via signal)."""

    def __init__(self, emitter):
        super().__init__()
        self._emitter = emitter
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)s  %(message)s",
                                            datefmt="%H:%M:%S"))

    def emit(self, record):
        try:
            self._emitter.message.emit(record.levelno, self.format(record))
        except Exception:
            pass


class _LogEmitter2(QObject):
    message = Signal(int, str)


class LogViewDock(QDockWidget):
    """Log view with a footer: level filter, search, clear, and live
    warning/error counts."""

    _instance = None
    _LEVELS = [("All", 0), ("Info", logging.INFO),
               ("Warnings", logging.WARNING), ("Errors", logging.ERROR)]

    def __init__(self, parent=None):
        super().__init__("Custom Widgets - Logs", parent)
        self.setObjectName("customWidgetsLogDock")
        LogViewDock._instance = self
        self._records = []  # (levelno, text), capped
        self._warnings = 0
        self._errors = 0

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)

        self._view = QPlainTextEdit()
        self._view.setReadOnly(True)
        self._view.setMaximumBlockCount(5000)
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self._view.setFont(font)
        layout.addWidget(self._view)

        # --- footer nav ---
        footer = QHBoxLayout()
        self._levelBox = QComboBox()
        for label, _ in self._LEVELS:
            self._levelBox.addItem(label)
        self._levelBox.currentIndexChanged.connect(self._rerender)
        footer.addWidget(self._levelBox)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Filter messages...")
        self._search.textChanged.connect(self._rerender)
        footer.addWidget(self._search, 1)

        self._counts = QLabel()
        footer.addWidget(self._counts)

        copy = QToolButton()
        copy.setText("Copy")
        copy.setToolTip("Copy the visible log messages to the clipboard")
        copy.clicked.connect(self.copyToClipboard)
        footer.addWidget(copy)

        clear = QToolButton()
        clear.setText("Clear")
        clear.clicked.connect(self.clear)
        footer.addWidget(clear)
        layout.addLayout(footer)

        self.setWidget(container)
        self._updateCounts()

        self._emitter = _LogEmitter2()
        self._emitter.message.connect(self._onRecord)
        self._handler = _DockLogHandler(self._emitter)
        logging.getLogger().addHandler(self._handler)

    def copyToClipboard(self):
        """Copy the currently visible (filtered) log messages to the
        clipboard, falling back to all records if the view is empty."""
        text = self._view.toPlainText()
        if not text:
            text = "\n".join(
                t for levelno, t in self._records
                if self._passesFilter(levelno, t))
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)

    def clear(self):
        self._records.clear()
        self._warnings = self._errors = 0
        self._view.clear()
        self._updateCounts()

    def _onRecord(self, levelno, text):
        self._records.append((levelno, text))
        if len(self._records) > 5000:
            self._records = self._records[-5000:]
        if levelno >= logging.ERROR:
            self._errors += 1
        elif levelno >= logging.WARNING:
            self._warnings += 1
        self._updateCounts()
        if self._passesFilter(levelno, text):
            self._view.appendPlainText(text)

    def _passesFilter(self, levelno, text):
        min_level = self._LEVELS[self._levelBox.currentIndex()][1]
        if levelno < min_level:
            return False
        needle = self._search.text().strip().lower()
        return not needle or needle in text.lower()

    def _rerender(self):
        self._view.clear()
        self._view.appendPlainText("\n".join(
            text for levelno, text in self._records
            if self._passesFilter(levelno, text)))

    def _updateCounts(self):
        self._counts.setText(f"⚠ {self._warnings}  ✕ {self._errors}")

    @classmethod
    def raiseAndFilterErrors(cls):
        inst = cls._instance
        if inst is None:
            return
        inst.setVisible(True)
        inst.raise_()
        inst._levelBox.setCurrentIndex(3)  # Errors


########################################################################
## FORM TEMPLATES - "New Form..." starting points
########################################################################
def _tmpl_dashboard(cls_name):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>{cls_name}</class>
 <widget class="QCustomQMainWindow" name="{cls_name}">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>960</width><height>640</height></rect>
  </property>
  <property name="windowTitle"><string>{cls_name}</string></property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="mainLayout">
    <property name="spacing"><number>0</number></property>
    <item>
     <widget class="QCustomSidebar" name="leftMenu">
      <layout class="QVBoxLayout" name="menuLayout">
       <item>
        <widget class="QPushButton" name="menuBtn">
         <property name="text"><string>MENU</string></property>
        </widget>
       </item>
       <item>
        <widget class="QCustomSidebarButton" name="homeBtn">
         <property name="text"><string>Home</string></property>
        </widget>
       </item>
       <item>
        <widget class="QCustomSidebarButton" name="settingsBtn">
         <property name="text"><string>Settings</string></property>
        </widget>
       </item>
       <item>
        <spacer name="menuSpacer">
         <property name="orientation"><enum>Qt::Vertical</enum></property>
        </spacer>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QCustomQStackedWidget" name="mainPages">
      <widget class="QWidget" name="homePage">
       <layout class="QVBoxLayout" name="homeLayout">
        <item>
         <widget class="QLabel" name="homeTitle">
          <property name="text"><string>Home</string></property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="settingsPage">
       <layout class="QVBoxLayout" name="settingsLayout">
        <item>
         <widget class="QLabel" name="settingsTitle">
          <property name="text"><string>Settings</string></property>
         </widget>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <customwidgets>
  <customwidget>
   <class>QCustomQMainWindow</class><extends>QMainWindow</extends>
   <header>Custom_Widgets.QCustomQMainWindow</header><container>1</container>
  </customwidget>
  <customwidget>
   <class>QCustomSidebar</class><extends>QWidget</extends>
   <header>Custom_Widgets.QCustomSidebar</header><container>1</container>
  </customwidget>
  <customwidget>
   <class>QCustomSidebarButton</class><extends>QPushButton</extends>
   <header>Custom_Widgets.QCustomSidebarButton</header>
  </customwidget>
  <customwidget>
   <class>QCustomQStackedWidget</class><extends>QStackedWidget</extends>
   <header>Custom_Widgets.QCustomQStackedWidget</header><container>1</container>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
"""


def _tmpl_login(cls_name):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>{cls_name}</class>
 <widget class="QWidget" name="{cls_name}">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>420</width><height>520</height></rect>
  </property>
  <property name="windowTitle"><string>Sign in</string></property>
  <layout class="QVBoxLayout" name="outerLayout">
   <item>
    <spacer name="topSpacer">
     <property name="orientation"><enum>Qt::Vertical</enum></property>
    </spacer>
   </item>
   <item>
    <widget class="QFrame" name="loginCard">
     <layout class="QVBoxLayout" name="cardLayout">
      <item>
       <widget class="QLabel" name="titleLabel">
        <property name="text"><string>Welcome back</string></property>
        <property name="alignment"><set>Qt::AlignCenter</set></property>
       </widget>
      </item>
      <item>
       <widget class="QLineEdit" name="emailEdit">
        <property name="placeholderText"><string>Email</string></property>
       </widget>
      </item>
      <item>
       <widget class="QLineEdit" name="passwordEdit">
        <property name="placeholderText"><string>Password</string></property>
        <property name="echoMode"><enum>QLineEdit::Password</enum></property>
       </widget>
      </item>
      <item>
       <widget class="QCustomCheckBox" name="rememberCheck">
        <property name="text"><string>Remember me</string></property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="signInBtn">
        <property name="text"><string>Sign in</string></property>
       </widget>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <spacer name="bottomSpacer">
     <property name="orientation"><enum>Qt::Vertical</enum></property>
    </spacer>
   </item>
  </layout>
 </widget>
 <customwidgets>
  <customwidget>
   <class>QCustomCheckBox</class><extends>QCheckBox</extends>
   <header>Custom_Widgets.QCustomCheckBox</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
"""


def _tmpl_settings(cls_name):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>{cls_name}</class>
 <widget class="QWidget" name="{cls_name}">
  <property name="geometry">
   <rect><x>0</x><y>0</y><width>560</width><height>480</height></rect>
  </property>
  <property name="windowTitle"><string>Settings</string></property>
  <layout class="QVBoxLayout" name="outerLayout">
   <item>
    <widget class="QLabel" name="pageTitle">
     <property name="text"><string>Settings</string></property>
    </widget>
   </item>
   <item>
    <widget class="QCustomHorizontalSeparator" name="titleSeparator"/>
   </item>
   <item>
    <layout class="QFormLayout" name="formLayout">
     <item row="0" column="0">
      <widget class="QLabel" name="nameLabel">
       <property name="text"><string>Display name</string></property>
      </widget>
     </item>
     <item row="0" column="1">
      <widget class="QLineEdit" name="nameEdit"/>
     </item>
     <item row="1" column="0">
      <widget class="QLabel" name="notifyLabel">
       <property name="text"><string>Notifications</string></property>
      </widget>
     </item>
     <item row="1" column="1">
      <widget class="QCustomCheckBox" name="notifyCheck"/>
     </item>
     <item row="2" column="0">
      <widget class="QLabel" name="themeLabel">
       <property name="text"><string>Theme</string></property>
      </widget>
     </item>
     <item row="2" column="1">
      <widget class="QCustomThemeList" name="themeList"/>
     </item>
    </layout>
   </item>
   <item>
    <spacer name="bottomSpacer">
     <property name="orientation"><enum>Qt::Vertical</enum></property>
    </spacer>
   </item>
  </layout>
 </widget>
 <customwidgets>
  <customwidget>
   <class>QCustomCheckBox</class><extends>QCheckBox</extends>
   <header>Custom_Widgets.QCustomCheckBox</header>
  </customwidget>
  <customwidget>
   <class>QCustomHorizontalSeparator</class><extends>QWidget</extends>
   <header>Custom_Widgets.QCustomHorizontalSeparator</header>
  </customwidget>
  <customwidget>
   <class>QCustomThemeList</class><extends>QComboBox</extends>
   <header>Custom_Widgets.QCustomThemeList</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
"""


FORM_TEMPLATES = {
    "Blank (icons prewired)": None,  # -> ProjectMaker.create_ui_file
    "Dashboard (sidebar + pages)": _tmpl_dashboard,
    "Login": _tmpl_login,
    "Settings page": _tmpl_settings,
}


########################################################################
## UI FILES WORKSPACE
########################################################################
class WorkspaceDock(QDockWidget):
    """Lists the .ui files of ONE user-chosen folder (default: the project's
    ui/ folder), plus any forms the user opened or created. Deduplicated by
    real path - no giant recursive dump."""

    _instance = None  # so the bridge can push opened/created files here
    _SKIP = {".git", "__pycache__", "generated-files", "node_modules", "venv", ".venv"}

    def __init__(self, parent=None, project_dir=None):
        super().__init__("Custom Widgets - UI Workspace", parent)
        self.setObjectName("customWidgetsWorkspaceDock")
        WorkspaceDock._instance = self
        self._project_dir = os.path.abspath(project_dir or projectRoot())
        # Auto-detect: the project's ui/ folder (project root = the folder
        # `Custom_Widgets --start-designer` was called from, pinned via
        # CUSTOM_WIDGETS_PROJECT_ROOT). A folder the user chose earlier for
        # THIS project is remembered and wins.
        ui_dir = os.path.join(self._project_dir, "ui")
        self._folder = ui_dir if os.path.isdir(ui_dir) else self._project_dir
        saved = _layoutSettings().value(self._folderSettingsKey())
        if saved and os.path.isdir(saved):
            self._folder = saved
        self._extra = []  # files opened/created outside the folder (realpaths)

        container = QWidget()
        layout = QVBoxLayout(container)

        header = QHBoxLayout()
        self._folderLabel = QLabel()
        self._folderLabel.setToolTip("Folder the workspace lists .ui files from")
        header.addWidget(self._folderLabel, 1)
        ws_btn = QPushButton("Open Workspace...")
        ws_btn.setToolTip("Switch the WHOLE session to another project "
                          "folder (ui files, styles, themes, run target)")
        ws_btn.clicked.connect(lambda: _chooseWorkspace(self))
        header.addWidget(ws_btn)
        set_btn = QPushButton("Set Folder...")
        set_btn.setToolTip("Change only which folder's .ui files are listed")
        set_btn.clicked.connect(self._chooseFolder)
        header.addWidget(set_btn)
        layout.addLayout(header)

        self._list = QListWidget()
        self._list.itemDoubleClicked.connect(self._openItem)
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._showContextMenu)
        layout.addWidget(self._list)

        row = QHBoxLayout()
        new_btn = QPushButton("New Form...")
        new_btn.clicked.connect(self._newForm)
        row.addWidget(new_btn)
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        row.addWidget(refresh)
        layout.addLayout(row)

        self.setWidget(container)
        self.refresh()

    def setProjectDir(self, root):
        """Workspace switcher: re-point at another project root."""
        self._project_dir = os.path.abspath(root)
        ui_dir = os.path.join(self._project_dir, "ui")
        self._folder = ui_dir if os.path.isdir(ui_dir) else self._project_dir
        saved = _layoutSettings().value(self._folderSettingsKey())
        if saved and os.path.isdir(saved):
            self._folder = saved
        self._extra = []
        self.refresh()

    @classmethod
    def noteFile(cls, path):
        """Record a form opened/created via the bridge so it shows in the
        list even if it lives outside the chosen folder."""
        inst = cls._instance
        if inst is None or not path:
            return
        real = os.path.realpath(path)
        if os.path.dirname(real) != os.path.realpath(inst._folder) and real not in inst._extra:
            inst._extra.append(real)
        inst.refresh()

    def _folderSettingsKey(self):
        import hashlib
        digest = hashlib.sha1(self._project_dir.encode("utf-8")).hexdigest()[:12]
        return f"workspace/folder-{digest}"

    def _chooseFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Choose UI folder", self._folder)
        if folder:
            self._folder = folder
            _layoutSettings().setValue(self._folderSettingsKey(), folder)
            self.refresh()

    def _newForm(self):
        from qtpy.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout)
        dialog = QDialog(self)
        dialog.setWindowTitle("New Form")
        form = QFormLayout(dialog)
        name_edit = QLineEdit("untitled")
        form.addRow("Form name:", name_edit)
        tmpl_combo = QComboBox()
        tmpl_combo.addItems(list(FORM_TEMPLATES))
        form.addRow("Template:", tmpl_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)
        if dialog.exec() != QDialog.Accepted:
            return
        base = "".join(c if c.isalnum() or c in "-_" else "_"
                       for c in name_edit.text().strip()) or "untitled"
        builder = FORM_TEMPLATES[tmpl_combo.currentText()]
        try:
            if builder is None:
                from Custom_Widgets.ProjectMaker import create_ui_file
                prev = os.getcwd()
                os.chdir(self._project_dir)
                try:
                    create_ui_file(base)
                finally:
                    os.chdir(prev)
            else:
                os.makedirs(self._folder, exist_ok=True)
                path = os.path.join(self._folder, base + ".ui")
                if os.path.exists(path):
                    logWarning(f"Workspace: {path} already exists")
                    return
                with open(path, "w", encoding="utf-8") as f:
                    f.write(builder(base))
                logInfo(f"Workspace: created {os.path.basename(path)} "
                        f"({tmpl_combo.currentText()})")
            self.refresh()
        except Exception as e:
            logException(e, message="Workspace: failed to create form")

    def refresh(self):
        self._folderLabel.setText("📁 " + os.path.relpath(self._folder, self._project_dir)
                                  if self._folder.startswith(self._project_dir)
                                  else "📁 " + self._folder)
        self._list.clear()
        seen = set()
        paths = []
        # deduped, sorted files from the chosen folder (recursive, filtered)
        for root, dirs, files in os.walk(self._folder):
            dirs[:] = [d for d in dirs if d not in self._SKIP]
            for name in files:
                if name.lower().endswith(".ui") and not name.startswith("new_"):
                    paths.append(os.path.join(root, name))
        for real in self._extra:  # opened/created elsewhere
            if os.path.exists(real):
                paths.append(real)
        for path in sorted(paths, key=lambda p: os.path.basename(p).lower()):
            real = os.path.realpath(path)
            if real in seen:
                continue
            seen.add(real)
            item = QListWidgetItem(os.path.relpath(path, self._project_dir)
                                   if path.startswith(self._project_dir)
                                   else os.path.basename(path))
            item.setToolTip(path)
            self._list.addItem(item)

    def _openItem(self, item):
        self._open(item.toolTip())

    def _showContextMenu(self, pos):
        item = self._list.itemAt(pos)
        if item is None:
            return
        path = item.toolTip()
        menu = QMenu(self._list)
        openAct = menu.addAction("Open in Designer")
        openAct.setToolTip("Opens the form in this Designer instance")
        menu.addSeparator()
        editAct = menu.addAction("Open in Editor")
        revealAct = menu.addAction("Reveal in File Manager")
        copyAct = menu.addAction("Copy Path")
        menu.addSeparator()
        refreshAct = menu.addAction("Refresh List")
        # Act on the CHOSEN action only after exec_() returns, i.e. after the
        # menu's nested event loop has fully unwound. Connecting to triggered
        # would run the handler while still inside that loop; opening a form
        # from there builds its custom widgets on a deep, re-entrant stack and
        # segfaults shiboken (see _open / faulthandler analysis).
        chosen = menu.exec_(self._list.viewport().mapToGlobal(pos))
        if chosen is None:
            return
        if chosen is openAct:
            self._open(path)
        elif chosen is editAct:
            self._openInEditor(path)
        elif chosen is revealAct:
            self._reveal(path)
        elif chosen is copyAct:
            QApplication.clipboard().setText(path)
        elif chosen is refreshAct:
            self.refresh()

    def _open(self, path):
        # Defer the real work to a clean stack. Opening a form synthesizes a
        # drop event that drives Designer's form builder to instantiate the
        # form's custom widgets. Doing that re-entrantly - from inside a
        # QMenu.exec_() popup loop or directly off a QListWidget signal - builds
        # the custom widget on a deep, nested call stack, and shiboken's wrapper
        # allocation segfaults there (confirmed via faulthandler). Running it
        # from the main event loop via singleShot(0) unwinds that nesting first.
        from qtpy.QtCore import QTimer
        QTimer.singleShot(0, lambda: self._openNow(path))

    def _openNow(self, path):
        # Open through the bridge. It opens plain forms in-instance via a
        # synthetic drop, and custom-widget forms in-instance via the safe
        # captured-core route (the drop path segfaults while building custom
        # widgets - see DesignerBridge._openViaDropEvent). Both keep the form
        # in THIS Designer instance; only a hard failure falls back to a new
        # process.
        try:
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            bridge = startDesignerBridge()
            opened = bridge.openFiles([path], new_process=False)
            logInfo(f"Workspace opened: {opened}")
        except Exception as e:
            logException(e, message="Workspace: failed to open form")

    def _openInEditor(self, path):
        """VS Code when available, else the OS default handler."""
        import shutil as _shutil
        import subprocess as _subprocess
        code = _shutil.which("code") or _shutil.which("codium")
        try:
            if code:
                _subprocess.Popen([code, path])
            else:
                from qtpy.QtGui import QDesktopServices
                from qtpy.QtCore import QUrl
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        except Exception as e:
            logException(e, message="Workspace: open in editor failed")

    def _reveal(self, path):
        try:
            from qtpy.QtGui import QDesktopServices
            from qtpy.QtCore import QUrl
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))
        except Exception as e:
            logException(e, message="Workspace: failed to reveal path")


########################################################################
## QSS EDITOR
########################################################################
class QssHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        def fmt(color, bold=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            return f

        self._rules = [
            (re.compile(r'\b[A-Z]\w+\b'), fmt("#569cd6", bold=True)),      # widget types
            (re.compile(r'::?[a-z-]+'), fmt("#c586c0")),                   # pseudo/subcontrol
            (re.compile(r'#\w+'), fmt("#4ec9b0")),                         # ids / hex colors
            (re.compile(r'\b[a-z-]+(?=\s*:)'), fmt("#9cdcfe")),            # properties
            (re.compile(r':\s*[^;{}]+'), fmt("#ce9178")),                  # values
            (re.compile(r'\$[A-Z_]+'), fmt("#dcdcaa", bold=True)),         # scss vars
            (re.compile(r'/\*.*?\*/', re.DOTALL), fmt("#6a9955")),         # comments
        ]

    def highlightBlock(self, text):
        for pattern, char_format in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), char_format)


class _CodeEditor(QPlainTextEdit):
    """QPlainTextEdit with the editor keys people expect: Tab/Shift+Tab
    (indent), Ctrl+/ (toggle comment), Ctrl+D (duplicate line), Ctrl+S
    (save), auto-indent on Enter, plus completer key routing."""

    INDENT = "    "

    def __init__(self, parent=None):
        super().__init__(parent)
        self._completer = None
        self._saveCallback = None
        self._extraShortcuts = {}  # Qt.Key -> callback, all with Ctrl

    def setCompleter(self, completer):
        self._completer = completer
        completer.setWidget(self)
        completer.activated.connect(self._insertCompletion)

    def setSaveCallback(self, cb):
        self._saveCallback = cb

    def bindShortcut(self, key, callback):
        """Bind Ctrl+<key> to a callback, handled by the editor itself."""
        self._extraShortcuts[key] = callback

    def _ownedCtrlKeys(self):
        return {Qt.Key_S, Qt.Key_D, Qt.Key_Slash} | set(self._extraShortcuts)

    def event(self, event):
        # Claim the editor's Ctrl-combos as ShortcutOverride so they are
        # delivered here as keyPressEvent, instead of being swallowed - or made
        # ambiguous - by window/application shortcuts (e.g. Designer's own
        # Ctrl+S). Without this, Ctrl+S in the QSS editor can silently do
        # nothing.
        from qtpy.QtCore import QEvent
        if event.type() == QEvent.ShortcutOverride:
            if (event.modifiers() & Qt.ControlModifier) and \
                    event.key() in self._ownedCtrlKeys():
                event.accept()
                return True
        return super().event(event)

    def _insertCompletion(self, completion):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.insertText(completion + ": ")
        self.setTextCursor(cursor)

    def _currentWord(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()

    def keyPressEvent(self, event):
        from qtpy.QtCore import Qt
        popup = self._completer.popup() if self._completer else None

        # While the completion popup is visible, let it consume nav/accept keys
        if popup is not None and popup.isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab,
                               Qt.Key_Escape, Qt.Key_Up, Qt.Key_Down):
                event.ignore()
                return

        ctrl = event.modifiers() & Qt.ControlModifier
        shift = event.modifiers() & Qt.ShiftModifier

        # Bound window shortcuts (Ctrl+O/N/Return...) - handled here so they
        # work reliably from inside the editor, without shortcut ambiguity.
        if ctrl and event.key() in self._extraShortcuts:
            self._extraShortcuts[event.key()]()
            return
        if ctrl and event.key() == Qt.Key_S:
            if self._saveCallback:
                self._saveCallback()
            return
        if ctrl and event.key() == Qt.Key_Slash:
            self._toggleComment()
            return
        if ctrl and event.key() == Qt.Key_D:
            self._duplicateLine()
            return
        if event.key() == Qt.Key_Tab and not ctrl:
            if self._indentSelection(1):
                return
            self.insertPlainText(self.INDENT)
            return
        if event.key() == Qt.Key_Backtab or (event.key() == Qt.Key_Tab and shift):
            self._indentSelection(-1)
            return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._autoIndentNewline()
            return

        super().keyPressEvent(event)

        # trigger completion on typed identifier chars
        if self._completer and event.text() and event.text().isprintable():
            word = self._currentWord()
            if len(word) >= 2:
                self._completer.setCompletionPrefix(word)
                if self._completer.completionCount():
                    rect = self.cursorRect()
                    rect.setWidth(self._completer.popup().sizeHintForColumn(0) + 24)
                    self._completer.complete(rect)
                else:
                    self._completer.popup().hide()
            elif self._completer.popup():
                self._completer.popup().hide()

    def _selectedLineSpan(self):
        cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        cursor.setPosition(start)
        first = cursor.blockNumber()
        cursor.setPosition(end)
        last = cursor.blockNumber()
        return first, last

    def _indentSelection(self, direction):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return False
        first, last = self._selectedLineSpan()
        cursor.beginEditBlock()
        doc = self.document()
        for line in range(first, last + 1):
            block = doc.findBlockByNumber(line)
            c = self.textCursor()
            c.setPosition(block.position())
            if direction > 0:
                c.insertText(self.INDENT)
            else:
                text = block.text()
                strip = len(text) - len(text.lstrip(" "))
                remove = min(strip, len(self.INDENT))
                for _ in range(remove):
                    c.deleteChar()
        cursor.endEditBlock()
        return True

    def _toggleComment(self):
        cursor = self.textCursor()
        first, last = self._selectedLineSpan()
        doc = self.document()
        lines = [doc.findBlockByNumber(n).text() for n in range(first, last + 1)]
        commented = all(l.strip().startswith("/*") and l.strip().endswith("*/")
                        for l in lines if l.strip())
        cursor.beginEditBlock()
        for n in range(first, last + 1):
            block = doc.findBlockByNumber(n)
            c = self.textCursor()
            c.setPosition(block.position())
            c.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            text = block.text()
            if not text.strip():
                continue
            if commented:
                new = text.replace("/*", "", 1).rsplit("*/", 1)
                new = "".join(new)
            else:
                indent = text[:len(text) - len(text.lstrip())]
                new = f"{indent}/* {text.strip()} */"
            c.insertText(new)
        cursor.endEditBlock()

    def _duplicateLine(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.LineUnderCursor)
        text = cursor.selectedText()
        cursor.movePosition(QTextCursor.EndOfLine)
        cursor.insertText("\n" + text)
        cursor.endEditBlock()

    def _autoIndentNewline(self):
        cursor = self.textCursor()
        line = cursor.block().text()
        indent = line[:len(line) - len(line.lstrip(" "))]
        if line.rstrip().endswith("{"):
            indent += self.INDENT
        cursor.insertText("\n" + indent)


class QssEditorWindow(QMainWindow):
    """Standalone (undockable) QSS / theme editor window with a menu bar and a
    top toolbar.

    A file list on the left switches between the project's .scss files;
    GENERATED files (main.scss, _styles.scss, _variables.scss) open READ-ONLY
    (preview) so users can't corrupt the theme machinery. Edits to your own
    files (defaultStyle.scss and imports) compile live (qtsass) and apply to
    the open form previews - and, with 'Paint entire Designer', to the whole
    Designer. Styles live in scss, never inline in .ui files."""

    # Generated / system files - preview only.
    READ_ONLY = {"main.scss", "_styles.scss", "_variables.scss"}

    def __init__(self, parent=None, project_dir=None):
        super().__init__(parent)
        self.setObjectName("customWidgetsQssWindow")
        # A real top-level window: movable, resizable, undockable.
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Custom Widgets — QSS / Theme Editor")
        self._project_dir = os.path.abspath(project_dir or projectRoot())
        self._scss_dir = os.path.join(self._project_dir, "Qss", "scss")
        self._path = os.path.join(self._scss_dir, "defaultStyle.scss")
        self._read_only = False
        self._centered = False

        # ---- actions (shared by the menu bar and the top toolbar) ----
        def _mk(text, slot, shortcut=None, tip=None):
            act = QAction(text, self)
            act.triggered.connect(slot)
            if shortcut:
                act.setShortcut(shortcut)
            if tip:
                act.setToolTip(tip)
            return act

        self._openAct = _mk("📂  Open…", self._open, "Ctrl+O",
                            "Open a stylesheet")
        self._newAct = _mk("✚  New Style…", self._newStyleFile, "Ctrl+N",
                           "Create a new .scss and @import it")
        self._saveAct = _mk("💾  Save", self._save, "Ctrl+S", "Save the file")
        self._checkAct = _mk("✓  Check", self._check, None,
                             "Lint the current buffer")
        self._applyAct = _mk("▶  Apply", self._apply, "Ctrl+Return",
                             "Compile and apply to the open form previews")
        close_act = _mk("Close", self.close, "Ctrl+W")

        self._autoApply = QAction("Auto-compile && apply on change", self)
        self._autoApply.setCheckable(True)
        self._autoApply.setChecked(True)
        self._autoApply.toggled.connect(lambda *_: self._scheduleApply())

        self._repaintDesigner = QAction("🎨  Paint entire Designer", self)
        self._repaintDesigner.setCheckable(True)
        self._repaintDesigner.setToolTip(
            "Apply the current theme to the whole Designer (and every open "
            "form). Uncheck to clear it.")
        self._repaintDesigner.toggled.connect(lambda *_: self._applyPaintDesigner())

        # ---- menu bar (top) ----
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self._openAct)
        file_menu.addAction(self._newAct)
        file_menu.addAction(self._saveAct)
        file_menu.addSeparator()
        file_menu.addAction(close_act)
        style_menu = menubar.addMenu("&Style")
        style_menu.addAction(self._checkAct)
        style_menu.addAction(self._applyAct)
        style_menu.addSeparator()
        style_menu.addAction(self._autoApply)
        style_menu.addAction(self._repaintDesigner)

        # ---- top toolbar (the "top nav") ----
        toolbar = QToolBar("QSS", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(self._openAct)
        toolbar.addAction(self._newAct)
        toolbar.addAction(self._saveAct)
        toolbar.addSeparator()
        toolbar.addAction(self._checkAct)
        toolbar.addAction(self._applyAct)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addAction(self._repaintDesigner)
        self.addToolBar(toolbar)

        # ---- central: file list | editor ----
        central = QWidget()
        root = QHBoxLayout(central)

        left = QVBoxLayout()
        left.addWidget(QLabel("Style files"))
        self._fileList = QListWidget()
        self._fileList.setMaximumWidth(230)
        self._fileList.currentItemChanged.connect(self._onFileSelected)
        left.addWidget(self._fileList)
        root.addLayout(left)

        editor_col = QVBoxLayout()
        self._fileLabel = QLabel()
        editor_col.addWidget(self._fileLabel)
        self._editor = _CodeEditor()
        self._editor.setPlaceholderText(
            "Default styles (Qss/scss/defaultStyle.scss)...\n"
            "Tab/Shift+Tab indent · Ctrl+/ comment · Ctrl+D duplicate · Ctrl+S save")
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self._editor.setFont(font)
        self._highlighter = QssHighlighter(self._editor.document())
        self._editor.setSaveCallback(self._save)
        # Route the window shortcuts through the editor so they work reliably
        # from inside it (Ctrl+S is the save callback above).
        self._editor.bindShortcut(Qt.Key_O, self._open)
        self._editor.bindShortcut(Qt.Key_N, self._newStyleFile)
        self._editor.bindShortcut(Qt.Key_Return, self._apply)
        self._editor.bindShortcut(Qt.Key_Enter, self._apply)
        editor_col.addWidget(self._editor)
        root.addLayout(editor_col, 1)

        self.setCentralWidget(central)
        self.resize(1000, 700)

        completer = QCompleter(QStringListModel(QSS_PROPERTIES, self))
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._editor.setCompleter(completer)

        # debounce live compile/apply
        self._applyTimer = QTimer(self)
        self._applyTimer.setSingleShot(True)
        self._applyTimer.setInterval(500)
        self._applyTimer.timeout.connect(self._apply)
        self._editor.textChanged.connect(self._scheduleApply)

        self._refreshFileList()
        self._loadDefault()  # open the default style by default

    # --- file handling --------------------------------------------------
    def setProjectDir(self, root):
        """Workspace switcher: edit the new project's default stylesheet."""
        self._project_dir = os.path.abspath(root)
        self._scss_dir = os.path.join(self._project_dir, "Qss", "scss")
        self._path = os.path.join(self._scss_dir, "defaultStyle.scss")
        self._refreshFileList()
        self._loadDefault()

    def _isReadOnly(self, path):
        return os.path.basename(path) in self.READ_ONLY

    def _refreshFileList(self):
        """List every .scss/.qss/.css in the project's scss folder. Generated
        files are flagged read-only (🔒), editable ones with ✎."""
        self._fileList.blockSignals(True)
        self._fileList.clear()
        try:
            names = sorted(f for f in os.listdir(self._scss_dir)
                           if f.endswith((".scss", ".qss", ".css")))
        except Exception:
            names = []
        for name in names:
            ro = name in self.READ_ONLY
            item = QListWidgetItem(("🔒 " if ro else "✎ ") + name)
            item.setData(Qt.UserRole, os.path.join(self._scss_dir, name))
            item.setToolTip("Generated file - preview only" if ro
                            else "Editable")
            self._fileList.addItem(item)
        self._fileList.blockSignals(False)

    def _onFileSelected(self, current, previous=None):
        if current is None:
            return
        path = current.data(Qt.UserRole)
        if path and os.path.isfile(path) and os.path.abspath(path) != os.path.abspath(self._path):
            self._load(path)

    def _loadDefault(self):
        os.makedirs(self._scss_dir, exist_ok=True)
        if not os.path.exists(self._path):
            with open(self._path, "w", encoding="utf-8") as f:
                f.write("// Project default styles (override theme styles)\n"
                        "// New style files are @import-ed here automatically.\n")
        self._load(self._path)

    def showFile(self, path, content=None):
        """Open the editor and DISPLAY `path` so an agent's style edits made
        over MCP are visible live to the user. Refreshes the file list first
        (so a newly-created .scss shows up). If `content` is given it is shown
        directly (stream a change in before/without a disk read)."""
        try:
            self._refreshFileList()
            self.openFloating()
            if content is not None:
                self._editor.setReadOnly(self._isReadOnly(path))
                self._editor.setPlainText(content)
                self._path = path
                rel = os.path.relpath(path, self._project_dir)
                self._fileLabel.setText("✎ " + rel)
                for i in range(self._fileList.count()):
                    item = self._fileList.item(i)
                    if os.path.abspath(item.data(Qt.UserRole)) == os.path.abspath(path):
                        self._fileList.blockSignals(True)
                        self._fileList.setCurrentItem(item)
                        self._fileList.blockSignals(False)
                        break
            elif path and os.path.isfile(path):
                self._load(path)
        except Exception as e:
            logException(e, message="QSS editor: showFile failed")

    def _load(self, path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            self._editor.setPlainText(f.read())
        self._path = path
        self._read_only = self._isReadOnly(path)
        # Preview-only for generated files: no editing, no saving.
        self._editor.setReadOnly(self._read_only)
        self._saveAct.setEnabled(not self._read_only)
        rel = os.path.relpath(path, self._project_dir)
        self._fileLabel.setText(("🔒 " + rel + "   —   read-only (preview)")
                                if self._read_only else ("✎ " + rel))
        # Keep the list selection in sync with programmatic loads.
        for i in range(self._fileList.count()):
            item = self._fileList.item(i)
            if os.path.abspath(item.data(Qt.UserRole)) == os.path.abspath(path):
                self._fileList.blockSignals(True)
                self._fileList.setCurrentItem(item)
                self._fileList.blockSignals(False)
                break

    def _inScssDir(self, path):
        """True if `path` lives inside the project's Qss/scss folder. All
        stylesheets are kept there for uniformity."""
        try:
            root = os.path.abspath(self._scss_dir)
            return os.path.abspath(path).startswith(root + os.sep)
        except Exception:
            return False

    def _open(self):
        # Only stylesheets from the project's Qss/scss folder may be opened -
        # styles must live there for uniformity. The dialog starts there; a
        # file chosen outside it is rejected (use 'New Style' to add one).
        path, _ = QFileDialog.getOpenFileName(
            self, "Open stylesheet (from Qss/scss/)", self._scss_dir,
            "Styles (*.scss *.qss *.css)")
        if not path:
            return
        if not self._inScssDir(path):
            logWarning("QSS editor: stylesheets must live in Qss/scss/ for "
                       f"uniformity - '{os.path.basename(path)}' is outside "
                       "that folder and was not opened.")
            return
        self._load(path)

    def _newStyleFile(self):
        """Create a new .scss INSIDE the project's Qss/scss folder (styles are
        kept there for uniformity) and @import it into defaultStyle.scss. Only
        a file NAME is asked for - any path the user types is stripped, so the
        file always lands in Qss/scss/."""
        from qtpy.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(
            self, "New style file", "Name (created in Qss/scss/):",
            text="custom.scss")
        if not ok:
            return
        # Strip any directory the user typed - the file stays in the folder.
        name = os.path.basename(name.strip())
        if not name:
            return
        if not name.endswith(".scss"):
            name += ".scss"
        if name in self.READ_ONLY:
            logWarning(f"QSS editor: '{name}' is a reserved generated file.")
            return
        os.makedirs(self._scss_dir, exist_ok=True)
        path = os.path.join(self._scss_dir, name)
        if os.path.exists(path):
            logWarning(f"QSS editor: {name} already exists - opening it.")
            self._refreshFileList()
            self._load(path)
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"// {name} - imported into defaultStyle.scss\n")
        self._ensureImport(name)
        self._refreshFileList()
        self._load(path)
        logInfo(f"QSS editor: created {name} and imported it into defaultStyle.scss")

    def _ensureImport(self, name):
        """Add `@import '<name>';` to defaultStyle.scss if missing."""
        default_path = os.path.join(self._scss_dir, "defaultStyle.scss")
        stem = name[:-5] if name.endswith(".scss") else name
        import_line = f"@import '{stem}';"
        content = ""
        if os.path.exists(default_path):
            with open(default_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        if import_line not in content:
            with open(default_path, "a", encoding="utf-8") as f:
                f.write(f"\n{import_line}\n")

    def _save(self):
        if self._read_only:
            logWarning(f"QSS editor: {os.path.basename(self._path)} is a "
                       "generated file - read-only (preview). Edit "
                       "defaultStyle.scss or your own imported files instead.")
            return
        if not self._inScssDir(self._path):
            logWarning("QSS editor: refusing to save outside Qss/scss/ - "
                       "stylesheets are kept in that folder for uniformity.")
            return
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(self._editor.toPlainText())
            logInfo(f"QSS editor: saved {os.path.relpath(self._path, self._project_dir)}")
            if self._autoApply.isChecked():
                self._apply()
        except Exception as e:
            logException(e, message="QSS editor: save failed")

    # --- lint -----------------------------------------------------------
    def _check(self):
        text = self._editor.toPlainText()
        problems = []
        if text.count("{") != text.count("}"):
            problems.append(f"unbalanced braces: {text.count('{')} '{{' vs {text.count('}')} '}}'")
        known = set(QSS_PROPERTIES)
        for line_no, line in enumerate(text.splitlines(), 1):
            match = re.match(r'\s*([a-z-]+)\s*:', line)
            if match and match.group(1) not in known and not match.group(1).startswith("qproperty"):
                problems.append(f"line {line_no}: unknown property '{match.group(1)}'")
        if problems:
            for problem in problems[:20]:
                logWarning(f"QSS check: {problem}")
        else:
            logInfo("QSS check: no problems found")

    # --- compile & apply ------------------------------------------------
    def _scheduleApply(self):
        if self._autoApply.isChecked():
            self._applyTimer.start()

    def _compile(self):
        """Compile the current buffer (SCSS) to CSS, resolving @imports from
        the scss folder and the theme's _variables.scss when present."""
        import qtsass
        source = self._editor.toPlainText()
        variables = os.path.join(self._scss_dir, "_variables.scss")
        if os.path.exists(variables):
            with open(variables, encoding="utf-8", errors="ignore") as f:
                source = f.read() + "\n" + source
        return qtsass.compile(source, include_paths=[self._scss_dir])

    def _apply(self):
        # Apply the edited buffer to the open form previews...
        try:
            css = self._compile()
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            startDesignerBridge()._setStyleSheet(css)
        except Exception as e:
            detail = None
            try:
                from Custom_Widgets.JSonStyles.tokens import \
                    describe_scss_compile_error
                # The buffer @imports resolve from the scss folder; also walk
                # main.scss so a dangling @import in an imported partial is caught.
                detail = describe_scss_compile_error(
                    os.path.join(self._scss_dir, "main.scss"), [self._scss_dir], e)
            except Exception:
                pass
            logWarning(f"QSS compile error: {detail or str(e).splitlines()[0]}")
        # ...and (independently) paint the whole Designer with the full theme.
        self._applyPaintDesigner()

    def _compileFullTheme(self):
        """Compile the FULL current theme - Qss/scss/main.scss (library base
        styles + the theme's _variables + your defaultStyle overrides) - so
        'Paint entire Designer' reflects the whole theme, not just the (usually
        empty) defaultStyle buffer. Falls back to the last generated main.css,
        then to the editor buffer."""
        import qtsass
        main_scss = os.path.join(self._scss_dir, "main.scss")
        if os.path.exists(main_scss):
            try:
                with open(main_scss, encoding="utf-8", errors="ignore") as f:
                    source = f.read()
                return qtsass.compile(source, include_paths=[self._scss_dir])
            except Exception as e:
                logWarning("QSS: full-theme compile failed "
                           f"({str(e).splitlines()[0]}); using generated CSS")
        generated = os.path.join(self._project_dir, "generated-files",
                                 "css", "main.css")
        if os.path.exists(generated):
            with open(generated, encoding="utf-8", errors="ignore") as f:
                return f.read()
        return self._compile()  # last resort: the editor buffer

    def _applyPaintDesigner(self):
        """Paint the ENTIRE Designer with the full current theme, or clear it
        when unchecked. Independent of the editor buffer so it always takes
        effect."""
        try:
            css = self._compileFullTheme() if self._repaintDesigner.isChecked() else ""
            self._paintEntireDesigner(css)
        except Exception as e:
            logException(e, message="QSS editor: paint entire Designer failed")

    def _paintEntireDesigner(self, css):
        """Apply (or clear) an APPLICATION-level stylesheet. Qt propagates an
        app-level stylesheet to every widget, so the whole Designer - chrome
        and every open form - takes the current theme. Passing "" removes it."""
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(css)

    def openFloating(self):
        """Show the editor window: centre it the first time, then just raise it
        so the user's position/size are kept. It is a standalone top-level
        window, opened from the Designer footer (never docked)."""
        if not self._centered:
            self._centered = True
            try:
                screen = QApplication.primaryScreen()
                if screen is not None:
                    center = screen.availableGeometry().center()
                    self.move(center.x() - self.width() // 2,
                              center.y() - self.height() // 2)
            except Exception as e:
                logDebug(f"QSS editor: positioning failed: {e}")
        self.showNormal()
        self.raise_()
        self.activateWindow()
        # Focus the editor so keystrokes (and its shortcuts) go to it.
        self._editor.setFocus()


########################################################################
## CUSTOM PROPERTIES
##
## A selection-following dock: click any Custom_Widgets widget on a form
## and this panel shows its custom properties with RICH editors - theme
## dropdown (style.json names), widget-reference dropdowns (matching
## widgets in the open form), color pickers, spin boxes - all applied
## through the form cursor (undo-aware, persisted to the .ui on save).
## Driven by the widget class's DESIGNER_CUSTOM_PROPS spec; the native
## property editor keeps showing the same properties as plain fields.
########################################################################

def _matchingWidgetNames(container, type_names):
    """objectNames of widgets under `container` inheriting any of
    `type_names` - the choices for a widget-ref dropdown."""
    if container is None:
        return []
    names = []
    for child in container.findChildren(QWidget):
        name = child.objectName()
        if not name or name.startswith("qt_"):
            continue
        if any(child.inherits(t) for t in type_names):
            if name not in names:
                names.append(name)
    return sorted(names)


class CustomPropertiesDock(QDockWidget):
    """'Custom Properties' pane - one place to edit every custom property
    of the selected Custom_Widgets widget."""

    def __init__(self, parent=None):
        super().__init__("Custom Properties", parent)
        self.setObjectName("CustomWidgetsPropertiesDock")
        self._widget = None      # the selected custom widget
        self._connected = set()  # form windows already hooked up (by id)

        from qtpy.QtWidgets import QScrollArea
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        body = QWidget()
        self._layout = QVBoxLayout(body)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)
        self._scroll.setWidget(body)
        self.setWidget(self._scroll)

        self._header = QLabel("")
        self._header.setStyleSheet("font-weight: bold;")
        self._placeholder = QLabel(
            "Select a Custom Widgets widget on a form\n"
            "to edit its custom properties here.")
        self._placeholder.setWordWrap(True)
        self._rebuild()

        # The form-editor core is captured by the registrars before the
        # docks install, but retry briefly in case of ordering surprises.
        self._attachCore()

    # ------------------------------------------------------------------
    # Selection tracking
    # ------------------------------------------------------------------
    def _core(self):
        try:
            from Custom_Widgets.DesignerBridge import formEditorCore
            return formEditorCore()
        except Exception:
            return None

    def _attachCore(self, attempt=0):
        core = self._core()
        if core is None:
            if attempt < 20:
                QTimer.singleShot(500, lambda: self._attachCore(attempt + 1))
            else:
                logWarning("Custom Properties dock: form editor core "
                           "unavailable; selection tracking disabled")
            return
        try:
            manager = core.formWindowManager()
            manager.activeFormWindowChanged.connect(self._onFormWindow)
            for i in range(manager.formWindowCount()):
                self._onFormWindow(manager.formWindow(i))
            if manager.activeFormWindow() is not None:
                self._onFormWindow(manager.activeFormWindow())
            logInfo("Custom Properties dock: selection tracking active")
        except Exception as e:
            logException(e, message="Custom Properties dock: core attach failed")

    def _onFormWindow(self, fw):
        if fw is None:
            return
        if id(fw) not in self._connected:
            self._connected.add(id(fw))
            try:
                fw.selectionChanged.connect(
                    lambda fw=fw: self._onSelectionChanged(fw))
                fw.destroyed.connect(
                    lambda _=None, key=id(fw): self._connected.discard(key))
            except Exception as e:
                logDebug(f"Custom Properties dock: connect failed: {e}")
        self._onSelectionChanged(fw)

    def _onSelectionChanged(self, fw):
        try:
            cursor = fw.cursor()
            target = None
            for i in range(cursor.selectedWidgetCount()):
                candidate = cursor.selectedWidget(i)
                if hasattr(type(candidate), "DESIGNER_CUSTOM_PROPS"):
                    target = candidate
                    break
            if target is None:
                container = fw.mainContainer()
                if container is not None and \
                        hasattr(type(container), "DESIGNER_CUSTOM_PROPS") and \
                        cursor.selectedWidgetCount() == 0:
                    target = container
            self.setTargetWidget(target)
        except RuntimeError as e:
            # The form window (or its cursor) is a C++ object that Qt deleted
            # out from under us - this fires routinely when a form is replaced
            # while a selection-changed signal is still in flight. Benign, so
            # swallow it silently instead of logging noise every reload.
            if "already deleted" in str(e).lower():
                return
            logDebug(f"Custom Properties dock: selection read failed: {e}")
        except Exception as e:
            logDebug(f"Custom Properties dock: selection read failed: {e}")

    # ------------------------------------------------------------------
    # Panel building
    # ------------------------------------------------------------------
    def setTargetWidget(self, widget):
        """Show `widget`'s custom properties (None -> placeholder). Public:
        the right-click task menu calls this before raising the dock."""
        self._widget = widget
        self._rebuild()

    def _clearLayout(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            child = item.widget()
            if child is not None and child not in (self._header, self._placeholder):
                child.deleteLater()
        self._header.setParent(None)
        self._placeholder.setParent(None)

    def _rebuild(self):
        self._clearLayout()
        widget = self._widget
        if widget is None or not hasattr(type(widget), "DESIGNER_CUSTOM_PROPS"):
            self._layout.addWidget(self._placeholder)
            self._placeholder.show()
            self._layout.addStretch(1)
            return
        name = widget.objectName() or "(unnamed)"
        self._header.setText(f"{type(widget).__name__}  —  {name}")
        self._layout.addWidget(self._header)
        self._header.show()

        groups = {}
        for spec in type(widget).DESIGNER_CUSTOM_PROPS:
            groups.setdefault(spec.get("group", "General"), []).append(spec)
        for group, specs in groups.items():
            label = QLabel(group)
            label.setStyleSheet("color: palette(mid); margin-top: 8px;")
            self._layout.addWidget(label)
            for spec in specs:
                row = self._buildRow(widget, spec)
                if row is not None:
                    self._layout.addWidget(row)
        self._layout.addStretch(1)

    def _buildRow(self, widget, spec):
        try:
            name = spec["name"]
            kind = spec.get("kind", "str")
            current = widget.property(name)
            row = QWidget()
            hbox = QHBoxLayout(row)
            hbox.setContentsMargins(0, 0, 0, 0)
            title = QLabel(name)
            title.setMinimumWidth(120)
            title.setToolTip(name)
            hbox.addWidget(title)
            hbox.addWidget(self._buildEditor(widget, name, kind, spec, current), 1)
            return row
        except Exception as e:
            logDebug(f"Custom Properties dock: row for {spec} failed: {e}")
            return None

    def _buildEditor(self, widget, name, kind, spec, current):
        from qtpy.QtWidgets import QSpinBox
        if kind == "choice":
            # Fixed choice set: spec["enum"] (an IntEnum class - labels are
            # member names, stored value is the int) or spec["choices"] (a
            # list of strings, stored as-is).
            combo = QComboBox()
            enum_cls = spec.get("enum")
            if enum_cls is not None:
                for member in enum_cls:
                    combo.addItem(member.name, int(member))
                try:
                    index = combo.findData(int(current))
                    combo.setCurrentIndex(index if index >= 0 else 0)
                except (TypeError, ValueError):
                    pass
            else:
                for choice in spec.get("choices", []):
                    combo.addItem(str(choice), str(choice))
                value = str(current) if current is not None else ""
                index = combo.findData(value)
                if index >= 0:
                    combo.setCurrentIndex(index)
            combo.activated.connect(
                lambda _i, c=combo: self._apply(name, c.currentData()))
            return combo
        if kind == "float":
            from qtpy.QtWidgets import QDoubleSpinBox
            spin = QDoubleSpinBox()
            spin.setRange(-9999.0, 9999.0)
            spin.setDecimals(spec.get("decimals", 2))
            spin.setSingleStep(spec.get("step", 0.1))
            try:
                spin.setValue(float(current or 0.0))
            except (TypeError, ValueError):
                pass
            spin.editingFinished.connect(
                lambda s=spin: self._apply(name, s.value()))
            return spin
        if kind == "easing":
            # Property holding a QEasingCurve.Type - offer the curve names.
            # Stores the int value, or the NAME when the spec sets
            # "string": True (for str-typed easing properties).
            from qtpy.QtCore import QEasingCurve
            as_string = bool(spec.get("string"))
            combo = QComboBox()
            members = [(t.name, t.value) for t in QEasingCurve.Type
                       if t.value <= QEasingCurve.Type.OutInBounce.value]
            for label, value in members:
                combo.addItem(label, label if as_string else value)
            if as_string:
                index = combo.findData(str(current))
                if index >= 0:
                    combo.setCurrentIndex(index)
            else:
                try:
                    index = combo.findData(int(current))
                    combo.setCurrentIndex(index if index >= 0 else 0)
                except (TypeError, ValueError):
                    pass
            combo.activated.connect(
                lambda _i, c=combo: self._apply(name, c.currentData()))
            return combo
        if kind == "file":
            box = QWidget()
            hbox = QHBoxLayout(box)
            hbox.setContentsMargins(0, 0, 0, 0)
            edit = QLineEdit(str(current) if current else "")
            edit.editingFinished.connect(
                lambda e=edit: self._apply(name, e.text()))
            browse = QToolButton()
            browse.setText("...")

            def pick(_=False, e=edit):
                path, _filter = QFileDialog.getOpenFileName(
                    self, name, e.text() or projectRoot(),
                    spec.get("filter", "All files (*)"))
                if path:
                    # Keep project files relative to the project dir (cwd).
                    rel = os.path.relpath(path, projectRoot())
                    value = rel if not rel.startswith("..") else path
                    e.setText(value)
                    self._apply(name, value)
            browse.clicked.connect(pick)
            hbox.addWidget(edit, 1)
            hbox.addWidget(browse)
            return box
        if kind == "theme":
            from Custom_Widgets.DesignerExtensions import readThemeNames
            combo = QComboBox()
            names = readThemeNames()
            combo.addItems(names)
            if current in names:
                combo.setCurrentText(str(current))
            combo.activated.connect(
                lambda _i, c=combo: self._apply(name, c.currentText()))
            return combo
        if kind == "widget-ref":
            combo = QComboBox()
            combo.addItem("")  # = not set
            for ref in _matchingWidgetNames(self._formContainer(widget),
                                            spec.get("types", ("QWidget",))):
                combo.addItem(ref)
            value = str(current) if current else ""
            if value and combo.findText(value) < 0:
                combo.addItem(value)  # keep values not (yet) in this form
            combo.setCurrentText(value)
            combo.activated.connect(
                lambda _i, c=combo: self._apply(name, c.currentText()))
            return combo
        if kind == "bool":
            box = QCheckBox()
            box.setChecked(bool(current))
            box.toggled.connect(lambda checked: self._apply(name, checked))
            return box
        if kind == "int":
            spin = QSpinBox()
            spin.setRange(-9999, 9999)
            try:
                spin.setValue(int(current or 0))
            except (TypeError, ValueError):
                pass
            spin.editingFinished.connect(
                lambda s=spin: self._apply(name, s.value()))
            return spin
        if kind == "color":
            button = QPushButton()
            color = QColor(current) if current is not None else QColor()
            self._paintColorButton(button, color)
            button.clicked.connect(
                lambda _=False, b=button: self._pickColor(name, b))
            return button
        # default: plain string
        edit = QLineEdit(str(current) if current is not None else "")
        edit.editingFinished.connect(lambda e=edit: self._apply(name, e.text()))
        return edit

    def _paintColorButton(self, button, color):
        text = color.name() if color.isValid() else "(none)"
        button.setText(text)
        if color.isValid():
            luma = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
            fg = "#000" if luma > 128 else "#fff"
            button.setStyleSheet(
                f"background-color: {color.name()}; color: {fg};")

    def _pickColor(self, name, button):
        from qtpy.QtWidgets import QColorDialog
        current = QColor(self._widget.property(name)) if self._widget else QColor()
        color = QColorDialog.getColor(current, self, f"{name}")
        if color.isValid():
            self._paintColorButton(button, color)
            self._apply(name, color)

    # ------------------------------------------------------------------
    # Applying values
    # ------------------------------------------------------------------
    def _formContainer(self, widget):
        try:
            from qtpy.QtDesigner import QDesignerFormWindowInterface
            fw = QDesignerFormWindowInterface.findFormWindow(widget)
            if fw is not None:
                return fw.mainContainer()
        except Exception:
            pass
        return widget.window() if widget is not None else None

    def _apply(self, name, value):
        widget = self._widget
        if widget is None:
            return
        try:
            from qtpy.QtDesigner import QDesignerFormWindowInterface
            fw = QDesignerFormWindowInterface.findFormWindow(widget)
            if fw is not None:
                # Undo-aware, marks the form dirty, saved to the .ui.
                fw.cursor().setWidgetProperty(widget, name, value)
            else:
                widget.setProperty(name, value)
            logInfo(f"Custom Properties dock: {name} = {value!r}")
        except Exception as e:
            logException(e, message=f"Custom Properties dock: applying {name} failed")


def raiseCustomProperties(widget=None):
    """Show + raise the Custom Properties dock, optionally focused on
    `widget`. Used by the right-click task menu (DesignerExtensions)."""
    dock = _tools.get("customprops")
    if dock is None:
        return False
    if widget is not None:
        dock.setTargetWidget(widget)
    dock.setVisible(True)
    dock.raise_()
    return True


########################################################################
## RUN CONTROLLER - the project's app, from inside Designer
##
## Runs `main.py` under the DevServer supervisor (Custom_Widgets --dev)
## as a QProcess, so while the app is running every form save in Designer
## regenerates src/ui_*.py and hot-restarts the app. Output streams into
## the Logs dock as "[app]" lines; a crash raises the dock.
########################################################################
class RunController(QObject):
    stateChanged = Signal(bool)  # running?

    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        RunController._instance = self
        self._proc = None
        self._tail = []  # last app-output lines for the MCP bridge

    # -- helpers --------------------------------------------------------
    def script(self):
        return os.path.join(projectRoot(), "main.py")

    def available(self):
        return os.path.isfile(self.script())

    def isRunning(self):
        from qtpy.QtCore import QProcess
        return self._proc is not None and \
            self._proc.state() != QProcess.NotRunning

    @staticmethod
    def _pythonPath():
        """A real python interpreter. Inside pyside6-designer sys.executable
        is the designer binary, so look next to it, then fall back to PATH."""
        import shutil as _shutil
        exe_dir = os.path.dirname(sys.executable)
        for name in ("python3", "python", "python.exe"):
            candidate = os.path.join(exe_dir, name)
            if os.path.isfile(candidate):
                return candidate
        return _shutil.which("python3") or _shutil.which("python") or "python3"

    # -- lifecycle ------------------------------------------------------
    def start(self):
        if self.isRunning():
            return True
        if not self.available():
            logWarning(f"Run: no main.py in {projectRoot()}")
            return False
        from qtpy.QtCore import QProcess, QProcessEnvironment
        proc = QProcess(self)
        proc.setWorkingDirectory(projectRoot())
        env = QProcessEnvironment.systemEnvironment()
        env.insert("CUSTOM_WIDGETS_PROJECT_ROOT", projectRoot())
        proc.setProcessEnvironment(env)
        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.readyReadStandardOutput.connect(self._onOutput)
        proc.finished.connect(self._onFinished)
        proc.start(self._pythonPath(),
                   ["-m", "Custom_Widgets.CMD", "--dev", self.script()])
        if not proc.waitForStarted(5000):
            logError("Run: could not start the dev server process")
            return False
        self._proc = proc
        logInfo("Run: app started under the dev server (form saves "
                "hot-restart it)")
        self.stateChanged.emit(True)
        return True

    def stop(self):
        if not self.isRunning():
            return
        logInfo("Run: stopping app")
        self._proc.terminate()  # SIGTERM -> DevServer tears down the app
        if not self._proc.waitForFinished(4000):
            self._proc.kill()
            self._proc.waitForFinished(2000)

    def restart(self):
        self.stop()
        self.start()

    # -- plumbing -------------------------------------------------------
    def _onOutput(self):
        if self._proc is None:
            return
        data = bytes(self._proc.readAllStandardOutput()).decode(
            "utf-8", errors="replace")
        logs = _tools.get("logs")
        for line in data.splitlines():
            if not line.strip():
                continue
            self._tail.append(line)
            if len(self._tail) > 500:
                self._tail = self._tail[-500:]
            if logs is not None:
                level = logging.ERROR if ("Traceback" in line or
                                          "Error" in line) else logging.INFO
                logs._onRecord(level, f"[app] {line}")

    def _onFinished(self, code, _status):
        logInfo(f"Run: dev server exited (code {code})")
        self._proc = None
        self.stateChanged.emit(False)
        if code not in (0,):  # crash -> surface the logs
            logs = _tools.get("logs")
            if logs is not None:
                logs.setVisible(True)
                logs.raise_()

    def appLogs(self, lines=100):
        return self._tail[-lines:]


def _applyPreviewTheme(name):
    """Toolbar theme switch: apply `appTheme` on an open QCustomQMainWindow
    form through the form cursor (undo-aware, same as the Custom Properties
    dock). Never restyles Designer's own chrome."""
    try:
        from Custom_Widgets.DesignerBridge import formEditorCore
        core = formEditorCore()
        if core is None:
            logWarning("Theme: form editor core unavailable")
            return
        manager = core.formWindowManager()
        for i in range(manager.formWindowCount()):
            fw = manager.formWindow(i)
            container = fw.mainContainer()
            if container is not None and \
                    container.metaObject().indexOfProperty("appTheme") >= 0:
                fw.cursor().setWidgetProperty(container, "appTheme", name)
                logInfo(f"Theme: '{name}' applied to "
                        f"{os.path.basename(fw.fileName() or 'form')}")
                return
        logWarning("Theme: open a QCustomQMainWindow form to preview themes")
    except Exception as e:
        logException(e, message="Theme: preview switch failed")


def _addRunToolbar(window):
    """'Custom Widgets' toolbar: Run/Stop/Restart the project app under the
    dev server, live theme preview combo, and a state indicator."""
    from qtpy.QtWidgets import QToolBar
    from qtpy.QtGui import QKeySequence

    runner = RunController(window)
    bar = QToolBar("Custom Widgets", window)
    bar.setObjectName("customWidgetsRunToolbar")

    run_act = bar.addAction("▶ Run")
    run_act.setToolTip("Run main.py under the dev server (F5).\n"
                       "Form saves regenerate + hot-restart the app.")
    run_act.setShortcut(QKeySequence("F5"))
    run_act.triggered.connect(runner.start)

    stop_act = bar.addAction("⏹ Stop")
    stop_act.setToolTip("Stop the running app (Shift+F5)")
    stop_act.setShortcut(QKeySequence("Shift+F5"))
    stop_act.triggered.connect(runner.stop)

    restart_act = bar.addAction("↻ Restart")
    restart_act.setToolTip("Restart the running app")
    restart_act.triggered.connect(runner.restart)

    bar.addSeparator()
    bar.addWidget(QLabel(" Theme: "))
    theme_combo = QComboBox()
    theme_combo.setToolTip("Preview a style.json theme on the open form")
    try:
        from Custom_Widgets.DesignerExtensions import readThemeNames
        theme_combo.addItems(readThemeNames())
    except Exception:
        pass
    theme_combo.activated.connect(
        lambda _i: _applyPreviewTheme(theme_combo.currentText()))
    bar.addWidget(theme_combo)

    bar.addSeparator()
    ws_label = QLabel(f" 📂 {os.path.basename(projectRoot())} ")
    ws_label.setToolTip(f"Workspace: {projectRoot()}")
    bar.addWidget(ws_label)
    _tools["workspace_label"] = ws_label

    bar.addSeparator()
    state = QLabel(" ○ app stopped ")
    state.setToolTip("State of the project app run from Designer")
    bar.addWidget(state)

    def on_state(running):
        state.setText(" ● app running " if running else " ○ app stopped ")
        run_act.setEnabled(not running)
        stop_act.setEnabled(running)
        restart_act.setEnabled(running)

    runner.stateChanged.connect(on_state)
    on_state(False)
    if not runner.available():
        run_act.setEnabled(False)
        run_act.setToolTip("No main.py found in the project folder")

    window.addToolBar(bar)
    _tools["runner"] = runner
    _tools["run_toolbar"] = bar
    _tools["run_action"] = run_act
    _tools["theme_combo"] = theme_combo


########################################################################
## WORKSPACE SWITCHER - open a different project without restarting
########################################################################
def _recentWorkspaces():
    value = _layoutSettings().value("workspace/recent") or []
    if isinstance(value, str):
        value = [value]
    return [w for w in value if os.path.isdir(w)]


def _rememberWorkspace(root):
    recents = [root] + [w for w in _recentWorkspaces() if w != root]
    _layoutSettings().setValue("workspace/recent", recents[:8])


def switchWorkspace(root):
    """Re-point the whole Designer session at another project: root (env +
    Project), workspace listing, QSS editor, bridge socket, theme combo and
    Run availability. Everything that resolves projectRoot() lazily follows
    automatically."""
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        logWarning(f"Workspace: not a folder: {root}")
        return False
    try:
        from Custom_Widgets.Project import setProjectRoot
        setProjectRoot(root)
        os.environ["CUSTOM_WIDGETS_PROJECT_ROOT"] = root  # child processes

        if "workspace" in _tools:
            _tools["workspace"].setProjectDir(root)
        if "qss" in _tools:
            _tools["qss"].setProjectDir(root)

        try:
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            startDesignerBridge().rebindProject(root)
        except Exception as e:
            logDebug(f"Workspace: bridge rebind failed: {e}")

        combo = _tools.get("theme_combo")
        if combo is not None:
            try:
                from Custom_Widgets.DesignerExtensions import readThemeNames
                combo.clear()
                combo.addItems(readThemeNames(root))
            except Exception:
                pass

        runner = _tools.get("runner")
        run_act = _tools.get("run_action")
        if runner is not None and run_act is not None and not runner.isRunning():
            run_act.setEnabled(runner.available())
            run_act.setToolTip(
                "Run main.py under the dev server (F5)" if runner.available()
                else "No main.py found in the project folder")
        ws_label = _tools.get("workspace_label")
        if ws_label is not None:
            ws_label.setText(f" 📂 {os.path.basename(root)} ")
            ws_label.setToolTip(f"Workspace: {root}")

        _rememberWorkspace(root)
        _refreshRecentMenu()
        logInfo(f"Workspace switched to: {root}")
        return True
    except Exception as e:
        logException(e, message="Workspace switch failed")
        return False


def _chooseWorkspace(parent=None):
    folder = QFileDialog.getExistingDirectory(
        parent, "Open Workspace (project folder)", projectRoot())
    if folder:
        switchWorkspace(folder)


_recent_menu = None


def _refreshRecentMenu():
    global _recent_menu
    if _recent_menu is None:
        return
    try:
        import shiboken6
        if not shiboken6.isValid(_recent_menu):
            _recent_menu = None
            return
        _recent_menu.clear()
        recents = _recentWorkspaces()
        if not recents:
            _recent_menu.addAction("(empty)").setEnabled(False)
            return
        for root in recents:
            action = _recent_menu.addAction(root)
            action.triggered.connect(lambda _=False, r=root: switchWorkspace(r))
    except Exception as e:
        logDebug(f"Recent workspaces menu refresh failed: {e}")
        _recent_menu = None


########################################################################
## DOCK LAYOUT - defaults + persistence
########################################################################
_LAYOUT_VERSION = 2  # bumped: QSS editor is no longer a dock (floating window)


def _layoutSettings():
    from qtpy.QtCore import QSettings
    return QSettings("CustomWidgets", "DesignerTools")


def _nativePropertyEditorDock(window):
    for dock in window.findChildren(QDockWidget):
        title = dock.windowTitle().replace("&", "").strip().lower()
        if title.startswith("property editor"):
            return dock
    return None


def _applyDefaultLayout(window):
    """Uncongested defaults: Custom Properties tabs NEXT TO Designer's own
    Property Editor; Workspace+QSS share one tabbed slot; Logs hidden (the
    status-bar footer reopens it, and it auto-raises on errors)."""
    native_prop = _nativePropertyEditorDock(window)
    if native_prop is not None:
        window.tabifyDockWidget(native_prop, _tools["customprops"])
    else:
        window.addDockWidget(Qt.RightDockWidgetArea, _tools["customprops"])
    window.addDockWidget(Qt.RightDockWidgetArea, _tools["workspace"])
    # The QSS editor is a standalone top-level window (not a dock) - opened
    # from the footer button; nothing to place here.
    window.addDockWidget(Qt.BottomDockWidgetArea, _tools["logs"])
    _tools["logs"].hide()
    _tools["customprops"].raise_()


def _saveLayout(window):
    try:
        settings = _layoutSettings()
        settings.setValue("layout/state", window.saveState(_LAYOUT_VERSION))
        settings.setValue("layout/version", _LAYOUT_VERSION)
    except Exception as e:
        logDebug(f"Designer tools: layout save failed: {e}")


def _restoreLayout(window):
    """True when a previously saved arrangement was restored."""
    try:
        settings = _layoutSettings()
        if int(settings.value("layout/version", -1)) != _LAYOUT_VERSION:
            return False
        state = settings.value("layout/state")
        return bool(state) and window.restoreState(state, _LAYOUT_VERSION)
    except Exception:
        return False


def _resetLayout(window):
    _layoutSettings().remove("layout/state")
    _applyDefaultLayout(window)
    for key in ("workspace", "customprops"):
        _tools[key].show()


class _LayoutSaver(QObject):
    """Persists the dock arrangement when Designer's main window closes."""

    def __init__(self, window):
        super().__init__(window)
        self._window = window
        window.installEventFilter(self)

    def eventFilter(self, obj, event):
        from qtpy.QtCore import QEvent
        if obj is self._window and event.type() == QEvent.Close:
            _saveLayout(self._window)
        return False


########################################################################
## INSTALLATION
########################################################################
def _designerMainWindow():
    app = QApplication.instance()
    if app is None:
        return None
    candidates = [w for w in app.topLevelWidgets()
                  if isinstance(w, QMainWindow) and w.menuBar() is not None]
    for window in candidates:
        if "designer" in window.metaObject().className().lower() \
                or "designer" in window.windowTitle().lower():
            return window
    return candidates[0] if candidates else None


def _addViewMenu(window):
    """Put show/hide toggles for the custom panes into the menu bar - in
    Designer's own View menu when present, else a 'Custom Widgets' menu."""
    menu_bar = window.menuBar()
    if menu_bar is None:
        return
    target = None
    for action in menu_bar.actions():
        if action.text().replace("&", "").strip().lower() in ("view", "views"):
            target = action.menu()
            break
    if target is None:
        target = menu_bar.addMenu("Custom &Widgets")
    else:
        target.addSeparator()
    for key in ("workspace", "customprops", "logs"):
        target.addAction(_tools[key].toggleViewAction())
    # QSS editor is a standalone window, not a dock - give it a menu entry too.
    qss_act = target.addAction("QSS / Theme Editor")
    qss_act.triggered.connect(lambda: _tools["qss"].openFloating()
                              if "qss" in _tools else None)
    # Workspace actions live in OUR OWN top-level menu: Designer rebuilds
    # its View menu dynamically, which destroys submenus we parent there.
    own = menu_bar.addMenu("&Workspace")
    open_ws = own.addAction("Open Workspace...")
    open_ws.triggered.connect(lambda: _chooseWorkspace(window))
    global _recent_menu
    _recent_menu = own.addMenu("Recent Workspaces")
    _refreshRecentMenu()
    own.addSeparator()
    reset = own.addAction("Reset Custom Widgets Layout")
    reset.triggered.connect(lambda: _resetLayout(window))


def _addStatusFooter(window):
    """A footer strip in Designer's status bar: quick access to the Logs
    pane, a live warning/error count that opens errors on click, and the
    latest message."""
    try:
        status = window.statusBar()
        if status is None:
            return

        qss_btn = QToolButton()
        qss_btn.setText("🎨 QSS Editor")
        qss_btn.setToolTip("Open the QSS / theme editor in a floating window")
        qss_btn.clicked.connect(
            lambda: _tools["qss"].openFloating() if "qss" in _tools else None)
        status.addPermanentWidget(qss_btn)

        logs_btn = QToolButton()
        logs_btn.setText("Logs")
        logs_btn.setToolTip("Show the Custom Widgets log pane")
        logs_btn.clicked.connect(lambda: (_tools["logs"].setVisible(True),
                                          _tools["logs"].raise_()))
        status.addPermanentWidget(logs_btn)

        errors_btn = QToolButton()
        errors_btn.setToolTip("Filter the log to errors")
        errors_btn.clicked.connect(LogViewDock.raiseAndFilterErrors)
        status.addPermanentWidget(errors_btn)

        latest = QLabel("")
        latest.setMinimumWidth(220)
        status.addWidget(latest)

        def on_record(levelno, text):
            errors_btn.setText(f"⚠ {_tools['logs']._warnings}  ✕ {_tools['logs']._errors}")
            latest.setText(text.split("  ", 1)[-1][:80])
        _tools["logs"]._emitter.message.connect(on_record)
        errors_btn.setText("⚠ 0  ✕ 0")
    except Exception as e:
        logException(e, message="Designer tools: status footer failed")


def _install(attempt=0):
    window = _designerMainWindow()
    if window is None:
        if attempt < 20:  # Designer's main window appears after plugin load
            QTimer.singleShot(500, lambda: _install(attempt + 1))
        else:
            logWarning("Designer tools: main window not found, docks not installed")
        return
    # Both registrar plugins call this, and Designer loads them as isolated
    # module instances (separate _tools globals), so guard on the shared
    # window itself - set the flag BEFORE the await-free dock creation so two
    # timers firing in the same tick can't both pass.
    if window.property("customWidgetsToolsInstalled") or _tools:
        return
    window.setProperty("customWidgetsToolsInstalled", True)
    try:
        _tools["logs"] = LogViewDock(window)
        _tools["workspace"] = WorkspaceDock(window)
        _tools["qss"] = QssEditorWindow(window)
        _tools["customprops"] = CustomPropertiesDock(window)
        # Uncongested defaults (Custom Properties tabs beside Designer's own
        # Property Editor); a saved user arrangement wins when present.
        _applyDefaultLayout(window)
        if _restoreLayout(window):
            logInfo("Designer tools: restored saved dock layout")
        # The QSS editor is a standalone window - keep it hidden until the
        # footer button opens it.
        _tools["qss"].hide()
        _LayoutSaver(window)
        _addRunToolbar(window)
        _addViewMenu(window)
        _rememberWorkspace(projectRoot())
        _refreshRecentMenu()
        _addStatusFooter(window)
        logInfo("Designer tools installed: Logs, UI Workspace, QSS Editor, "
                "Custom Properties, Run toolbar")
        # Designer pops a modal "New Form" dialog on launch. Here it is
        # redundant (the Workspace dock creates/opens forms) and, being modal,
        # it sits in front and blocks autonomous / MCP-driven control until a
        # human closes it. Dismiss it shortly after startup.
        for delay in (200, 900, 1800):
            QTimer.singleShot(delay, _dismissStartupNewForm)
    except Exception as e:
        logException(e, message="Designer tools installation failed")


def _dismissStartupNewForm():
    """Close Designer's startup 'New Form' dialog if it is showing."""
    try:
        from qtpy.QtWidgets import QDialog
        app = QApplication.instance()
        for w in (app.topLevelWidgets() if app else []):
            if isinstance(w, QDialog) and w.isVisible():
                haystack = (w.windowTitle() + " "
                            + w.metaObject().className()).lower()
                if "new form" in haystack or "newform" in haystack:
                    w.reject()
                    logInfo("Designer tools: dismissed startup New Form dialog")
                    return
    except Exception as e:
        logDebug(f"Designer tools: dismiss startup New Form failed: {e}")


_scheduled = False


def installDesignerTools():
    """Called from the Designer plugin registrars (both of them - guard
    against double installation)."""
    global _scheduled
    if _scheduled or _tools:
        return
    _scheduled = True
    QTimer.singleShot(1500, _install)
