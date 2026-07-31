"""QCustomSankey — graph layout derived from a bare link list.

Nothing about a Sankey's layout is given: columns, vertical order and the
stacking of each ribbon at both ends all fall out of the links, so most of
these cover the derivation rather than the painting.
"""
from qtpy.QtCore import QEvent, QPointF, Qt
from qtpy.QtGui import QMouseEvent

LINKS = [("Search", "Signup", 120), ("Social", "Signup", 80),
         ("Referral", "Signup", 45), ("Signup", "Trial", 150),
         ("Signup", "Bounce", 95), ("Trial", "Paid", 70),
         ("Trial", "Churn", 80)]


def _chart(links=LINKS, size=(560, 340)):
    from Custom_Widgets.QCustomSankey import QCustomSankey
    c = QCustomSankey(links=list(links))
    c.resize(*size)
    return c


class TestSankeyData:
    def test_links(self, qapp):
        c = _chart()
        assert c.linkCount() == 7
        assert c.links()[0] == ("Search", "Signup", 120.0)

    def test_accepts_dicts(self, qapp):
        c = _chart([{"source": "A", "target": "B", "value": 5}])
        assert c.links() == [("A", "B", 5.0)]

    def test_drops_unlayoutable_links(self, qapp):
        """Self-loops, zero flows and unnamed ends cannot be drawn."""
        c = _chart([("A", "B", 5), ("A", "A", 3), ("A", "B", 0),
                    ("", "B", 4), ("A", "", 4), ("A", "B", "x"), None])
        assert c.linkCount() == 1

    def test_nodes_in_first_seen_order(self, qapp):
        c = _chart([("A", "B", 1), ("C", "B", 1)])
        assert c.nodes() == ["A", "B", "C"]

    def test_node_value_is_max_of_in_and_out(self, qapp):
        c = _chart()
        assert c.nodeValue("Signup") == 245.0      # in 245, out 245
        assert c.nodeValue("Search") == 120.0      # out only
        assert c.nodeValue("Paid") == 70.0         # in only

    def test_clear(self, qapp):
        c = _chart()
        c.clearLinks()
        assert c.linkCount() == 0 and c.nodes() == []

    def test_empty_is_safe(self, qapp):
        c = _chart([])
        assert c.columns() == []
        c.grab()


class TestSankeyLayout:
    def test_depths(self, qapp):
        c = _chart()
        depths = c.nodeDepths()
        assert depths["Search"] == 0
        assert depths["Signup"] == 1
        assert depths["Trial"] == 2
        assert depths["Paid"] == 3

    def test_depth_takes_the_longest_path(self, qapp):
        """Fed by both a 1-hop and a 2-hop path, a node must sit after both
        or its ribbons run backwards."""
        c = _chart([("A", "B", 1), ("B", "C", 1), ("A", "C", 1)])
        assert c.nodeDepths()["C"] == 2

    def test_cycle_does_not_hang(self, qapp):
        """Relaxation is bounded by node count, so a cycle terminates."""
        c = _chart([("A", "B", 1), ("B", "C", 1), ("C", "A", 1)])
        assert isinstance(c.nodeDepths(), dict)
        c.grab()

    def test_columns_group_by_depth(self, qapp):
        c = _chart()
        columns = c.columns()
        assert columns[0] == ["Search", "Social", "Referral"]
        assert columns[1] == ["Signup"]

    def test_one_rect_per_node(self, qapp):
        c = _chart()
        c.grab()
        assert set(c.nodeRects()) == set(c.nodes())

    def test_columns_run_left_to_right(self, qapp):
        c = _chart()
        c.grab()
        rects = c.nodeRects()
        assert rects["Search"].left() < rects["Signup"].left() < rects["Trial"].left()

    def test_node_height_tracks_throughput(self, qapp):
        c = _chart()
        c.grab()
        rects = c.nodeRects()
        assert rects["Search"].height() > rects["Referral"].height()

    def test_nodes_stay_inside_the_widget(self, qapp):
        c = _chart()
        c.grab()
        for name, rect in c.nodeRects().items():
            assert rect.top() >= 0 and rect.bottom() <= c.height() + 1
            assert rect.left() >= 0 and rect.right() <= c.width() + 1

    def test_one_ribbon_per_link(self, qapp):
        c = _chart()
        c.grab()
        assert len(c.ribbons()) == c.linkCount()

    def test_ribbons_are_not_empty(self, qapp):
        c = _chart()
        c.grab()
        assert all(not path.isEmpty() for path in c.ribbons())

    def test_ribbon_stacking_fills_its_node(self, qapp):
        """Every ribbon leaving a node stacks within that node's height, or
        the diagram claims flow the node does not have.

        Measured at the SOURCE end via the path's first element, not with
        boundingRect(): a ribbon is a cubic spanning two columns, so its
        bounding box includes the curve's excursion toward the target and is
        legitimately taller than either node.
        """
        c = _chart()
        c.grab()
        rects = c.nodeRects()
        ribbons = c.ribbons()
        for name in c.nodes():
            outgoing = [i for i, (s, _t, _v) in enumerate(c.links()) if s == name]
            if len(outgoing) < 2:
                continue
            tops = [ribbons[i].elementAt(0).y for i in outgoing]
            node = rects[name]
            assert min(tops) >= node.top() - 1
            assert max(tops) <= node.bottom() + 1

    def test_sink_detection(self, qapp):
        c = _chart()
        assert c.isSink("Bounce") is True       # dead end mid-graph
        assert c.isSink("Paid") is True
        assert c.isSink("Signup") is False


