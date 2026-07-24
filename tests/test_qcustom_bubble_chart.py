"""QCustomBubbleChart — headless construction + paint smoke, packing produces
non-overlapping bubbles, category colours render, itemsJson, bubbleClicked."""

import math
from qtpy.QtGui import QColor


def _img(w, size=(340, 320)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _has_color(img, target, tol=45):
    t = QColor(target)
    for y in range(0, img.height(), 3):
        for x in range(0, img.width(), 3):
            c = QColor(img.pixel(x, y))
            if (abs(c.red() - t.red()) + abs(c.green() - t.green())
                    + abs(c.blue() - t.blue())) <= tol:
                return True
    return False


class TestBubbleChart:
    def test_construct_and_paint(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart()
        img = _img(w)
        seen = {img.pixel(x, y) for y in range(0, img.height(), 6)
                for x in range(0, img.width(), 6)}
        assert len(seen) > 4

    def test_packing_no_overlap(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart(items=[{"label": "a", "value": 40},
                                      {"label": "b", "value": 30},
                                      {"label": "c", "value": 20},
                                      {"label": "d", "value": 10}])
        ns = w._nodes
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                d = math.hypot(ns[j]["x"] - ns[i]["x"], ns[j]["y"] - ns[i]["y"])
                # allow a tiny epsilon; relaxation should keep them apart
                assert d >= ns[i]["r"] + ns[j]["r"] - 1.0

    def test_area_proportional_to_value(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart(items=[{"label": "big", "value": 100},
                                      {"label": "small", "value": 25}])
        rbig = next(n["r"] for n in w._nodes if n["label"] == "big")
        rsmall = next(n["r"] for n in w._nodes if n["label"] == "small")
        assert rbig > rsmall

    def test_category_colours(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart(items=[{"label": "p", "value": 50, "category": "positive"},
                                      {"label": "n", "value": 50, "category": "negative"}])
        w.setCategoryColors({"positive": "#00c853", "negative": "#ff1744"})
        w.showLabels = False
        img = _img(w)
        assert _has_color(img, "#00c853") or _has_color(img, "#ff1744")

    def test_items_json_roundtrip(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        import json
        w = QCustomBubbleChart()
        w.itemsJson = json.dumps([{"label": "X", "value": 10, "category": "neutral"}])
        assert w.items()[0]["label"] == "X"
        assert "X" in w.itemsJson

    def test_bubble_clicked(self, qapp):
        from qtpy.QtCore import QPointF, Qt, QEvent
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart(items=[{"label": "solo", "value": 50}])
        w.showControls = False
        _img(w)
        seen = []
        w.bubbleClicked.connect(seen.append)
        label, cx, cy, r, _m = w._screen[0]
        pt = QPointF(cx, cy)
        press = QMouseEvent(QEvent.MouseButtonPress, pt, Qt.LeftButton,
                            Qt.LeftButton, Qt.NoModifier)
        release = QMouseEvent(QEvent.MouseButtonRelease, pt, Qt.LeftButton,
                              Qt.LeftButton, Qt.NoModifier)
        w.mousePressEvent(press)
        w.mouseReleaseEvent(release)          # click fires on release (not a drag)
        assert seen == ["solo"]

    def test_search_dims_and_zoom(self, qapp):
        from Custom_Widgets.QCustomBubbleChart import QCustomBubbleChart
        w = QCustomBubbleChart(items=[{"label": "Alpha", "value": 40},
                                      {"label": "Beta", "value": 30}])
        w.setSearchQuery("alph")
        assert w.searchQuery == "alph"
        _img(w)                               # non-matching bubble dims, still paints
        z0 = w._zoom
        w.zoomIn()
        assert w._zoom > z0
        w.resetView()
        assert w._zoom == 1.0
