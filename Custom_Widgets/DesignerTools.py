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
##
## Everything is best-effort and must never break Designer startup.
########################################################################
import logging
import os
import re

from qtpy.QtCore import Qt, QObject, QTimer, Signal, QStringListModel
from qtpy.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                        QTextCursor)
from qtpy.QtWidgets import (QApplication, QCompleter, QDockWidget, QFileDialog,
                            QHBoxLayout, QLineEdit, QListWidget,
                            QListWidgetItem, QMainWindow, QMenu, QPlainTextEdit,
                            QPushButton, QVBoxLayout, QWidget)

from Custom_Widgets.Log import *

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
class _LogEmitter(QObject):
    message = Signal(str)


class _DockLogHandler(logging.Handler):
    """Feeds python logging records into the dock (thread-safe via signal)."""

    def __init__(self, emitter):
        super().__init__()
        self._emitter = emitter
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)s  %(message)s",
                                            datefmt="%H:%M:%S"))

    def emit(self, record):
        try:
            self._emitter.message.emit(self.format(record))
        except Exception:
            pass


class LogViewDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Custom Widgets - Logs", parent)
        self.setObjectName("customWidgetsLogDock")
        self._view = QPlainTextEdit()
        self._view.setReadOnly(True)
        self._view.setMaximumBlockCount(2000)
        self.setWidget(self._view)

        self._emitter = _LogEmitter()
        self._emitter.message.connect(self._append)
        self._handler = _DockLogHandler(self._emitter)
        logging.getLogger().addHandler(self._handler)

    def _append(self, text):
        self._view.appendPlainText(text)


########################################################################
## UI FILES WORKSPACE
########################################################################
class WorkspaceDock(QDockWidget):
    """The project's .ui files; double-click opens the form (through the
    Designer bridge server's open logic)."""

    def __init__(self, parent=None, project_dir=None):
        super().__init__("Custom Widgets - UI Workspace", parent)
        self.setObjectName("customWidgetsWorkspaceDock")
        self._project_dir = os.path.abspath(project_dir or os.getcwd())

        container = QWidget()
        layout = QVBoxLayout(container)
        self._list = QListWidget()
        self._list.itemDoubleClicked.connect(self._openItem)
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._showContextMenu)
        layout.addWidget(self._list)
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        layout.addWidget(refresh)
        self.setWidget(container)
        self.refresh()

    def refresh(self):
        self._list.clear()
        skip = {".git", "__pycache__", "generated-files", "node_modules", "venv", ".venv"}
        for root, dirs, files in os.walk(self._project_dir):
            dirs[:] = [d for d in dirs if d not in skip]
            for name in sorted(files):
                if name.lower().endswith(".ui") and not name.startswith("new_"):
                    path = os.path.join(root, name)
                    item = QListWidgetItem(os.path.relpath(path, self._project_dir))
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
        menu.addAction("Open").triggered.connect(lambda: self._open(path))
        menu.addAction("Open in New Window").triggered.connect(
            lambda: self._open(path, new_window=True))
        menu.addSeparator()
        menu.addAction("Reveal in File Manager").triggered.connect(
            lambda: self._reveal(path))
        menu.addAction("Copy Path").triggered.connect(
            lambda: QApplication.clipboard().setText(path))
        menu.addSeparator()
        menu.addAction("Refresh List").triggered.connect(self.refresh)
        menu.exec_(self._list.viewport().mapToGlobal(pos))

    def _open(self, path, new_window=False):
        try:
            if new_window:
                from qtpy.QtCore import QProcess
                import sys
                program = (sys.executable if "designer" in sys.executable.lower()
                           else "pyside6-designer")
                QProcess.startDetached(program, [path])
                logInfo(f"Workspace: opened {os.path.basename(path)} in new window")
                return
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            opened = startDesignerBridge().openFiles([path])
            logInfo(f"Workspace opened: {opened}")
        except Exception as e:
            logException(e, message="Workspace: failed to open form")

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


class QssEditorDock(QDockWidget):
    """Edit QSS with highlighting + property autocomplete and push it onto
    the open form previews (same path the theme engine uses)."""

    def __init__(self, parent=None):
        super().__init__("Custom Widgets - QSS Editor", parent)
        self.setObjectName("customWidgetsQssDock")
        self._path = None

        container = QWidget()
        layout = QVBoxLayout(container)

        self._editor = QPlainTextEdit()
        self._editor.setPlaceholderText(
            "QSS / theme styles...\nCtrl+Space or type to autocomplete properties")
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self._editor.setFont(font)
        self._highlighter = QssHighlighter(self._editor.document())
        layout.addWidget(self._editor)

        row = QHBoxLayout()
        for label, slot in (("Open...", self._open), ("Save", self._save),
                            ("Check", self._check), ("Apply to forms", self._apply)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        layout.addLayout(row)
        self.setWidget(container)

        self._completer = QCompleter(QStringListModel(QSS_PROPERTIES, self))
        self._completer.setWidget(self._editor)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.activated.connect(self._insertCompletion)
        self._editor.textChanged.connect(self._maybeComplete)

    # --- completion -----------------------------------------------------
    def _currentWord(self):
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()

    def _maybeComplete(self):
        word = self._currentWord()
        if len(word) < 2:
            self._completer.popup().hide()
            return
        self._completer.setCompletionPrefix(word)
        if self._completer.completionCount() == 0:
            self._completer.popup().hide()
            return
        rect = self._editor.cursorRect()
        rect.setWidth(self._completer.popup().sizeHintForColumn(0) + 24)
        self._completer.complete(rect)

    def _insertCompletion(self, completion):
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.insertText(completion + ": ")
        self._editor.setTextCursor(cursor)

    # --- actions --------------------------------------------------------
    def _open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open stylesheet", os.getcwd(),
            "Styles (*.qss *.css *.scss);;All files (*)")
        if path:
            with open(path, encoding="utf-8", errors="ignore") as f:
                self._editor.setPlainText(f.read())
            self._path = path

    def _save(self):
        path = self._path
        if not path:
            path, _ = QFileDialog.getSaveFileName(
                self, "Save stylesheet", os.getcwd(), "Styles (*.qss *.scss)")
            if not path:
                return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._editor.toPlainText())
        self._path = path
        logInfo(f"QSS editor: saved {path}")

    def _check(self):
        """Basic lint: brace balance + unknown property names."""
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

    def _apply(self):
        try:
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            startDesignerBridge()._setStyleSheet(self._editor.toPlainText())
        except Exception as e:
            logException(e, message="QSS editor: apply failed")


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
    for key in ("workspace", "qss", "logs"):
        target.addAction(_tools[key].toggleViewAction())


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
        _tools["qss"] = QssEditorDock(window)
        window.addDockWidget(Qt.RightDockWidgetArea, _tools["workspace"])
        window.addDockWidget(Qt.RightDockWidgetArea, _tools["qss"])
        window.addDockWidget(Qt.BottomDockWidgetArea, _tools["logs"])
        _tools["qss"].raise_()
        _addViewMenu(window)
        logInfo("Designer tools installed: Logs, UI Workspace, QSS Editor")
    except Exception as e:
        logException(e, message="Designer tools installation failed")


_scheduled = False


def installDesignerTools():
    """Called from the Designer plugin registrars (both of them - guard
    against double installation)."""
    global _scheduled
    if _scheduled or _tools:
        return
    _scheduled = True
    QTimer.singleShot(1500, _install)
