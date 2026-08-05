########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomChatListItem - one conversation row in a messenger list.
##
## A leading avatar (with an online status dot), the contact name, an elided
## last-message preview, a timestamp and an optional unread-count badge -- the
## exact anatomy of a chat/messenger conversation list. Composed from QLabels
## and a QCustomAvatar so the text uses real fonts and themes by role, while a
## painted rounded background gives the selected row its highlight pill. Set
## `active` to mark the open conversation, `unread` for the badge count, and
## `muted` to dim the row. Emits `clicked` so a list can route selection.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QRectF, QSize
from qtpy.QtGui import QColor, QPainter, QBrush, QPixmap, QFontMetrics
from qtpy.QtWidgets import (QFrame, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                            QSizePolicy)

try:
    from Custom_Widgets.QCustomAvatar import QCustomAvatar
except Exception:                                   # pragma: no cover
    QCustomAvatar = None


class _Badge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._count = 0
        self._bg = QColor("#1b74e4")
        self._fg = QColor("#ffffff")
        self._d = 20
        self.setFixedSize(self._d, self._d)

    def setCount(self, n):
        self._count = max(0, int(n))
        self.setVisible(self._count > 0)
        self.update()

    def setColors(self, bg, fg):
        self._bg, self._fg = QColor(bg), QColor(fg)
        self.update()

    def paintEvent(self, e):
        if self._count <= 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawEllipse(self.rect())
        p.setPen(self._fg)
        f = self.font()
        f.setPixelSize(int(self._d * 0.52))
        f.setBold(True)
        p.setFont(f)
        txt = "9+" if self._count > 9 else str(self._count)
        p.drawText(self.rect(), Qt.AlignCenter, txt)
        p.end()


