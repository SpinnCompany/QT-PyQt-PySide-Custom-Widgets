"""QCustomTabWidget + QCustomAccordion."""
from qtpy.QtWidgets import QLabel, QWidget
from qtpy.QtTest import QTest


class TestTabs:
    def test_add_and_current(self, qapp):
        from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
        t = QCustomTabWidget()
        t.addTab(QLabel("one"), "One")
        t.addTab(QLabel("two"), "Two")
        assert t.count() == 2
        seen = []
        t.currentChanged.connect(seen.append)
        t.setCurrentIndex(1)
        assert t.currentIndex() == 1 and seen[-1] == 1

    def test_tabstyle_and_size_props(self, qapp):
        from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
        t = QCustomTabWidget()
        assert t.tabStyle == "underline"
        t.tabStyle = "pills"
        t.sizeVariant = "lg"
        assert t.tabStyle == "pills" and t.property("tabStyle") == "pills"
        assert t.sizeVariant == "lg"
        assert t.size() is not None            # QWidget.size() not shadowed

    def test_pills_selected_paints_accent(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        t = QCustomTabWidget()
        t.tabStyle = "pills"
        t.addTab(QLabel("a"), "AAAA")
        t.addTab(QLabel("b"), "BBBB")
        t.setCurrentIndex(0)
        t.resize(300, 200)
        t.show()
        t.ensurePolished()
        img = t.tabBar().grab().toImage()
        # the selected pill should carry accent (#2563eb) somewhere along its row
        found = any(QColor(img.pixel(x, img.height() // 2)).name().lower() == "#2563eb"
                    for x in range(0, min(img.width(), 80)))
        assert found
        qapp.setStyleSheet("")


class TestAccordion:
    def _acc(self, qapp, exclusive=False):
        from Custom_Widgets.QCustomAccordion import QCustomAccordion
        a = QCustomAccordion(exclusive=exclusive)
        a.addSection("First", QLabel("content one"))
        a.addSection("Second", QLabel("content two"))
        a.addSection("Third", QLabel("content three"))
        a.resize(320, 400)
        a.show()
        return a

    def test_sections_start_collapsed(self, qapp):
        a = self._acc(qapp)
        assert a.sectionCount() == 3
        assert a.expandedIndices() == []

    def test_expand_and_signal(self, qapp):
        a = self._acc(qapp)
        seen = []
        a.sectionToggled.connect(lambda i, e: seen.append((i, e)))
        a.setExpanded(1, True, animate=False)
        assert a.section(1).isExpanded() is True
        assert a.expandedIndices() == [1]
        assert (1, True) in seen

    def test_exclusive_collapses_others(self, qapp):
        a = self._acc(qapp, exclusive=True)
        a.setExpanded(0, True, animate=False)
        a.setExpanded(2, True, animate=False)      # opening 2 must close 0
        assert a.expandedIndices() == [2]

    def test_non_exclusive_allows_multiple(self, qapp):
        a = self._acc(qapp, exclusive=False)
        a.setExpanded(0, True, animate=False)
        a.setExpanded(2, True, animate=False)
        assert a.expandedIndices() == [0, 2]

    def test_header_glyph_updates(self, qapp):
        a = self._acc(qapp)
        assert a.section(0)._header.text().startswith("▸")
        a.setExpanded(0, True, animate=False)
        assert a.section(0)._header.text().startswith("▾")
