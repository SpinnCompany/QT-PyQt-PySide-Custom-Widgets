"""QCustomTreeWidget + QCustomDrawer + QCustomStepper."""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel
from qtpy.QtTest import QTest


class TestTree:
    def test_nested_setitems(self, qapp):
        from Custom_Widgets.QCustomTreeWidget import QCustomTreeWidget
        t = QCustomTreeWidget()
        t.setItems([
            {"text": "Fruits", "expanded": True, "children": [
                {"text": "Apple", "data": 1}, "Banana"]},
            {"text": "Veg", "children": ["Carrot"]},
        ])
        root = t.invisibleRootItem()
        assert root.childCount() == 2
        fruits = t.topLevelItem(0)
        assert fruits.text(0) == "Fruits" and fruits.childCount() == 2
        assert fruits.isExpanded() is True
        assert fruits.child(0).data(0, Qt.UserRole) == 1
        assert t.topLevelItem(1).child(0).text(0) == "Carrot"

    def test_variant_size_props(self, qapp):
        from Custom_Widgets.QCustomTreeWidget import QCustomTreeWidget
        t = QCustomTreeWidget()
        t.variant = "ghost"; t.sizeVariant = "lg"
        assert t.property("variant") == "ghost" and t.sizeVariant == "lg"
        assert t.size() is not None


class TestDrawer:
    def test_open_close(self, qapp):
        from Custom_Widgets.QCustomDrawer import QCustomDrawer
        win = QWidget(); win.resize(600, 400); win.show()
        d = QCustomDrawer(win, side="left", size=280)
        d.addWidget(QLabel("nav"))
        opened = []
        d.opened.connect(lambda: opened.append(1))
        d.open()
        assert d.isOpen() and d.isVisible() and opened == [1]
        # panel occupies the left edge, full height
        assert d._panel.width() == 280
        assert d._panel.height() == d.height()
        d.close()
        QTest.qWait(320)                          # slide + fade out
        assert not d.isVisible()

    def test_side_positions(self, qapp):
        from Custom_Widgets.QCustomDrawer import QCustomDrawer
        win = QWidget(); win.resize(600, 400); win.show()
        d = QCustomDrawer(win, side="right", size=200)
        d.open()
        # right drawer's shown x is parent width - panel width
        assert d._shownPos().x() == d.width() - d._panel.width()


class TestStepper:
    def _stepper(self, qapp):
        from Custom_Widgets.QCustomStepper import QCustomStepper
        s = QCustomStepper()
        s.setSteps(["Account", "Profile", "Confirm"])
        s.show()
        return s

    def test_states_and_navigation(self, qapp):
        s = self._stepper(qapp)
        assert s.stepCount() == 3
        assert s.currentStep() == 0
        assert s._circles[0].property("state") == "active"
        assert s._circles[1].property("state") == "pending"

        seen = []
        s.currentStepChanged.connect(seen.append)
        s.next()
        assert s.currentStep() == 1 and seen[-1] == 1
        assert s._circles[0].property("state") == "completed"
        assert s._circles[0].text() == "✓"
        assert s._circles[1].property("state") == "active"
        # connector 0 (between step 0 and 1) is completed
        assert s._connectors[0].property("state") == "completed"

    def test_clamped_and_complete(self, qapp):
        s = self._stepper(qapp)
        s.previous()                              # can't go below 0
        assert s.currentStep() == 0
        s.setCurrentStep(99)                      # clamped to last
        assert s.currentStep() == 2 and s.isComplete()

    def test_active_circle_accent(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        s = self._stepper(qapp)
        s.setCurrentStep(0)
        c = s._circles[0]
        c.ensurePolished()
        img = c.grab().toImage()
        # active circle has an accent border
        border = QColor(img.pixel(c.width() // 2, 1)).name().lower()
        assert border == "#2563eb"
        qapp.setStyleSheet("")
