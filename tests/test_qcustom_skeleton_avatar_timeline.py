"""QCustomSkeleton + QCustomAvatarGroup + QCustomTimeline."""
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLabel


class TestSkeleton:
    def test_shapes_and_animation(self, qapp):
        from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
        from qtpy.QtCore import QVariantAnimation
        s = QCustomSkeleton(shape="circle")
        assert s.shape == "circle"
        assert s.size().width() == 40 and s.size().height() == 40
        assert s._anim.state() == QVariantAnimation.Running   # shimmer running
        s.stop()
        assert s._anim.state() != QVariantAnimation.Running
        s.shape = "line"
        assert s.height() == 14

    def test_colors_via_qproperty_tokens(self, qapp):
        from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        s = QCustomSkeleton()
        s.ensurePolished()
        # skeleton_qss feeds surface-muted / surface via qproperty
        assert s.baseColor.name().lower() == "#f1f5f9"       # surface-muted
        assert s.highlightColor.name().lower() == "#ffffff"  # surface
        qapp.setStyleSheet("")

    def test_paints_without_error(self, qapp):
        from Custom_Widgets.QCustomSkeleton import QCustomSkeleton
        s = QCustomSkeleton(shape="rect")
        s.resize(180, 60)
        s._t = 0.5
        s.grab()                                             # must not raise (gradient stops valid)


class TestAvatarGroup:
    def test_overflow(self, qapp):
        from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
        g = QCustomAvatarGroup(maxVisible=3)
        g.setAvatars(["Ada Lovelace", "Alan Turing", "Grace Hopper",
                      "Linus Torvalds", "Ken Thompson"])
        circles = [c for c in g.findChildren(QLabel)]
        overflow = [c for c in circles if c.objectName() == "avatarOverflow"]
        shown = [c for c in circles if c.objectName() == "avatarCircle"]
        assert len(shown) == 3
        assert len(overflow) == 1 and overflow[0].text() == "+2"

    def test_no_overflow_when_within_max(self, qapp):
        from Custom_Widgets.QCustomAvatarGroup import QCustomAvatarGroup
        g = QCustomAvatarGroup(maxVisible=5)
        g.setAvatars(["Ada Lovelace", "Alan Turing"])
        overflow = [c for c in g.findChildren(QLabel) if c.objectName() == "avatarOverflow"]
        assert overflow == []

    def test_initials(self, qapp):
        from Custom_Widgets.QCustomAvatarGroup import _initials
        assert _initials("Ada Lovelace") == "AL"
        assert _initials("Cher") == "CH"
        assert _initials("") == "?"


class TestTimeline:
    def test_build_and_count(self, qapp):
        from Custom_Widgets.QCustomTimeline import QCustomTimeline
        t = QCustomTimeline()
        t.setItems([
            {"title": "Created", "time": "09:00", "description": "Ticket opened"},
            {"title": "In progress", "time": "11:30"},
            ("Resolved", "15:00"),
        ])
        assert t.count() == 3
        titles = [l.text() for l in t.findChildren(QLabel)
                  if l.objectName() == "timelineTitle"]
        assert titles == ["Created", "In progress", "Resolved"]

    def test_rail_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomTimeline import QCustomTimeline
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        t = QCustomTimeline()
        t.ensurePolished()
        assert t.lineColor.name().lower() == "#cbd5e1"       # outline
        assert t.dotColor.name().lower() == "#2563eb"        # accent
        qapp.setStyleSheet("")

    def test_per_item_dot_color_override(self, qapp):
        from Custom_Widgets.QCustomTimeline import QCustomTimeline, _Rail
        t = QCustomTimeline()
        t.addItem("Green step", color=QColor("#22c55e"))
        rail = t.findChildren(_Rail)[0]
        assert rail._dot == QColor("#22c55e")
