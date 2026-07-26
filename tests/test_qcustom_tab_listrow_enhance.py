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
    """The custom buttons TINT the icon set via qproperty-icon url (no iconName)
    to iconColor (resting) / iconColorActive (checked). Colours come from QSS."""

    def _src(self):
        from Custom_Widgets.Utils import resolve_icon_path
        from qtpy.QtGui import QIcon
        return QIcon(resolve_icon_path("layers"))

    def test_iconname_removed(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        for cls in (QCustomQPushButton, QCustomSidebarButton):
            b = cls()
            assert not hasattr(b, "iconName"), "%s still has iconName" % cls.__name__
            assert not hasattr(b, "iconNameActive")

    def test_iconcolor_tints_the_current_icon(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        from qtpy.QtCore import QSize
        from qtpy.QtWidgets import QApplication
        for cls in (QCustomQPushButton, QCustomSidebarButton):
            b = cls()
            b.setIconSize(QSize(20, 20))
            b.setIcon(self._src())
            b.iconColor = QColor("#8b90a6")
            QApplication.processEvents()           # deferred tint runs
            muted = b.icon().pixmap(20, 20).toImage()
            b.iconColor = QColor("#ff2200")
            QApplication.processEvents()
            red = b.icon().pixmap(20, 20).toImage()
            assert muted != red, "%s icon did not re-tint on iconColor change" % cls.__name__

    def test_active_colour_on_toggle(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
        from qtpy.QtCore import QSize
        from qtpy.QtWidgets import QApplication
        for cls in (QCustomQPushButton, QCustomSidebarButton):
            b = cls()
            b.setCheckable(True)
            b.setIconSize(QSize(20, 20))
            b.setIcon(self._src())
            b.iconColor = QColor("#8b90a6")
            b.iconColorActive = QColor("#6c7bff")
            QApplication.processEvents()
            rest = b.icon().pixmap(20, 20).toImage()
            b.setChecked(True)                     # toggled -> tint w/ active colour
            QApplication.processEvents()
            active = b.icon().pixmap(20, 20).toImage()
            assert rest != active, "%s active icon colour did not update" % cls.__name__


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