class TestSankeyInteraction:
    def test_node_at(self, qapp):
        c = _chart()
        c.grab()
        assert c.nodeAt(c.nodeRects()["Signup"].center()) == "Signup"

    def test_node_at_misses(self, qapp):
        c = _chart()
        c.grab()
        assert c.nodeAt(QPointF(0, 0)) == ""

    def test_node_hover_and_click(self, qapp):
        c = _chart()
        c.grab()
        hovered, clicked = [], []
        c.nodeHovered.connect(hovered.append)
        c.nodeClicked.connect(clicked.append)
        centre = c.nodeRects()["Trial"].center()
        c.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, centre, Qt.NoButton,
                                     Qt.NoButton, Qt.NoModifier))
        c.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, centre,
                                        Qt.LeftButton, Qt.LeftButton,
                                        Qt.NoModifier))
        assert hovered == ["Trial"] and clicked == ["Trial"]
        c.leaveEvent(QEvent(QEvent.Leave))
        assert hovered == ["Trial", ""]

    def test_link_at_finds_a_ribbon(self, qapp):
        c = _chart()
        c.grab()
        ribbon = c.ribbons()[0]
        assert c.linkAt(ribbon.boundingRect().center()) >= 0


class TestSankeyDesigner:
    def test_links_csv_roundtrip(self, qapp):
        c = _chart([])
        c.linksCsv = "A>B=10;B>C=4"
        assert c.linkCount() == 2
        assert c.linksCsv == "A>B=10;B>C=4"

    def test_links_csv_skips_malformed(self, qapp):
        c = _chart([])
        c.linksCsv = "A>B=10;nonsense;C>D;E>F=x;;G>H=2"
        assert [s for s, _t, _v in c.links()] == ["A", "G"]

    def test_node_colors_csv(self, qapp):
        c = _chart()
        c.nodeColorsCsv = "Signup=#ff0000,Paid=#00ff00"
        assert c.nodeColor("Signup").name() == "#ff0000"
        assert c.nodeColor("Paid").name() == "#00ff00"
        assert c.nodeColor("Search").isValid()

    def test_numeric_properties_clamp(self, qapp):
        c = _chart()
        c.nodeWidth = 0
        c.nodePadding = -5
        c.linkOpacity = 5
        c.curvature = -1
        assert c.nodeWidth == 2 and c.nodePadding == 0
        assert c.linkOpacity == 1.0 and c.curvature == 0.0


class TestSankeyPainting:
    def test_paints(self, qapp):
        c = _chart()
        img = c.grab().toImage()
        colors = {img.pixel(x, y) for y in range(0, img.height(), 4)
                  for x in range(0, img.width(), 4)}
        assert len(colors) > 3

    def test_labels_toggle_changes_render(self, qapp):
        on = _chart()
        off = _chart()
        off.showLabels = False
        assert on.grab().toImage() != off.grab().toImage()

    def test_values_toggle_changes_render(self, qapp):
        plain = _chart()
        valued = _chart()
        valued.showValues = True
        assert plain.grab().toImage() != valued.grab().toImage()

    def test_curvature_changes_render(self, qapp):
        curved = _chart()
        straight = _chart()
        straight.curvature = 0.0
        assert curved.grab().toImage() != straight.grab().toImage()

    def test_no_qtcharts_import(self, qapp):
        import ast
        import Custom_Widgets.QCustomSankey as mod
        tree = ast.parse(open(mod.__file__, encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not any("QtChart" in n for n in imported), imported

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        c = _chart()
        c.ensurePolished()
        assert c.labelColor.name().lower() == "#0f172a"
        qapp.setStyleSheet("")
