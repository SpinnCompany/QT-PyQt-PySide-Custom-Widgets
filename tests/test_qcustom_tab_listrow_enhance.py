"""Opt-in enhancements: QCustomTabWidget closable tabs + '+' add-tab button,
and QCustomListRow reorder drag-handle. Defaults must be OFF (unchanged
behaviour); enabling them wires the affordance + signal."""

from qtpy.QtGui import QColor
from qtpy.QtWidgets import QWidget


class TestTabWidgetEnhance:
    def _tw(self):
        from Custom_Widgets.QCustomTabWidget import QCustomTabWidget
        tw = QCustomTabWidget()
        tw.addTab(QWidget(), "One")
        tw.addTab(QWidget(), "Two")
        return tw

    def test_defaults_off(self, qapp):
        tw = self._tw()
        assert tw.closableTabs is False
        assert tw.showAddButton is False
        assert tw.tabsClosable() is False
        assert tw.cornerWidget() is None

    def test_closable_optin(self, qapp):
        tw = self._tw()
        tw.closableTabs = True
        assert tw.closableTabs is True
        assert tw.tabsClosable() is True

    def test_add_button_and_signal(self, qapp):
        tw = self._tw()
        tw.showAddButton = True
        assert tw.showAddButton is True
        btn = tw.cornerWidget()
        assert btn is not None and btn.objectName() == "tabAddButton"
        fired = []
        tw.addTabRequested.connect(lambda: fired.append(1))
        btn.click()
        assert fired == [1]

    def test_add_button_removable(self, qapp):
        tw = self._tw()
        tw.showAddButton = True
        tw.showAddButton = False
        assert tw.showAddButton is False
        assert tw.cornerWidget() is None


class TestListRowDragHandle:
    def _row(self):
        from Custom_Widgets.QCustomListRow import QCustomListRow
        return QCustomListRow(title="Mode", value="Fun")

    def test_hidden_by_default(self, qapp):
        r = self._row()
        assert r.showDragHandle is False
        assert r._grip.isVisible() is False

    def test_show_and_colour(self, qapp):
        r = self._row()
        r.resize(320, 60)
        r.show()
        r.showDragHandle = True
        assert r.showDragHandle is True
        r.dragHandleColor = "#ff0000"
        assert QColor(r.dragHandleColor).name() == "#ff0000"
        # paints without error
        img = r.grab().toImage()
        assert img.width() > 0
