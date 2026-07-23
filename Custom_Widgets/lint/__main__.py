"""Command-line entry point: ``python -m Custom_Widgets.lint`` / ``Custom_Widgets-lint``."""
from __future__ import annotations

import argparse
import json
import sys

from . import baseline as _baseline
from .config import load_config
from .core import ERROR, lint_paths
from .rules import RULES


def _build_parser():
    p = argparse.ArgumentParser(
        prog="Custom_Widgets-lint",
        description="Enforce Custom_Widgets design rules (glyph icons, hardcoded "
                    "hex, drop shadows) across .py/.ui sources.")
    p.add_argument("paths", nargs="*",
                   help="files/dirs to scan (default: [tool.custom_widgets_lint] "
                        "paths, else the project root)")
    p.add_argument("--select", metavar="IDS",
                   help="comma-separated rule ids to run exclusively")
    p.add_argument("--ignore", metavar="IDS",
                   help="comma-separated rule ids to skip")
    p.add_argument("--strict", action="store_true",
                   help="treat warnings as failures (non-zero exit)")
    p.add_argument("--format", choices=["text", "json", "github"], default="text",
                   help="output format (github = CI annotations)")
    p.add_argument("--no-config", action="store_true",
                   help="ignore pyproject [tool.custom_widgets_lint]")
    p.add_argument("--root", default=".",
                   help="project root (used to resolve config + relative paths)")
    p.add_argument("--list-rules", action="store_true",
                   help="print the registered rules and exit")
    p.add_argument("--baseline", metavar="FILE", default=None,
                   help="ignore violations recorded in FILE (default: "
                        ".custom_widgets_lint_baseline.json if present)")
    p.add_argument("--no-baseline", action="store_true",
                   help="do not apply any baseline")
    p.add_argument("--generate-baseline", action="store_true",
                   help="write current violations to the baseline file and exit")
    return p


def _csv(val):
    return frozenset(t.strip() for t in val.split(",") if t.strip()) if val else None


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)

    if args.list_rules:
        for r in RULES.values():
            print("%-14s [%s]  %s" % (r.id, r.default_severity, r.summary))
            if r.help:
                print("               %s" % r.help)
        return 0

    config = load_config(args.root, use_pyproject=not args.no_config)
    config = config.with_overrides(
        paths=tuple(args.paths) or None,
        select=_csv(args.select),
        ignore=_csv(args.ignore),
        strict=True if args.strict else None,
    )
    paths = config.paths or (config.root,)

    baseline_path = args.baseline or _baseline.default_path(config.root)

    if args.generate_baseline:
        target = args.baseline or _baseline.default_path(config.root)
        all_findings = lint_paths(paths, config)
        n = _baseline.save(target, all_findings)
        print("Wrote %d fingerprint(s) to %s" % (n, target))
        return 0

    baseline = None if args.no_baseline else _baseline.load(baseline_path)
    findings = lint_paths(paths, config, baseline=baseline)

    errors = [f for f in findings if f.severity == ERROR]
    warnings = [f for f in findings if f.severity != ERROR]
    failed = bool(errors) or (config.strict and bool(findings))

    if args.format == "json":
        print(json.dumps({
            "summary": {"files_with_findings": len({f.path for f in findings}),
                        "errors": len(errors), "warnings": len(warnings),
                        "failed": failed},
            "findings": [f.__dict__ for f in findings],
        }, indent=2))
    elif args.format == "github":
        for f in findings:
            level = "error" if f.severity == ERROR else "warning"
            print("::%s file=%s,line=%d,col=%d::%s: %s"
                  % (level, f.path, f.line, f.col, f.rule, f.message))
        _print_summary(errors, warnings, failed, stream=sys.stderr)
    else:
        for f in findings:
            print("%s:%d:%d: [%s] %s: %s"
                  % (f.path, f.line, f.col, f.severity, f.rule, f.message))
        _print_summary(errors, warnings, failed)

    return 1 if failed else 0


def _print_summary(errors, warnings, failed, stream=sys.stdout):
    if not errors and not warnings:
        print("OK: no design-rule violations.", file=stream)
        return
    print("", file=stream)
    print("%d error(s), %d warning(s)%s"
          % (len(errors), len(warnings),
             "" if failed else " (warnings only — not failing; use --strict)"),
          file=stream)


if __name__ == "__main__":
    raise SystemExit(main())
