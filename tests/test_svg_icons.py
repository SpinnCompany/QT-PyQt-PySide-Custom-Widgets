"""Tests for the SVG theme-icon pipeline.

Run locally with the project venv (PySide6 is the preferred binding):

    .venv/bin/python -m pytest tests/ -v

Run against another binding:

    QT_API=pyqt6 python -m pytest tests/ -v

See tests/run_all_bindings.sh for running the suite on every supported binding.
"""
import os
import re
import xml.etree.ElementTree as ET

import pytest

PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Custom_Widgets"))
MASTER_ICONS_DIR = os.path.join(PACKAGE_DIR, "Qss", "icons")

THEME_COLOR = "#ff5722"
THEME_FOLDER = THEME_COLOR.replace("#", "")


def master_icon_count():
    count = 0
    for root, dirs, files in os.walk(MASTER_ICONS_DIR):
        count += sum(1 for f in files if f.lower().endswith(".svg"))
    return count


def generated_svgs(base):
    found = []
    for root, dirs, files in os.walk(base):
        found.extend(os.path.join(root, f) for f in files if f.lower().endswith(".svg"))
    return found


@pytest.fixture
def theme_icons(theme, project_dir):
    """Generate the themed icon set once into a fresh project dir."""
    theme.generateIcons(None, THEME_COLOR, "", THEME_FOLDER, createQrc=False)
    return project_dir / "Qss" / "icons" / THEME_FOLDER


class TestThemeIconGeneration:
    def test_all_master_icons_generated_as_svg(self, theme_icons):
        assert theme_icons.is_dir()
        svgs = generated_svgs(str(theme_icons))
        assert len(svgs) == master_icon_count()

    def test_no_png_generated(self, theme_icons):
        pngs = [f for _, _, fs in os.walk(theme_icons) for f in fs if f.lower().endswith(".png")]
        assert pngs == []

    def test_icons_recolored_to_theme_color(self, theme_icons):
        sample = theme_icons / "feather" / "check.svg"
        content = sample.read_text(encoding="utf-8")
        assert THEME_COLOR in content
        assert "#ffffff" not in content

    def test_existing_icons_not_regenerated(self, theme, theme_icons):
        sample = theme_icons / "feather" / "check.svg"
        first_mtime = sample.stat().st_mtime_ns
        theme.generateIcons(None, THEME_COLOR, "", THEME_FOLDER, createQrc=False)
        assert sample.stat().st_mtime_ns == first_mtime

    def test_generation_is_fast(self, theme, project_dir):
        import time

        start = time.time()
        theme.generateIcons(None, "#123456", "", "123456", createQrc=False)
        elapsed = time.time() - start
        # cairosvg took minutes; the text-substitution pipeline must stay fast
        assert elapsed < 15


