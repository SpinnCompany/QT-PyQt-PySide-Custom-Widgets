"""QCustomDateRangePicker — headless construction + paint smoke, range logic,
in-range test, navigation, and the rangeChanged signal."""

from qtpy.QtCore import QDate


def _img(w, size=(560, 300)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


class TestDateRangePicker:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker()
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 8)
                for x in range(0, img.width(), 8)}
        assert len(seen) > 3

    def test_in_range_logic(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker(start=QDate(2025, 6, 23), end=QDate(2025, 7, 9))
        assert w._in_range(QDate(2025, 6, 28))       # between
        assert not w._in_range(QDate(2025, 6, 23))   # endpoints not "in range"
        assert not w._in_range(QDate(2025, 7, 10))   # after end
        assert w._is_end(QDate(2025, 6, 23))
        assert w._is_end(QDate(2025, 7, 9))

    def test_pick_start_then_end(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker(start=QDate(2025, 6, 1), end=QDate(2025, 6, 10))
        # a fresh pick (both set) restarts the range
        w._pick(QDate(2025, 6, 15))
        assert w.startDate() == QDate(2025, 6, 15) and not w.endDate().isValid()
        # a later pick sets the end
        w._pick(QDate(2025, 6, 20))
        assert w.endDate() == QDate(2025, 6, 20)
        # an earlier pick moves the start
        w._pick(QDate(2025, 6, 12))
        assert w.startDate() == QDate(2025, 6, 12)

    def test_range_changed_signal(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker()
        seen = []
        w.rangeChanged.connect(lambda s, e: seen.append((s, e)))
        w.setRange(QDate(2025, 6, 1), QDate(2025, 6, 5))
        assert seen and seen[-1][0] == QDate(2025, 6, 1)

    def test_end_before_start_swaps(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker(start=QDate(2025, 6, 20), end=QDate(2025, 6, 25))
        w.setEndDate(QDate(2025, 6, 10))
        assert w.startDate() == QDate(2025, 6, 10)
        assert w.endDate() == QDate(2025, 6, 20)

    def test_navigation_shifts_month(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker()
        _img(w)
        m0 = w._first
        w.showMonth(2025, 3)
        assert w._first == QDate(2025, 3, 1)
        _img(w)

    def test_months_visible(self, qapp):
        from Custom_Widgets.QCustomDateRangePicker import QCustomDateRangePicker
        w = QCustomDateRangePicker()
        w.monthsVisible = 3
        assert w.monthsVisible == 3
        assert len(w._panels()) == 3