class QCustomChatListItem(QFrame):

    clicked = Signal()

    WIDGET_ICON = "components/icons/chat_list_item.png"
    WIDGET_TOOLTIP = "A conversation row for a messenger list"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatListItem"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatListItem' name='customChatListItem'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>340</width><height>68</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatListItem",
        "props": {
            "name": {"type": "string", "default": "Ricky Smith"},
            "preview": {"type": "string", "default": "YOU: Okay, let's get the file over to..."},
            "time": {"type": "string", "default": "1min ago"},
            "unread": {"type": "int", "default": 0},
            "online": {"type": "bool", "default": True},
            "active": {"type": "bool", "default": False},
            "muted": {"type": "bool", "default": False},
            "activeColor": {"type": "color", "default": "#12203a"},
            "nameColor": {"type": "color", "default": "#1f2430"},
            "previewColor": {"type": "color", "default": "#8a93a6"},
            "timeColor": {"type": "color", "default": "#8a93a6"},
            "activeNameColor": {"type": "color", "default": "#ffffff"},
            "activeTimeColor": {"type": "color", "default": "#4c8dff"},
            "accentColor": {"type": "color", "default": "#1b74e4"},
            "radius": {"type": "int", "default": 14},
            "avatarSize": {"type": "int", "default": 44},
        },
        "signals": ["clicked"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None, name="", preview="", time=""):
        super().__init__(parent)
        self.setObjectName("QCustomChatListItem")
        self._active = False
        self._muted = False
        self._radius = 14
        self._active_color = QColor("#12203a")
        self._name_color = QColor("#1f2430")
        self._preview_color = QColor("#8a93a6")
        self._time_color = QColor("#8a93a6")
        self._active_name_color = QColor("#ffffff")
        self._active_time_color = QColor("#4c8dff")
        self._accent = QColor("#1b74e4")
        self._avatar_size = 44
        self._preview_full = preview
        self._name_full = name

        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 10, 14, 10)
        lay.setSpacing(12)

        if QCustomAvatar is not None:
            self._avatar = QCustomAvatar(self, text=(name[:1] or "?"))
            self._avatar.setFixedSize(self._avatar_size, self._avatar_size)
            self._avatar.statusPosition = "bottom-right"
            self._avatar.statusColor = QColor("#31c48d")
        else:                                       # pragma: no cover
            self._avatar = QLabel()
            self._avatar.setFixedSize(self._avatar_size, self._avatar_size)
        lay.addWidget(self._avatar, 0)

        mid = QVBoxLayout()
        mid.setContentsMargins(0, 0, 0, 0)
        mid.setSpacing(3)
        self._name = QLabel(name)
        self._name.setObjectName("chatItemName")
        # Ignored horizontal policy: the labels must NOT report their full text
        # width as a minimum, or a long preview forces the whole row (and the
        # panel) far too wide. They take whatever width the row gives and elide.
        self._name.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self._preview = QLabel(preview)
        self._preview.setObjectName("chatItemPreview")
        self._preview.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        mid.addWidget(self._name)
        mid.addWidget(self._preview)
        midw = QWidget()
        midw.setObjectName("cliMid")
        midw.setLayout(mid)
        midw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lay.addWidget(midw, 1)

        right = QVBoxLayout()
        right.setContentsMargins(0, 2, 0, 2)
        right.setSpacing(6)
        self._time = QLabel(time)
        self._time.setObjectName("chatItemTime")
        self._time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._badge = _Badge(self)
        badgeRow = QHBoxLayout()
        badgeRow.setContentsMargins(0, 0, 0, 0)
        badgeRow.addStretch(1)
        badgeRow.addWidget(self._badge, 0)
        right.addWidget(self._time, 0)
        right.addLayout(badgeRow)
        rightw = QWidget()
        rightw.setObjectName("cliRight")
        rightw.setLayout(right)
        lay.addWidget(rightw, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(64)
        self.setCursor(Qt.PointingHandCursor)
        self._badge.setCount(0)
        self._restyle()

    # ------------------------------------------------------------------ #
    ## Content API
    # ------------------------------------------------------------------ #
    def setName(self, text):
        self._name_full = str(text)
        self._elide_name()
        if QCustomAvatar is not None and not self._has_image():
            self._avatar.setText((str(text)[:1] or "?"))

    def _elide_name(self):
        fm = QFontMetrics(self._name.font())
        avail = max(20, self._name.width())
        self._name.setText(fm.elidedText(self._name_full, Qt.ElideRight, avail))

    def _has_image(self):
        return getattr(self._avatar, "_pixmap", None) is not None

    def setPreview(self, text):
        self._preview_full = str(text)
        self._elide()

    def setTime(self, text):
        self._time.setText(str(text))

    def setAvatarImage(self, image):
        if QCustomAvatar is not None:
            self._avatar.setImage(image)

    def _elide(self):
        fm = QFontMetrics(self._preview.font())
        avail = max(20, self._preview.width())
        self._preview.setText(fm.elidedText(self._preview_full, Qt.ElideRight, avail))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._elide()
        self._elide_name()

    # ------------------------------------------------------------------ #
    ## Painting (selected pill)
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        if self._active:
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing, True)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(self._active_color))
            p.drawRoundedRect(QRectF(0, 0, self.width(), self.height()),
                              self._radius, self._radius)
            p.end()
        super().paintEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)

    # ------------------------------------------------------------------ #
    ## Styling
    # ------------------------------------------------------------------ #
    def _restyle(self):
        # No per-widget stylesheet: state is exposed as Qt properties (active,
        # muted) that the APP QSS targets, and we only re-polish so the theme
        # engine re-evaluates our rules (incl. the qproperty-* painted colours)
        # on every theme change. Label colours/fonts all live in the app QSS.
        for w in (self, self._name, self._preview, self._time):
            w.style().unpolish(w)
            w.style().polish(w)
        self._badge.setColors(self._accent, self._badge._fg)
        if QCustomAvatar is not None:
            self._avatar.setStatus(self._online)
        self.update()

    _online = True

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def name(self):
        return self._name.text()

    @name.setter
    def name(self, v):
        self.setName(v)

    @Property(str)
    def preview(self):
        return self._preview_full

    @preview.setter
    def preview(self, v):
        self.setPreview(v)

    @Property(str)
    def time(self):
        return self._time.text()

    @time.setter
    def time(self, v):
        self.setTime(v)

    @Property(int)
    def unread(self):
        return self._badge._count

    @unread.setter
    def unread(self, v):
        self._badge.setCount(v)

    @Property(bool)
    def online(self):
        return self._online

    @online.setter
    def online(self, v):
        self._online = bool(v)
        if QCustomAvatar is not None:
            self._avatar.setStatus(self._online)

    @Property(bool)
    def active(self):
        return self._active

    @active.setter
    def active(self, v):
        self._active = bool(v)
        self._restyle()

    @Property(bool)
    def muted(self):
        return self._muted

    @muted.setter
    def muted(self, v):
        self._muted = bool(v)
        self._restyle()

    @Property(QColor)
    def activeColor(self):
        return self._active_color

    @activeColor.setter
    def activeColor(self, c):
        self._active_color = QColor(c)
        self.update()

    @Property(QColor)
    def nameColor(self):
        return self._name_color

    # NOTE: colour qproperty setters must NOT re-polish — the app QSS applies
    # these via `qproperty-*` DURING a polish, so re-polishing here re-enters the
    # setter forever (RecursionError). Just store + repaint; label colours come
    # straight from the QSS selectors, so most of these are vestigial.
    @nameColor.setter
    def nameColor(self, c):
        self._name_color = QColor(c)
        self.update()

    @Property(QColor)
    def previewColor(self):
        return self._preview_color

    @previewColor.setter
    def previewColor(self, c):
        self._preview_color = QColor(c)
        self.update()

    @Property(QColor)
    def timeColor(self):
        return self._time_color

    @timeColor.setter
    def timeColor(self, c):
        self._time_color = QColor(c)
        self.update()

    @Property(QColor)
    def activeNameColor(self):
        return self._active_name_color

    @activeNameColor.setter
    def activeNameColor(self, c):
        self._active_name_color = QColor(c)
        self.update()

    @Property(QColor)
    def activeTimeColor(self):
        return self._active_time_color

    @activeTimeColor.setter
    def activeTimeColor(self, c):
        self._active_time_color = QColor(c)
        self.update()

    @Property(QColor)
    def accentColor(self):
        return self._accent

    @accentColor.setter
    def accentColor(self, c):
        self._accent = QColor(c)
        self._badge.setColors(self._accent, self._badge._fg)
        self.update()

    @Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, v):
        self._radius = max(0, int(v))
        self.update()

    @Property(int)
    def avatarSize(self):
        return self._avatar_size

    @avatarSize.setter
    def avatarSize(self, v):
        self._avatar_size = max(24, int(v))
        self._avatar.setFixedSize(self._avatar_size, self._avatar_size)
