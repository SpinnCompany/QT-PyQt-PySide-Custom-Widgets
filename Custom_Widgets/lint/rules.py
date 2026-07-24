"""The design rules.

Each rule is a :class:`Rule` with an ``id``, a one-line ``summary``, a
``default_severity`` and a ``check(ctx)`` generator that yields
:class:`~Custom_Widgets.lint.core.Finding`. Register a new rule by adding it to
``RULES`` at the bottom — nothing else needs to change; the CLI, config,
pre-commit hook, CI job and MCP tool all pick it up automatically.

No literal icon glyphs appear in this source (codepoints are given as integers)
so the linter never trips over itself.
"""
from __future__ import annotations

import ast
import re
import unicodedata
from dataclasses import dataclass
from typing import Callable, Iterable

from .core import ERROR, WARNING, Finding, FileCtx


@dataclass(frozen=True)
class Rule:
    id: str
    summary: str
    default_severity: str
    check: Callable[[FileCtx], Iterable[Finding]]
    help: str = ""


# ------------------------------------------------------------------------- #
# glyph-icons — no unicode symbol/emoji glyph used as a UI "icon"
# ------------------------------------------------------------------------- #
# Codepoint ranges that read as pictographic "icons" (never real icon assets).
# Deliberately EXCLUDES ordinary typographic punctuation (— – · › » … × etc.,
# all below 0x2190) so window titles and breadcrumbs are fine.
_ICON_RANGES = (
    (0x2190, 0x21FF),   # Arrows
    (0x2300, 0x23FF),   # Miscellaneous Technical (⌚ ⏰ ⎋ …)
    (0x2460, 0x24FF),   # Enclosed Alphanumerics (① ② …)
    (0x25A0, 0x25FF),   # Geometric Shapes (◑ ● ▲ ◈ …)   <- the AuroraJobs ◑
    (0x2600, 0x26FF),   # Miscellaneous Symbols (☀ ⚙ ☰ …)
    (0x2700, 0x27BF),   # Dingbats (✂ ✓ ✦ ➤ …)
    (0x2900, 0x297F),   # Supplemental Arrows-B
    (0x2B00, 0x2BFF),   # Misc Symbols & Arrows (★ ⬆ …)
    (0xFE00, 0xFE0F),   # Variation Selectors (emoji presentation)
    (0xFF01, 0xFF0F),   # Fullwidth ASCII symbols (＋ ％ ＊ …)   <- the ＋
    (0x1F000, 0x1FAFF), # Emoji & pictographs
)


def _is_icon_glyph(ch: str, allow: str) -> bool:
    if ch in allow:
        return False
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in _ICON_RANGES)


def _describe(ch: str) -> str:
    try:
        return unicodedata.name(ch)
    except ValueError:
        return "U+%04X" % ord(ch)


def _locate(value: str, base_line: int, base_col: int, offset: int):
    """Map an offset inside a (possibly multi-line) literal to (line, col)."""
    nl = value.count("\n", 0, offset)
    if nl == 0:
        return base_line, base_col + offset
    return base_line + nl, offset - value.rfind("\n", 0, offset)


def _check_glyphs(ctx: FileCtx):
    allow = ctx.config.allow_glyphs
    for value, line, col, _pal in ctx.strings():
        for i, ch in enumerate(value):
            if _is_icon_glyph(ch, allow):
                fl, fc = _locate(value, line, col, i)
                yield Finding(
                    "glyph-icons", ctx.rel, fl, fc,
                    "glyph %r (%s) used as an icon in a UI string — use a real "
                    "icon asset (themed SVG via qproperty-icon / setIcon), not a "
                    "unicode glyph" % (ch, _describe(ch)),
                    ERROR, symbol=ch)
                break  # one finding per string is enough


# ------------------------------------------------------------------------- #
# hardcoded-hex — raw #rrggbb in code instead of a token role / palette const
# ------------------------------------------------------------------------- #
_HEX_RE = re.compile(r"(?<![\w#])#([0-9a-fA-F]{3,8})\b")


def _check_hardcoded_hex(ctx: FileCtx):
    if not ctx.is_python:
        return
    for value, line, col, is_palette in ctx.strings():
        if is_palette:
            continue  # ALL-CAPS colour constants are the sanctioned home
        for m in _HEX_RE.finditer(value):
            if len(m.group(1)) in (3, 4, 6, 8):
                fl, fc = _locate(value, line, col, m.start())
                yield Finding(
                    "hardcoded-hex", ctx.rel, fl, fc,
                    "hardcoded colour %s — drive chrome from token roles "
                    "(tokens.role(...)) or a named palette constant so it flips "
                    "with the theme" % m.group(0),
                    WARNING, symbol=m.group(0))


