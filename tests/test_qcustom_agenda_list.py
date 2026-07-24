"""QCustomAgendaList — headless construction + paint smoke, status colours,
itemsJson round-trip, itemClicked, sizing."""

from qtpy.QtGui import QColor


def _img(w, size=(320, 320)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=40):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestAgendaList:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
        w = QCustomAgendaList()
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 3

    def test_status_marker_colours(self, qapp):
        from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
        w = QCustomAgendaList()
        w.doneColor = "#00e676"; w.activeColor = "#ffab00"
        img = _img(w)
        assert _has_color(img, "#00e676"), "done colour missing"
        assert _has_color(img, "#ffab00"), "active colour missing"

    def test_set_items_and_height(self, qapp):
        from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
        w = QCustomAgendaList()
        w.setItems([{"time": "10:00", "title": "One", "status": "pending"},
                    {"time": "11:00", "title": "Two", "status": "done"}])
        assert len(w.items()) == 2
        assert w.sizeHint().height() == int(2 * w._row_height())
        _img(w)

    def test_items_json_roundtrip(self, qapp):
        from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
        import json
        w = QCustomAgendaList()
        w.itemsJson = json.dumps([{"time": "9", "title": "Standup", "status": "active"}])
        assert w.items()[0]["title"] == "Standup"
        assert "Standup" in w.itemsJson

    def test_item_clicked_signal(self, qapp):
        from qtpy.QtCore import QPointF, Qt, QEvent
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomAgendaList import QCustomAgendaList
        w = QCustomAgendaList()
        _img(w)
        seen = []
        w.itemClicked.connect(seen.append)
        rh = w._row_height()
        pt = QPointF(120, rh * 2 + rh / 2)      # third row
        ev = QMouseEvent(QEvent.MouseButtonPress, pt, Qt.LeftButton,
                         Qt.LeftButton, Qt.NoModifier)
        w.mousePressEvent(ev)
        assert seen == [2]