class TestSharedIconSet:
    """One icons folder (Qss/icons/icons) shared by the app stylesheet,
    ui files and Qt Designer - recolored in place when the color changes."""

    @pytest.fixture
    def shared_set(self, theme, project_dir):
        theme.generateNewIcons(None)
        return project_dir / "Qss" / "icons"

    def test_single_folder_only(self, shared_set):
        subdirs = sorted(d.name for d in shared_set.iterdir() if d.is_dir())
        assert subdirs == ["icons"], "expected exactly one shared icon folder"

    def test_icons_are_svg_sized_24(self, shared_set):
        sample = shared_set / "icons" / "feather" / "check.svg"
        content = sample.read_text(encoding="utf-8")
        assert 'width="24"' in content
        assert 'height="24"' in content
        assert "viewBox=" in content  # keeps scalability

    def test_namespaced_material_icons_also_sized_24(self, shared_set):
        pack = shared_set / "icons" / "material_design"
        sample = next(pack.glob("*.svg"))
        content = sample.read_text(encoding="utf-8")
        # material masters use a namespaced root (<ns0:svg>)
        assert 'width="24"' in content
        assert 'height="24"' in content
        assert 'width="100"' not in content

    def test_qrc_prefixes_use_underscores(self, shared_set):
        text = (shared_set / "_icons.qrc").read_text(encoding="utf-8")
        assert 'prefix="font_awesome_solid"' in text
        # nested pack prefixes must never contain path separators
        assert re.search(r'prefix="[^"]*/[^"]*"', text) is None

    def test_designer_icons_color_applies_to_all_icons(self, theme, shared_set):
        from qtpy.QtCore import QSettings

        sample = shared_set / "icons" / "feather" / "check.svg"
        old_color = theme.designerIconsColor

        theme.designerIconsColor = "#ab34cd"
        try:
            theme.generateNewIcons(None)
            assert "#ab34cd" in sample.read_text(encoding="utf-8")
            assert QSettings().value("GENERATED-ICONS-COLOR") == "#ab34cd"
        finally:
            theme.designerIconsColor = old_color

    def test_theme_mode_follows_active_theme(self, theme, shared_set):
        sample = shared_set / "icons" / "feather" / "check.svg"
        old_color = theme.designerIconsColor

        theme.designerIconsColor = "theme"
        try:
            theme.generateNewIcons(None)
            active = theme.getCurrentThemeInfo()["icons-color"]
            assert active in sample.read_text(encoding="utf-8")
        finally:
            theme.designerIconsColor = old_color

    def test_qss_icons_color_override_wins(self, theme, shared_set, project_dir):
        scss_dir = project_dir / "Qss" / "scss"
        scss_dir.mkdir(parents=True, exist_ok=True)
        (scss_dir / "defaultStyle.scss").write_text(
            "// user styles\n$ICONS_COLOR: #12ef56;\n", encoding="utf-8")

        old_color = theme.designerIconsColor
        theme.designerIconsColor = "#ab34cd"  # must lose against the QSS var
        try:
            theme.generateNewIcons(None)
            sample = shared_set / "icons" / "feather" / "check.svg"
            assert "#12ef56" in sample.read_text(encoding="utf-8")
        finally:
            theme.designerIconsColor = old_color

    def test_qrc_lists_only_svg(self, shared_set):
        qrc = shared_set / "_icons.qrc"
        assert qrc.is_file()
        text = qrc.read_text(encoding="utf-8")
        assert ".svg</file>" in text
        assert ".png" not in text

    def test_qrc_is_valid_xml_and_files_exist(self, shared_set):
        qrc = shared_set / "_icons.qrc"
        tree = ET.parse(qrc)
        entries = [el.text for el in tree.iter("file")]
        assert entries
        # qrc <file> entries are relative to the qrc file's directory
        for entry in entries[:50]:
            assert (shared_set / entry).is_file(), entry


class TestSvgHelpers:
    def test_set_svg_size_replaces_existing_attributes(self, theme):
        svg = '<svg xmlns="x" width="100" height="100" viewBox="0 0 24 24"><path d="m0 0"/></svg>'
        out = theme._setSvgSize(svg, 24, 24)
        assert 'width="24"' in out and 'height="24"' in out
        assert 'width="100"' not in out and 'height="100"' not in out
        assert 'viewBox="0 0 24 24"' in out

    def test_set_svg_size_adds_missing_attributes(self, theme):
        svg = '<svg xmlns="x" viewBox="0 0 24 24"><path d="m0 0"/></svg>'
        out = theme._setSvgSize(svg, 24, 24)
        assert 'width="24"' in out and 'height="24"' in out

    def test_set_svg_size_self_closing_root(self, theme):
        svg = '<svg xmlns="x" width="10" height="10"/>'
        out = theme._setSvgSize(svg, 24, 24)
        assert out.endswith('width="24" height="24"/>')

    def test_resolve_maps_png_to_svg(self, theme):
        assert theme._resolveThemedIconPath("/p/icons/abc/feather/save.png") == "/p/icons/abc/feather/save.svg"
        assert theme._resolveThemedIconPath("/p/icons/abc/feather/save.PNG") == "/p/icons/abc/feather/save.svg"

    def test_resolve_leaves_other_paths_alone(self, theme):
        assert theme._resolveThemedIconPath("/p/icons/save.svg") == "/p/icons/save.svg"
        assert theme._resolveThemedIconPath("/p/photo.jpg") == "/p/photo.jpg"


