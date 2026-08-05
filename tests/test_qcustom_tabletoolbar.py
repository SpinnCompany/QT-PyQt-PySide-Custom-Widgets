"""Tests for QCustomTableToolbar: search, filter chips, status pills, switch."""


def _toolbar():
    from Custom_Widgets.QCustomTableToolbar import QCustomTableToolbar
    tb = QCustomTableToolbar()
    tb.setStatuses([
        {"key": "pending", "label": "Pending", "count": 1235, "color": "#06b6d4"},
        {"key": "scheduled", "label": "Scheduled", "count": 8902, "color": "#f59e0b"},
        {"key": "completed", "label": "Completed", "count": 565, "color": "#10b981"},
    ])
    return tb


class TestSearch:
    def test_search_signal(self, qapp):
        tb = _toolbar()
        seen = []
        tb.searchChanged.connect(lambda s: seen.append(s))
        tb.setSearchText("boiler")
        assert seen and seen[-1] == "boiler"
        assert tb.searchText() == "boiler"

    def test_placeholder(self, qapp):
        tb = _toolbar()
        tb.setSearchPlaceholder("Search jobs")
        assert tb.searchInput().placeholderText() == "Search jobs"


class TestFilterChips:
    def test_add_and_keys(self, qapp):
        tb = _toolbar()
        tb.setFilterChips([
            {"key": "status", "label": "Status", "value": "Pending"},
            ("jobtype", "Job type", "Standard job"),
        ])
        assert tb.filterChipKeys() == ["status", "jobtype"]

    def test_remove_emits_and_drops(self, qapp):
        tb = _toolbar()
        tb.addFilterChip("date", "Date", "01/10/21")
        removed = []
        tb.filterChipRemoved.connect(lambda k: removed.append(k))
        # simulate the chip's x being clicked
        tb._chips["date"]._close.click()
        assert removed == ["date"]
        assert "date" not in tb.filterChipKeys()

    def test_clear_filters_signal(self, qapp):
        tb = _toolbar()
        fired = []
        tb.clearFiltersClicked.connect(lambda: fired.append(True))
        tb._clearBtn.click()
        assert fired == [True]

    def test_readd_same_key_updates(self, qapp):
        tb = _toolbar()
        tb.addFilterChip("status", "Status", "Pending")
        tb.addFilterChip("status", "Status", "Completed")   # same key -> update
        assert tb.filterChipKeys() == ["status"]


class TestStatusPills:
    def test_all_pill_default_active(self, qapp):
        tb = _toolbar()
        assert tb.activeStatus() == tb.ALL_KEY

    def test_select_status_emits_and_activates(self, qapp):
        tb = _toolbar()
        seen = []
        tb.statusSelected.connect(lambda k: seen.append(k))
        tb._pills["scheduled"].clicked.emit("scheduled")
        assert seen == ["scheduled"]
        assert tb.activeStatus() == "scheduled"
        assert tb._pills["scheduled"].isChecked()
        assert not tb._pills[tb.ALL_KEY].isChecked()

    def test_set_status_count(self, qapp):
        tb = _toolbar()
        tb.setStatusCount("pending", 1240)
        assert tb._pills["pending"]._count.text() == "1240"

    def test_rebuild_statuses_keeps_all(self, qapp):
        tb = _toolbar()
        tb.setStatuses([{"key": "x", "label": "X", "count": 1, "color": "#000"}])
        assert tb.ALL_KEY in tb._pills and "x" in tb._pills
        assert "pending" not in tb._pills


class TestShowStatuses:
    def test_switch_toggles_visibility_and_signal(self, qapp):
        tb = _toolbar()
        seen = []
        tb.showStatusesToggled.connect(lambda b: seen.append(b))
        tb.setShowStatuses(False)
        assert seen and seen[-1] is False
        assert not tb._pillBox.isVisible() or tb._pillBox.isHidden()
        tb.setShowStatuses(True)
        assert seen[-1] is True


class TestPaintAndTheme:
    def test_theme_colors_and_paint(self, qapp):
        tb = _toolbar()
        tb.setFilterChips([{"key": "status", "label": "Status", "value": "Pending"}])
        tb.setThemeColors(surface="#0b1220", on_surface="#e2e8f0",
                          muted="#94a3b8", outline="#1e293b", accent="#f97316")
        tb.resize(1000, 120)
        pm = tb.grab()
        assert not pm.isNull() and pm.width() > 0

    def test_status_pill_radius_never_exceeds_half_height(self, qapp):
        # REGRESSION: Qt does NOT clamp border-radius — a radius > height/2
        # renders SQUARE corners (this only bit on the real xcb display where
        # font metrics made the pill 29px tall vs a 15px radius). The pill must
        # keep an EVEN pinned height and a radius == height/2 so it stays a pill.
        import re
        tb = _toolbar()
        tb.resize(1000, 120)
        tb.show()
        qapp.processEvents()
        pill = next(p for k, p in tb._pills.items() if k != tb.ALL_KEY)
        h = pill.height()
        assert h > 0 and h % 2 == 0                    # even, so height/2 is exact
        m = re.search(r"border-radius:\s*(\d+)px", pill.styleSheet())
        assert m, "pill has no border-radius"
        assert int(m.group(1)) <= h // 2               # never square