# ------------------------------------------------------------------------- #
# drop-shadow — QGraphicsDropShadowEffect without an explicit justification
# ------------------------------------------------------------------------- #
def _shadow_targets(node: ast.AST):
    """(name, lineno, col) for a shadow-effect construction / attach, else None."""
    if not isinstance(node, ast.Call):
        return None
    fn = node.func
    if isinstance(fn, ast.Name) and fn.id == "QGraphicsDropShadowEffect":
        return "QGraphicsDropShadowEffect", node.lineno, node.col_offset + 1
    if isinstance(fn, ast.Attribute):
        if fn.attr == "QGraphicsDropShadowEffect":
            return "QGraphicsDropShadowEffect", node.lineno, node.col_offset + 1
        if fn.attr == "setGraphicsEffect":
            return "setGraphicsEffect", node.lineno, node.col_offset + 1
    return None


def _check_drop_shadow(ctx: FileCtx):
    if ctx.tree is None:
        return
    for node in ast.walk(ctx.tree):
        hit = _shadow_targets(node)
        if not hit:
            continue
        name, line, col = hit
        # explicit opt-in on the line keeps intentional shadows quiet
        src = ctx.lines[line - 1] if 0 < line <= len(ctx.lines) else ""
        if "allow-shadow" in src:
            continue
        yield Finding(
            "drop-shadow", ctx.rel, line, col,
            "%s — the design bar is 'no drop shadows unless necessary'; prefer a "
            "borderless card fill + big radius. If genuinely needed, justify with "
            "a trailing `# allow-shadow: <reason>`" % name,
            WARNING, symbol="")


# ------------------------------------------------------------------------- #
# large-icon — a LARGE image pushed through QIcon/setIcon instead of a QPixmap
# ------------------------------------------------------------------------- #
# QIcon caps + softens when a button scales it up; prominent/large images should
# be a QPixmap (QLabel.setPixmap / QPainter.drawPixmap at 2x). Conservative: we
# only fire on `setIconSize(QSize(<int>, <int>))` where a LITERAL dimension is
# >= the threshold. Small button glyphs and any computed/variable size never
# trip it, so false positives are minimal.
_LARGE_ICON_PX = 40


def _int_const(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    return None


def _qsize_max(arg):
    """max(w, h) for a literal QSize(w, h) call, else None."""
    if not (isinstance(arg, ast.Call) and len(arg.args) >= 2):
        return None
    fn = arg.func
    name = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
    if name != "QSize":
        return None
    w, h = _int_const(arg.args[0]), _int_const(arg.args[1])
    if w is None or h is None:
        return None
    return max(w, h)


def _check_large_icon(ctx: FileCtx):
    if ctx.tree is None:
        return
    for node in ast.walk(ctx.tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "setIconSize" and node.args):
            continue
        size = _qsize_max(node.args[0])
        if size is None or size < _LARGE_ICON_PX:
            continue
        line, col = node.lineno, node.col_offset + 1
        src = ctx.lines[line - 1] if 0 < line <= len(ctx.lines) else ""
        if "allow-large-icon" in src:
            continue
        yield Finding(
            "large-icon", ctx.rel, line, col,
            "setIconSize(%dpx) puts a LARGE image on a QIcon — QIcon caps + softens "
            "when scaled up. Render large/prominent images as a QPixmap "
            "(QLabel.setPixmap or QPainter.drawPixmap at 2x); reserve setIcon for "
            "small (<=~22px) button glyphs. Justify a deliberate case with a "
            "trailing `# allow-large-icon: <reason>`." % size,
            WARNING, symbol="")


# ------------------------------------------------------------------------- #
# registry
# ------------------------------------------------------------------------- #
_ALL = [
    Rule("glyph-icons",
         "No unicode glyph used as a UI icon (use a real icon asset).",
         ERROR, _check_glyphs,
         help="Ban geometric-shape/dingbat/arrow/emoji/fullwidth glyphs as icon "
              "stand-ins in button/label text. They don't recolour on theme, "
              "hide on rail-collapse, and render inconsistently across "
              "fonts/platforms."),
    Rule("hardcoded-hex",
         "No raw #rrggbb in code — use token roles or a named palette constant.",
         WARNING, _check_hardcoded_hex,
         help="Chrome colours should come from tokens.role(...) so they flip "
              "with the theme. ALL-CAPS module constants (e.g. a named GREEN "
              "colour literal) are allowed as an intentional data palette."),
    Rule("drop-shadow",
         "No QGraphicsDropShadowEffect unless justified with # allow-shadow.",
         WARNING, _check_drop_shadow,
         help="Depth should come from a borderless fill a step off the canvas + "
              "big radius, not shadows or hairline borders."),
    Rule("large-icon",
         "Large images belong on a QPixmap, not a scaled QIcon/setIcon.",
         WARNING, _check_large_icon,
         help="setIconSize(QSize(N,N)) with N>=40 flags a LARGE QIcon; QIcon caps "
              "+ softens when scaled up. Use QLabel.setPixmap / QPainter."
              "drawPixmap at 2x for prominent images; keep setIcon for small "
              "button glyphs. Only literal QSize sizes are checked (no false "
              "positives from computed sizes); suppress with `# allow-large-icon`."),
]

RULES = {r.id: r for r in _ALL}
