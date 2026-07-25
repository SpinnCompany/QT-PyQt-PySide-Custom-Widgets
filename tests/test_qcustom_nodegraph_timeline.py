"""Smoke + behaviour tests for the two node-based-studio widgets:
QCustomNodeGraph (canvas, nodes, ports, bezier edges) and
QCustomMediaTimeline (ruler, playhead, clips, waveform). They must construct,
paint a non-trivial image, round-trip their colour props, and honour the
data + interaction APIs."""

from qtpy.QtGui import QColor


def _img(w, size=(640, 420)):
    w.resize(*size)
    w.ensurePolished()
    return w.grab().toImage()


def _distinct_colours(img, step=8):
    return {img.pixel(x, y) for y in range(0, img.height(), step)
            for x in range(0, img.width(), step)}


class TestNodeGraph:
    def _graph(self):
        from Custom_Widgets.QCustomNodeGraph import QCustomNodeGraph
        g = QCustomNodeGraph()
        g.setGraph({
            "nodes": [
                {"nid": "a", "title": "Ideas", "x": 20, "y": 30, "w": 200, "h": 130,
                 "text": "hello", "outputs": ["out"]},
                {"nid": "b", "title": "Settings", "x": 320, "y": 40, "w": 220, "h": 180,
                 "inputs": ["in"], "outputs": ["out"],
                 "rows": [{"label": "Mode", "value": "Fun", "dot": "#f2a63b"}]},
            ],
            "edges": [{"src": "a", "srcPort": 0, "dst": "b", "dstPort": 0}],
        })
        return g

    def test_builds_and_paints(self, qapp):
        g = self._graph()
        img = _img(g)
        assert len(_distinct_colours(img)) > 5

    def test_graph_model(self, qapp):
        g = self._graph()
        assert len(g._nodes) == 2
        assert len(g._edges) == 1
        assert g.nodeById("a").title == "Ideas"

    def test_add_edge_and_clear(self, qapp):
        g = self._graph()
        g.addEdge("b", 0, "a", 0, "#ff0000")
        assert len(g._edges) == 2
        g.clear()
        assert g._nodes == [] and g._edges == []

    def test_colour_props_roundtrip(self, qapp):
        g = self._graph()
        g.portColor = "#123456"
        g.edgeColor = "#654321"
        assert QColor(g.portColor).name() == "#123456"
        assert QColor(g.edgeColor).name() == "#654321"

    def test_set_node_position(self, qapp):
        g = self._graph()
        g.setNodePosition("a", 111, 222)
        assert g.nodeById("a").x == 111 and g.nodeById("a").y == 222


class TestMediaTimeline:
    def _tl(self):
        from Custom_Widgets.QCustomMediaTimeline import QCustomMediaTimeline
        tl = QCustomMediaTimeline()
        tl.setTimeline({
            "duration": 9, "position": 1.5,
            "tracks": [
                {"name": "Clip", "kind": "clips",
                 "clips": [{"start": 0.5, "end": 8.0, "color": "#c17ce0", "label": "Anim"}]},
                {"name": "Audio", "kind": "wave", "values": [0.2, -0.5, 0.8, -0.3, 0.6]},
            ],
        })
        return tl

    def test_builds_and_paints(self, qapp):
        tl = self._tl()
        img = _img(tl, size=(620, 150))
        assert len(_distinct_colours(img)) > 4

    def test_position_clamped_and_signal(self, qapp):
        tl = self._tl()
        seen = []
        tl.positionChanged.connect(seen.append)
        tl.setPosition(100)          # clamps to duration
        assert tl.positionSeconds() == 9.0
        assert seen and seen[-1] == 9.0

    def test_clip_model(self, qapp):
        tl = self._tl()
        assert len(tl._tracks) == 2
        assert tl._tracks[0].clips[0].label == "Anim"
        assert tl._tracks[1].kind == "wave" and len(tl._tracks[1].values) == 5

    def test_colour_props_roundtrip(self, qapp):
        tl = self._tl()
        tl.clipColor = "#00ff00"
        tl.playheadColor = "#ff00ff"
        assert QColor(tl.clipColor).name() == "#00ff00"
        assert QColor(tl.playheadColor).name() == "#ff00ff"

    def test_duration_property(self, qapp):
        tl = self._tl()
        tl.duration = 20
        assert tl.duration == 20.0
