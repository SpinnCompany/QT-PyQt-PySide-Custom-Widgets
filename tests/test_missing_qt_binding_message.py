"""A bare install must explain itself.

A Qt binding is deliberately not a hard dependency, so `pip install
QT-PyQt-PySide-Custom-Widgets` on its own leaves the user one step short.
qtpy's own failure is a raw QtBindingsNotFoundError traceback that never says
what to do, so the package root translates it into an instruction.

2.4.0 shipped with that translation broken: the guard lived only inside
__getattr__, while the root eagerly imported Custom_Widgets.Log (which reaches
qtpy) a few lines above it. The eager import raised first, so the guard never
ran and users got the raw traceback back. The test suite could not see it
because the suite always runs with a binding installed -- hence a subprocess
with a stub qtpy that raises exactly what the real one raises.
"""
import subprocess
import sys
import textwrap

REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]

STUB_QTPY = '''
class QtBindingsNotFoundError(ImportError):
    pass

raise QtBindingsNotFoundError
'''


def _importInStubbedEnv(tmp_path, statement):
    """Import with a qtpy that fails the way a binding-less install fails."""
    stub = tmp_path / "qtpy"
    stub.mkdir()
    (stub / "__init__.py").write_text(STUB_QTPY)

    script = textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(tmp_path)!r})   # stub qtpy wins
        sys.path.insert(1, {str(REPO_ROOT)!r})
        {statement}
    """)
    return subprocess.run([sys.executable, "-c", script],
                          capture_output=True, text=True)


def test_bare_import_explains_how_to_install_a_binding(tmp_path):
    result = _importInStubbedEnv(tmp_path, "import Custom_Widgets")

    assert result.returncode != 0, "expected the import to fail without a binding"
    err = result.stderr
    assert "needs a Qt binding" in err, (
        "the raw qtpy traceback leaked instead of the instruction:\n" + err)
    assert "pip install PySide6" in err
    assert "QtBindingsNotFoundError" not in err.splitlines()[-1], (
        "the final line should be the instruction, not qtpy's error:\n" + err)


def test_lazy_attribute_access_explains_too(tmp_path):
    """The __getattr__ path must give the same message, not a different one."""
    result = _importInStubbedEnv(
        tmp_path,
        "import Custom_Widgets; Custom_Widgets.QCustomTheme")

    assert result.returncode != 0
    assert "needs a Qt binding" in result.stderr
