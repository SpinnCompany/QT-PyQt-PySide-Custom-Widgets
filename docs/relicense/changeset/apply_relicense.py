#!/usr/bin/env python3
"""Apply the GPLv3 -> LGPLv3 relicense of the free core.

**Run this only after** (a) the external-contribution consent/de-minimis calls are
confirmed by counsel, and (b) the CLA is in place for new contributions. See
`../external-contributions-audit.md` and `../../design/lgpl-relicense-plan.md`.

Dry-run by default — it prints exactly what it would change and touches nothing:

    python docs/relicense/changeset/apply_relicense.py            # dry-run
    python docs/relicense/changeset/apply_relicense.py --apply    # execute

What it does (from the repo root):
  1. Installs the license files: COPYING (GPLv3), COPYING.LESSER (LGPLv3), and a
     new root LICENSE notice — all read from this changeset directory.
  2. Rewrites the two license lines in `pyproject.toml` (SPDX id + classifier).
  3. Adds `# SPDX-License-Identifier: LGPL-3.0-or-later` to project-authored
     Python files (skips vendored/third-party, generated, and already-stamped
     files).
  4. Writes `RELICENSE-RECORD.md` at the repo root.

The README license badge is dynamic (`img.shields.io/github/license/...`) and
updates itself once GitHub detects LGPL from `COPYING.LESSER`, so no README edit
is needed.

After running with --apply: review `git diff`, run the test suite, then commit as
a single "Relicense to LGPLv3" commit.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPDX_LINE = "# SPDX-License-Identifier: LGPL-3.0-or-later\n"

# Directories never scanned for SPDX stamping.
SKIP_DIRS = {".git", ".venv", "venv", "build", "dist", "__pycache__", ".claude",
             ".pytest_cache", ".mypy_cache", "node_modules", ".eggs"}

# Only these top-level trees hold project-authored source.
INCLUDE_ROOTS = ("Custom_Widgets", "tests", "examples")

# Vendored / third-party code under other licenses — must NOT get the project
# SPDX id (their license stays whatever it is; recorded in THIRD_PARTY_NOTICES).
EXCLUDE_REL = {
    os.path.normpath("Custom_Widgets/iconify"),                    # vendored iconify
    os.path.normpath("Custom_Widgets/AnalogGaugeWidget.py"),       # Stefan Holstein
    os.path.normpath("Custom_Widgets/QCustomProgressIndicator.py"),  # Morgan Leborgne pattern
}

# Markers that identify machine-generated files (skip — they are regenerated).
GENERATED_MARKERS = (
    "Qt User Interface Compiler",
    "All changes made in this file will be lost",
    "WARNING! All changes made in this file",
)

CODING_RE = re.compile(r"#.*coding[:=]")


def repo_root():
    # docs/relicense/changeset/ -> repo root is three levels up.
    return os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def is_excluded(rel):
    rel = os.path.normpath(rel)
    for ex in EXCLUDE_REL:
        if rel == ex or rel.startswith(ex + os.sep):
            return True
    return False


def iter_py_files(root):
    for base in INCLUDE_ROOTS:
        top = os.path.join(root, base)
        if not os.path.isdir(top):
            continue
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                if is_excluded(rel):
                    continue
                yield full, rel


def spdx_plan(root):
    """Return (to_stamp, skipped) lists of (rel, reason)."""
    to_stamp, skipped = [], []
    for full, rel in iter_py_files(root):
        try:
            with open(full, "r", encoding="utf-8") as fh:
                head = fh.read(4000)
        except (OSError, UnicodeDecodeError) as exc:
            skipped.append((rel, "unreadable: %s" % exc))
            continue
        if "SPDX-License-Identifier" in head:
            skipped.append((rel, "already stamped"))
            continue
        if any(m in head for m in GENERATED_MARKERS):
            skipped.append((rel, "generated"))
            continue
        to_stamp.append(rel)
    return to_stamp, skipped


def stamp_file(full):
    with open(full, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    idx = 0
    if lines and lines[0].startswith("#!"):
        idx = 1
    if idx < len(lines) and CODING_RE.match(lines[idx]):
        idx += 1
    lines.insert(idx, SPDX_LINE)
    with open(full, "w", encoding="utf-8") as fh:
        fh.writelines(lines)


def patch_pyproject(root, apply):
    path = os.path.join(root, "pyproject.toml")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    subs = [
        ('license = { text = "GPL-3.0-only" }',
         'license = { text = "LGPL-3.0-or-later" }'),
        ('"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",',
         '"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",'),
    ]
    changed = []
    for old, new in subs:
        if old in text:
            text = text.replace(old, new)
            changed.append(new)
        else:
            changed.append("!! NOT FOUND: %s" % old)
    if apply:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return changed


def install_file(root, name, apply, dest=None):
    src = os.path.join(HERE, name)
    dst = os.path.join(root, dest or name)
    with open(src, "r", encoding="utf-8") as fh:
        data = fh.read()
    if apply:
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(data)
    return os.path.relpath(dst, root), len(data)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Apply the GPLv3->LGPLv3 relicense.")
    ap.add_argument("--apply", action="store_true",
                    help="actually write changes (default: dry-run).")
    ap.add_argument("--root", default=None, help="repo root (default: auto).")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root) if args.root else repo_root()
    apply = args.apply
    mode = "APPLY" if apply else "DRY-RUN (nothing written)"
    print("Relicense GPLv3 -> LGPLv3   [%s]" % mode)
    print("Repo root: %s\n" % root)

    print("1. License files:")
    for name, dest in (("COPYING", None), ("COPYING.LESSER", None),
                       ("LICENSE", None), ("RELICENSE-RECORD.md", None)):
        rel, n = install_file(root, name, apply, dest)
        print("   %-22s (%d bytes)" % (rel, n))

    print("\n2. pyproject.toml:")
    for line in patch_pyproject(root, apply):
        print("   -> %s" % line)

    print("\n3. SPDX headers (LGPL-3.0-or-later):")
    to_stamp, skipped = spdx_plan(root)
    print("   would stamp: %d files" % len(to_stamp))
    reasons = {}
    for _rel, reason in skipped:
        key = reason.split(":")[0]
        reasons[key] = reasons.get(key, 0) + 1
    print("   skipped: %d  (%s)" % (
        len(skipped), ", ".join("%s=%d" % kv for kv in sorted(reasons.items()))))
    if apply:
        for rel in to_stamp:
            stamp_file(os.path.join(root, rel))
        print("   stamped %d files." % len(to_stamp))
    else:
        for rel in to_stamp[:8]:
            print("     + %s" % rel)
        if len(to_stamp) > 8:
            print("     ... and %d more" % (len(to_stamp) - 8))

    print("\nDone (%s)." % mode)
    if not apply:
        print("Re-run with --apply to execute, then review 'git diff', run the "
              "test suite, and commit as 'Relicense to LGPLv3'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
