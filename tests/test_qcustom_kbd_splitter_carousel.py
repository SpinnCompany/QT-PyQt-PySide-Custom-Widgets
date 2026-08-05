"""QCustomKbd + QCustomSplitter + QCustomCarousel."""

import xml.etree.ElementTree as ET


class TestKbd:
    def test_parse_shortcut_string(self, qapp):
        from Custom_Widgets.QCustomKbd import QCustomKbd
        k = QCustomKbd("Ctrl+Shift+K")
        assert k.keysList() == ["Ctrl", "Shift", "K"]
        assert k.keys == "Ctrl+Shift+K"

    def test_set_keys_list_and_property(self, qapp):
        from Custom_Widgets.QCustomKbd import QCustomKbd
        k = QCustomKbd()
        k.setKeys(["Cmd", "P"])
        assert k.keysList() == ["Cmd", "P"]
        k.keys = "Alt+F4"
        assert k.keysList() == ["Alt", "F4"]

    def test_custom_separator(self, qapp):
        from Custom_Widgets.QCustomKbd import QCustomKbd
        k = QCustomKbd("Ctrl-Alt-Del", separator="-")
        assert k.keysList() == ["Ctrl", "Alt", "Del"]

    def test_builds_keycap_widgets(self, qapp):
        from Custom_Widgets.QCustomKbd import QCustomKbd
        from qtpy.QtWidgets import QLabel
        k = QCustomKbd("Ctrl+K")
        caps = [w for w in k.findChildren(QLabel)
                if w.objectName() == "kbdKey"]
        assert [c.text() for c in caps] == ["Ctrl", "K"]

    def test_dom_xml_wellformed(self, qapp):
        from Custom_Widgets.QCustomKbd import QCustomKbd
        root = ET.fromstring(QCustomKbd.WIDGET_DOM_XML)
        assert root.find("widget").get("class") == "QCustomKbd"


class TestSplitter:
    def test_holds_widgets(self, qapp):
        from Custom_Widgets.QCustomSplitter import QCustomSplitter
        from qtpy.QtWidgets import QLabel
        s = QCustomSplitter()
        s.addWidget(QLabel("A"))
        s.addWidget(QLabel("B"))
        assert s.count() == 2

    def test_orientation_name(self, qapp):
        from Custom_Widgets.QCustomSplitter import QCustomSplitter
        from qtpy.QtCore import Qt
        s = QCustomSplitter(Qt.Horizontal)
        assert s.orientationName == "horizontal"
        s.orientationName = "vertical"
        assert s.orientation() == Qt.Vertical

    def test_dom_xml_wellformed(self, qapp):
        from Custom_Widgets.QCustomSplitter import QCustomSplitter
        root = ET.fromstring(QCustomSplitter.WIDGET_DOM_XML)
        assert root.find("widget").get("class") == "QCustomSplitter"


class TestCarousel:
    def _carousel(self, n=3):
        from Custom_Widgets.QCustomCarousel import QCustomCarousel
        from qtpy.QtWidgets import QLabel
        c = QCustomCarousel()
        for i in range(n):
            c.addSlide(QLabel("Slide %d" % i))
        return c

    def test_add_slides_and_dots(self, qapp):
        c = self._carousel(3)
        assert c.count() == 3
        assert len(c._dots) == 3
        assert c.currentIndex() == 0

    def test_next_previous_and_signal(self, qapp):
        c = self._carousel(3)
        seen = []
        c.currentChanged.connect(seen.append)
        c.next()
        c.next()
        assert c.currentIndex() == 2 and seen == [1, 2]

    def test_wrap_around(self, qapp):
        c = self._carousel(3)
        c.setCurrentIndex(2)
        c.next()                              # wraps 2 -> 0
        assert c.currentIndex() == 0

    def test_no_wrap_clamps(self, qapp):
        c = self._carousel(3)
        c.setWrap(False)
        c.setCurrentIndex(0)
        c.previous()                          # clamped at 0
        assert c.currentIndex() == 0
        c.setCurrentIndex(2)
        c.next()                              # clamped at last
        assert c.currentIndex() == 2

    def test_active_dot_tracks_current(self, qapp):
        c = self._carousel(3)
        c.setCurrentIndex(1)
        actives = [d.property("active") for d in c._dots]
        assert actives == [False, True, False]

    def test_single_slide_has_no_dots(self, qapp):
        c = self._carousel(1)
        assert len(c._dots) == 0              # no indicators for a single slide

    def test_dom_xml_wellformed(self, qapp):
        from Custom_Widgets.QCustomCarousel import QCustomCarousel
        root = ET.fromstring(QCustomCarousel.WIDGET_DOM_XML)
        assert root.find("widget").get("class") == "QCustomCarousel"
