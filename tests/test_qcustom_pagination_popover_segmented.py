"""QCustomPagination + QCustomPopover + QCustomSegmentedControl."""
from qtpy.QtWidgets import QWidget, QLabel, QPushButton


class TestPagination:
    def test_pages_to_show_ellipsis(self, qapp):
        from Custom_Widgets.QCustomPagination import pages_to_show
        assert pages_to_show(1, 5) == [1, 2, 3, 4, 5]          # small: no ellipsis
        assert pages_to_show(6, 20) == [1, "...", 5, 6, 7, "...", 20]
        assert pages_to_show(1, 20) == [1, 2, "...", 20]
        assert pages_to_show(20, 20) == [1, "...", 19, 20]

    def test_navigation_and_signal(self, qapp):
        from Custom_Widgets.QCustomPagination import QCustomPagination
        p = QCustomPagination(pageCount=10)
        assert p.currentPage() == 1
        seen = []
        p.pageChanged.connect(seen.append)
        p.setCurrentPage(5)
        assert p.currentPage() == 5 and seen[-1] == 5
        p.setCurrentPage(99)                                    # clamped
        assert p.currentPage() == 10

    def test_current_button_marked(self, qapp):
        from Custom_Widgets.QCustomPagination import QCustomPagination
        p = QCustomPagination(pageCount=5)
        p.setCurrentPage(3)
        marked = [b for b in p.findChildren(QPushButton)
                  if b.objectName() == "pageBtn" and b.property("current")]
        assert len(marked) == 1 and marked[0].text() == "3"


class TestPopover:
    def test_attach_and_content(self, qapp):
        from Custom_Widgets.QCustomPopover import QCustomPopover
        win = QWidget(); win.resize(400, 300); win.show()
        trigger = QPushButton("info", win)
        pop = QCustomPopover.attach(trigger, placement="bottom")
        pop.addWidget(QLabel("Hello from a popover"))
        opened = []
        pop.opened.connect(lambda: opened.append(1))
        trigger.click()                                         # attached -> opens
        assert pop.isVisible() and opened == [1]
        assert pop._placement == "bottom"
        pop.hide()

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomPopover import QCustomPopover
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        win = QWidget()
        pop = QCustomPopover(win, placement="top")
        pop.ensurePolished()
        assert pop.panelColor.name().lower() == "#ffffff"      # surface
        assert pop.borderColor.name().lower() == "#cbd5e1"     # outline
        qapp.setStyleSheet("")


class TestSegmented:
    def test_segments_and_selection(self, qapp):
        from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
        s = QCustomSegmentedControl()
        s.setSegments([("Day", "d"), ("Week", "w"), ("Month", "m")])
        assert s.count() == 3
        assert s.currentIndex() == 0 and s.currentData() == "d"
        seen = []
        s.currentChanged.connect(seen.append)
        s.setCurrentIndex(2)
        assert s.currentIndex() == 2 and s.currentData() == "m"
        assert seen[-1] == 2

    def test_exclusive_checked(self, qapp):
        from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
        s = QCustomSegmentedControl()
        s.setSegments(["A", "B", "C"])
        s.setCurrentIndex(1)
        checked = [b.text() for b in s._buttons if b.isChecked()]
        assert checked == ["B"]                                # exactly one

    def test_seg_position_property(self, qapp):
        from Custom_Widgets.QCustomSegmentedControl import QCustomSegmentedControl
        s = QCustomSegmentedControl()
        s.setSegments(["A", "B", "C"])
        assert [b.property("seg") for b in s._buttons] == ["first", "middle", "last"]
        s.setSegments(["Solo"])
        assert s._buttons[0].property("seg") == "only"
