"""Tests for the Custom_Widgets.lint design-rule linter.

Pure static analysis — no Qt, no display. Glyphs are built with chr() so this
test file never trips the linter it exercises.
"""
import json
import os

import pytest

from Custom_Widgets.lint import (Config, Finding, RULES, lint_file, lint_paths,
                                 load_config, baseline)
from Custom_Widgets.lint.core import ERROR, WARNING

MOON = chr(0x25D1)      # ◑  CIRCLE WITH RIGHT HALF BLACK
FULL_PLUS = chr(0xFF0B)  # ＋  FULLWIDTH PLUS SIGN
GEAR = chr(0x2699)      # ⚙  GEAR
EMDASH = chr(0x2014)    # —  (typographic, allowed)
ANGLE = chr(0x203A)     # ›  (typographic, allowed)


def _write(tmp_path, name, src):
    p = tmp_path / name
    p.write_text(src, encoding="utf-8")
    return str(p)


def _cfg(tmp_path, **kw):
    return Config(root=str(tmp_path), paths=(str(tmp_path),), **kw)


# --------------------------------------------------------------------------- #
# glyph-icons
# --------------------------------------------------------------------------- #
def test_glyph_icon_in_button_is_flagged(tmp_path):
    src = 'b = QPushButton("%s")\n' % MOON
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    glyphs = [f for f in findings if f.rule == "glyph-icons"]
    assert len(glyphs) == 1
    assert glyphs[0].severity == ERROR
    assert glyphs[0].symbol == MOON
    assert glyphs[0].line == 1


def test_fullwidth_plus_is_flagged(tmp_path):
    src = 'x = QPushButton("%s  Add job")\n' % FULL_PLUS
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert any(f.rule == "glyph-icons" and f.symbol == FULL_PLUS for f in findings)


def test_typographic_punctuation_is_not_flagged(tmp_path):
    src = 'title = "Aurora %s Work %s Jobs"\n' % (EMDASH, ANGLE)
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "glyph-icons"]


def test_glyph_in_docstring_is_ignored(tmp_path):
    src = '"""A kebab %s menu lives here."""\nx = 1\n' % chr(0x22EE)
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "glyph-icons"]


def test_glyph_in_comment_is_ignored(tmp_path):
    src = 'x = 1  # the %s toggle\n' % GEAR
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "glyph-icons"]


def test_noqa_suppresses(tmp_path):
    src = 'b = QPushButton("%s")  # noqa: glyph-icons\n' % MOON
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "glyph-icons"]


def test_cwlint_allow_suppresses(tmp_path):
    src = 'b = QPushButton("%s")  # cwlint: allow glyph-icons legacy\n' % MOON
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "glyph-icons"]


def test_allow_glyphs_config(tmp_path):
    src = 'b = QLabel("%s")\n' % GEAR
    cfg = _cfg(tmp_path, allow_glyphs=GEAR)
    assert not [f for f in lint_file(_write(tmp_path, "a.py", src), cfg)
                if f.rule == "glyph-icons"]


def test_glyph_in_ui_file(tmp_path):
    src = '<widget><property name="text"><string>%s</string></property></widget>\n' % MOON
    findings = lint_file(_write(tmp_path, "form.ui", src), _cfg(tmp_path))
    assert any(f.rule == "glyph-icons" for f in findings)


def test_multiline_string_reports_real_line(tmp_path):
    src = 'S = ("line one\\n"\n     "two %s here")\n' % MOON
    # implicit-concat is two constants; put the glyph in a real triple-quoted block:
    src = 'S = """\nrow one\nrow %s two\n"""\n' % MOON
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    g = [f for f in findings if f.rule == "glyph-icons"]
    assert g and g[0].line == 3


# --------------------------------------------------------------------------- #
# hardcoded-hex
# --------------------------------------------------------------------------- #
def test_hardcoded_hex_in_chrome_is_warned(tmp_path):
    src = 'w.setStyleSheet("background: #0f172a;")\n'
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    hexes = [f for f in findings if f.rule == "hardcoded-hex"]
    assert len(hexes) == 1 and hexes[0].severity == WARNING


def test_allcaps_palette_constant_is_allowed(tmp_path):
    src = 'GREEN = "#22c55e"\nORANGE = "#f97316"\n'
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "hardcoded-hex"]


def test_hex_severity_override_to_error(tmp_path):
    src = 'w.setStyleSheet("color: #fff;")\n'
    cfg = _cfg(tmp_path, severity={"hardcoded-hex": "error"})
    findings = lint_file(_write(tmp_path, "a.py", src), cfg)
    assert any(f.rule == "hardcoded-hex" and f.severity == ERROR for f in findings)


