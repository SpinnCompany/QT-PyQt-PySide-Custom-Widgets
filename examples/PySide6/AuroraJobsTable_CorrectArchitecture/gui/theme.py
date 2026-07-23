"""Theme helpers — read colours straight from json-styles/style.json so nothing
is hard-coded in Python.

 * the two CustomThemes give the token role colours (Background / Text / Accent);
   the DataTable delegate + toolbar are coloured from these so they flip on a
   theme switch.
 * StatusPalette holds the semantic DATA hues (a job status has ONE meaning, so
   the same colour in both themes).
 * Brand holds the intentionally theme-INDEPENDENT dark rail colours.
"""

import json
import os

from qtpy.QtGui import QColor

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_LIGHT = "Aurora Light"
THEME_DARK = "Aurora Dark"


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_light(theme_name):
    return "light" in str(theme_name or "").lower()


def status_palette():
    """Semantic data hues (job statuses, link/schedule colours)."""
    return _load().get("StatusPalette", {})


def brand():
    """Theme-independent brand chrome (dark rail)."""
    return _load().get("Brand", {})


def _theme(theme_name):
    themes = _load()["QSettings"]["ThemeSettings"]["CustomThemes"]
    for t in themes:
        if t.get("Theme-name") == theme_name:
            return t
    return themes[0]


def roles(theme_name):
    """The active theme's role colours the delegate/toolbar need, read from the
    CustomTheme entry (Background-color IS the card/surface colour; the generator
    derives a slightly-off page shade for the window). `outline`/`muted` are
    computed by blending Text toward Surface so they track the theme."""
    t = _theme(theme_name)
    text = t.get("Text-color", "#0f172a")
    surface = t.get("Background-color", "#ffffff")   # the card / surface colour
    accent = t.get("Accent-color", "#f97316")
    icons = t.get("Icons-color", "#64748b")          # topbar/nav glyph colour
    outline = _blend(text, surface, 0.86)            # faint separator line
    muted = _blend(text, surface, 0.45)              # muted secondary text
    icon_strong = _blend(text, surface, 0.28)        # crisp topbar/nav glyphs
    return {"text": text, "background": surface, "accent": accent, "icons": icons,
            "surface": surface, "outline": outline, "muted": muted,
            "iconStrong": icon_strong}


def _blend(fg, bg, f):
    """Blend fg toward bg by fraction f (0 = fg, 1 = bg)."""
    a, b = QColor(fg), QColor(bg)
    return QColor(int(a.red() + (b.red() - a.red()) * f),
                  int(a.green() + (b.green() - a.green()) * f),
                  int(a.blue() + (b.blue() - a.blue()) * f)).name()
