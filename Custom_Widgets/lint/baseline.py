"""Baseline support — adopt the linter on an existing codebase without a
mass-cleanup PR.

A baseline records the *fingerprints* of the violations that exist today. On
later runs those are ignored, so CI only fails on **new** violations while the
backlog is burned down over time. Fingerprints are line-independent (rule +
path + symbol + stripped source line), so they survive edits elsewhere in the
file but correctly stop matching once the offending line is actually fixed.

Regenerate after intentionally clearing items:  ``--generate-baseline``.
"""
from __future__ import annotations

import json
import os

DEFAULT_BASELINE = ".custom_widgets_lint_baseline.json"


def default_path(root: str) -> str:
    return os.path.join(root, DEFAULT_BASELINE)


def load(path: str):
    """Return a set of fingerprint tuples, or None if the file is absent."""
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    return {tuple(item) for item in data.get("fingerprints", [])}


def save(path: str, findings) -> int:
    """Write the fingerprints of *findings* to *path*. Returns the count."""
    fps = sorted({f.fingerprint() for f in findings})
    payload = {
        "_comment": "Custom_Widgets design-lint baseline — grandfathered "
                    "violations. Only NEW violations fail. Regenerate with "
                    "`Custom_Widgets-lint --generate-baseline`.",
        "count": len(fps),
        "fingerprints": [list(fp) for fp in fps],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return len(fps)
