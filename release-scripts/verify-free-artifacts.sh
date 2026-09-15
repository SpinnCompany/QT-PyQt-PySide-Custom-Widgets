#!/usr/bin/env bash
# Verify free-core release artifacts before they are uploaded to PyPI.
#
#   usage: release-scripts/verify-free-artifacts.sh <dist-dir> <version>
#
# A PyPI version can never be re-uploaded, so every check here is a hard gate:
# the script exits non-zero on the first failure and prints ALL-GATES-PASSED
# only if every one succeeds. Build from `git archive main`, not the working
# tree -- the internal branches carry docs/design, and an sdist bundles source.
set -euo pipefail

DIST="${1:?usage: verify-free-artifacts.sh <dist-dir> <version>}"
VERSION="${2:?usage: verify-free-artifacts.sh <dist-dir> <version>}"

WHEEL=$(ls "$DIST"/*.whl 2>/dev/null | head -1)
SDIST=$(ls "$DIST"/*.tar.gz 2>/dev/null | head -1)
[ -n "$WHEEL" ] || { echo "FAIL: no wheel in $DIST"; exit 1; }
[ -n "$SDIST" ] || { echo "FAIL: no sdist in $DIST"; exit 1; }

echo "wheel: $(basename "$WHEEL")"
echo "sdist: $(basename "$SDIST")"

python3 - "$WHEEL" "$SDIST" "$VERSION" <<'PY'
import sys, zipfile, tarfile, re, pathlib, subprocess

wheel, sdist, version = sys.argv[1], sys.argv[2], sys.argv[3]
fails = []

def check(ok, gate, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {gate}" + (f" -- {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(gate)

wheel_names = zipfile.ZipFile(wheel).namelist()
with tarfile.open(sdist) as t:
    sdist_names = t.getnames()

# Gate 1 -- no internal material in either artifact.
INTERNAL = ("docs/design", "docs/relicense", "AGENTS.md", ".claude/")
def internal_hits(names):
    return [n for n in names
            if any(p in n.replace("\\", "/") for p in INTERNAL)]
w_hits, s_hits = internal_hits(wheel_names), internal_hits(sdist_names)
check(not w_hits, "1a no internal paths in wheel", str(w_hits[:5]))
check(not s_hits, "1b no internal paths in sdist", str(s_hits[:5]))

# Gate 2 -- no compiled bytecode in the wheel.
pyc = [n for n in wheel_names if n.endswith(".pyc") or "__pycache__" in n]
check(not pyc, "2  no .pyc/__pycache__ in wheel", str(pyc[:5]))

# Gate 3 -- metadata is what we intend to publish.
meta_name = next(n for n in wheel_names if n.endswith(".dist-info/METADATA"))
meta = zipfile.ZipFile(wheel).read(meta_name).decode("utf-8", "replace")
head, _, body = meta.partition("\n\n")
def field(name):
    m = re.search(rf"^{name}:\s*(.+)$", head, re.M)
    return m.group(1).strip() if m else None
check(field("Version") == version, "3a version matches", f"got {field('Version')!r}")
rp = field("Requires-Python") or ""
check(">=3.10" in rp.replace(" ", ""), "3b Requires-Python >=3.10", f"got {rp!r}")
check("pyside6" in head.lower(), "3c pyside6 extra present")

# Gate 4 -- long_description is exactly the repo README.
readme = subprocess.run(["git", "show", "main:README.md"],
                        capture_output=True, text=True)
if readme.returncode != 0:
    check(False, "4  long_description == main:README.md", "cannot read main:README.md")
else:
    check(body.strip() == readme.stdout.strip(),
          "4  long_description == main:README.md",
          f"{len(body.strip())} vs {len(readme.stdout.strip())} chars")

print("GATES-1-4:", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)
PY

# Gate 5 -- twine's own validation of both artifacts.
echo "  [ .. ] 5  twine check"
python3 -m twine check "$WHEEL" "$SDIST" | sed 's/^/        /'

echo "ALL-GATES-PASSED"
