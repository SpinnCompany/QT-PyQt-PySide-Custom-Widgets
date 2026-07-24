"""Theme helpers — read the token-driven ChartPalette + icon colours straight
from json-styles/style.json so every painted hue lives WITH the theme and flips
when the theme switches (rather than being hard-coded in Python)."""

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_DARK = "CheckBox Dark"
THEME_LIGHT = "CheckBox Light"

ICON_COLOR = {THEME_DARK: "#c9cbd1", THEME_LIGHT: "#5b5d66"}
SHELL_BG = {THEME_DARK: "#0c0c0e", THEME_LIGHT: "#f2f3f5"}


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def chart_palette(theme_name):
    """Return the ChartPalette dict for the active theme (falls back to dark)."""
    pal = _load().get("ChartPalette", {})
    return pal.get(theme_name) or pal.get(THEME_DARK) or {}


def is_dark(theme_name):
    return "dark" in str(theme_name or "").lower()


def is_light(theme_name):
    return not is_dark(theme_name)


def icon_color(theme_name):
    return ICON_COLOR.get(theme_name, ICON_COLOR[THEME_DARK])


def shell_bg(theme_name):
    return SHELL_BG.get(theme_name, SHELL_BG[THEME_DARK])
