"""DevServer: the `Custom_Widgets --dev` supervisor."""
import os
import sys
import textwrap
import time

import pytest

from Custom_Widgets.DevServer import DevServer, _classify, _scan


class TestScanClassify:
    def test_scan_picks_watched_suffixes_only(self, tmp_path):
        (tmp_path / "main.py").write_text("")
        (tmp_path / "ui").mkdir()
        (tmp_path / "ui" / "form.ui").write_text("<ui/>")
        (tmp_path / "notes.txt").write_text("")
        (tmp_path / "style.scss").write_text("")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "x.py").write_text("")
        (tmp_path / "generated-files").mkdir()
        (tmp_path / "generated-files" / "y.py").write_text("")

        snap = _scan(str(tmp_path))
        names = {os.path.relpath(p, tmp_path) for p in snap}
        assert names == {"main.py", os.path.join("ui", "form.ui"), "style.scss"}

    def test_scan_detects_change(self, tmp_path):
        f = tmp_path / "main.py"
        f.write_text("a")
        snap1 = _scan(str(tmp_path))
        os.utime(f, (time.time() + 5, time.time() + 5))
        snap2 = _scan(str(tmp_path))
        changed = [p for p, m in snap2.items() if snap1.get(p) != m]
        assert changed == [str(f)]

    def test_classify(self):
        ui, py, style = _classify([
            "/p/ui/a.ui", "/p/main.py", "/p/Qss/scss/defaultStyle.scss",
            "/p/json-styles/style.json"])
        assert ui == ["/p/ui/a.ui"]
        assert py == ["/p/main.py"]
        assert set(style) == {"/p/Qss/scss/defaultStyle.scss",
                              "/p/json-styles/style.json"}


class TestSupervision:
    @pytest.fixture
    def app_project(self, tmp_path):
        script = tmp_path / "main.py"
        script.write_text(textwrap.dedent("""
            import time
            while True:
                time.sleep(0.1)
        """))
        return tmp_path, script

    def test_start_stop(self, app_project):
        root, script = app_project
        server = DevServer(script=str(script), project_dir=str(root))
        server.start_app()
        assert server.child.poll() is None  # running
        server.stop_app()
        assert server.child.poll() is not None  # stopped

    def test_restart_spawns_new_process(self, app_project):
        root, script = app_project
        server = DevServer(script=str(script), project_dir=str(root))
        server.start_app()
        first_pid = server.child.pid
        server.restart_app("test")
        assert server.child.pid != first_pid
        assert server.child.poll() is None
        server.stop_app()

    def test_child_env_carries_project_root(self, app_project, tmp_path):
        root, script = app_project
        out = tmp_path / "root.txt"
        script.write_text(textwrap.dedent(f"""
            import os
            open({str(out)!r}, "w").write(
                os.environ.get("CUSTOM_WIDGETS_PROJECT_ROOT", ""))
        """))
        server = DevServer(script=str(script), project_dir=str(root))
        server.start_app()
        server.child.wait(timeout=10)
        assert out.read_text() == str(root)

    def test_missing_script_fails_cleanly(self, tmp_path):
        server = DevServer(script=str(tmp_path / "nope.py"),
                           project_dir=str(tmp_path))
        assert server.run() == 1