# --------------------------------------------------------------------------- #
# drop-shadow
# --------------------------------------------------------------------------- #
def test_drop_shadow_flagged(tmp_path):
    src = 'e = QGraphicsDropShadowEffect(self)\n'
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert any(f.rule == "drop-shadow" for f in findings)


def test_drop_shadow_allow_comment(tmp_path):
    src = 'e = QGraphicsDropShadowEffect(self)  # allow-shadow: hero card\n'
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "drop-shadow"]


def test_unused_shadow_import_not_flagged(tmp_path):
    # importing without constructing/attaching is not a shadow use
    src = 'from PySide6.QtWidgets import QGraphicsDropShadowEffect\n'
    findings = lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))
    assert not [f for f in findings if f.rule == "drop-shadow"]


# --------------------------------------------------------------------------- #
# selection / config / clean pass
# --------------------------------------------------------------------------- #
def test_select_runs_only_chosen_rule(tmp_path):
    src = 'b = QPushButton("%s")\nw.setStyleSheet("c: #fff;")\n' % MOON
    cfg = _cfg(tmp_path, select=frozenset({"glyph-icons"}))
    rules = {f.rule for f in lint_file(_write(tmp_path, "a.py", src), cfg)}
    assert rules == {"glyph-icons"}


def test_ignore_skips_rule(tmp_path):
    src = 'b = QPushButton("%s")\n' % MOON
    cfg = _cfg(tmp_path, ignore=frozenset({"glyph-icons"}))
    assert not lint_file(_write(tmp_path, "a.py", src), cfg)


def test_clean_file_passes(tmp_path):
    src = 'b = QPushButton("Add job")\nb.setIcon(QIcon(painted("plus")))\n'
    assert not lint_file(_write(tmp_path, "a.py", src), _cfg(tmp_path))


def test_syntax_error_does_not_crash(tmp_path):
    findings = lint_file(_write(tmp_path, "a.py", "def (:\n"), _cfg(tmp_path))
    assert isinstance(findings, list)  # no exception


def test_excluded_dirs_are_skipped(tmp_path):
    (tmp_path / "__pycache__").mkdir()
    _write(tmp_path, "__pycache__/x.py", 'QPushButton("%s")\n' % MOON)
    _write(tmp_path, "good.py", "x = 1\n")
    findings = lint_paths([str(tmp_path)], _cfg(tmp_path))
    assert not findings


# --------------------------------------------------------------------------- #
# baseline
# --------------------------------------------------------------------------- #
def test_baseline_grandfathers_existing_and_catches_new(tmp_path):
    f = _write(tmp_path, "a.py", 'b = QPushButton("%s")\n' % MOON)
    cfg = _cfg(tmp_path)
    existing = lint_paths([str(tmp_path)], cfg)
    assert existing  # violation present

    bl_path = str(tmp_path / "baseline.json")
    baseline.save(bl_path, existing)
    bl = baseline.load(bl_path)

    # same file → grandfathered, nothing new
    assert lint_paths([str(tmp_path)], cfg, baseline=bl) == []

    # add a NEW, different glyph → not in baseline → surfaces
    _write(tmp_path, "b.py", 'x = QLabel("%s")\n' % GEAR)
    new = lint_paths([str(tmp_path)], cfg, baseline=bl)
    assert len(new) == 1 and new[0].symbol == GEAR


def test_baseline_survives_line_shift(tmp_path):
    src = 'b = QPushButton("%s")\n' % MOON
    f = _write(tmp_path, "a.py", src)
    cfg = _cfg(tmp_path)
    bl_path = str(tmp_path / "b.json")
    baseline.save(bl_path, lint_paths([str(tmp_path)], cfg))
    bl = baseline.load(bl_path)
    # insert lines ABOVE the violation — fingerprint is line-independent
    (tmp_path / "a.py").write_text("# a\n# b\n" + src, encoding="utf-8")
    assert lint_paths([str(tmp_path)], cfg, baseline=bl) == []


# --------------------------------------------------------------------------- #
# config loading
# --------------------------------------------------------------------------- #
def test_load_config_reads_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        "[tool.custom_widgets_lint]\n"
        'paths = ["src"]\nignore = ["drop-shadow"]\nstrict = true\n',
        encoding="utf-8")
    cfg = load_config(str(tmp_path))
    assert cfg.paths == ("src",)
    assert "drop-shadow" in cfg.ignore
    assert cfg.strict is True
