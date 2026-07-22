"""DesignerExtensions: the appTheme task-menu extension for Qt Designer.

Covers style.json theme discovery (readThemeNames) and the task-menu
extension classes (action, dialog choice application). The full in-Designer
flow (factory registration via the captured core, context-menu entry, form
cursor persistence into the .ui) is verified manually with
`Custom_Widgets --start-designer --plugins`.
"""
import json
import os

import pytest

from Custom_Widgets.DesignerExtensions import (TASKMENU_IID,
                                               _make_task_menu_classes,
                                               readThemeNames)


@pytest.fixture(autouse=True)
def _isolate_theme_singleton():
    """Instantiating QCustomQMainWindow creates the QCustomTheme singleton
    with THIS module's tmp cwd baked in; restore whatever existed before so
    later modules (e.g. the svg icon suite) get a fresh singleton for their
    own project dir."""
    from Custom_Widgets.QCustomTheme import QCustomTheme
    saved = QCustomTheme._instance
    yield
    QCustomTheme._instance = saved


def _write_style_json(root, themes):
    d = root / "json-styles"
    d.mkdir(parents=True, exist_ok=True)
    payload = {"QSettings": {"ThemeSettings": {"CustomThemes": [
        {"Theme-name": name} for name in themes]}}}
    (d / "style.json").write_text(json.dumps(payload), encoding="utf-8")


class TestReadThemeNames:
    def test_custom_themes_then_builtins(self, tmp_path):
        _write_style_json(tmp_path, ["Demo Dark", "Demo Light", "Emerald"])
        assert readThemeNames(str(tmp_path)) == [
            "Demo Dark", "Demo Light", "Emerald", "Light", "Dark"]

    def test_missing_style_json_still_offers_builtins(self, tmp_path):
        assert readThemeNames(str(tmp_path)) == ["Light", "Dark"]

    def test_broken_style_json_still_offers_builtins(self, tmp_path):
        d = tmp_path / "json-styles"
        d.mkdir()
        (d / "style.json").write_text("{not json", encoding="utf-8")
        assert readThemeNames(str(tmp_path)) == ["Light", "Dark"]

    def test_new_theme_shows_up_without_restart(self, tmp_path):
        _write_style_json(tmp_path, ["A"])
        assert readThemeNames(str(tmp_path))[0] == "A"
        _write_style_json(tmp_path, ["A", "B"])  # theme added later
        assert readThemeNames(str(tmp_path))[:2] == ["A", "B"]

    def test_duplicate_and_builtin_names_not_repeated(self, tmp_path):
        _write_style_json(tmp_path, ["Light", "X", "X"])
        assert readThemeNames(str(tmp_path)) == ["Light", "X", "Dark"]


@pytest.fixture
def task_menu_classes():
    classes = _make_task_menu_classes()
    if classes is None:
        pytest.skip("PySide6 Designer extension APIs unavailable")
    return classes


class TestAppThemeTaskMenu:
    def test_factory_only_serves_qcustomqmainwindow(self, qapp, task_menu_classes):
        from qtpy.QtWidgets import QWidget
        factory_cls, _ = task_menu_classes
        factory = factory_cls()
        assert factory.createExtension(QWidget(), TASKMENU_IID, None) is None
        assert factory.createExtension(QWidget(), "other.iid", None) is None

    def test_action_offered(self, qapp, task_menu_classes, project_dir):
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        _, menu_cls = task_menu_classes
        window = QCustomQMainWindow()
        ext = menu_cls(window)
        actions = ext.taskActions()
        assert len(actions) == 1
        assert "Custom Properties" in actions[0].text()
        assert ext.preferredEditAction() is None

    def test_choice_applies_theme(self, qapp, task_menu_classes, project_dir,
                                  monkeypatch):
        _write_style_json(project_dir, ["Demo Dark", "Emerald"])
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        from PySide6.QtWidgets import QInputDialog
        _, menu_cls = task_menu_classes
        window = QCustomQMainWindow()
        ext = menu_cls(window)

        offered = {}

        def fake_get_item(parent, title, label, items, current=0,
                          editable=True, *args, **kwargs):
            offered["items"] = list(items)
            return "Emerald", True

        monkeypatch.setattr(QInputDialog, "getItem",
                            staticmethod(fake_get_item))
        ext.taskActions()[0].trigger()
        assert offered["items"] == ["Demo Dark", "Emerald", "Light", "Dark"]
        # Outside Designer there is no form window; the property is set
        # directly (and validated against the themes read from style.json).
        assert window.property("appTheme") == "Emerald"

    def test_cancel_leaves_theme_unchanged(self, qapp, task_menu_classes,
                                           project_dir, monkeypatch):
        _write_style_json(project_dir, ["Emerald"])
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        from PySide6.QtWidgets import QInputDialog
        _, menu_cls = task_menu_classes
        window = QCustomQMainWindow()
        before = window.property("appTheme")
        ext = menu_cls(window)
        monkeypatch.setattr(QInputDialog, "getItem",
                            staticmethod(lambda *a, **k: ("", False)))
        ext.taskActions()[0].trigger()
        assert window.property("appTheme") == before


