"""Project root resolution (Custom_Widgets.Project)."""
import os

import pytest

from Custom_Widgets import Project


@pytest.fixture(autouse=True)
def _clean_root(monkeypatch):
    monkeypatch.delenv("CUSTOM_WIDGETS_PROJECT_ROOT", raising=False)
    Project.clearProjectRoot()
    yield
    Project.clearProjectRoot()


class TestResolution:
    def test_defaults_to_cwd(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert Project.projectRoot() == str(tmp_path)
        assert not Project.hasExplicitRoot()

    def test_env_var_wins_over_cwd(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        other = tmp_path / "elsewhere"
        other.mkdir()
        monkeypatch.setenv("CUSTOM_WIDGETS_PROJECT_ROOT", str(other))
        assert Project.projectRoot() == str(other)
        assert Project.hasExplicitRoot()

    def test_explicit_wins_over_env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CUSTOM_WIDGETS_PROJECT_ROOT", str(tmp_path / "env"))
        explicit = tmp_path / "explicit"
        explicit.mkdir()
        Project.setProjectRoot(str(explicit))
        assert Project.projectRoot() == str(explicit)

    def test_file_argument_uses_its_directory(self, tmp_path):
        f = tmp_path / "main.py"
        f.write_text("")
        Project.setProjectRoot(str(f))
        assert Project.projectRoot() == str(tmp_path)

    def test_clear_returns_to_cwd(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        Project.setProjectRoot(str(tmp_path / "sub"))
        Project.clearProjectRoot()
        assert Project.projectRoot() == str(tmp_path)


class TestPaths:
    def test_well_known_locations(self, tmp_path):
        Project.setProjectRoot(str(tmp_path))
        assert Project.scssDir() == str(tmp_path / "Qss" / "scss")
        assert Project.iconsDir() == str(tmp_path / "Qss" / "icons")
        assert Project.generatedDir("css") == str(tmp_path / "generated-files" / "css")
        assert Project.projectPath("a", "b") == str(tmp_path / "a" / "b")

    def test_style_json_prefers_json_styles(self, tmp_path):
        Project.setProjectRoot(str(tmp_path))
        (tmp_path / "json-styles").mkdir()
        preferred = tmp_path / "json-styles" / "style.json"
        legacy = tmp_path / "style.json"
        legacy.write_text("{}")
        assert Project.styleJsonPath() == str(legacy)  # only legacy exists
        preferred.write_text("{}")
        assert Project.styleJsonPath() == str(preferred)

    def test_theme_engine_uses_project_root(self, tmp_path, qapp, monkeypatch):
        """QCustomTheme.script_dir must follow the pinned root, not argv[0]."""
        from Custom_Widgets.QCustomTheme import QCustomTheme
        monkeypatch.chdir(tmp_path)
        saved = QCustomTheme._instance
        QCustomTheme._instance = None
        try:
            Project.setProjectRoot(str(tmp_path))
            theme = QCustomTheme()
            assert theme.script_dir.rstrip("/") == str(tmp_path).replace("\\", "/")
        finally:
            QCustomTheme._instance = saved
