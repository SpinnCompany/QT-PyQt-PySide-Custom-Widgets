"""Custom_Widgets design-rule linter.

A small, dependency-free static checker that enforces the project's *visual*
rules — the ones a type checker or pyflakes will never catch — across ``.py``
and ``.ui`` sources:

* ``glyph-icons``   — no unicode glyph used as a UI icon (use a real icon asset)
* ``hardcoded-hex`` — no raw ``#rrggbb`` in chrome (use token roles / palette)
* ``drop-shadow``   — no ``QGraphicsDropShadowEffect`` without justification

It ships **with the library** so downstream projects that build Custom_Widgets
apps — including AI agents doing the building — get the same guardrails:

    python -m Custom_Widgets.lint            # scan configured paths
    python -m Custom_Widgets.lint app/ ui/   # scan specific paths
    Custom_Widgets-lint --format github      # CI annotations

Programmatic use::

    from Custom_Widgets.lint import load_config, lint_paths
    cfg = load_config(".")
    findings = lint_paths(cfg.paths, cfg)

See :mod:`Custom_Widgets.lint.rules` to add a rule and
:mod:`Custom_Widgets.lint.config` for the ``[tool.custom_widgets_lint]``
options.
"""
from __future__ import annotations

from . import baseline
from .config import Config, load_config, find_root
from .core import (ERROR, WARNING, Finding, FileCtx, lint_file, lint_paths,
                   iter_files, active_rules)
from .rules import RULES, Rule

__all__ = [
    "Config", "load_config", "find_root",
    "ERROR", "WARNING", "Finding", "FileCtx",
    "lint_file", "lint_paths", "iter_files", "active_rules",
    "RULES", "Rule", "baseline",
]
