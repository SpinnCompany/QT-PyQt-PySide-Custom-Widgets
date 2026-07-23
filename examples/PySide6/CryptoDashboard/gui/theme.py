"""Theme helpers — read the token-driven ChartPalette + coin brand colours
straight from json-styles/style.json so hues live WITH the theme and flip when
the theme switches (rather than being hard-coded in Python)."""

import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STYLE = os.path.join(_ROOT, "json-styles", "style.json")

THEME_LIGHT = "Crypto Light"
THEME_DARK = "Crypto Dark"

# Icon stroke colour per theme, split by the surface the icon sits on:
#   rail  -> icons live on the DARK sidebar (light-grey stroke in both themes)
#   card  -> icons live on the LIGHT card   (muted stroke that flips with theme)
RAIL_ICON = {THEME_LIGHT: "#9aa1b6", THEME_DARK: "#9aa1b6"}
CARD_ICON = {THEME_LIGHT: "#8b90a2", THEME_DARK: "#aeb4c4"}


def _load():
    with open(_STYLE, "r", encoding="utf-8") as f:
        return json.load(f)


def chart_palette(theme_name):
    """Return the ChartPalette dict for the active theme (falls back to light)."""
    pal = _load().get("ChartPalette", {})
    return pal.get(theme_name) or pal.get(THEME_LIGHT) or {}


def coins():
    """Ticker -> brand colour (theme-independent)."""
    return _load().get("Coins", {})


def is_light(theme_name):
    return "light" in str(theme_name or "").lower()


def rail_icon_color(theme_name):
    return RAIL_ICON.get(theme_name, RAIL_ICON[THEME_LIGHT])


def card_icon_color(theme_name):
    return CARD_ICON.get(theme_name, CARD_ICON[THEME_LIGHT])
