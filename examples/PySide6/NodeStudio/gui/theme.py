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
