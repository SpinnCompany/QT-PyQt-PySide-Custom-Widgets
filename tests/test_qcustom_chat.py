"""Chat-widget family: bubble, divider, list, list-item, thread, input, typing
indicator and voice message. Headless behavioural coverage (part of the widget
hardening pass toward the tiering gate)."""


def _painted(w, size=(120, 40)):
    """Grab the widget and return the count of distinct pixel colours - proof it
    actually painted something rather than a blank rect."""
    w.resize(*size)
    w.ensurePolished()
    img = w.grab().toImage()
    return len({img.pixel(x, y) for y in range(0, img.height(), 4)
                for x in range(0, img.width(), 4)})


class TestChatBubble:
    def test_construct_sides_and_text(self, qapp):
        from Custom_Widgets.QCustomChatBubble import QCustomChatBubble
        b = QCustomChatBubble(text="hello", side="incoming")
        assert b.text == "hello" and b.side == "incoming"     # Designer @Property
        b.side = "outgoing"
        assert b.side == "outgoing"
        b.setText("changed")
        assert b.text == "changed"

    def test_meta_setters_and_paint(self, qapp):
        from Custom_Widgets.QCustomChatBubble import QCustomChatBubble
        b = QCustomChatBubble(text="hi there")
        b.setSender("Ada")
        b.setTime("09:41")
        b.setFoot("delivered")
        assert _painted(b, (160, 80)) > 1


class TestChatDivider:
    def test_text_and_variant_props(self, qapp):
        from Custom_Widgets.QCustomChatDivider import QCustomChatDivider
        d = QCustomChatDivider(text="Today", variant="pill")
        assert d.text == "Today" and d.variant == "pill"       # both Designer @Property
        d.variant = "line"
        d.text = "Yesterday"
        assert d.variant == "line" and d.text == "Yesterday"


class TestChatListItem:
    def test_props_and_click_signal(self, qapp):
        from qtpy.QtCore import Qt, QPoint
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomChatListItem import QCustomChatListItem
        it = QCustomChatListItem(name="Ada", preview="hey", time="09:41")
        assert it.name == "Ada" and it.preview == "hey"        # Designer @Property
        it.setName("Ben")
        it.setPreview("yo")
        it.setTime("10:00")
        assert it.name == "Ben" and it.preview == "yo"
        it.unread = 3                        # unread badge count (@Property)
        assert it.unread == 3

        seen = []
        it.clicked.connect(lambda: seen.append(1))
        ev = QMouseEvent(QMouseEvent.MouseButtonPress, QPoint(4, 4),
                         Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        it.mousePressEvent(ev)
        assert seen == [1]


class TestChatList:
    def test_set_conversations_and_current(self, qapp):
        from Custom_Widgets.QCustomChatList import QCustomChatList
        lst = QCustomChatList()
        lst.setConversations([
            {"name": "Ada", "preview": "hi", "time": "1m", "unread": 2},
            {"name": "Ben", "preview": "yo", "time": "3m"},
            {"name": "Cara", "preview": "ok", "time": "9m", "muted": True},
        ])
        assert lst.count() == 3
        assert lst.currentIndex() == 0        # first row auto-selected (no emit)

        got = []
        lst.currentChanged.connect(got.append)
        lst.setCurrentIndex(2)
        assert lst.currentIndex() == 2 and got == [2]

    def test_empty_conversations_safe(self, qapp):
        from Custom_Widgets.QCustomChatList import QCustomChatList
        lst = QCustomChatList()
        lst.setConversations([])
        lst.setConversations(None)
        assert lst.count() == 0


class TestChatThread:
    def test_set_messages_mixed_kinds(self, qapp):
        from Custom_Widgets.QCustomChatThread import QCustomChatThread
        t = QCustomChatThread()
        t.setSenderName("Ada")
        t.setMessages([
            {"kind": "date", "text": "Today"},
            {"kind": "text", "text": "hey", "side": "incoming"},
            {"kind": "text", "text": "hi!", "side": "outgoing"},
            {"kind": "typing"},
        ])
        qapp.processEvents()
        assert _painted(t, (240, 200)) >= 1

    def test_empty_messages_safe(self, qapp):
        from Custom_Widgets.QCustomChatThread import QCustomChatThread
        t = QCustomChatThread()
        t.setMessages([])
        t.setMessages(None)


class TestChatInput:
    def test_send_signal_and_clear(self, qapp):
        from Custom_Widgets.QCustomChatInput import QCustomChatInput
        inp = QCustomChatInput()
        sent = []
        inp.sendMessage.connect(sent.append)
        inp.setText("  hello world  ")
        inp.sendButton().click()
        assert sent == ["hello world"]        # stripped
        assert inp.text() == ""               # clearOnSend default True

    def test_empty_send_is_ignored(self, qapp):
        from Custom_Widgets.QCustomChatInput import QCustomChatInput
        inp = QCustomChatInput()
        sent = []
        inp.sendMessage.connect(sent.append)
        inp.setText("   ")
        inp.sendButton().click()
        assert sent == []

    def test_keep_text_when_clear_off(self, qapp):
        from Custom_Widgets.QCustomChatInput import QCustomChatInput
        inp = QCustomChatInput()
        inp.clearOnSend = False
        inp.setText("stay")
        inp.sendButton().click()
        assert inp.text() == "stay"

    def test_placeholder_and_insert(self, qapp):
        from Custom_Widgets.QCustomChatInput import QCustomChatInput
        inp = QCustomChatInput()
        inp.placeholder = "Message..."
        assert inp.placeholder == "Message..."
        inp.setText("ab")
        inp.insertText("cd")
        assert inp.text() == "abcd"


class TestTypingIndicator:
    def test_start_stop_running(self, qapp):
        from Custom_Widgets.QCustomTypingIndicator import QCustomTypingIndicator
        ti = QCustomTypingIndicator()
        ti.start()
        assert ti.running is True
        ti.stop()
        assert ti.running is False
        ti.running = True                     # property path
        assert ti.running is True


class TestVoiceMessage:
    def test_progress_and_paint(self, qapp):
        from Custom_Widgets.QCustomVoiceMessage import QCustomVoiceMessage
        vm = QCustomVoiceMessage()
        vm.progress = 0.5                     # Designer @Property (float 0..1)
        vm.playing = True
        assert vm.progress == 0.5 and vm.playing is True
        assert _painted(vm, (220, 56)) > 1
