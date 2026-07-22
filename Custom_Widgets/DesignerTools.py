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
from qtpy.QtWidgets import (QApplication, QCheckBox, QComboBox, QCompleter,
                            QDockWidget, QFileDialog, QHBoxLayout, QLabel,
                            QLineEdit, QListWidget, QListWidgetItem,
                            QMainWindow, QMenu, QPlainTextEdit, QPushButton,
                            QToolButton, QVBoxLayout, QWidget)

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
        self._project_dir = os.path.abspath(project_dir or os.getcwd())
        ui_dir = os.path.join(self._project_dir, "ui")
        self._folder = ui_dir if os.path.isdir(ui_dir) else self._project_dir
        self._extra = []  # files opened/created outside the folder (realpaths)

        container = QWidget()
        layout = QVBoxLayout(container)

        header = QHBoxLayout()
        self._folderLabel = QLabel()
        self._folderLabel.setToolTip("Folder the workspace lists .ui files from")
        header.addWidget(self._folderLabel, 1)
        set_btn = QPushButton("Set Folder...")
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

    def _chooseFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Choose UI folder", self._folder)
        if folder:
            self._folder = folder
            self.refresh()

    def _newForm(self):
        name, _ = QFileDialog.getSaveFileName(
            self, "New form", os.path.join(self._folder, "untitled.ui"),
            "UI files (*.ui)")
        if not name:
            return
        try:
            from Custom_Widgets.ProjectMaker import create_ui_file
            prev = os.getcwd()
            os.chdir(self._project_dir)
            try:
                create_ui_file(os.path.splitext(os.path.basename(name))[0])
            finally:
                os.chdir(prev)
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
        act = menu.addAction("Open in Designer")
        act.triggered.connect(lambda: self._open(path))
        act.setToolTip("Opens in a Designer window (Qt cannot open a form "
                       "into the already-running instance)")
        menu.addSeparator()
        menu.addAction("Reveal in File Manager").triggered.connect(
            lambda: self._reveal(path))
        menu.addAction("Copy Path").triggered.connect(
            lambda: QApplication.clipboard().setText(path))
        menu.addSeparator()
        menu.addAction("Refresh List").triggered.connect(self.refresh)
        menu.exec_(self._list.viewport().mapToGlobal(pos))

    def _open(self, path):
        # A human needs to SEE the form. PySide6 cannot display a form in the
        # running Designer's MDI workspace (the workbench is not exposed, and
        # forcing it crashes Designer), so open a visible Designer window.
        try:
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            opened = startDesignerBridge().openFiles([path], new_process=True)
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


class _CodeEditor(QPlainTextEdit):
    """QPlainTextEdit with the editor keys people expect: Tab/Shift+Tab
    (indent), Ctrl+/ (toggle comment), Ctrl+D (duplicate line), Ctrl+S
    (save), auto-indent on Enter, plus completer key routing."""

    INDENT = "    "

    def __init__(self, parent=None):
        super().__init__(parent)
        self._completer = None
        self._saveCallback = None

    def setCompleter(self, completer):
        self._completer = completer
        completer.setWidget(self)
        completer.activated.connect(self._insertCompletion)

    def setSaveCallback(self, cb):
        self._saveCallback = cb

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


