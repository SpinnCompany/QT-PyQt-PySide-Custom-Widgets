"""Theme helpers — read the NodePalette straight from json-styles/style.json so
the node/timeline hues live WITH the theme and flip when the theme switches
(rather than being hard-coded in Python)."""

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_DARK = "Studio Dark"
THEME_LIGHT = "Studio Light"


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def node_palette(theme_name):
    """Return the NodePalette dict for the active theme (falls back to dark)."""
    pal = _load().get("NodePalette", {})
    return pal.get(theme_name) or pal.get(THEME_DARK) or {}


def is_light(theme_name):
    return "light" in str(theme_name or "").lower()


# Icon stroke + accent per theme (mirror each theme's Icons-color / Accent-color).
ICON_COLOR = {THEME_DARK: "#c9cde0", THEME_LIGHT: "#3a3f52"}
ACCENT = {THEME_DARK: "#6c7bff", THEME_LIGHT: "#5865f2"}


def icon_color(theme_name):
    return ICON_COLOR.get(theme_name, ICON_COLOR[THEME_DARK])


def accent(theme_name):
    return ACCENT.get(theme_name, ACCENT[THEME_DARK])
