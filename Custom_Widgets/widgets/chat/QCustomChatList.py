########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomChatList - a data-driven conversation list.
##
## Wraps a scrollable column of QCustomChatListItem rows and owns the selection
## (active pill), so a manager just calls setConversations([...]) with DATA and
## connects `currentChanged(index)` — it never builds or colours rows. All the
## row styling (accent, active pill, name/preview/time colours, online dot) is
## exposed as qproperties on the LIST and forwarded to every row, so the whole
## look is set in Designer / QSS. Designer-droppable.
##
## Each conversation is a dict: {name, preview, time, unread, online, muted,
## avatarColor, avatarImage}.
########################################################################
from qtpy.QtCore import Qt, Property, Signal
from qtpy.QtGui import QColor, QPixmap
from qtpy.QtWidgets import (QFrame, QWidget, QVBoxLayout, QScrollArea, QSizePolicy)

from Custom_Widgets.QCustomChatListItem import QCustomChatListItem


class QCustomChatList(QFrame):

    currentChanged = Signal(int)
    itemClicked = Signal(int)

    WIDGET_ICON = "components/icons/forum.png"
    WIDGET_TOOLTIP = "A data-driven conversation list"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatList"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatList' name='customChatList'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>520</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatList",
        "props": {"accentColor": {"type": "color", "default": "#1b74e4"},
                  "activeColor": {"type": "color", "default": "#12203a"},
                  "nameColor": {"type": "color", "default": "#1f2430"},
                  "previewColor": {"type": "color", "default": "#8a93a6"},
                  "timeColor": {"type": "color", "default": "#99a0b0"},
                  "activeNameColor": {"type": "color", "default": "#ffffff"},
                  "activeTimeColor": {"type": "color", "default": "#4c8dff"},
                  "onlineColor": {"type": "color", "default": "#31c48d"},
                  "surfaceColor": {"type": "color", "default": "#ffffff"},
                  "rowSpacing": {"type": "int", "default": 2}},
        "signals": ["currentChanged", "itemClicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomChatList")
        self._accent = QColor("#1b74e4")
        self._active = QColor("#12203a")
        self._name = QColor("#1f2430")
        self._preview = QColor("#8a93a6")
        self._time = QColor("#99a0b0")
        self._active_name = QColor("#ffffff")
        self._active_time = QColor("#4c8dff")
        self._online = QColor("#31c48d")
        self._surface = QColor("#ffffff")
        self._row_spacing = 2
        self._items = []
        self._current = -1
        self._avatar_palette = ["#f2704e", "#3d7bff", "#8b5cf6", "#12b8a6",
                                "#e8477f", "#f0a92b", "#2fb673", "#5b74ff"]

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self._scroll = QScrollArea(self)
        self._scroll.setObjectName("chatListScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._contents = QWidget()
        self._contents.setObjectName("chatListContents")
        self._vbox = QVBoxLayout(self._contents)
        self._vbox.setContentsMargins(0, 0, 0, 0)
        self._vbox.setSpacing(self._row_spacing)
        self._vbox.addStretch(1)
        self._scroll.setWidget(self._contents)
        outer.addWidget(self._scroll)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setConversations(self, conversations):
        self._clear()
        for i, c in enumerate(conversations or []):
            item = QCustomChatListItem(name=c.get("name", ""),
                                       preview=c.get("preview", ""),
                                       time=c.get("time", ""))
            item.setObjectName("chatListRow_%d" % i)
            item.online = bool(c.get("online", True))
            item.unread = int(c.get("unread", 0) or 0)
            item.muted = bool(c.get("muted", False))
            self._apply_row_style(item)
            color = c.get("avatarColor") or self._avatar_palette[i % len(self._avatar_palette)]
            item._avatar.bgColor = QColor(color)
            img = c.get("avatarImage")
            if img is not None:
                item.setAvatarImage(img if isinstance(img, QPixmap) else QPixmap(str(img)))
            item.clicked.connect(lambda idx=i: self._on_item_clicked(idx))
            self._vbox.insertWidget(i, item)
            self._items.append(item)
        if self._items:
            self.setCurrentIndex(0, emit=False)

    def setAvatarImageAt(self, index, image):
        if 0 <= index < len(self._items):
            self._items[index].setAvatarImage(image if isinstance(image, QPixmap) else QPixmap(str(image)))

    def setCurrentIndex(self, index, emit=True):
        if not (0 <= index < len(self._items)):
            return
        self._current = index
        for i, it in enumerate(self._items):
            it.active = (i == index)
        if emit:
            self.currentChanged.emit(index)

    def currentIndex(self):
        return self._current

    def count(self):
        return len(self._items)

    def _on_item_clicked(self, index):
        self.setCurrentIndex(index)
        self.itemClicked.emit(index)

    def _clear(self):
        for it in self._items:
            it.setParent(None)
            it.deleteLater()
        self._items = []
        self._current = -1

    # ------------------------------------------------------------------ #
    ## Styling forwarded to rows
    # ------------------------------------------------------------------ #
    def _apply_row_style(self, item):
        item.accentColor = self._accent
        item.nameColor = self._name
        item.previewColor = self._preview
        item.timeColor = self._time
        item.activeColor = self._active
        item.activeNameColor = self._active_name
        item.activeTimeColor = self._active_time
        item._avatar.statusColor = QColor(self._online)
        item._avatar.statusBorderColor = QColor(self._surface)

    def _restyle_all(self):
        for it in self._items:
            self._apply_row_style(it)

    def _prop(self, attr):
        return getattr(self, attr)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def activeColor(self):
        return self._active

    @activeColor.setter
    def activeColor(self, c):
        self._active = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def nameColor(self):
        return self._name

    @nameColor.setter
    def nameColor(self, c):
        self._name = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def previewColor(self):
        return self._preview

    @previewColor.setter
    def previewColor(self, c):
        self._preview = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def timeColor(self):
        return self._time

    @timeColor.setter
    def timeColor(self, c):
        self._time = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def activeNameColor(self):
        return self._active_name

    @activeNameColor.setter
    def activeNameColor(self, c):
        self._active_name = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def activeTimeColor(self):
        return self._active_time

    @activeTimeColor.setter
    def activeTimeColor(self, c):
        self._active_time = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def onlineColor(self):
        return self._online

    @onlineColor.setter
    def onlineColor(self, c):
        self._online = QColor(c)
        self._restyle_all()

    @Property(QColor)
    def surfaceColor(self):
        return self._surface

    @surfaceColor.setter
    def surfaceColor(self, c):
        self._surface = QColor(c)
        self._restyle_all()

    @Property(int)
    def rowSpacing(self):
        return self._row_spacing

    @rowSpacing.setter
    def rowSpacing(self, v):
        self._row_spacing = max(0, int(v))
        self._vbox.setSpacing(self._row_spacing)
