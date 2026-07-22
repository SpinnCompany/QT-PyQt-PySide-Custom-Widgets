"""QCustomBreadcrumbs + QCustomRating + QCustomChip(Group)."""


class TestBreadcrumbs:
    def test_build_and_click(self, qapp):
        from Custom_Widgets.QCustomBreadcrumbs import QCustomBreadcrumbs
        from qtpy.QtWidgets import QPushButton, QLabel
        b = QCustomBreadcrumbs()
        b.setItems([("Home", "/"), ("Docs", "/docs"), "Widgets"])
        links = b.findChildren(QPushButton)
        currents = [l for l in b.findChildren(QLabel) if l.objectName() == "breadcrumbCurrent"]
        assert len(links) == 2                     # first two are links
        assert len(currents) == 1                  # last is the current label
        assert currents[0].text() == "Widgets"
        seen = []
        b.itemClicked.connect(lambda i, d: seen.append((i, d)))
        links[1].click()
        assert seen[-1] == (1, "/docs")


class TestRating:
    def test_set_value_and_signal(self, qapp):
        from Custom_Widgets.QCustomRating import QCustomRating
        r = QCustomRating(maximum=5)
        assert r.maximum == 5 and r.value == 0
        seen = []
        r.valueChanged.connect(seen.append)
        r.setValue(3)
        assert r.value == 3 and seen[-1] == 3
        # stars 0..2 filled, 3..4 empty
        assert [s.property("filled") for s in r._stars] == [True, True, True, False, False]
        assert r._stars[0].text() == "★" and r._stars[4].text() == "☆"

    def test_clamp_and_readonly(self, qapp):
        from Custom_Widgets.QCustomRating import QCustomRating
        r = QCustomRating(maximum=5)
        r.setValue(99)
        assert r.value == 5
        r.readOnly = True
        assert r.readOnly is True

    def test_click_same_star_clears(self, qapp):
        from qtpy.QtCore import QPointF, Qt
        from qtpy.QtGui import QMouseEvent
        from qtpy.QtWidgets import QApplication
        from Custom_Widgets.QCustomRating import QCustomRating
        r = QCustomRating(maximum=5)
        r.resize(160, 30)
        r.show()
        QApplication.processEvents()               # lay out the stars
        r.setValue(3)
        pos = r._stars[2].geometry().center()      # 3rd star (index 2), real geometry
        ev = QMouseEvent(QMouseEvent.MouseButtonPress, QPointF(pos), Qt.LeftButton,
                         Qt.LeftButton, Qt.NoModifier)
        r.mousePressEvent(ev)
        assert r.value == 0                        # clicking the current top star clears


class TestChips:
    def test_add_remove(self, qapp):
        from Custom_Widgets.QCustomChip import QCustomChipGroup
        g = QCustomChipGroup(closable=True)
        g.setChips(["python", "qt", ("pyside", 6)])
        assert g.count() == 3
        removed = []
        g.chipRemoved.connect(removed.append)
        g.chips()[0].removed.emit()                # simulate close click
        assert g.count() == 2 and removed[-1] == "python"

    def test_exclusive_selection(self, qapp):
        from Custom_Widgets.QCustomChip import QCustomChipGroup
        g = QCustomChipGroup(selectable=True, exclusive=True)
        g.setChips(["a", "b", "c"])
        seen = []
        g.selectionChanged.connect(seen.append)
        g.chips()[0].setSelected(True)
        g.chips()[1].setSelected(True)             # exclusive -> deselect a
        assert g.selectedData() == ["b"]
        assert seen[-1] == ["b"]

    def test_multi_selection(self, qapp):
        from Custom_Widgets.QCustomChip import QCustomChipGroup
        g = QCustomChipGroup(selectable=True, exclusive=False)
        g.setChips(["a", "b", "c"])
        g.chips()[0].setSelected(True)
        g.chips()[2].setSelected(True)
        assert sorted(g.selectedData()) == ["a", "c"]

    def test_chip_selected_property(self, qapp):
        from Custom_Widgets.QCustomChip import QCustomChip
        c = QCustomChip("x", selectable=True)
        assert c.property("selected") is False
        c.setSelected(True)
        assert c.isSelected() and c.property("selected") is True
