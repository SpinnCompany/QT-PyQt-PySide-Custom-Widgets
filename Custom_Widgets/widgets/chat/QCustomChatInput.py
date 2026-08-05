########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomChatInput - a message composer bar.
##
## The bottom "Write something…" row: attach + mic buttons, a text field, an
## emoji button and a send button, wired to signals (`sendMessage(text)` on
## Enter or send-click, plus `attachClicked` / `micClicked` / `emojiClicked`).
## The buttons carry stable objectNames (attachBtn / micBtn / emojiBtn / sendBtn
## / messageField) so their icons and colours are set from QSS
## (`#sendBtn { qproperty-icon: url(theme-icons:…) }`) — Python only reacts to
## the signals. Designer-droppable, so the whole bar is one widget in the form.
########################################################################
from qtpy.QtCore import Qt, Property, Signal, QSize
from qtpy.QtWidgets import (QFrame, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy)


class QCustomChatInput(QFrame):

    sendMessage = Signal(str)
    attachClicked = Signal()
    micClicked = Signal()
    emojiClicked = Signal()
    textChanged = Signal(str)

    WIDGET_ICON = "components/icons/chat_input.png"
    WIDGET_TOOLTIP = "A chat message composer bar"
    WIDGET_MODULE = "Custom_Widgets.QCustomChatInput"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomChatInput' name='customChatInput'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>560</width><height>64</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomChatInput",
        "props": {"placeholder": {"type": "string", "default": "   Write something.."},
                  "clearOnSend": {"type": "bool", "default": True},
                  "showAttach": {"type": "bool", "default": True},
                  "showMic": {"type": "bool", "default": True},
                  "showEmoji": {"type": "bool", "default": True},
                  "iconSize": {"type": "int", "default": 19}},
        "signals": ["sendMessage", "attachClicked", "micClicked", "emojiClicked", "textChanged"],
        "tokens_used": ["accent"],
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("QCustomChatInput")
        self._clear_on_send = True
        self._icon_size = 19

        lay = QHBoxLayout(self)
        lay.setContentsMargins(22, 12, 22, 14)
        lay.setSpacing(8)

        self._attach = self._icon_button("attachBtn", 38)
        self._mic = self._icon_button("micBtn", 38)
        self._field = QLineEdit(self)
        self._field.setObjectName("messageField")
        self._field.setPlaceholderText("   Write something..")
        self._field.setMinimumHeight(46)
        self._field.returnPressed.connect(self._emit_send)
        self._field.textChanged.connect(self.textChanged)
        self._emoji = self._icon_button("emojiBtn", 38)
        self._send = self._icon_button("sendBtn", 46)

        lay.addWidget(self._attach, 0)
        lay.addWidget(self._mic, 0)
        lay.addWidget(self._field, 1)
        lay.addWidget(self._emoji, 0)
        lay.addWidget(self._send, 0)

        self._attach.clicked.connect(self.attachClicked)
        self._mic.clicked.connect(self.micClicked)
        self._emoji.clicked.connect(self.emojiClicked)
        self._send.clicked.connect(self._emit_send)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _icon_button(self, name, size):
        btn = QPushButton(self)
        btn.setObjectName(name)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(size, size)
        btn.setIconSize(QSize(self._icon_size, self._icon_size))
        return btn

    def _emit_send(self):
        text = self._field.text().strip()
        if not text:
            return
        self.sendMessage.emit(text)
        if self._clear_on_send:
            self._field.clear()

    # ------------------------------------------------------------------ #
    ## Convenience accessors (the buttons/field are QSS-styleable by name)
    # ------------------------------------------------------------------ #
    def field(self):
        return self._field

    def text(self):
        return self._field.text()

    def setText(self, t):
        self._field.setText(str(t))

    def insertText(self, t):
        self._field.setText(self._field.text() + str(t))

    def sendButton(self):
        return self._send

    def emojiButton(self):
        return self._emoji

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(str)
    def placeholder(self):
        return self._field.placeholderText()

    @placeholder.setter
    def placeholder(self, v):
        self._field.setPlaceholderText(str(v))

    @Property(bool)
    def clearOnSend(self):
        return self._clear_on_send

    @clearOnSend.setter
    def clearOnSend(self, v):
        self._clear_on_send = bool(v)

    @Property(bool)
    def showAttach(self):
        return self._attach.isVisible()

    @showAttach.setter
    def showAttach(self, v):
        self._attach.setVisible(bool(v))

    @Property(bool)
    def showMic(self):
        return self._mic.isVisible()

    @showMic.setter
    def showMic(self, v):
        self._mic.setVisible(bool(v))

    @Property(bool)
    def showEmoji(self):
        return self._emoji.isVisible()

    @showEmoji.setter
    def showEmoji(self, v):
        self._emoji.setVisible(bool(v))

    @Property(int)
    def iconSize(self):
        return self._icon_size

    @iconSize.setter
    def iconSize(self, v):
        self._icon_size = max(10, int(v))
        for b in (self._attach, self._mic, self._emoji, self._send):
            b.setIconSize(QSize(self._icon_size, self._icon_size))
