"""QCustomCommandPalette: fuzzy scoring, filtering/ranking, keyboard nav,
command triggering."""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget


class TestFuzzyScore:
    def test_subsequence_match(self, qapp):
        from Custom_Widgets.QCustomCommandPalette import fuzzy_score
        assert fuzzy_score("gs", "Git Status") is not None    # g..s in order
        assert fuzzy_score("xyz", "Git Status") is None       # not a subsequence
        assert fuzzy_score("", "anything") == 0               # empty matches all

    def test_contiguous_and_wordstart_rank_higher(self, qapp):
        from Custom_Widgets.QCustomCommandPalette import fuzzy_score
        # "save" contiguous in "Save File" beats scattered match in "Show Avatars ..."
        contiguous = fuzzy_score("save", "Save File")
        scattered = fuzzy_score("save", "Show Avatar viEw")
        assert contiguous is not None and scattered is not None
        assert contiguous > scattered


class TestPalette:
    def _palette(self, qapp):
        from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette
        win = QWidget(); win.resize(800, 600); win.show()
        p = QCustomCommandPalette(win)
        p.setCommands([
            {"id": "save", "title": "Save File", "shortcut": "Ctrl+S"},
            {"id": "saveall", "title": "Save All Files"},
            {"id": "open", "title": "Open File"},
            {"id": "theme", "title": "Toggle Dark Theme"},
        ])
        return win, p

    def test_filter_and_rank(self, qapp):
        win, p = self._palette(qapp)
        p.open()
        p._populate("save")
        titles = [p._list.item(i).text() for i in range(p._list.count())]
        assert titles == ["Save File", "Save All Files"]   # only saves, filtered
        p._populate("file")
        assert p._list.count() == 3                        # Save File, Save All Files, Open File

    def test_keyboard_navigation_wraps(self, qapp):
        win, p = self._palette(qapp)
        p.open(); p._populate("")
        n = p._list.count()
        p._list.setCurrentRow(0)
        p._onNavKey(Qt.Key_Up)                             # wraps to last
        assert p._list.currentRow() == n - 1
        p._onNavKey(Qt.Key_Down)                           # wraps to first
        assert p._list.currentRow() == 0

    def test_trigger_runs_callback_and_emits(self, qapp):
        from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette
        win = QWidget(); win.resize(800, 600); win.show()
        p = QCustomCommandPalette(win)
        ran = []
        p.setCommands([{"id": "go", "title": "Do It", "callback": lambda: ran.append(1)}])
        fired = []
        p.commandTriggered.connect(fired.append)
        p.open()
        p._list.setCurrentRow(0)
        p._triggerCurrent()
        assert ran == [1]
        assert fired == ["go"]

    def test_escape_closes(self, qapp):
        win, p = self._palette(qapp)
        p.open()
        assert p.isVisible()
        p._onNavKey(Qt.Key_Escape)
        from qtpy.QtTest import QTest
        QTest.qWait(200)                                   # let fade-out hide it
        assert not p.isVisible()

    def test_install_shortcut(self, qapp):
        from Custom_Widgets.QCustomCommandPalette import QCustomCommandPalette
        win = QWidget(); win.resize(400, 300)
        p = QCustomCommandPalette.installShortcut(win, "Ctrl+K",
                                                  commands=[{"id": "x", "title": "X"}])
        assert isinstance(p, QCustomCommandPalette)
        assert p._shortcut is not None
