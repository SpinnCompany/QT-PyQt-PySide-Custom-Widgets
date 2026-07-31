"""The flat `Custom_Widgets.<Module>` paths must survive the regrouping.

They are published API in two places: user imports, and the
`<header>Custom_Widgets.QCustomX</header>` that Qt Designer bakes into every
.ui file it writes. Breaking them surfaces as a .ui load failure pointing at
the user's form rather than at the rename that caused it.
"""
import importlib
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestAliasTable:
    def test_aliases_cover_moved_modules(self, qapp):
        from Custom_Widgets import _legacy_paths
        aliases = _legacy_paths.build_aliases()
        assert "Custom_Widgets.QCustomRadioButton" in aliases
        assert aliases["Custom_Widgets.QCustomRadioButton"] == \
            "Custom_Widgets.widgets.input.QCustomRadioButton"

    def test_alias_table_is_derived_not_hardcoded(self, qapp):
        """Every alias must point at a file that actually exists."""
        from Custom_Widgets import _legacy_paths
        for legacy, real in _legacy_paths.build_aliases().items():
            rel = real.split(".", 1)[1].replace(".", os.sep) + ".py"
            assert os.path.isfile(os.path.join(REPO, "Custom_Widgets", rel)), \
                "%s -> %s has no file" % (legacy, real)

    def test_duplicate_basenames_are_rejected(self, qapp, tmp_path, monkeypatch):
        """An ambiguous flat alias must fail loudly, not pick one at random."""
        from Custom_Widgets import _legacy_paths
        root = tmp_path / "pkg"
        for group in ("widgets", "tools"):
            d = root / group
            d.mkdir(parents=True)
            (d / "__init__.py").write_text("")
            (d / "Clash.py").write_text("")
        monkeypatch.setattr(_legacy_paths, "_ROOT", str(root))
        with pytest.raises(ImportError, match="ambiguous"):
            _legacy_paths.build_aliases()


class TestLegacyImports:
    @pytest.mark.parametrize("name", [
        "QCustomRadioButton", "QCustomRadioGroup", "QCustomTextArea",
        "QCustomVerificationCode", "QCustomSwitch", "QCustomNumberInput",
        "QCustomInput", "QCustomButtonGroup",
    ])
    def test_flat_path_still_imports(self, qapp, name):
        module = importlib.import_module("Custom_Widgets.%s" % name)
        assert hasattr(module, name)

    def test_flat_and_real_paths_are_the_same_module(self, qapp):
        """Not a copy — a second execution would re-register Designer widgets."""
        legacy = importlib.import_module("Custom_Widgets.QCustomSwitch")
        real = importlib.import_module("Custom_Widgets.widgets.input.QCustomSwitch")
        assert legacy is real
        assert legacy.QCustomSwitch is real.QCustomSwitch

    def test_from_import_works(self, qapp):
        from Custom_Widgets.QCustomRadioGroup import QCustomRadioGroup
        assert QCustomRadioGroup(options=["a", "b"]).count() == 2

    def test_widget_module_constant_stays_public(self, qapp):
        """Designer writes WIDGET_MODULE into .ui files, so it must not move."""
        from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
        from Custom_Widgets.QCustomTextArea import QCustomTextArea
        assert QCustomRadioButton.WIDGET_MODULE == "Custom_Widgets.QCustomRadioButton"
        assert QCustomTextArea.WIDGET_MODULE == "Custom_Widgets.QCustomTextArea"

    def test_unknown_module_still_raises(self, qapp):
        """The finder must only fill gaps, never swallow real import errors."""
        with pytest.raises(ImportError):
            importlib.import_module("Custom_Widgets.QCustomDefinitelyNotAWidget")

    def test_real_modules_win_over_aliases(self, qapp):
        """A module still at the top level resolves to itself, not an alias."""
        mod = importlib.import_module("Custom_Widgets.QCustomTheme")
        assert mod.__name__ == "Custom_Widgets.QCustomTheme"


class TestUiHeadersResolve:
    def test_every_ui_header_in_repo_is_importable(self, qapp):
        """Walk the .ui files and import each Custom_Widgets header they name.

        This is the regression that would otherwise reach users first.
        """
        import re
        pattern = re.compile(r"<header>(Custom_Widgets[^<]*)</header>")
        headers = set()
        for dirpath, dirnames, filenames in os.walk(REPO):
            dirnames[:] = [d for d in dirnames
                           if d not in (".git", "__pycache__", ".claude")]
            for filename in filenames:
                if not filename.endswith(".ui"):
                    continue
                path = os.path.join(dirpath, filename)
                try:
                    text = open(path, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                headers.update(pattern.findall(text))

        assert headers, "no .ui headers found — the guard would be vacuous"
        broken = []
        for header in sorted(headers):
            # Some older example forms carry a C++-style "<module>.h" header,
            # which is what Designer writes for C++ widgets. The Python loaders
            # ignore the suffix, so check the module that actually gets
            # imported rather than failing on the spelling.
            module = header[:-2] if header.endswith(".h") else header
            try:
                importlib.import_module(module)
            except Exception as exc:                # noqa: BLE001 - report all
                broken.append("%s (%s)" % (header, exc.__class__.__name__))
        assert not broken, "unimportable .ui headers: %s" % ", ".join(broken)
