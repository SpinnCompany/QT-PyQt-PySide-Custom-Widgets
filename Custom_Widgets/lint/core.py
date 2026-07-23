"""Core linter machinery: findings, per-file context, file discovery, runner.

Pure standard library. A ``FileCtx`` parses a source file once (AST for Python)
and exposes cheap, cached lookups the rules need — which physical lines carry
string literals, which of those are palette-constant definitions, and which
lines are suppressed with ``# noqa`` / ``# cwlint: allow``.
"""
from __future__ import annotations

import ast
import fnmatch
import os
import re
import warnings
from dataclasses import dataclass

from .config import Config, EXCLUDE_DIRS, LINT_EXTENSIONS

ERROR = "error"
WARNING = "warning"
_SEV_RANK = {WARNING: 1, ERROR: 2}

# `# noqa: rule-a, rule-b`  or  `# cwlint: allow rule-a rule-b [reason]`
_SUPPRESS_RE = re.compile(
    r"#\s*(?:noqa|cwlint:\s*allow)\b[:\s]*([a-z0-9,\-\s]*)", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str          # repo-relative, posix
    line: int
    col: int
    message: str
    severity: str = ERROR
    symbol: str = ""   # offending character, when the rule is about one
    context: str = ""  # stripped source line — for output + line-stable baseline

    @property
    def rank(self) -> int:
        return _SEV_RANK.get(self.severity, 0)

    def fingerprint(self):
        """Line-independent identity for baselining (survives edits above it)."""
        return (self.rule, self.path, self.symbol, self.context)


def _parse_suppressions(lines):
    """line number (1-based) -> set of suppressed rule ids ('*' = all)."""
    out = {}
    for i, line in enumerate(lines, 1):
        m = _SUPPRESS_RE.search(line)
        if not m:
            continue
        body = m.group(1).strip()
        ids = {t for t in re.split(r"[,\s]+", body) if t}
        out[i] = ids or {"*"}
    return out


class FileCtx:
    """Everything a rule needs about one file, parsed once."""

    def __init__(self, path: str, rel: str, text: str, config: Config):
        self.path = path
        self.rel = rel.replace(os.sep, "/")
        self.text = text
        self.lines = text.splitlines()
        self.config = config
        self.is_ui = path.endswith(".ui")
        self.is_python = path.endswith(".py")
        self.tree = None
        self.syntax_error = None
        if self.is_python:
            try:
                # target files may have their own escape/deprecation warnings;
                # we're only parsing them, so keep our own output clean.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    self.tree = ast.parse(text, filename=path)
            except (SyntaxError, ValueError) as exc:  # report, don't crash
                self.syntax_error = exc
        self._suppress = _parse_suppressions(self.lines)
        self._strings = None   # list of (value, lineno, col, is_palette)

    # -- suppression -------------------------------------------------------- #
    def suppressed(self, line: int, rule: str) -> bool:
        ids = self._suppress.get(line)
        return bool(ids) and ("*" in ids or rule in ids)

    # -- string literals (cached) ------------------------------------------- #
    def strings(self):
        """List of (value, lineno, col, is_palette) for every user-facing string
        literal — Python str constants (docstrings excluded) or, for non-Python
        files, each raw line. ``is_palette`` marks ALL-CAPS colour constants."""
        if self._strings is not None:
            return self._strings
        out = []
        if self.tree is not None:
            skip = self._docstring_ids()
            pal_ids = self._palette_ids()
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                        and id(node) not in skip:
                    out.append((node.value, node.lineno, node.col_offset + 1,
                                id(node) in pal_ids))
        elif not self.is_python:
            for i, line in enumerate(self.lines, 1):
                out.append((line, i, 1, False))
        self._strings = out
        return out

    def _docstring_ids(self):
        skip = set()
        for node in ast.walk(self.tree):
            body = getattr(node, "body", None)
            if isinstance(node, (ast.Module, ast.FunctionDef,
                                 ast.AsyncFunctionDef, ast.ClassDef)) and body:
                first = body[0]
                if isinstance(first, ast.Expr) and \
                        isinstance(first.value, ast.Constant) and \
                        isinstance(first.value.value, str):
                    skip.add(id(first.value))
        return skip

    def _palette_ids(self):
        """Constant nodes inside ``NAME = "..."`` palette assignments (target(s)
        ALL-CAPS). These are the sanctioned place for raw colour literals."""
        ids = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and node.targets:
                names = [t for t in node.targets if isinstance(t, ast.Name)]
                if names and len(names) == len(node.targets) and \
                        all(n.id.isupper() and len(n.id) >= 2 for n in names):
                    for sub in ast.walk(node.value):
                        if isinstance(sub, ast.Constant):
                            ids.add(id(sub))
        return ids


# ------------------------------------------------------------------------- #
# file discovery
# ------------------------------------------------------------------------- #
def _glob_re(pattern: str) -> re.Pattern:
    return re.compile(fnmatch.translate(pattern.replace(os.sep, "/")))


def iter_files(paths, config: Config):
    """Yield (abspath, rel) for every lintable file under *paths*."""
    root = os.path.abspath(config.root)
    excludes = [_glob_re(p) for p in config.exclude]
    seen = set()
    for base in paths:
        base = base if os.path.isabs(base) else os.path.join(root, base)
        base = os.path.abspath(base)
        if os.path.isfile(base):
            files = [(os.path.dirname(base), [os.path.basename(base)])]
        else:
            files = None
        if files is None:
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in dirnames
                               if d not in EXCLUDE_DIRS
                               and not d.endswith(".egg-info")]
                for name in filenames:
                    yield from _emit(dirpath, name, root, excludes, seen)
        else:
            for dirpath, names in files:
                for name in names:
                    yield from _emit(dirpath, name, root, excludes, seen)


def _emit(dirpath, name, root, excludes, seen):
    if not name.endswith(LINT_EXTENSIONS):
        return
    full = os.path.abspath(os.path.join(dirpath, name))
    if full in seen:
        return
    seen.add(full)
    rel = os.path.relpath(full, root).replace(os.sep, "/")
    if any(rx.match(rel) for rx in excludes):
        return
    yield full, rel


# ------------------------------------------------------------------------- #
# runner
# ------------------------------------------------------------------------- #
def active_rules(config: Config):
    from .rules import RULES
    ids = set(config.select) if config.select else set(RULES)
    ids -= set(config.ignore)
    return [RULES[i] for i in RULES if i in ids]


def lint_file(path: str, config: Config, rel: str = None):
    if rel is None:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(config.root))
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return [Finding("read-error", rel.replace(os.sep, "/"), 1, 1,
                        "could not read file: %s" % exc, WARNING)]
    ctx = FileCtx(path, rel, text, config)
    findings = []
    for rule in active_rules(config):
        sev = config.severity.get(rule.id, rule.default_severity)
        for f in rule.check(ctx):
            if ctx.suppressed(f.line, rule.id):
                continue
            src = ctx.lines[f.line - 1].strip() if 0 < f.line <= len(ctx.lines) else ""
            findings.append(Finding(f.rule, ctx.rel, f.line, f.col,
                                    f.message, sev, f.symbol, src))
    return findings


def lint_paths(paths, config: Config, baseline=None):
    """Lint *paths*. If *baseline* (a set of fingerprints) is given, findings it
    contains are dropped so only NEW violations surface."""
    out = []
    for full, rel in iter_files(paths, config):
        out.extend(lint_file(full, config, rel))
    if baseline:
        out = [f for f in out if f.fingerprint() not in baseline]
    out.sort(key=lambda f: (f.path, f.line, f.col, f.rule))
    return out
