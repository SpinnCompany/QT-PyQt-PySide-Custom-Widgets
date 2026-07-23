"""Theme helpers — read the token-driven chart / data-viz palette + icon colours
straight from json-styles/style.json so hues live WITH the theme and flip when
the theme switches (rather than being hard-coded in Python)."""

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_LIGHT = "Finance Light"
THEME_DARK = "Finance Dark"

# Icon stroke colour per theme (mirrors each theme's Icons-color in style.json).
ICON_COLOR = {THEME_LIGHT: "#9aa1b2", THEME_DARK: "#c2c6d2"}


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def chart_palette(theme_name):
    """Return the ChartPalette dict for the active theme (falls back to light)."""
    pal = _load().get("ChartPalette", {})
    return pal.get(theme_name) or pal.get(THEME_LIGHT) or {}


def is_light(theme_name):
    return "light" in str(theme_name or "").lower()


def icon_color(theme_name):
    return ICON_COLOR.get(theme_name, ICON_COLOR[THEME_LIGHT])
