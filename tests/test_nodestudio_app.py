"""App-level checks for the examples/PySide6/NodeStudio build: the compiled
component forms build their promoted custom widgets, and the theme module
exposes a complete NodePalette for both themes. Loaded by file path so no
example package pollutes sys.modules."""

import importlib.util
import os

from qtpy.QtWidgets import QWidget

_APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "examples", "PySide6", "NodeStudio")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build(form_file, ui_cls, qapp):
    mod = _load(os.path.join(_APP, "src", form_file), form_file[:-3])
    host = QWidget()
    ui = getattr(mod, ui_cls)()
    ui.setupUi(host)
    return ui, host


class TestComponentForms:
    def test_canvas_form_builds_nodegraph(self, qapp):
        from Custom_Widgets.QCustomNodeGraph import QCustomNodeGraph
        ui, _ = _build("ui_CanvasComponent.py", "Ui_CanvasComponent", qapp)
        assert isinstance(ui.nodeGraph, QCustomNodeGraph)

    def test_timeline_form_builds_timeline(self, qapp):
        from Custom_Widgets.QCustomMediaTimeline import QCustomMediaTimeline
        ui, _ = _build("ui_TimelineComponent.py", "Ui_TimelineComponent", qapp)
        assert isinstance(ui.mediaTimeline, QCustomMediaTimeline)

    def test_thoughts_form_builds_codeeditor(self, qapp):
        from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
        ui, _ = _build("ui_ThoughtsComponent.py", "Ui_ThoughtsComponent", qapp)
        assert isinstance(ui.codeEditor, QCustomCodeEditor)

    def test_preview_form_builds_label(self, qapp):
        ui, _ = _build("ui_PreviewComponent.py", "Ui_PreviewComponent", qapp)
        assert ui.previewImage.objectName() == "previewImage"

    def test_mainwindow_form_has_containers(self, qapp):
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        mod = _load(os.path.join(_APP, "src", "ui_MainWindow.py"), "ui_MainWindow")
        win = QCustomQMainWindow()
        ui = mod.Ui_MainWindow()
        ui.setupUi(win)
        for c in ("canvasContainer", "thoughtsContainer",
                  "previewContainer", "timelineContainer"):
            assert hasattr(ui, c), c
        # the interactive controls live in the shell
        for b in ("tabNew", "rlLayers", "rrCursor", "playBtn", "exportBtn", "fabAdd"):
            assert hasattr(ui, b), b


class TestThemeModule:
    KEYS = {"canvasBg", "gridColor", "nodeColor", "nodeHeaderColor", "text",
            "muted", "ideas", "refs", "settings", "models", "cableWarm",
            "cableViolet", "cableIndigo", "clip", "wave"}

    def _theme(self):
        return _load(os.path.join(_APP, "gui", "theme.py"), "nodestudio_theme")

    def test_both_palettes_complete(self, qapp):
        T = self._theme()
        for name in (T.THEME_DARK, T.THEME_LIGHT):
            pal = T.node_palette(name)
            assert self.KEYS <= set(pal), "missing keys in %s" % name

    def test_is_light(self, qapp):
        T = self._theme()
        assert T.is_light("Studio Light") and not T.is_light("Studio Dark")
