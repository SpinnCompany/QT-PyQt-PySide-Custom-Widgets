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


class TestCustomButtonIconRecolor:
    """The custom buttons recolour their icon FROM QSS (iconName + iconColor),
    so a :checked state selector recolours the icon with no setIcon in code."""

    def test_qpushbutton_icon_from_qss_props(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        assert b.icon().isNull()
        b.iconName = "layers"
        b.iconColor = QColor("#6c7bff")
        assert not b.icon().isNull()
        assert b.iconName == "layers"
        assert QColor(b.iconColor).name() == "#6c7bff"

    def test_sidebarbutton_icon_from_qss_props(self, qapp):
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        b = QCustomSidebarButton()
        assert b.icon().isNull()
        b.iconName = "home"
        b.iconColor = QColor("#22a55b")
        assert not b.icon().isNull()
        assert b.iconName == "home"
        assert QColor(b.iconColor).name() == "#22a55b"

    def test_iconcolor_change_rebuilds(self, qapp):
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        b = QCustomSidebarButton()
        b.iconName = "home"
        b.iconColor = QColor("#888888")
        first = b.icon().pixmap(20, 20).toImage()
        b.iconColor = QColor("#ff2200")
        second = b.icon().pixmap(20, 20).toImage()
        assert first != second, "icon did not recolour when iconColor changed"

    def test_active_state_swaps_colour_and_name_on_toggle(self, qapp):
        # Qt does NOT re-apply :checked qproperty, so the active look is a base
        # property the button swaps to on toggle. Both custom buttons must do it.
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        for cls in (QCustomQPushButton, QCustomSidebarButton):
            b = cls()
            b.setCheckable(True)
            b.iconName = "play_arrow"
            b.iconColor = QColor("#8b90a6")
            b.iconNameActive = "pause"
            b.iconColorActive = QColor("#6c7bff")
            rest = b.icon().pixmap(20, 20).toImage()
            b.setChecked(True)                     # toggled -> rebuild w/ active
            active = b.icon().pixmap(20, 20).toImage()
            assert rest != active, "%s icon did not swap on checked" % cls.__name__
            b.setChecked(False)
            assert b.icon().pixmap(20, 20).toImage() == rest, \
                "%s icon did not revert on uncheck" % cls.__name__


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
