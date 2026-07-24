"""Theme helpers — read the token-driven ChartPalette + icon colours from
json-styles/style.json so every painted / gradient hue flips on theme switch."""

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_DARK = "SmartHome Dark"
THEME_LIGHT = "SmartHome Light"

ICON_COLOR = {THEME_DARK: "#c3c7ea", THEME_LIGHT: "#7b7fae"}
SHELL_BG = {THEME_DARK: "#1e2142", THEME_LIGHT: "#eef0f7"}


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def chart_palette(theme_name):
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
