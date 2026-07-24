"""QCustomCardStack, QCustomMenu, QCustomModal — interactive stack + popup
menu + modal dialog. Headless construction, behaviour and paint smoke."""

from qtpy.QtWidgets import QWidget, QLabel


def _paints(w, size=(320, 230)):
    w.resize(*size)
    w.ensurePolished()
    img = w.grab().toImage()
    return len({img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}) > 3


class TestCardStack:
    def _cards(self):
        return [
            {"brand": "VISA", "amount": "€ 1,00", "number": "1111", "top": "#0f4a43", "bottom": "#0a2b27"},
            {"brand": "MC", "amount": "€ 2,00", "number": "2222", "top": "#0f4a43", "bottom": "#0a2b27"},
            {"brand": "VISA", "amount": "€ 3,00", "number": "3333", "top": "#0f4a43", "bottom": "#0a2b27"},
        ]

    def test_set_cards_and_paint(self, qapp):
        from Custom_Widgets.QCustomCardStack import QCustomCardStack
        s = QCustomCardStack()
        s.setCards(self._cards())
        assert s.count() == 3
        assert s.currentIndexValue() == 0
        assert _paints(s)

    def test_next_cycles_and_signals(self, qapp):
        from Custom_Widgets.QCustomCardStack import QCustomCardStack
        s = QCustomCardStack()
        s.setCards(self._cards())
        seen = []
        s.currentChanged.connect(seen.append)
        s.next()
        assert s.currentIndexValue() == 1
        s.next(); s.next()          # wraps back to 0
        assert s.currentIndexValue() == 0
        assert seen == [1, 2, 0]

    def test_recolor_keeps_index(self, qapp):
        from Custom_Widgets.QCustomCardStack import QCustomCardStack
        s = QCustomCardStack()
        s.setCards(self._cards())
        s.next()
        s.setCardColors("#123456", "#654321")
        assert s.currentIndexValue() == 1


class TestMenu:
    def test_actions_and_trigger(self, qapp):
        from Custom_Widgets.QCustomMenu import QCustomMenu
        m = QCustomMenu()
        m.addAction("Export", "export")
        m.addSeparator()
        m.addAction("Delete", "del", danger=True)
        got = []
        m.triggered.connect(got.append)
        m.applyColors(bg="#ffffff", text="#111111", accent="#16a34a", danger="#e5484d")
        m._pick("export")
        assert got == ["export"]

    def test_panel_paints(self, qapp):
        from Custom_Widgets.QCustomMenu import QCustomMenu
        m = QCustomMenu()
        m.addAction("One", "one")
        m.addAction("Two", "two")
        m._panel.resize(200, 100)
        m._panel.ensurePolished()
        img = m._panel.grab().toImage()
        assert img.width() > 0 and img.height() > 0


class TestModal:
    def test_content_actions_and_signals(self, qapp):
        from Custom_Widgets.QCustomModal import QCustomModal
        host = QWidget(); host.resize(600, 400)
        m = QCustomModal(host)
        m.setTitle("Send money")
        m.setSubtitle("to a payee")
        m.addContent(QLabel("row"))
        m.addAction("Cancel", "cancel")
        m.addAction("Send", "send", primary=True)
        got = []
        m.triggered.connect(got.append)
        closed = []
        m.closed.connect(lambda: closed.append(True))
        m.showModal()
        assert not m.isHidden()     # shown (host isn't, so isVisible() would be False)
        m._pick("send")             # triggers + closes
        assert got == ["send"]
        assert closed == [True]
        assert m.isHidden()

    def test_backdrop_paints(self, qapp):
        from Custom_Widgets.QCustomModal import QCustomModal
        host = QWidget(); host.resize(500, 360)
        m = QCustomModal(host)
        m.setTitle("Hi")
        m.showModal()
        m.resize(500, 360)
        img = m.grab().toImage()
        assert img.width() == 500
