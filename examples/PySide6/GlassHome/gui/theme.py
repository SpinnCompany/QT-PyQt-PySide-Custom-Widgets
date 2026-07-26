"""ChartPalette reader — painted hues that QSS can't drive (the wallpaper
fallback gradient) live WITH the theme in style.json so they flip on switch."""

import json
import os

_STYLE_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "json-styles", "style.json")
_CACHE = None


def _palettes():
    global _CACHE
    if _CACHE is None:
        with open(_STYLE_JSON, "r") as f:
            _CACHE = json.load(f).get("ChartPalette", {})
    return _CACHE


def current_theme_name(window):
    engine = getattr(window, "themeEngine", None)
    name = getattr(engine, "theme", "") if engine else ""
    return name or "Glass Dusk"


def palette(window):
    pals = _palettes()
    return pals.get(current_theme_name(window)) or pals.get("Glass Dusk") or {}