class TestQtRendering:
    def test_qicon_renders_generated_svg(self, theme_icons):
        from qtpy.QtGui import QIcon

        pm = QIcon(str(theme_icons / "feather" / "check.svg")).pixmap(64, 64)
        assert not pm.isNull()
        assert pm.width() == 64

    def test_qss_search_path_resolves_svg(self, theme_icons, project_dir):
        from qtpy.QtCore import QDir
        from qtpy.QtGui import QPixmap

        QDir.addSearchPath("theme-icons", str(project_dir / "Qss" / "icons") + os.sep)
        pm = QPixmap(f"theme-icons:{THEME_FOLDER}/feather/check.svg")
        assert not pm.isNull()

    def test_material_icons_load_via_qpixmap(self, theme, project_dir):
        """Designer previews use the QPixmap/QImageReader path, which rejects
        namespace-prefixed svg roots (<ns0:svg>). Generated icons must be
        normalized so this path works for every pack."""
        from qtpy.QtGui import QPixmap

        theme.generateNewIcons(None)
        pack = project_dir / "Qss" / "icons" / "icons" / "material_design"
        sample = next(pack.glob("*.svg"))
        assert sample.read_text(encoding="utf-8").lstrip().startswith("<svg")
        pm = QPixmap(str(sample))
        assert not pm.isNull()
        assert pm.width() > 0

    def test_svg_plugin_available(self, qapp):
        from qtpy.QtGui import QImageReader

        formats = [bytes(f).decode().lower() for f in QImageReader.supportedImageFormats()]
        assert "svg" in formats


class TestNoLegacyPngPipeline:
    def test_shipped_styles_scss_uses_svg_only(self):
        styles = os.path.join(PACKAGE_DIR, "Qss", "scss", "_styles.scss")
        with open(styles, encoding="utf-8") as f:
            content = f.read()
        assert ".png" not in content
        assert re.search(r"\$PATH_RESOURCES\+'[^']+\.svg'", content)

    def test_cairosvg_not_imported(self):
        source = os.path.join(PACKAGE_DIR, "QCustomTheme.py")
        with open(source, encoding="utf-8") as f:
            content = f.read()
        assert "cairosvg" not in content

    def test_cairosvg_not_in_install_requires(self):
        setup_py = os.path.join(PACKAGE_DIR, "..", "setup.py")
        with open(setup_py, encoding="utf-8") as f:
            content = f.read()
        assert "cairosvg" not in content


class TestNewUiCommand:
    def test_create_ui_file_prewires_icons_qrc(self, qapp, project_dir):
        from Custom_Widgets.ProjectMaker import create_ui_file

        path = create_ui_file("MyForm")
        assert path and os.path.isfile(path)
        content = open(path, encoding="utf-8").read()
        assert "<class>MyForm</class>" in content
        assert "_icons.qrc" in content
        ET.fromstring(content)  # valid Designer XML

    def test_create_ui_file_refuses_overwrite(self, qapp, project_dir):
        from Custom_Widgets.ProjectMaker import create_ui_file

        assert create_ui_file("Twice") is not None
        assert create_ui_file("Twice") is None


class TestFullThemeApplication:
    def test_apply_compiled_sass_end_to_end(self, theme, project_dir):
        """applyCompiledSass must compile the SVG-based scss and generate the
        active theme + designer icon sets."""
        theme.themesRead = True
        theme.applyCompiledSass(generateIcons=True, paintEntireApp=False)
        assert theme.customWidgetsThreadpool.waitForDone(60000)

        css = project_dir / "generated-files" / "css" / "main.css"
        assert css.is_file()
        compiled = css.read_text(encoding="utf-8")
        assert "theme-icons:icons/" in compiled
        assert ".svg" in compiled
        assert ".png" not in compiled

        # exactly one shared icon set - no per-theme color folders
        icons_root = project_dir / "Qss" / "icons"
        assert (icons_root / "icons" / "feather" / "check.svg").is_file()
        extra = [d.name for d in icons_root.iterdir() if d.is_dir() and d.name != "icons"]
        assert extra == [], f"unexpected per-theme folders: {extra}"

        # the icon color is exposed to user stylesheets
        variables = (project_dir / "Qss" / "scss" / "_variables.scss").read_text(encoding="utf-8")
        assert "$ICONS_COLOR:" in variables
