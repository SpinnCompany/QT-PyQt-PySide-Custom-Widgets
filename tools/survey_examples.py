#!/usr/bin/env python3
"""Launch every example app, screenshot it, and report what is broken.

Written because "update the old examples" needs evidence first: 96 apps, an
unknown number of which stopped working across the restructure and the API
changes. Guessing which ones to fix would waste the effort on the wrong ones.

Each app runs in its own process, chdir'd into its own folder (they load
resources relatively), with a watchdog that grabs the top-level window and
quits. A crash, a hang and a blank window are three different failures and
are reported separately.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(ROOT, "examples", "PySide6")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/example-survey"
# Optional comma-separated substring filter (CI boots a flagship subset rather
# than all ~96 apps). Empty = every example.
ONLY = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), "")
# Per-app timeout. First boot on a machine without a warm icon cache spends
# tens of seconds generating the icon set; CI passes a generous value.
TIMEOUT = int(next((a.split("=", 1)[1] for a in sys.argv
                    if a.startswith("--timeout=")), "40"))

RUNNER = r'''
import os, runpy, sys
from qtpy.QtCore import QTimer, Qt
from qtpy.QtWidgets import QApplication

target, shotDir, name = sys.argv[1], sys.argv[2], sys.argv[3]
os.chdir(os.path.dirname(target))
sys.path.insert(0, os.path.dirname(target))  # match `python main.py` from the app dir
sys.argv = [target]

def _blank_ratio(img):
    """Fraction of a 16x16 downsample that is (near) a single colour — a quick
    blank-window test. A genuinely empty form grabs as one flat colour, so a
    ratio above ~0.98 flags it without needing an image library."""
    small = img.scaled(16, 16, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    lums = []
    for y in range(small.height()):
        for x in range(small.width()):
            c = small.pixelColor(x, y)
            lums.append(0.299 * c.red() + 0.587 * c.green() + 0.114 * c.blue())
    if not lums:
        return 1.0
    lo, hi = min(lums), max(lums)
    return 1.0 if (hi - lo) < 8 else 0.0

def capture():
    app = QApplication.instance()
    if app is None:
        print("SURVEY:NOAPP"); os._exit(3)
    wins = [w for w in app.topLevelWidgets() if w.isVisible()]
    if not wins:
        print("SURVEY:NOWINDOW"); os._exit(4)
    best = max(wins, key=lambda w: w.width() * w.height())
    img = best.grab()
    path = os.path.join(shotDir, name + ".png")
    ok = img.save(path)
    blank = _blank_ratio(img.toImage())
    if blank >= 0.98:
        print("SURVEY:BLANK %dx%d %.2f %s" % (best.width(), best.height(), blank, ok))
    else:
        print("SURVEY:OK %dx%d %s" % (best.width(), best.height(), ok))
    os._exit(0)

# The capture timer can only be scheduled once the app's own QApplication
# exists and its event loop is about to run: wrap exec so the timer starts
# at that moment (a timer scheduled before QApplication is created never
# fires, which used to classify every working app as a hang).
_real_exec = QApplication.exec
def _survey_exec(*_a, **_k):
    QTimer.singleShot(6000, capture)
    return _real_exec()
QApplication.exec = _survey_exec
QApplication.exec_ = _survey_exec

try:
    runpy.run_path(target, run_name="__main__")
except SystemExit:
    pass
except Exception as exc:
    print("SURVEY:CRASH %s: %s" % (type(exc).__name__, exc)); os._exit(2)
capture()  # app never entered exec (or quit early): report what is there
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    runner = os.path.join(OUT, "_runner.py")
    open(runner, "w").write(RUNNER)

    filters = [f.strip() for f in ONLY.split(",") if f.strip()]
    names = sorted(d for d in os.listdir(EXAMPLES)
                   if os.path.isfile(os.path.join(EXAMPLES, d, "main.py")))
    if filters:
        names = [n for n in names if any(f.lower() in n.lower() for f in filters)]
    env = dict(os.environ, QT_API="pyside6", PYTHONPATH=ROOT,
               PYTHONUNBUFFERED="1")
    env.setdefault("QT_QPA_PLATFORM", "offscreen")  # actually headless
    results = []
    for index, name in enumerate(names, 1):
        target = os.path.join(EXAMPLES, name, "main.py")
        try:
            proc = subprocess.run([sys.executable, runner, target, OUT, name],
                                  capture_output=True, text=True, timeout=TIMEOUT,
                                  env=env)
            out = (proc.stdout or "") + (proc.stderr or "")
            if "SURVEY:OK" in out:
                status, detail = "ok", out.split("SURVEY:OK")[1].split("\n")[0].strip()
            elif "SURVEY:BLANK" in out:
                status, detail = "blank", out.split("SURVEY:BLANK")[1].split("\n")[0].strip()
            elif "SURVEY:NOWINDOW" in out:
                status, detail = "no-window", "ran but showed nothing"
            elif "SURVEY:CRASH" in out:
                status, detail = "crash", out.split("SURVEY:CRASH")[1].split("\n")[0].strip()
            else:
                tail = [l for l in out.strip().splitlines()
                        if l.strip() and "DEBUG" not in l and "INFO:" not in l]
                status, detail = "error", (tail[-1][:160] if tail else "exit %d" % proc.returncode)
        except subprocess.TimeoutExpired:
            status, detail = "hang", "no window within %ds" % TIMEOUT
        results.append({"name": name, "status": status, "detail": detail})
        print("[%3d/%d] %-12s %-44s %s" % (index, len(names), status, name, detail[:70]),
              flush=True)

    json.dump(results, open(os.path.join(OUT, "survey.json"), "w"), indent=1)
    from collections import Counter
    print("\n" + json.dumps(dict(Counter(r["status"] for r in results))))
    # CI gate: any non-ok result (crash, hang, blank, no-window, error) fails.
    bad = [r for r in results if r["status"] != "ok"]
    if bad:
        print("SURVEY-FAIL %d app(s) not ok" % len(bad), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