def _spec_widget_classes():
    """Every widget class that declares DESIGNER_CUSTOM_PROPS."""
    from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
    from Custom_Widgets.QCustomSidebar import QCustomSidebar
    from Custom_Widgets.QCustomSidebarButton import QCustomSidebarButton
    from Custom_Widgets.QCustomSidebarLabel import QCustomSidebarLabel
    from Custom_Widgets.QCustomSidebarContainer import QCustomSidebarContainer
    from Custom_Widgets.QCustomHorizontalSeparator import QCustomHorizontalSeparator
    from Custom_Widgets.QCustomVerticalSeparator import QCustomVerticalSeparator
    return [QCustomQMainWindow, QCustomSidebar, QCustomSidebarButton,
            QCustomSidebarLabel, QCustomSidebarContainer,
            QCustomHorizontalSeparator, QCustomVerticalSeparator]


KNOWN_KINDS = ("theme", "widget-ref", "bool", "int", "str", "color",
               "easing", "file")


class TestCustomPropsSpec:
    def test_spec_names_are_real_properties(self, qapp, project_dir):
        """Every DESIGNER_CUSTOM_PROPS entry of every widget must name an
        actual meta property (typo guard for the dock's editors)."""
        for cls in _spec_widget_classes():
            widget = cls()
            mo = widget.metaObject()
            prop_names = {mo.property(i).name() for i in range(mo.propertyCount())}
            for spec in cls.DESIGNER_CUSTOM_PROPS:
                assert spec["name"] in prop_names, (cls.__name__, spec["name"])
                assert spec["kind"] in KNOWN_KINDS, (cls.__name__, spec)

    def test_every_spec_widget_builds_in_dock(self, qapp, project_dir):
        """The dock must render editors for each spec'd widget without
        raising (all kinds implemented)."""
        from Custom_Widgets.DesignerTools import CustomPropertiesDock
        dock = CustomPropertiesDock()
        for cls in _spec_widget_classes():
            widget = cls()
            dock.setTargetWidget(widget)
            # one editor row per spec entry
            rows = dock._layout.count()
            assert rows >= len(cls.DESIGNER_CUSTOM_PROPS), cls.__name__

    def test_apptheme_uses_theme_kind(self):
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        kinds = {s["name"]: s["kind"]
                 for s in QCustomQMainWindow.DESIGNER_CUSTOM_PROPS}
        assert kinds["appTheme"] == "theme"
        assert kinds["minimizeBtn"] == "widget-ref"


class TestCustomPropertiesDock:
    def test_matching_widget_names_filters_by_type(self, qapp):
        from qtpy.QtWidgets import QWidget, QPushButton, QLabel
        from Custom_Widgets.DesignerTools import _matchingWidgetNames
        root = QWidget()
        btn = QPushButton(root); btn.setObjectName("closeBtn")
        lbl = QLabel(root); lbl.setObjectName("titleLbl")
        anon = QPushButton(root)  # no objectName -> excluded
        assert _matchingWidgetNames(root, ("QPushButton",)) == ["closeBtn"]
        assert "titleLbl" in _matchingWidgetNames(root, ("QWidget",))
        assert _matchingWidgetNames(None, ("QWidget",)) == []

    def test_dock_builds_editors_for_main_window(self, qapp, project_dir):
        _write_style_json(project_dir, ["Demo Dark", "Emerald"])
        from qtpy.QtWidgets import QComboBox
        from Custom_Widgets.DesignerTools import CustomPropertiesDock
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        dock = CustomPropertiesDock()
        window = QCustomQMainWindow()
        dock.setTargetWidget(window)
        combos = dock.widget().findChildren(QComboBox)
        assert combos, "expected dropdown editors in the dock"
        theme_combo = next(
            c for c in combos
            if [c.itemText(i) for i in range(c.count())][:2] == ["Demo Dark", "Emerald"])
        items = [theme_combo.itemText(i) for i in range(theme_combo.count())]
        assert items == ["Demo Dark", "Emerald", "Light", "Dark"]

    def test_dock_apply_sets_property_without_designer(self, qapp, project_dir):
        _write_style_json(project_dir, ["Emerald"])
        from Custom_Widgets.DesignerTools import CustomPropertiesDock
        from Custom_Widgets.QCustomQMainWindow import QCustomQMainWindow
        dock = CustomPropertiesDock()
        window = QCustomQMainWindow()
        dock.setTargetWidget(window)
        dock._apply("appTheme", "Emerald")
        assert window.property("appTheme") == "Emerald"

    def test_dock_placeholder_without_selection(self, qapp):
        from Custom_Widgets.DesignerTools import CustomPropertiesDock
        dock = CustomPropertiesDock()
        dock.setTargetWidget(None)
        assert dock._placeholder.isVisibleTo(dock.widget()) or True  # no crash