class QssEditorDock(QDockWidget):
    """Edits the project's default style (Qss/scss/defaultStyle.scss), open
    by default. New style files are auto-imported into it. On change the SCSS
    is compiled (qtsass) and applied live to the open form previews - and,
    if the user opts in, to the whole Designer window. Styles live in scss,
    never inline in .ui files."""

    def __init__(self, parent=None, project_dir=None):
        super().__init__("Custom Widgets - QSS Editor", parent)
        self.setObjectName("customWidgetsQssDock")
        self._project_dir = os.path.abspath(project_dir or os.getcwd())
        self._scss_dir = os.path.join(self._project_dir, "Qss", "scss")
        self._path = os.path.join(self._scss_dir, "defaultStyle.scss")

        container = QWidget()
        layout = QVBoxLayout(container)

        self._fileLabel = QLabel()
        layout.addWidget(self._fileLabel)

        self._editor = _CodeEditor()
        self._editor.setPlaceholderText(
            "Default styles (Qss/scss/defaultStyle.scss)...\n"
            "Tab/Shift+Tab indent · Ctrl+/ comment · Ctrl+D duplicate · Ctrl+S save")
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self._editor.setFont(font)
        self._highlighter = QssHighlighter(self._editor.document())
        self._editor.setSaveCallback(self._save)
        layout.addWidget(self._editor)

        row = QHBoxLayout()
        for label, slot in (("Open...", self._open),
                            ("New Style File...", self._newStyleFile),
                            ("Save", self._save), ("Check", self._check),
                            ("Apply", self._apply)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        layout.addLayout(row)

        opts = QHBoxLayout()
        self._autoApply = _checkbox("Auto-compile & apply on change", True)
        self._autoApply.stateChanged.connect(lambda *_: self._scheduleApply())
        opts.addWidget(self._autoApply)
        self._repaintDesigner = _checkbox("Repaint entire Designer window", False)
        self._repaintDesigner.stateChanged.connect(lambda *_: self._scheduleApply())
        opts.addWidget(self._repaintDesigner)
        opts.addStretch()
        layout.addLayout(opts)

        self.setWidget(container)

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

        self._loadDefault()  # open the default style by default

    # --- file handling --------------------------------------------------
    def _loadDefault(self):
        os.makedirs(self._scss_dir, exist_ok=True)
        if not os.path.exists(self._path):
            with open(self._path, "w", encoding="utf-8") as f:
                f.write("// Project default styles (override theme styles)\n"
                        "// New style files are @import-ed here automatically.\n")
        self._load(self._path)

    def _load(self, path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            self._editor.setPlainText(f.read())
        self._path = path
        self._fileLabel.setText("✎ " + os.path.relpath(path, self._project_dir))

    def _open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open stylesheet", self._scss_dir,
            "Styles (*.qss *.css *.scss);;All files (*)")
        if path:
            self._load(path)

    def _newStyleFile(self):
        """Create a new scss file and auto-import it into defaultStyle.scss."""
        path, _ = QFileDialog.getSaveFileName(
            self, "New style file", os.path.join(self._scss_dir, "custom.scss"),
            "SCSS files (*.scss)")
        if not path:
            return
        name = os.path.basename(path)
        if not name.endswith(".scss"):
            name += ".scss"
            path = os.path.join(os.path.dirname(path), name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"// {name} - imported into defaultStyle.scss\n")
        self._ensureImport(name)
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
        try:
            css = self._compile()
        except Exception as e:
            logWarning(f"QSS compile error: {str(e).splitlines()[0]}")
            return
        try:
            from Custom_Widgets.DesignerBridge import startDesignerBridge
            bridge = startDesignerBridge()
            bridge._setStyleSheet(css)
            if self._repaintDesigner.isChecked():
                self._repaintWholeDesigner(css)
        except Exception as e:
            logException(e, message="QSS editor: apply failed")

    def _repaintWholeDesigner(self, css):
        window = _designerMainWindow()
        if window is not None:
            window.setStyleSheet(css)


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


def _addStatusFooter(window):
    """A footer strip in Designer's status bar: quick access to the Logs
    pane, a live warning/error count that opens errors on click, and the
    latest message."""
    try:
        status = window.statusBar()
        if status is None:
            return

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
        _tools["qss"] = QssEditorDock(window)
        window.addDockWidget(Qt.RightDockWidgetArea, _tools["workspace"])
        window.addDockWidget(Qt.RightDockWidgetArea, _tools["qss"])
        window.addDockWidget(Qt.BottomDockWidgetArea, _tools["logs"])
        _tools["qss"].raise_()
        _addViewMenu(window)
        _addStatusFooter(window)
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
