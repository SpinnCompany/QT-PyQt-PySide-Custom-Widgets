"""QCustomEmptyState + QCustomFileDropZone + QCustomRangeSlider."""


class TestEmptyState:
    def test_content_and_action(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        e = QCustomEmptyState(title="No projects", description="Create one to begin")
        assert e._title.text() == "No projects"
        assert e._desc.isHidden() is False
        assert e._action.isHidden() is True       # hidden until action text set
        seen = []
        e.actionClicked.connect(lambda: seen.append(1))
        e.setActionText("New project")
        assert e._action.isHidden() is False and e._action.text() == "New project"
        e.actionButton().click()
        assert seen == [1]

    def test_description_toggles_visibility(self, qapp):
        from Custom_Widgets.QCustomEmptyState import QCustomEmptyState
        e = QCustomEmptyState()
        assert e._desc.isHidden() is True         # empty -> hidden
        e.setDescription("now visible")
        assert e._desc.isHidden() is False


class TestDropZone:
    def test_accepts_and_filters(self, qapp):
        from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
        z = QCustomFileDropZone(extensions=[".png", "jpg"])
        added = []
        z.filesDropped.connect(added.append)
        z._addPaths(["/a/photo.png", "/a/doc.pdf", "/a/pic.JPG"])
        assert z.files() == ["/a/photo.png", "/a/pic.JPG"]   # pdf filtered, case-insensitive
        assert added and added[-1] == ["/a/photo.png", "/a/pic.JPG"]

    def test_single_mode_replaces(self, qapp):
        from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
        z = QCustomFileDropZone(multiple=False)
        z._addPaths(["/a/one.txt"])
        z._addPaths(["/a/two.txt"])
        assert z.files() == ["/a/two.txt"]          # single: latest only

    def test_dedupe_and_clear(self, qapp):
        from Custom_Widgets.QCustomFileDropZone import QCustomFileDropZone
        z = QCustomFileDropZone()
        z._addPaths(["/a/x.txt", "/a/x.txt", "/a/y.txt"])
        assert z.files() == ["/a/x.txt", "/a/y.txt"]
        z.clear()
        assert z.files() == []


class TestRangeSlider:
    def test_values_and_clamp(self, qapp):
        from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
        s = QCustomRangeSlider(minimum=0, maximum=100)
        s.setValues(20, 80)
        assert s.values() == (20, 80)
        seen = []
        s.valuesChanged.connect(lambda lo, hi: seen.append((lo, hi)))
        s.setValues(-10, 200)                       # clamped to [0, 100]
        assert s.values() == (0, 100) and seen[-1] == (0, 100)

    def test_handles_dont_cross(self, qapp):
        from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
        s = QCustomRangeSlider(minimum=0, maximum=100)
        s.setValues(30, 70)
        s.setLowerValue(90)                         # can't pass the upper
        assert s.lowerValue == 70 and s.values() == (70, 70)
        s.setUpperValue(10)                         # can't pass the lower
        assert s.upperValue == 70

    def test_swap_if_reversed(self, qapp):
        from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
        s = QCustomRangeSlider()
        s.setValues(80, 20)                         # reversed -> swapped
        assert s.values() == (20, 80)

    def test_colors_via_qproperty(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomRangeSlider import QCustomRangeSlider
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        s = QCustomRangeSlider()
        s.ensurePolished()
        assert s.trackColor.name().lower() == "#cbd5e1"    # outline
        assert s.fillColor.name().lower() == "#2563eb"     # accent
        qapp.setStyleSheet("")
