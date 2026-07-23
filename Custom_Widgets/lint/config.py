"""Configuration for the Custom_Widgets design-rule linter.

Config is read from ``[tool.custom_widgets_lint]`` in the nearest
``pyproject.toml`` (walking up from the target). Everything is optional — the
defaults below are what ship with the library. Downstream projects that install
Custom_Widgets get the same rules out of the box and can tune them per repo::

    [tool.custom_widgets_lint]
    paths   = ["src", "app"]        # what to scan when no paths are given
    ignore  = ["hardcoded-hex"]     # turn a rule off
    select  = ["glyph-icons"]       # or run ONLY these rules
    strict  = true                  # warnings fail too (exit 1)
    exclude = ["**/vendored/**"]    # extra path globs to skip
    allow-glyphs = "✓✗"   # extra codepoints that are NOT icons here

    [tool.custom_widgets_lint.severity]
    hardcoded-hex = "error"         # promote a warning to an error

This module is pure standard library so the linter stays fast and dependency
free (a Qt binding is only pulled in transitively by the package ``__init__``).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, replace

# Directory names pruned during a walk. These are duplicated-repo / build /
# cache / asset trees that should never be linted. The huge bundled SVG icon
# set lives under Qss/icons and is excluded here too (and by the extension
# filter, since we only read .py/.ui).
EXCLUDE_DIRS = frozenset({
    ".git", ".hg", ".svn",
    ".venv", "venv", "env", ".env",
    "build", "dist", "site-packages",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "node_modules", "generated-files",
    ".claude",            # skills + duplicate worktrees
})

# File extensions the linter understands.
LINT_EXTENSIONS = (".py", ".ui")


@dataclass(frozen=True)
class Config:
    """Resolved linter configuration."""
    root: str = "."
    paths: tuple = (".",)
    exclude: tuple = ()               # extra path globs (posix, support **)
    select: frozenset = frozenset()   # empty => all registered rules
    ignore: frozenset = frozenset()
    severity: dict = field(default_factory=dict)   # rule id -> "error"|"warning"
    allow_glyphs: str = ""            # extra codepoints treated as non-icon
    palette_globs: tuple = ()         # files where hardcoded hex is fine
    strict: bool = False              # warnings become failures

    def with_overrides(self, **kw) -> "Config":
        clean = {k: v for k, v in kw.items() if v is not None}
        return replace(self, **clean)


DEFAULTS = dict(
    paths=(".",),
    exclude=(),
    select=frozenset(),
    ignore=frozenset(),
    severity={},
    allow_glyphs="",
    palette_globs=(),
    strict=False,
)


def find_root(start: str = ".") -> str:
    """Walk up from *start* to the project root (dir with pyproject.toml, else
    a .git dir). Falls back to *start* itself."""
    cur = os.path.abspath(start)
    if os.path.isfile(cur):
        cur = os.path.dirname(cur)
    while True:
        if os.path.isfile(os.path.join(cur, "pyproject.toml")) or \
           os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start)
        cur = parent


def _load_toml(path: str) -> dict:
    try:
        import tomllib as toml  # py3.11+
    except ModuleNotFoundError:
        try:
            import tomli as toml  # backport
        except ModuleNotFoundError:
            return {}
    try:
        with open(path, "rb") as fh:
            return toml.load(fh)
    except (OSError, ValueError):
        return {}


def load_config(root: str = ".", use_pyproject: bool = True) -> Config:
    """Build a Config for *root*, merging pyproject settings over the defaults."""
    root = find_root(root)
    data = {}
    if use_pyproject:
        section = _load_toml(os.path.join(root, "pyproject.toml"))
        data = (section.get("tool", {}) or {}).get("custom_widgets_lint", {}) or {}

    def _seq(key, default):
        val = data.get(key, default)
        if isinstance(val, str):
            val = [val]
        return tuple(val)

    severity = dict(data.get("severity", {}) or {})
    return Config(
        root=root,
        paths=_seq("paths", DEFAULTS["paths"]),
        exclude=_seq("exclude", DEFAULTS["exclude"]),
        select=frozenset(_seq("select", ())),
        ignore=frozenset(_seq("ignore", ())),
        severity={str(k): str(v) for k, v in severity.items()},
        allow_glyphs=str(data.get("allow-glyphs", data.get("allow_glyphs", ""))),
        palette_globs=_seq("palette-globs", data.get("palette_globs", ())),
        strict=bool(data.get("strict", False)),
    )
