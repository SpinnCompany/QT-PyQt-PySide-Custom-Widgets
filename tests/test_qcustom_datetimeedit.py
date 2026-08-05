"""QCustomDateEdit / QCustomTimeEdit / QCustomDateRangeEdit."""
from qtpy.QtCore import QDate, QTime


class TestDateEdit:
    def test_calendar_popup_and_format(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateEdit
        d = QCustomDateEdit()
        assert d.calendarPopup() is True
        assert d.displayFormat() == "yyyy-MM-dd"
        cal = d.calendarWidget()
        assert cal is not None and cal.objectName() == "customCalendar"

    def test_set_get_date_and_signal(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateEdit
        d = QCustomDateEdit()
        seen = []
        d.dateChanged.connect(seen.append)
        d.setDate(QDate(2020, 1, 15))          # a date that isn't today
        assert d.date() == QDate(2020, 1, 15)
        assert seen and seen[-1] == QDate(2020, 1, 15)

    def test_variant_size_props(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateEdit
        d = QCustomDateEdit()
        d.variant = "ghost"
        d.sizeVariant = "sm"
        assert d.variant == "ghost" and d.property("variant") == "ghost"
        assert d.sizeVariant == "sm"
        assert d.size() is not None            # QWidget.size() not shadowed


class TestTimeEdit:
    def test_set_get_time(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomTimeEdit
        t = QCustomTimeEdit()
        assert t.displayFormat() == "HH:mm"
        t.setTime(QTime(14, 30))
        assert t.time() == QTime(14, 30)


class TestDateRange:
    def test_range_api_and_signal(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateRangeEdit
        r = QCustomDateRangeEdit()
        seen = []
        r.rangeChanged.connect(lambda s, e: seen.append((s, e)))
        r.setDateRange(QDate(2026, 1, 1), QDate(2026, 1, 31))
        assert r.startDate() == QDate(2026, 1, 1)
        assert r.endDate() == QDate(2026, 1, 31)
        assert r.dateRange() == (QDate(2026, 1, 1), QDate(2026, 1, 31))
        assert seen

    def test_end_never_before_start(self, qapp):
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateRangeEdit
        r = QCustomDateRangeEdit()
        r.setDateRange(QDate(2026, 1, 10), QDate(2026, 1, 20))
        # push start beyond end -> end is clamped up to start (min-date rule)
        r.startEdit().setDate(QDate(2026, 1, 25))
        assert r.endDate() >= r.startDate()
        assert r.endDate() == QDate(2026, 1, 25)
        # end cannot go before start
        r.endEdit().setDate(QDate(2026, 1, 1))
        assert r.endDate() >= r.startDate()


class TestStyling:
    def test_tokenized_background(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomDateTimeEdit import QCustomDateEdit
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        d = QCustomDateEdit()
        d.resize(160, 34)
        d.ensurePolished()
        px = QColor(d.grab().toImage().pixel(6, 17)).name().lower()   # left padding, not a glyph
        assert px == "#ffffff"                 # surface (light)
        qapp.setStyleSheet("")
