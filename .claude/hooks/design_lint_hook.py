#!/usr/bin/env python3
"""Claude Code PostToolUse hook — enforce Custom_Widgets design rules on edit.

Wired from .claude/settings.json so EVERY session (this one and every inherited
one) runs it after Edit/Write/MultiEdit. It lints only the file that was just
written; if a *new* design-rule ERROR is introduced (e.g. a unicode-glyph icon)
it exits 2, which feeds the message back to the model so it fixes it before
moving on. Warnings never block. Pre-existing violations are grandfathered by
the repo baseline, so this only fires on regressions.

Pure stdlib; shells out to the shipped linter so it always matches the library.
"""
import json
import os
import subprocess
import sys

LINT_EXT = (".py", ".ui")


def _changed_path(event):
    ti = event.get("tool_input") or {}
    return ti.get("file_path") or ti.get("path") or ""


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0  # never break the session on a malformed payload

    path = _changed_path(event)
    if not path or not path.endswith(LINT_EXT) or not os.path.isfile(path):
        return 0

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "Custom_Widgets.lint", path, "--format", "text"],
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return 0  # linter unavailable -> don't block the session

    # exit 1 == blocking ERROR-severity findings (glyph-icons by default).
    if proc.returncode == 1:
        sys.stderr.write(
            "Custom_Widgets design-rule violation introduced in %s:\n%s\n"
            "Fix it (e.g. use a real painted/SVG icon instead of a unicode "
            "glyph). See docs/design/design-rules.md, or suppress a false "
            "positive with `# noqa: <rule-id>`.\n" % (path, proc.stdout.strip()))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
