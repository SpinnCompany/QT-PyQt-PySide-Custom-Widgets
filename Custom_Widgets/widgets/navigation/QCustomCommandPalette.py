########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomCommandPalette - a fuzzy-searchable command launcher (Ctrl/Cmd+K).
##
## A dimmed overlay with a search field and a fuzzy-filtered, keyboard-
## navigable command list. Register commands with callbacks; open with a
## shortcut. Styled from design tokens.
##
##     palette = QCustomCommandPalette.installShortcut(window, "Ctrl+K")
##     palette.setCommands([
##         {"id": "save", "title": "Save File", "callback": save, "shortcut": "Ctrl+S"},
##         {"id": "theme", "title": "Toggle Dark Theme", "callback": toggle},
##     ])
########################################################################
from qtpy.QtCore import Qt, Signal, QPropertyAnimation
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import (QWidget, QFrame, QVBoxLayout, QLineEdit, QListWidget,
                            QListWidgetItem, QGraphicsOpacityEffect, QShortcut)


def fuzzy_score(query, text):
    """Subsequence fuzzy match. Returns None if `query` is not an ordered
    subsequence of `text`, else an int score (higher = better; contiguous and
    word-start matches score more). Empty query scores 0 (matches all)."""
    if not query:
        return 0
    q, t = query.lower(), text.lower()
    ti = 0
    score = 0
    last = -2
    for qc in q:
        idx = t.find(qc, ti)
        if idx == -1:
            return None
        if idx == last + 1:
            score += 3                     # contiguous run
        elif idx == 0 or t[idx - 1] in " -_/":
            score += 2                     # start of a word
        else:
            score += 1
        last = idx
        ti = idx + 1
    return score


class Command(object):
    def __init__(self, id, title, callback=None, subtitle=None,
                 shortcut=None, category=None):
        self.id = id
        self.title = title
        self.callback = callback
        self.subtitle = subtitle
        self.shortcut = shortcut
        self.category = category

    @classmethod
    def ensure(cls, item):
        if isinstance(item, cls):
            return item
        if isinstance(item, dict):
            return cls(item.get("id", item.get("title")), item.get("title", ""),
                       callback=item.get("callback"), subtitle=item.get("subtitle"),
                       shortcut=item.get("shortcut"), category=item.get("category"))
        return cls(str(item), str(item))


class _PaletteSearch(QLineEdit):
    def __init__(self, palette):
        super().__init__(palette)
        self._palette = palette

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Down, Qt.Key_Up, Qt.Key_Return, Qt.Key_Enter,
                       Qt.Key_Escape):
            self._palette._onNavKey(e.key())
        else:
            super().keyPressEvent(e)


class QCustomCommandPalette(QWidget):
    commandTriggered = Signal(str)     # command id
    FADE_MS = 120

    __catalog__ = {
        "name": "QCustomCommandPalette",
        "props": {},
        "signals": ["commandTriggered"],
        "tokens_used": ["surface", "on-surface", "surface-muted", "outline",
                        "accent", "on-primary"],
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("QCustomCommandPalette")     # dim backdrop
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._commands = []
        self.hide()

        self._panel = QFrame(self)
        self._panel.setObjectName("commandPalettePanel")
        self._panel.setFixedWidth(560)
        col = QVBoxLayout(self._panel)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(0)

        self._search = _PaletteSearch(self)
        self._search.setParent(self._panel)
        self._search.setObjectName("commandPaletteSearch")
        self._search.setPlaceholderText("Type a command...")
        self._search.textChanged.connect(self._populate)
        col.addWidget(self._search)

        self._list = QListWidget(self._panel)
        self._list.setObjectName("commandPaletteList")
        self._list.setMaximumHeight(360)
        self._list.itemClicked.connect(lambda _it: self._triggerCurrent())
        col.addWidget(self._list)

        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)
        self._fade = QPropertyAnimation(self._opacity, b"opacity", self)
        self._fade.setDuration(self.FADE_MS)
        self._closing = False
        self._fade.finished.connect(self._onFadeFinished)

    def _onFadeFinished(self):
        if self._closing:
            self._closing = False
            self.hide()

    # ------------------------------------------------------------------ #
    ## Commands
    # ------------------------------------------------------------------ #
    def setCommands(self, commands):
        self._commands = [Command.ensure(c) for c in (commands or [])]
        if self.isVisible():
            self._populate(self._search.text())

    def addCommand(self, *args, **kw):
        self._commands.append(Command(*args, **kw) if args and not isinstance(args[0], (Command, dict))
                              else Command.ensure(args[0]))

    def _populate(self, query):
        self._list.clear()
        scored = []
        for cmd in self._commands:
            s = fuzzy_score(query, cmd.title)
            if s is None and cmd.subtitle:
                s = fuzzy_score(query, cmd.subtitle)
            if s is not None:
                scored.append((s, cmd))
        # higher score first; stable within equal scores (original order)
        scored.sort(key=lambda sc: -sc[0])
        for _s, cmd in scored:
            it = QListWidgetItem(cmd.title)
            if cmd.subtitle:
                it.setToolTip(cmd.subtitle)
            it.setData(Qt.UserRole, cmd)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)

    # ------------------------------------------------------------------ #
    ## Open / close / navigate
    # ------------------------------------------------------------------ #
    def open(self):
        p = self.parentWidget()
        if p is not None:
            self.setGeometry(p.rect())
            self._panel.setFixedWidth(min(560, max(280, p.width() - 40)))
        self._search.clear()
        self._populate("")
        self.show()
        self.raise_()
        self._positionPanel()
        self._search.setFocus()
        self._closing = False
        self._fade.stop()
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.start()

    def close(self):
        self._closing = True
        self._fade.stop()
        self._fade.setStartValue(self._opacity.opacity())
        self._fade.setEndValue(0.0)
        self._fade.start()
        return True

    def _positionPanel(self):
        x = max(0, (self.width() - self._panel.width()) // 2)
        y = max(40, int(self.height() * 0.12))
        self._panel.adjustSize()
        self._panel.move(x, y)

    def _onNavKey(self, key):
        if key == Qt.Key_Escape:
            self.close()
            return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self._triggerCurrent()
            return
        n = self._list.count()
        if n == 0:
            return
        row = self._list.currentRow()
        row = (row + 1) % n if key == Qt.Key_Down else (row - 1) % n
        self._list.setCurrentRow(row)

    def _triggerCurrent(self):
        it = self._list.currentItem()
        if it is None:
            return
        cmd = it.data(Qt.UserRole)
        self.close()
        if cmd is not None:
            if callable(cmd.callback):
                cmd.callback()
            self.commandTriggered.emit(cmd.id)

    def mousePressEvent(self, e):
        # click on the dim backdrop (outside the panel) closes the palette
        if not self._panel.geometry().contains(e.pos()):
            self.close()

    # ------------------------------------------------------------------ #
    ## Shortcut helper
    # ------------------------------------------------------------------ #
    @staticmethod
    def installShortcut(window, sequence="Ctrl+K", commands=None):
        """Create a palette over `window` and bind `sequence` (Qt maps Ctrl->Cmd
        on macOS, so 'Ctrl+K' is Cmd+K there) to open it."""
        palette = QCustomCommandPalette(window)
        if commands:
            palette.setCommands(commands)
        sc = QShortcut(QKeySequence(sequence), window)
        sc.activated.connect(palette.open)
        palette._shortcut = sc
        return palette
