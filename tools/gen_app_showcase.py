#!/usr/bin/env python3
"""Generate the app-showcase page from the example apps.

The widget gallery answers "what widgets exist"; this answers "what do real
apps built from them look like". Every example app is booted headlessly (same
harness idea as survey_examples.py), its main window captured into the docs
repo, and docs/05-Usage-Examples/AppShowcase.mdx regenerated: featured
applications first, then the single-widget demos grouped small.

Usage:
    python tools/gen_app_showcase.py                # capture missing + write page
    python tools/gen_app_showcase.py --reshoot      # recapture everything
    python tools/gen_app_showcase.py --page-only    # just rewrite the page
    python tools/gen_app_showcase.py --with-source-links
        # add GitHub links to each card — only once the examples are pushed,
        # or every card links to a 404.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(ROOT, "examples", "PySide6")
DOCS = os.path.join(os.path.dirname(ROOT), "Docs-QT-PyQt-PySide-Custom-Widgets")
SHOTS = os.path.join(DOCS, "static", "img", "showcase-apps")
PAGE = os.path.join(DOCS, "docs", "05-Usage-Examples", "AppShowcase.mdx")
GITHUB = ("https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/"
          "tree/main/examples/PySide6/")

#: Architecture variants photograph identically to their siblings, and the
#: two non-app folders have no main.py anyway.
SKIP = {"AuroraJobsTable_CorrectArchitecture", "WinningDashboard_CorrectArchitecture"}

#: Apps whose SOURCE ships to supporters only (decided 2026-08-05). They live
#: in the sibling private repo, not under examples/ — the screenshots stay on
#: the public showcase (they sell the thing), the card gets a PATREON badge,
#: and with --with-source-links these link to the plans page instead of the
#: public repo.
PATREON = {"FinanceDashboard", "CryptoDashboard", "CashFlowDashboard",
           "SmartHomeDashboard", "WinningDashboard", "CheckBoxDashboard",
           "AuroraChat", "AuroraCommandDeck", "AuroraDeckPro",
           "AuroraJobsTable", "NodeStudio", "RhythmoTune"}

#: Where the supporter-only apps live on disk (sibling private repo).
PREMIUM = os.path.join(os.path.dirname(ROOT), "Custom-Widgets-Premium-Examples")

PLANS_URL = "https://customwidgets.org/pricing/"


def appDir(name):
    """Resolve an app folder across the public examples and the premium repo."""
    for root in (EXAMPLES, PREMIUM):
        candidate = os.path.join(root, name)
        if os.path.isfile(os.path.join(candidate, "main.py")):
            return candidate
    return None


def allApps():
    names = set()
    for root in (EXAMPLES, PREMIUM):
        if not os.path.isdir(root):
            continue
        for d in os.listdir(root):
            if d in SKIP or d in ("README.md", "LICENSE"):
                continue
            if os.path.isfile(os.path.join(root, d, "main.py")):
                names.add(d)
    return sorted(names)

#: (section, [(app, blurb)]) — curated, in display order. Apps not listed
#: land in the trailing "Widget demos" grid automatically.
FEATURED = [
    ("Dashboards & analytics", [
        ("FinanceDashboard",
         "Personal finance: card wallet, balance, monthly summary and transactions."),
        ("CryptoDashboard",
         "Crypto wallet dashboard: portfolio chart, market table and a trade panel."),
        ("CashFlowDashboard",
         "Banking-style operations board: balance hero, cash-flow bars, stat cards."),
        ("SmartHomeDashboard",
         "Smart-home control: dial gauges, room tiles, lighting and security."),
        ("WinningDashboard",
         "E-commerce admin: sparkline stat row, sales charts, radial distribution."),
        ("CheckBoxDashboard",
         "High-contrast analytics: dot matrix, beeswarm and a projects timeline."),
    ]),
    ("Applications", [
        ("AuroraChat",
         "Chat client: threads, reactions, voice messages and a composer."),
        ("AuroraCommandDeck",
         "Forecast-network console: KPI tiles, stations table, probability rings."),
        ("AuroraDeckPro",
         "Aurora-watch operator console: stat tiles, activity feed, shift roster."),
        ("AuroraJobsTable",
         "Field-service job board on the DataTable: filters, statuses, row actions."),
        ("NodeStudio",
         "Creative-studio shell: node graph, code editor, preview and timeline."),
        ("RhythmoTune",
         "Music player: cover-flow hero, category chips and a bottom player bar."),
        ("AgendaDemo",
         "Dark agenda board: timeline rows with status dots for plans and meetings."),
    ]),
    ("Starters & showcases", [
        ("GlassHome",
         "The glassmorphism starter behind the docs' showcase walkthrough."),
        ("PrismShowcase",
         "Motion tour: gradient and sparkle text, rainbow buttons, progress rings."),
        ("WidgetShowcase",
         "Kitchen-sink tour of the core widget set on one scrolling page."),
        ("NewWidgetsShowcase",
         "Release-ready tour of the newest inputs, gauges, waveform and heatmap."),
        ("ReleaseStarterApp",
         "Minimal template wiring theming, icons and layout the recommended way."),
        ("DesignTokens",
         "Button variants and sizes under the token system, with live theme switch."),
        ("QMainWindow",
         "Frameless main-window chrome: custom title bar, move and resize."),
    ]),
]


def slugFor(name):
    return re.sub(r"[^A-Za-z0-9]+", "", name).lower()


# --------------------------------------------------------------------------- #
# Capture
# --------------------------------------------------------------------------- #
RUNNER = r'''
import os, runpy, sys
from qtpy.QtCore import QTimer, Qt
from qtpy.QtWidgets import QApplication

target, shotPath = sys.argv[1], sys.argv[2]
os.chdir(os.path.dirname(target))
sys.path.insert(0, os.path.dirname(target))
sys.argv = [target]

def capture():
    app = QApplication.instance()
    if app is None:
        print("SHOWCASE:NOAPP"); os._exit(3)
    wins = [w for w in app.topLevelWidgets() if w.isVisible()]
    if not wins:
        print("SHOWCASE:NOWINDOW"); os._exit(4)
    best = max(wins, key=lambda w: w.width() * w.height())
    pm = best.grab()
    if pm.width() > 960:                     # the grid renders ~420px cards
        pm = pm.scaledToWidth(960, Qt.SmoothTransformation)
    ok = pm.save(shotPath)
    print("SHOWCASE:OK %dx%d saved=%s" % (best.width(), best.height(), ok))
    os._exit(0)

_real_exec = QApplication.exec
def _showcase_exec(*_a, **_k):
    QTimer.singleShot(6000, capture)
    return _real_exec()
QApplication.exec = _showcase_exec
QApplication.exec_ = _showcase_exec

try:
    runpy.run_path(target, run_name="__main__")
except SystemExit:
    pass
except Exception as exc:
    print("SHOWCASE:CRASH %s: %s" % (type(exc).__name__, exc)); os._exit(2)
capture()
'''


def captureAll(reshoot=False):
    os.makedirs(SHOTS, exist_ok=True)
    runner = os.path.join(SHOTS, "_runner.py")
    open(runner, "w").write(RUNNER)
    names = allApps()
    env = dict(os.environ, QT_API="pyside6", PYTHONPATH=ROOT,
               PYTHONUNBUFFERED="1")
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    failed = []
    for index, name in enumerate(names, 1):
        shot = os.path.join(SHOTS, slugFor(name) + ".png")
        if os.path.isfile(shot) and not reshoot:
            continue
        target = os.path.join(appDir(name), "main.py")
        try:
            proc = subprocess.run([sys.executable, runner, target, shot],
                                  capture_output=True, text=True, timeout=40,
                                  env=env)
            out = (proc.stdout or "") + (proc.stderr or "")
            ok = "SHOWCASE:OK" in out
        except subprocess.TimeoutExpired:
            out, ok = "timeout", False
        print("[%3d/%d] %-7s %s" % (index, len(names),
                                    "ok" if ok else "FAIL", name), flush=True)
        if not ok:
            failed.append(name)
    os.remove(runner)
    return names, failed


# --------------------------------------------------------------------------- #
# Widget usage per app
# --------------------------------------------------------------------------- #
def widgetsUsed(name, known):
    """The QCustom* classes an app actually references, most-used first."""
    counts = {}
    folder = appDir(name)
    if folder is None:
        return []
    for base, _dirs, files in os.walk(folder):
        if "generated-files" in base:
            continue
        for f in files:
            if not f.endswith((".py", ".ui")):
                continue
            try:
                text = open(os.path.join(base, f), encoding="utf-8",
                            errors="replace").read()
            except OSError:
                continue
            for match in re.findall(r"\bQCustom[A-Za-z0-9]+", text):
                if match in known:
                    counts[match] = counts.get(match, 0) + 1
    return [w for w, _n in sorted(counts.items(), key=lambda kv: -kv[1])]


def knownWidgets():
    path = os.path.join(ROOT, "docs", "design", "tiering-manifest.json")
    rows = json.load(open(path, encoding="utf-8"))
    rows = rows if isinstance(rows, list) else rows.get("widgets", rows)
    return {r["widget"] for r in rows}


# --------------------------------------------------------------------------- #
# Page
# --------------------------------------------------------------------------- #
def card(name, blurb, widgets, withLinks):
    shot = slugFor(name) + ".png"
    if not os.path.isfile(os.path.join(SHOTS, shot)):
        return None
    img = "<Zoomable src={useBaseUrl('/img/showcase-apps/%s')} alt=\"%s\" />" % (shot, name)
    badge = ('<span className="ag-patreon">PATREON</span>'
             if name in PATREON else "")
    chips = "".join('<span className="ag-chip">%s</span>' % w for w in widgets[:4])
    body = ('%s<span className="ag-name">%s%s</span>'
            '<span className="ag-blurb">%s</span>'
            '<span className="ag-chips">%s</span>'
            % (img, name, badge, blurb, chips))
    if withLinks:
        href = PLANS_URL if name in PATREON else GITHUB + name
        return '<a className="ag-card" href="%s">%s</a>' % (href, body)
    return '<div className="ag-card">%s</div>' % body


def writePage(names, withLinks):
    known = knownWidgets()
    featuredNames = {n for _s, apps in FEATURED for n, _b in apps}
    out = ["---", "title: App showcase", "sidebar_label: App showcase",
           "sidebar_position: 1",
           "description: Complete applications built from Custom Widgets — "
           "dashboards, chat, media and starter templates, every one a "
           "runnable example in the repo.",
           "---", "",
           "import useBaseUrl from '@docusaurus/useBaseUrl';",
           "import Zoomable from '@site/src/components/Zoomable';", "",
           "# App showcase", "",
           "Every screenshot below is a real, runnable app from the repo's "
           "`examples/PySide6/` folder — captured from the app itself, not a "
           "mockup. Click any screenshot to expand it. Featured applications "
           "first; the single-widget demos follow.", ""]
    if PATREON:
        out += ["Apps marked **PATREON** ship their full source to "
                "[supporters](%s); everything else is in the public repo."
                % PLANS_URL, ""]
    for section, apps in FEATURED:
        cards = [card(n, b, widgetsUsed(n, known), withLinks) for n, b in apps]
        cards = [c for c in cards if c]
        if not cards:
            continue
        out += ["## %s" % section, "", '<div className="app-gallery">', ""]
        out += cards
        out += ["", "</div>", ""]
    demos = [n for n in names if n not in featuredNames]
    cards = []
    for n in demos:
        shot = slugFor(n) + ".png"
        if not os.path.isfile(os.path.join(SHOTS, shot)):
            continue
        img = "<Zoomable src={useBaseUrl('/img/showcase-apps/%s')} alt=\"%s\" />" % (shot, n)
        badge = ('<span className="ag-patreon">PATREON</span>'
                 if n in PATREON else "")
        body = '%s<span className="ag-name">%s%s</span>' % (img, n, badge)
        if withLinks:
            href = PLANS_URL if n in PATREON else GITHUB + n
            cards.append('<a className="ag-card ag-demo" href="%s">%s</a>'
                         % (href, body))
        else:
            cards.append('<div className="ag-card ag-demo">%s</div>' % body)
    if cards:
        out += ["## Widget demos", "",
                "One app per widget (or widget family) — the shortest runnable "
                "answer to \"how do I wire this up\".", "",
                '<div className="app-gallery">', ""]
        out += cards
        out += ["", "</div>", ""]
    open(PAGE, "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    reshoot = "--reshoot" in sys.argv
    pageOnly = "--page-only" in sys.argv
    withLinks = "--with-source-links" in sys.argv
    if pageOnly:
        names = allApps()
        failed = []
    else:
        names, failed = captureAll(reshoot)
    writePage(names, withLinks)
    shots = len([f for f in os.listdir(SHOTS) if f.endswith(".png")])
    print("app showcase: %d apps, %d shots on disk, %d capture failures"
          % (len(names), shots, len(failed)))
    if failed:
        print("FAILED: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
