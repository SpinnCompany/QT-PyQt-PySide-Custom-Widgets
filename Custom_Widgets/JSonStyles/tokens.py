########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## Design token system (hybrid model).
##
##   * Primitives  - raw, theme-independent scales (Tailwind-like):
##                   colours, spacing, radius, font.
##   * Semantic    - roles that REFERENCE primitives and differ per theme
##                   (light / dark): surface, primary, outline, etc.
##
## Components style themselves against SEMANTIC roles only, via the
## variant/size dynamic properties + QSS attribute selectors. See:
##     docs/design/variant-token-system.md
##
## A reference like "{color.blue.600}" resolves through the primitive tree.
## `DesignTokens.role(name)` returns the final value for a semantic role;
## `applyDesignTokens(target, theme=...)` generates component QSS and applies
## it to a QApplication or widget (idempotent, so theme switching is safe).
########################################################################
import os
import re


########################################################################
## Default primitives (raw values, theme-independent)
########################################################################
_PRIMITIVES = {
    "color": {
        "white": "#ffffff",
        "black": "#000000",
        "slate": {
            "50": "#f8fafc", "100": "#f1f5f9", "200": "#e2e8f0", "300": "#cbd5e1",
            "400": "#94a3b8", "500": "#64748b", "600": "#475569", "700": "#334155",
            "800": "#1e293b", "900": "#0f172a", "950": "#020617",
        },
        "blue": {
            "50": "#eff6ff", "400": "#60a5fa", "500": "#3b82f6",
            "600": "#2563eb", "700": "#1d4ed8",
        },
        "red": {
            "400": "#f87171", "500": "#ef4444", "600": "#dc2626", "700": "#b91c1c",
        },
        "green": {
            "400": "#4ade80", "500": "#22c55e", "600": "#16a34a", "700": "#15803d",
        },
        "amber": {
            "400": "#fbbf24", "500": "#f59e0b", "600": "#d97706", "700": "#b45309",
        },
    },
    "space": {"1": 4, "2": 8, "3": 12, "4": 16, "6": 24},
    "radius": {"sm": 4, "md": 8, "lg": 12, "full": 9999},
    "font": {
        "size": {"sm": 13, "md": 14, "lg": 16, "xl": 20, "2xl": 28},
        "weight": {"regular": 400, "medium": 500, "semibold": 600, "bold": 700},
    },
}


########################################################################
## Default semantic roles per theme (reference primitives)
########################################################################
_SEMANTIC = {
    "light": {
        "surface": "{color.white}",
        "on-surface": "{color.slate.900}",
        "surface-muted": "{color.slate.100}",
        "primary": "{color.blue.600}",
        "on-primary": "{color.white}",
        "primary-hover": "{color.blue.700}",
        "secondary": "{color.slate.200}",
        "on-secondary": "{color.slate.900}",
        "secondary-hover": "{color.slate.300}",
        "outline": "{color.slate.300}",
        "destructive": "{color.red.600}",
        "on-destructive": "{color.white}",
        "destructive-hover": "{color.red.700}",
        "success": "{color.green.600}",
        "on-success": "{color.white}",
        "warning": "{color.amber.600}",
        "on-warning": "{color.white}",
        "info": "{color.blue.600}",
        "on-info": "{color.white}",
        "accent": "{color.blue.600}",
        "focus-ring": "{color.blue.500}",
    },
    "dark": {
        "surface": "{color.slate.900}",
        "on-surface": "{color.slate.100}",
        "surface-muted": "{color.slate.800}",
        "primary": "{color.blue.500}",
        "on-primary": "{color.white}",
        "primary-hover": "{color.blue.400}",
        "secondary": "{color.slate.700}",
        "on-secondary": "{color.slate.100}",
        "secondary-hover": "{color.slate.600}",
        "outline": "{color.slate.600}",
        "destructive": "{color.red.500}",
        "on-destructive": "{color.white}",
        "destructive-hover": "{color.red.400}",
        "success": "{color.green.500}",
        "on-success": "{color.white}",
        "warning": "{color.amber.500}",
        "on-warning": "{color.white}",
        "info": "{color.blue.400}",
        "on-info": "{color.white}",
        "accent": "{color.blue.400}",
        "focus-ring": "{color.blue.400}",
    },
}


def _deep_merge(base, override):
    """Recursively merge ``override`` into a copy of ``base``."""
    out = dict(base)
    for key, val in (override or {}).items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = val
    return out


class DesignTokens(object):
    """Resolves the hybrid token model for a given theme.

    theme       "light" or "dark".
    primitives  optional dict deep-merged over the default primitives.
    semantic    optional dict of per-theme overrides, e.g.
                {"light": {"primary": "{color.red.600}"}}.
    """

    def __init__(self, theme="light", primitives=None, semantic=None):
        self.theme = theme if theme in _SEMANTIC else "light"
        self._primitives = _deep_merge(_PRIMITIVES, primitives)
        self._semantic = _deep_merge(_SEMANTIC[self.theme],
                                     (semantic or {}).get(self.theme))

    def _lookup(self, path):
        node = self._primitives
        for part in path.split("."):
            node = node[part]   # raises KeyError on an unknown path
        return node

    def resolve(self, value):
        """Resolve a value that may be a "{ref}" chain into its primitive."""
        seen = set()
        while isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            ref = value[1:-1]
            if ref in seen:
                break               # cycle guard
            seen.add(ref)
            value = self._lookup(ref)
        return value

    def role(self, name):
        """Final resolved value for a semantic role, or a raw primitive path
        (e.g. "space.2", "radius.md")."""
        if name in self._semantic:
            return self.resolve(self._semantic[name])
        return self.resolve("{%s}" % name)

    # convenience: "12px" from a spacing/radius/size role
    def px(self, name):
        return "%dpx" % int(self.role(name))


########################################################################
## Component QSS generation (styled against semantic roles only)
########################################################################
def button_qss(tokens):
    """Generate QCustomQPushButton QSS for every variant x size, from tokens.

    Uses the `variant` and `sizeVariant` dynamic properties as QSS attribute
    selectors. `sizeVariant` (not `size`) avoids shadowing QWidget.size().
    """
    r = tokens.role
    px = tokens.px
    css = []

    css.append(
        "QCustomQPushButton {\n"
        "    border: 1px solid transparent;\n"
        "    border-radius: %s;\n"
        "    font-weight: %d;\n"
        "    padding: %s %s;\n"          # md defaults
        "    font-size: %s;\n"
        "}\n" % (px("radius.md"), int(r("font.weight.medium")),
                 px("space.2"), px("space.3"), px("font.size.md"))
    )

    sizes = {
        "sm": ("space.1", "space.2", "font.size.sm"),
        "md": ("space.2", "space.3", "font.size.md"),
        "lg": ("space.3", "space.4", "font.size.lg"),
    }
    for name, (pad_y, pad_x, fsize) in sizes.items():
        css.append('QCustomQPushButton[sizeVariant="%s"] { padding: %s %s; font-size: %s; }\n'
                   % (name, px(pad_y), px(pad_x), px(fsize)))

    def variant(sel, decls):
        css.append('QCustomQPushButton[variant="%s"] { %s }\n' % (sel, decls))

    variant("primary", "background-color: %s; color: %s;" % (r("primary"), r("on-primary")))
    css.append('QCustomQPushButton[variant="primary"]:hover { background-color: %s; }\n' % r("primary-hover"))

    variant("secondary", "background-color: %s; color: %s;" % (r("secondary"), r("on-secondary")))
    css.append('QCustomQPushButton[variant="secondary"]:hover { background-color: %s; }\n' % r("secondary-hover"))

    variant("outline", "background-color: transparent; color: %s; border: 1px solid %s;"
            % (r("on-surface"), r("outline")))
    css.append('QCustomQPushButton[variant="outline"]:hover { background-color: %s; }\n' % r("surface-muted"))

    variant("ghost", "background-color: transparent; color: %s;" % r("on-surface"))
    css.append('QCustomQPushButton[variant="ghost"]:hover { background-color: %s; }\n' % r("surface-muted"))

    variant("destructive", "background-color: %s; color: %s;" % (r("destructive"), r("on-destructive")))
    css.append('QCustomQPushButton[variant="destructive"]:hover { background-color: %s; }\n' % r("destructive-hover"))

    # focus ring (a11y) + disabled
    css.append('QCustomQPushButton:focus { border: 2px solid %s; }\n' % r("focus-ring"))
    css.append('QCustomQPushButton:disabled { color: %s; background-color: %s; }\n'
               % (r("outline"), r("surface-muted")))
    return "".join(css)


def datatable_qss(tokens):
    """Generate QCustomDataTable QSS (view, header, selection, footer) from
    tokens. Scoped to the widget's class + object names so it never leaks."""
    r = tokens.role
    px = tokens.px
    css = []

    css.append("QCustomDataTable { background-color: %s; }\n" % r("surface"))

    css.append(
        "QCustomDataTable QTableView {\n"
        "    background-color: %s;\n"
        "    alternate-background-color: %s;\n"
        "    color: %s;\n"
        "    gridline-color: %s;\n"
        "    border: 1px solid %s;\n"
        "    border-radius: %s;\n"
        "    selection-background-color: %s;\n"
        "    selection-color: %s;\n"
        "}\n" % (r("surface"), r("surface-muted"), r("on-surface"),
                 r("outline"), r("outline"), px("radius.md"),
                 r("accent"), r("on-primary")))

    css.append("QCustomDataTable QTableView::item { padding: %s %s; }\n"
               % (px("space.1"), px("space.2")))

    css.append(
        "QCustomDataTable QHeaderView::section {\n"
        "    background-color: %s;\n"
        "    color: %s;\n"
        "    border: none;\n"
        "    border-bottom: 1px solid %s;\n"
        "    padding: %s;\n"
        "    font-weight: %d;\n"
        "}\n" % (r("surface-muted"), r("on-surface"), r("outline"),
                 px("space.2"), int(r("font.weight.semibold"))))

    css.append("QCustomDataTable QTableCornerButton::section { "
               "background-color: %s; border: none; }\n" % r("surface-muted"))

    css.append("QCustomDataTable #dataTableFooter { background-color: %s; }\n" % r("surface"))
    css.append("QCustomDataTable #dataTablePageLabel { color: %s; }\n" % r("on-surface"))

    css.append(
        "QCustomDataTable #dataTablePrev, QCustomDataTable #dataTableNext {\n"
        "    background-color: transparent; color: %s;\n"
        "    border: 1px solid %s; border-radius: %s; padding: %s %s;\n"
        "}\n" % (r("on-surface"), r("outline"), px("radius.md"),
                 px("space.1"), px("space.3")))
    css.append("QCustomDataTable #dataTablePrev:hover, QCustomDataTable #dataTableNext:hover "
               "{ background-color: %s; }\n" % r("surface-muted"))
    css.append("QCustomDataTable #dataTablePrev:disabled, QCustomDataTable #dataTableNext:disabled "
               "{ color: %s; }\n" % r("outline"))

    # sizeVariant -> density + font-size
    dens = {"sm": ("font.size.sm", "space.1"),
            "md": ("font.size.md", "space.1"),
            "lg": ("font.size.lg", "space.2")}
    for name, (fsize, pad_y) in dens.items():
        css.append('QCustomDataTable[sizeVariant="%s"] QTableView { font-size: %s; }\n'
                   % (name, px(fsize)))
        css.append('QCustomDataTable[sizeVariant="%s"] QTableView::item { padding: %s %s; }\n'
                   % (name, px(pad_y), px("space.2")))

    # variant -> table border emphasis
    css.append('QCustomDataTable[variant="ghost"] QTableView { border: none; }\n')
    css.append('QCustomDataTable[variant="primary"] QTableView { border: 1px solid %s; }\n'
               % r("accent"))
    return "".join(css)


def toast_qss(tokens):
    """Generate QCustomToast QSS from tokens. A surface card with a coloured
    left accent bar per type (variant)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append(
        "QCustomToast {\n"
        "    background-color: %s;\n"
        "    color: %s;\n"
        "    border: 1px solid %s;\n"
        "    border-radius: %s;\n"
        "}\n" % (r("surface"), r("on-surface"), r("outline"), px("radius.md")))
    css.append("QCustomToast #toastMessage { color: %s; }\n" % r("on-surface"))
    css.append("QCustomToast #toastTitle { color: %s; font-weight: %d; }\n"
               % (r("on-surface"), int(r("font.weight.semibold"))))
    css.append(
        "QCustomToast #toastClose {\n"
        "    background-color: transparent; border: none; color: %s;\n"
        "    border-radius: %s;\n"
        "}\n" % (r("on-surface"), px("radius.sm")))
    css.append("QCustomToast #toastClose:hover { background-color: %s; }\n" % r("surface-muted"))
    # per-type accent bar (variant)
    for variant, role in (("success", "success"), ("error", "destructive"),
                          ("warning", "warning"), ("info", "info")):
        css.append('QCustomToast[variant="%s"] { border-left: 4px solid %s; }\n'
                   % (variant, r(role)))
        css.append('QCustomToast[variant="%s"] #toastIcon { color: %s; }\n'
                   % (variant, r(role)))
    return "".join(css)


def combobox_qss(tokens):
    """Generate QCustomComboBox QSS (field, drop-down, and both popup lists)
    from tokens."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append(
        "QCustomComboBox {\n"
        "    background-color: %s;\n"
        "    color: %s;\n"
        "    border: 1px solid %s;\n"
        "    border-radius: %s;\n"
        "    padding: %s %s;\n"
        "}\n" % (r("surface"), r("on-surface"), r("outline"), px("radius.md"),
                 px("space.2"), px("space.3")))
    css.append("QCustomComboBox:focus { border: 2px solid %s; }\n" % r("focus-ring"))
    css.append("QCustomComboBox:disabled { color: %s; }\n" % r("outline"))
    css.append("QCustomComboBox QLineEdit { background: transparent; border: none; color: %s; }\n"
               % r("on-surface"))
    css.append("QCustomComboBox::drop-down { border: none; width: 22px;"
               " subcontrol-origin: padding; subcontrol-position: center right; }\n")

    sizes = {"sm": ("space.1", "space.2", "font.size.sm"),
             "md": ("space.2", "space.3", "font.size.md"),
             "lg": ("space.3", "space.4", "font.size.lg")}
    for name, (pad_y, pad_x, fsize) in sizes.items():
        css.append('QCustomComboBox[sizeVariant="%s"] { padding: %s %s; font-size: %s; }\n'
                   % (name, px(pad_y), px(pad_x), px(fsize)))
    css.append('QCustomComboBox[variant="ghost"] { border: none; }\n')
    css.append('QCustomComboBox[variant="primary"] { border: 1px solid %s; }\n' % r("accent"))

    # both popup lists: the arrow drop-down (#comboDropdown) and the autocomplete
    # completer popup (#comboCompleterPopup)
    for oid in ("comboDropdown", "comboCompleterPopup"):
        css.append(
            "#%s {\n"
            "    background-color: %s; color: %s; border: 1px solid %s; outline: 0;\n"
            "    selection-background-color: %s; selection-color: %s;\n"
            "}\n" % (oid, r("surface"), r("on-surface"), r("outline"),
                     r("accent"), r("on-primary")))
        css.append("#%s::item { padding: %s %s; }\n"
                   % (oid, px("space.1"), px("space.2")))
    return "".join(css)


def datetime_qss(tokens):
    """Generate QCustomDateEdit / QCustomTimeEdit field QSS + the (scoped)
    calendar popup QSS from tokens."""
    r = tokens.role
    px = tokens.px
    css = []
    sizes = {"sm": ("space.1", "space.2", "font.size.sm"),
             "md": ("space.2", "space.3", "font.size.md"),
             "lg": ("space.3", "space.4", "font.size.lg")}
    for cls in ("QCustomDateEdit", "QCustomTimeEdit"):
        css.append(
            "%s {\n"
            "    background-color: %s; color: %s;\n"
            "    border: 1px solid %s; border-radius: %s; padding: %s %s;\n"
            "}\n" % (cls, r("surface"), r("on-surface"), r("outline"),
                     px("radius.md"), px("space.2"), px("space.3")))
        css.append("%s:focus { border: 2px solid %s; }\n" % (cls, r("focus-ring")))
        css.append("%s::drop-down { border: none; width: 22px;"
                   " subcontrol-origin: padding; subcontrol-position: center right; }\n" % cls)
        for name, (pad_y, pad_x, fsize) in sizes.items():
            css.append('%s[sizeVariant="%s"] { padding: %s %s; font-size: %s; }\n'
                       % (cls, name, px(pad_y), px(pad_x), px(fsize)))
        css.append('%s[variant="ghost"] { border: none; }\n' % cls)
        css.append('%s[variant="primary"] { border: 1px solid %s; }\n' % (cls, r("accent")))

    # calendar popup (scoped by objectName so it doesn't restyle other calendars)
    css.append("#customCalendar { background-color: %s; }\n" % r("surface"))
    css.append("#customCalendar QWidget#qt_calendar_navigationbar { background-color: %s; }\n"
               % r("surface-muted"))
    css.append("#customCalendar QToolButton { color: %s; background-color: transparent;"
               " border: none; padding: 4px; }\n" % r("on-surface"))
    css.append("#customCalendar QToolButton:hover { background-color: %s; }\n" % r("surface-muted"))
    css.append("#customCalendar QMenu { background-color: %s; color: %s; }\n"
               % (r("surface"), r("on-surface")))
    css.append(
        "#customCalendar QAbstractItemView {\n"
        "    background-color: %s; color: %s; outline: 0;\n"
        "    selection-background-color: %s; selection-color: %s;\n"
        "}\n" % (r("surface"), r("on-surface"), r("accent"), r("on-primary")))
    css.append("#customCalendar QAbstractItemView:disabled { color: %s; }\n" % r("outline"))
    css.append("QCustomDateRangeEdit #dateRangeSep { color: %s; }\n" % r("on-surface"))
    return "".join(css)


def commandpalette_qss(tokens):
    """Generate QCustomCommandPalette QSS (dim backdrop, panel, search, list)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomCommandPalette { background-color: rgba(0, 0, 0, 110); }\n")
    css.append(
        "#commandPalettePanel {\n"
        "    background-color: %s; border: 1px solid %s; border-radius: %s;\n"
        "}\n" % (r("surface"), r("outline"), px("radius.lg")))
    css.append(
        "#commandPaletteSearch {\n"
        "    background-color: transparent; border: none;\n"
        "    border-bottom: 1px solid %s; color: %s;\n"
        "    padding: %s; font-size: %s;\n"
        "}\n" % (r("outline"), r("on-surface"), px("space.3"), px("font.size.lg")))
    css.append(
        "#commandPaletteList {\n"
        "    background-color: %s; color: %s; border: none; outline: 0;\n"
        "}\n" % (r("surface"), r("on-surface")))
    css.append("#commandPaletteList::item { padding: %s %s; border-radius: %s; }\n"
               % (px("space.2"), px("space.3"), px("radius.sm")))
    css.append("#commandPaletteList::item:selected { background-color: %s; color: %s; }\n"
               % (r("accent"), r("on-primary")))
    css.append("#commandPaletteList::item:hover { background-color: %s; }\n" % r("surface-muted"))
    return "".join(css)


def tabs_qss(tokens):
    """Generate QCustomTabWidget QSS with three tab styles (underline / pills /
    enclosed) and sizeVariant density."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomTabWidget::pane { border: 1px solid %s; border-radius: %s;"
               " background-color: %s; top: -1px; }\n"
               % (r("outline"), px("radius.md"), r("surface")))
    css.append("QCustomTabWidget QTabBar::tab {\n"
               "    background-color: transparent; color: %s;\n"
               "    padding: %s %s; border: none; margin-right: 2px;\n"
               "}\n" % (r("on-surface"), px("space.2"), px("space.3")))
    css.append("QCustomTabWidget QTabBar::tab:hover { color: %s; }\n" % r("accent"))

    # underline (default): accent underline on the selected tab
    css.append('QCustomTabWidget[tabStyle="underline"] QTabBar::tab:selected {'
               ' color: %s; border-bottom: 2px solid %s; }\n'
               % (r("accent"), r("accent")))
    # pills: rounded accent background on the selected tab
    css.append('QCustomTabWidget[tabStyle="pills"] QTabBar::tab {'
               ' border-radius: %s; }\n' % px("radius.md"))
    css.append('QCustomTabWidget[tabStyle="pills"] QTabBar::tab:selected {'
               ' background-color: %s; color: %s; }\n' % (r("accent"), r("on-primary")))
    # enclosed: bordered tabs merging into the pane
    css.append('QCustomTabWidget[tabStyle="enclosed"] QTabBar::tab {'
               ' border: 1px solid %s; border-bottom: none;'
               ' border-top-left-radius: %s; border-top-right-radius: %s; }\n'
               % (r("outline"), px("radius.sm"), px("radius.sm")))
    css.append('QCustomTabWidget[tabStyle="enclosed"] QTabBar::tab:selected {'
               ' background-color: %s; color: %s; }\n' % (r("surface"), r("accent")))

    sizes = {"sm": ("space.1", "space.2", "font.size.sm"),
             "md": ("space.2", "space.3", "font.size.md"),
             "lg": ("space.3", "space.4", "font.size.lg")}
    for name, (pad_y, pad_x, fsize) in sizes.items():
        css.append('QCustomTabWidget[sizeVariant="%s"] QTabBar::tab {'
                   ' padding: %s %s; font-size: %s; }\n'
                   % (name, px(pad_y), px(pad_x), px(fsize)))
    return "".join(css)


def accordion_qss(tokens):
    """Generate QCustomAccordion QSS (section headers + content)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomAccordion #accordionHeader {\n"
               "    text-align: left; background-color: %s; color: %s;\n"
               "    border: 1px solid %s; border-radius: %s;\n"
               "    padding: %s %s; font-weight: %d;\n"
               "}\n" % (r("surface-muted"), r("on-surface"), r("outline"),
                        px("radius.md"), px("space.2"), px("space.3"),
                        int(r("font.weight.semibold"))))
    css.append("QCustomAccordion #accordionHeader:hover { border-color: %s; }\n" % r("accent"))
    css.append("QCustomAccordion #accordionHeader:checked { color: %s; border-color: %s; }\n"
               % (r("accent"), r("accent")))
    css.append("QCustomAccordion #accordionContent {\n"
               "    background-color: %s; color: %s;\n"
               "    border: 1px solid %s; border-top: none;\n"
               "    border-bottom-left-radius: %s; border-bottom-right-radius: %s;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"),
                        px("radius.md"), px("radius.md")))
    return "".join(css)


def tree_qss(tokens):
    """Generate QCustomTreeWidget QSS (items, selection, hover)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomTreeWidget {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s; outline: 0;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"), px("radius.md")))
    css.append("QCustomTreeWidget::item { padding: %s %s; }\n"
               % (px("space.1"), px("space.2")))
    css.append("QCustomTreeWidget::item:hover { background-color: %s; }\n" % r("surface-muted"))
    css.append("QCustomTreeWidget::item:selected { background-color: %s; color: %s; }\n"
               % (r("accent"), r("on-primary")))
    css.append("QCustomTreeWidget QHeaderView::section {\n"
               "    background-color: %s; color: %s; border: none;\n"
               "    border-bottom: 1px solid %s; padding: %s;\n"
               "}\n" % (r("surface-muted"), r("on-surface"), r("outline"), px("space.2")))
    sizes = {"sm": "font.size.sm", "md": "font.size.md", "lg": "font.size.lg"}
    for name, fsize in sizes.items():
        css.append('QCustomTreeWidget[sizeVariant="%s"] { font-size: %s; }\n'
                   % (name, px(fsize)))
    return "".join(css)


def drawer_qss(tokens):
    """Generate QCustomDrawer QSS (dim backdrop + panel)."""
    r = tokens.role
    css = []
    css.append("QCustomDrawer { background-color: rgba(0, 0, 0, 110); }\n")
    css.append("#drawerPanel { background-color: %s; color: %s; border: 1px solid %s; }\n"
               % (r("surface"), r("on-surface"), r("outline")))
    return "".join(css)


def stepper_qss(tokens):
    """Generate QCustomStepper QSS (circles + connectors + labels) driven by
    the `state` dynamic property: completed / active / pending."""
    r = tokens.role
    css = []
    css.append("QCustomStepper #stepperCircle {\n"
               "    border-radius: 14px; border: 2px solid %s; color: %s;\n"
               "    background-color: %s; font-weight: %d;\n"
               "}\n" % (r("outline"), r("on-surface"), r("surface"),
                        int(r("font.weight.semibold"))))
    css.append('QCustomStepper #stepperCircle[state="active"] {'
               ' border-color: %s; color: %s; }\n' % (r("accent"), r("accent")))
    css.append('QCustomStepper #stepperCircle[state="completed"] {'
               ' border-color: %s; background-color: %s; color: %s; }\n'
               % (r("accent"), r("accent"), r("on-primary")))
    css.append('QCustomStepper #stepperCircle[state="pending"] {'
               ' border-color: %s; color: %s; }\n' % (r("outline"), r("outline")))
    css.append("QCustomStepper #stepperLabel { color: %s; }\n" % r("on-surface"))
    css.append('QCustomStepper #stepperConnector[state="completed"] { color: %s;'
               ' background-color: %s; }\n' % (r("accent"), r("accent")))
    css.append('QCustomStepper #stepperConnector[state="pending"] { color: %s;'
               ' background-color: %s; }\n' % (r("outline"), r("outline")))
    return "".join(css)


def richtext_qss(tokens):
    """Generate QCustomRichTextEditor QSS (toolbar, buttons, editor)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomRichTextEditor { border: 1px solid %s; border-radius: %s;"
               " background-color: %s; }\n"
               % (r("outline"), px("radius.md"), r("surface")))
    css.append("#rteToolbar { background-color: %s; border-bottom: 1px solid %s; }\n"
               % (r("surface-muted"), r("outline")))
    css.append("#rteSep { background-color: %s; margin: 2px 4px; }\n" % r("outline"))
    css.append("#rteButton {\n"
               "    background-color: transparent; color: %s; border: none;\n"
               "    border-radius: %s; padding: 4px 8px; min-width: 18px;\n"
               "}\n" % (r("on-surface"), px("radius.sm")))
    css.append("#rteButton:hover { background-color: %s; }\n" % r("surface"))
    css.append("#rteButton:checked { background-color: %s; color: %s; }\n"
               % (r("accent"), r("on-primary")))
    css.append("#rteEditor { background-color: %s; color: %s; border: none; padding: %s; }\n"
               % (r("surface"), r("on-surface"), px("space.2")))
    return "".join(css)


def colorpicker_qss(tokens):
    """Generate QCustomColorPicker QSS (hex field + preset popup)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("#colorHex {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s; padding: %s %s;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"), px("radius.md"),
                        px("space.1"), px("space.2")))
    css.append("#colorHex:focus { border: 2px solid %s; }\n" % r("focus-ring"))
    css.append("#colorPopup { background-color: %s; border: 1px solid %s; border-radius: %s; }\n"
               % (r("surface"), r("outline"), px("radius.md")))
    css.append("#colorCustomBtn {\n"
               "    background-color: transparent; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s; padding: %s;\n"
               "}\n" % (r("on-surface"), r("outline"), px("radius.sm"), px("space.1")))
    css.append("#colorCustomBtn:hover { background-color: %s; }\n" % r("surface-muted"))
    return "".join(css)


def breadcrumbs_qss(tokens):
    """Generate QCustomBreadcrumbs QSS (links, current, separator)."""
    r = tokens.role
    css = []
    css.append("QCustomBreadcrumbs #breadcrumbLink {"
               " background-color: transparent; border: none; color: %s; padding: 0 2px; }\n"
               % r("accent"))
    css.append("QCustomBreadcrumbs #breadcrumbLink:hover { color: %s; }\n" % r("primary-hover"))
    css.append("QCustomBreadcrumbs #breadcrumbCurrent { color: %s; font-weight: %d; }\n"
               % (r("on-surface"), int(r("font.weight.semibold"))))
    css.append("QCustomBreadcrumbs #breadcrumbSep { color: %s; }\n" % r("outline"))
    return "".join(css)


def rating_qss(tokens):
    """Generate QCustomRating QSS (empty vs filled stars)."""
    r = tokens.role
    css = []
    css.append("QCustomRating #ratingStar { color: %s; font-size: 18px; }\n" % r("outline"))
    css.append('QCustomRating #ratingStar[filled="true"] { color: %s; }\n' % r("warning"))
    return "".join(css)


def chip_qss(tokens):
    """Generate QCustomChip QSS (default + selected filter chip)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomChip {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s;\n"
               "}\n" % (r("surface-muted"), r("on-surface"), r("outline"),
                        px("radius.full")))
    css.append("QCustomChip #chipLabel { color: %s; background-color: transparent; }\n"
               % r("on-surface"))
    css.append('QCustomChip[selected="true"] { background-color: %s; border-color: %s; }\n'
               % (r("accent"), r("accent")))
    css.append('QCustomChip[selected="true"] #chipLabel { color: %s; }\n' % r("on-primary"))
    css.append("QCustomChip #chipClose {\n"
               "    background-color: transparent; border: none; color: %s; border-radius: %s;\n"
               "}\n" % (r("on-surface"), px("radius.full")))
    css.append("QCustomChip #chipClose:hover { background-color: %s; }\n" % r("outline"))
    css.append('QCustomChip[selected="true"] #chipClose { color: %s; }\n' % r("on-primary"))
    return "".join(css)


def skeleton_qss(tokens):
    """Feed token colours to the painted QCustomSkeleton via qproperty."""
    r = tokens.role
    return ("QCustomSkeleton { qproperty-baseColor: %s; qproperty-highlightColor: %s; }\n"
            % (r("surface-muted"), r("surface")))


def avatargroup_qss(tokens):
    """Separating ring colour + overflow-chip colours for QCustomAvatarGroup.
    The ring matches the surface; the '+N' chip uses the muted surface role."""
    r = tokens.role
    return ("QCustomAvatarGroup { qproperty-ringColor: %s; "
            "qproperty-overflowBg: %s; qproperty-overflowText: %s; }\n"
            % (r("surface"), r("surface-muted"), r("on-surface")))


def timeline_qss(tokens):
    """Rail colours (qproperty) + content text for QCustomTimeline."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomTimeline { qproperty-lineColor: %s; qproperty-dotColor: %s; }\n"
               % (r("outline"), r("accent")))
    css.append("QCustomTimeline #timelineTitle { color: %s; font-weight: %d; }\n"
               % (r("on-surface"), int(r("font.weight.semibold"))))
    css.append("QCustomTimeline #timelineTime { color: %s; font-size: %s; }\n"
               % (r("accent"), px("font.size.sm")))
    css.append("QCustomTimeline #timelineDesc { color: %s; }\n" % r("outline"))
    return "".join(css)


def pagination_qss(tokens):
    """Generate QCustomPagination QSS (page buttons, current, nav, ellipsis)."""
    r = tokens.role
    px = tokens.px
    css = []
    for oid in ("pageBtn", "pageNav"):
        css.append("QCustomPagination #%s {\n"
                   "    background-color: transparent; color: %s; border: 1px solid %s;\n"
                   "    border-radius: %s; padding: %s %s; min-width: 16px;\n"
                   "}\n" % (oid, r("on-surface"), r("outline"), px("radius.md"),
                            px("space.1"), px("space.2")))
        css.append("QCustomPagination #%s:hover { background-color: %s; }\n"
                   % (oid, r("surface-muted")))
        css.append("QCustomPagination #%s:disabled { color: %s; }\n" % (oid, r("outline")))
    css.append('QCustomPagination #pageBtn[current="true"] {'
               ' background-color: %s; color: %s; border-color: %s; }\n'
               % (r("accent"), r("on-primary"), r("accent")))
    css.append("QCustomPagination #pageEllipsis { color: %s; padding: 0 2px; }\n" % r("outline"))
    return "".join(css)


def popover_qss(tokens):
    """Feed token colours to the painted QCustomPopover via qproperty, and
    colour its content text."""
    r = tokens.role
    css = []
    css.append("QCustomPopover { qproperty-panelColor: %s; qproperty-borderColor: %s; }\n"
               % (r("surface"), r("outline")))
    css.append("QCustomPopover, QCustomPopover QLabel { color: %s; }\n" % r("on-surface"))
    return "".join(css)


def segmented_qss(tokens):
    """Generate QCustomSegmentedControl QSS (joined buttons, rounded ends,
    selected segment)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomSegmentedControl #segmentButton {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    padding: %s %s; margin: 0; border-left-width: 0;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"),
                        px("space.2"), px("space.3")))
    css.append('QCustomSegmentedControl #segmentButton[seg="first"],'
               ' QCustomSegmentedControl #segmentButton[seg="only"] {'
               ' border-left-width: 1px; border-top-left-radius: %s; border-bottom-left-radius: %s; }\n'
               % (px("radius.md"), px("radius.md")))
    css.append('QCustomSegmentedControl #segmentButton[seg="last"],'
               ' QCustomSegmentedControl #segmentButton[seg="only"] {'
               ' border-top-right-radius: %s; border-bottom-right-radius: %s; }\n'
               % (px("radius.md"), px("radius.md")))
    css.append("QCustomSegmentedControl #segmentButton:hover { background-color: %s; }\n"
               % r("surface-muted"))
    css.append("QCustomSegmentedControl #segmentButton:checked {"
               " background-color: %s; color: %s; border-color: %s; }\n"
               % (r("accent"), r("on-primary"), r("accent")))
    return "".join(css)


def emptystate_qss(tokens):
    """Generate QCustomEmptyState QSS (icon, title, description)."""
    r = tokens.role
    px = tokens.px
    css = []
    # markColor drives the PAINTED default mark; the #emptyIcon colour still
    # applies when a caller passes a string icon of their own.
    css.append("QCustomEmptyState { qproperty-markColor: %s; }\n" % r("outline"))
    css.append("QCustomEmptyState #emptyIcon { color: %s; font-size: 44px; }\n" % r("outline"))
    css.append("QCustomEmptyState #emptyTitle { color: %s; font-weight: %d; font-size: %s; }\n"
               % (r("on-surface"), int(r("font.weight.semibold")), px("font.size.lg")))
    css.append("QCustomEmptyState #emptyDesc { color: %s; }\n" % r("outline"))
    return "".join(css)


def chat_qss(tokens):
    """Generate QCustomChatList / QCustomChatThread QSS.

    Both paint from qproperties rather than QSS, and nothing was driving those
    properties — so the two widgets rendered byte-identically in light and dark
    and simply ignored the app theme.
    """
    r = tokens.role
    css = []
    css.append("QCustomChatList {\n"
               "    qproperty-surfaceColor: %s;\n"
               "    qproperty-nameColor: %s;\n"
               "    qproperty-previewColor: %s;\n"
               "    qproperty-timeColor: %s;\n"
               "    qproperty-activeColor: %s;\n"
               "    qproperty-activeNameColor: %s;\n"
               "    qproperty-activeTimeColor: %s;\n"
               "    qproperty-accentColor: %s;\n"
               "    qproperty-onlineColor: %s;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"), r("outline"),
                        r("primary"), r("on-primary"), r("on-primary"),
                        r("accent"), r("success")))
    css.append("QCustomChatThread {\n"
               "    qproperty-incomingBubbleColor: %s;\n"
               "    qproperty-incomingTextColor: %s;\n"
               "    qproperty-outgoingBubbleColor: %s;\n"
               "    qproperty-outgoingTextColor: %s;\n"
               "    qproperty-metaColor: %s;\n"
               "    qproperty-dateBgColor: %s;\n"
               "    qproperty-dateTextColor: %s;\n"
               "    qproperty-accentColor: %s;\n"
               "    qproperty-waveUnplayedColor: %s;\n"
               "}\n" % (r("secondary"), r("on-secondary"), r("primary"),
                        r("on-primary"), r("outline"), r("surface-muted"),
                        r("on-surface"), r("accent"), r("outline")))
    return "".join(css)


def tagedit_qss(tokens):
    """Generate QTagEdit QSS (surface + themed tag pills)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QTagEdit {\n"
               "    background-color: %s; border: 1px solid %s;\n"
               "    border-radius: %s;\n"
               "    qproperty-tagColor: %s; qproperty-tagTextColor: %s;\n"
               "}\n" % (r("surface"), r("outline"), px("radius.md"),
                        r("secondary"), r("on-secondary")))
    css.append("QTagEdit QLineEdit { background: transparent; color: %s; }\n"
               % r("on-surface"))
    return "".join(css)


def dropzone_qss(tokens):
    """Generate QCustomFileDropZone QSS (dashed zone + drag-active highlight)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomFileDropZone {\n"
               "    background-color: %s; border: 2px dashed %s; border-radius: %s;\n"
               "}\n" % (r("surface"), r("outline"), px("radius.md")))
    css.append('QCustomFileDropZone[dragActive="true"] {'
               ' background-color: %s; border-color: %s; }\n'
               % (r("surface-muted"), r("accent")))
    css.append("QCustomFileDropZone #dropPrompt { color: %s; font-weight: %d;"
               " background-color: transparent; }\n"
               % (r("on-surface"), int(r("font.weight.medium"))))
    css.append("QCustomFileDropZone #dropDetail { color: %s; background-color: transparent; }\n"
               % r("accent"))
    return "".join(css)


def rangeslider_qss(tokens):
    """Feed token colours to the painted QCustomRangeSlider via qproperty."""
    r = tokens.role
    return ("QCustomRangeSlider {\n"
            "    qproperty-trackColor: %s; qproperty-fillColor: %s;\n"
            "    qproperty-handleColor: %s; qproperty-handleBorderColor: %s;\n"
            "}\n" % (r("outline"), r("accent"), r("surface"), r("accent")))


def switch_qss(tokens):
    """Feed token colours to the painted QCustomSwitch via qproperty."""
    r = tokens.role
    return ("QCustomSwitch {\n"
            "    qproperty-trackOnColor: %s; qproperty-trackOffColor: %s;\n"
            "    qproperty-thumbColor: %s;\n"
            "}\n" % (r("accent"), r("outline"), r("surface")))


def radio_qss(tokens):
    """Feed token colours to the painted QCustomRadioButton via qproperty."""
    r = tokens.role
    return ("QCustomRadioButton {\n"
            "    qproperty-ringColor: %s; qproperty-ringCheckedColor: %s;\n"
            "    qproperty-dotColor: %s; qproperty-textColor: %s;\n"
            "}\n" % (r("outline"), r("accent"), r("accent"), r("on-surface")))


def gradientpicker_qss(tokens):
    """Feed token colours to the painted QCustomGradientPicker."""
    r = tokens.role
    return ("QCustomGradientPicker {\n"
            "    qproperty-borderColor: %s;\n"
            "    qproperty-borderActiveColor: %s;\n"
            "    qproperty-borderErrorColor: %s;\n"
            "    qproperty-handleColor: %s;\n"
            "    qproperty-handleBorderColor: %s;\n"
            "}\n" % (r("outline"), r("focus-ring"), r("destructive"),
                     r("surface"), r("on-surface")))


def imagepicker_qss(tokens):
    """Feed token colours to the painted QCustomImagePicker drop target."""
    r = tokens.role
    return ("QCustomImagePicker {\n"
            "    qproperty-borderColor: %s;\n"
            "    qproperty-borderActiveColor: %s;\n"
            "    qproperty-borderErrorColor: %s;\n"
            "    qproperty-backgroundColor: %s;\n"
            "    qproperty-textColor: %s;\n"
            "}\n" % (r("outline"), r("accent"), r("destructive"),
                     r("surface-muted"), r("on-surface")))


def multiselect_qss(tokens):
    """Feed token colours to QCustomMultiSelect (painted field + its popup)."""
    r = tokens.role
    px = tokens.px
    return ("QCustomMultiSelect {\n"
            "    qproperty-fieldBackgroundColor: %s;\n"
            "    qproperty-fieldBorderColor: %s;\n"
            "    qproperty-fieldBorderActiveColor: %s;\n"
            "    qproperty-fieldBorderErrorColor: %s;\n"
            "    qproperty-chipBackgroundColor: %s;\n"
            "    qproperty-chipTextColor: %s;\n"
            "    qproperty-textColor: %s;\n"
            "    qproperty-placeholderColor: %s;\n"
            "}\n"
            "QFrame#QCustomMultiSelectPopup {\n"
            "    background-color: %s; border: 1px solid %s; border-radius: %s;\n"
            "}\n"
            "QListWidget#QCustomMultiSelectList {\n"
            "    background-color: %s; color: %s; border: none;\n"
            "}\n" % (r("surface"), r("outline"), r("focus-ring"),
                     r("destructive"), r("surface-muted"), r("on-surface"),
                     r("on-surface"), r("outline"),
                     r("surface"), r("outline"), px("radius.md"),
                     r("surface"), r("on-surface")))


def verificationcode_qss(tokens):
    """Feed token colours to the painted QCustomVerificationCode boxes."""
    r = tokens.role
    return ("QCustomVerificationCode {\n"
            "    qproperty-boxBackgroundColor: %s;\n"
            "    qproperty-boxBorderColor: %s;\n"
            "    qproperty-boxBorderActiveColor: %s;\n"
            "    qproperty-boxBorderErrorColor: %s;\n"
            "    qproperty-textColor: %s;\n"
            "}\n" % (r("surface"), r("outline"), r("focus-ring"),
                     r("destructive"), r("on-surface")))


def textarea_qss(tokens):
    """Generate QCustomTextArea QSS (field chrome + counter colours).

    Note QCustomInput has no equivalent generator, so it is currently styled by
    whatever global QSS is loaded rather than by tokens. Worth closing, but not
    by leaving this widget in the same state.
    """
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomTextArea {\n"
               "    background-color: %s; color: %s;\n"
               "    border: 1px solid %s; border-radius: %s;\n"
               "    qproperty-counterColor: %s;\n"
               "    qproperty-counterOverColor: %s;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"),
                        px("radius.md"), r("on-surface"), r("destructive")))
    css.append("QCustomTextArea[state='focused'] {\n"
               "    border: 1px solid %s;\n"
               "}\n" % r("focus-ring"))
    css.append("QCustomTextArea[state='error'] {\n"
               "    border: 1px solid %s;\n"
               "}\n" % r("destructive"))
    css.append("QCustomTextArea[state='disabled'], QCustomTextArea:disabled {\n"
               "    background-color: %s; color: %s;\n"
               "}\n" % (r("surface-muted"), r("outline")))
    css.append("QCustomTextArea[variant='ghost'] {\n"
               "    background-color: transparent; border: 1px solid transparent;\n"
               "}\n")
    return "".join(css)


def motion_qss(tokens):
    """Token colours for the motion widgets."""
    r = tokens.role
    return ("QCustomNumberCounter { qproperty-textColor: %s; }\n"
            "QCustomTypewriterText {\n"
            "    qproperty-textColor: %s; qproperty-caretColor: %s;\n"
            "}\n"
            "QCustomRainbowButton {\n"
            "    qproperty-textColor: %s; qproperty-surfaceColor: %s;\n"
            "}\n"
            "QCustomSparklesText { qproperty-textColor: %s; }\n"
            % (r("on-surface"), r("on-surface"), r("accent"),
               r("on-surface"), r("surface"), r("on-surface")))


def chrome_qss(tokens):
    """Token colours for the chrome/branding widgets."""
    r = tokens.role
    return ("QCustomFeaturedIcon {\n"
            "    qproperty-accentColor: %s; qproperty-iconColor: %s;\n"
            "    qproperty-surfaceColor: %s;\n"
            "}\n"
            "QCustomCopyButton {\n"
            "    qproperty-accentColor: %s; qproperty-successColor: %s;\n"
            "    qproperty-textColor: %s; qproperty-surfaceColor: %s;\n"
            "}\n"
            "QCustomSocialButton {\n"
            "    qproperty-surfaceColor: %s;\n"
            "}\n"
            "QCustomHeaderNav {\n"
            "    qproperty-accentColor: %s; qproperty-textColor: %s;\n"
            "    qproperty-activeTextColor: %s; qproperty-surfaceColor: %s;\n"
            "    qproperty-dividerColor: %s;\n"
            "}\n" % (r("accent"), r("accent"), r("surface"),
                     r("accent"), r("success"), r("on-surface"), r("surface"),
                     r("surface"),
                     r("accent"), r("outline"), r("on-surface"), r("surface"),
                     r("surface-muted")))


def sankey_qss(tokens):
    """Feed the token text colour to the painted QCustomSankey labels."""
    return ("QCustomSankey {\n"
            "    qproperty-labelColor: %s;\n"
            "}\n" % tokens.role("on-surface"))


def radialbars_qss(tokens):
    """Feed token colours to QCustomRadialBars and QCustomRadialLines."""
    r = tokens.role
    return ("QCustomRadialBars {\n"
            "    qproperty-trackColor: %s;\n"
            "    qproperty-labelColor: %s;\n"
            "}\n"
            "QCustomRadialLines {\n"
            "    qproperty-gridColor: %s;\n"
            "    qproperty-labelColor: %s;\n"
            "}\n" % (r("surface-muted"), r("on-surface"),
                     r("surface-muted"), r("on-surface")))


def rangebar_qss(tokens):
    """Feed token colours to the painted QCustomRangeBarChart."""
    r = tokens.role
    return ("QCustomRangeBarChart {\n"
            "    qproperty-barColor: %s;\n"
            "    qproperty-gridColor: %s;\n"
            "    qproperty-labelColor: %s;\n"
            "    qproperty-boundsColor: %s;\n"
            "}\n" % (r("accent"), r("surface-muted"), r("on-surface"),
                     r("on-surface")))


def funnel_qss(tokens):
    """Feed token colours to the painted QCustomFunnelChart labels."""
    r = tokens.role
    return ("QCustomFunnelChart {\n"
            "    qproperty-labelColor: %s;\n"
            "    qproperty-outsideLabelColor: %s;\n"
            "}\n" % (r("on-primary"), r("on-surface")))


def scatter_qss(tokens):
    """Feed token colours to the painted QCustomScatterChart."""
    r = tokens.role
    return ("QCustomScatterChart {\n"
            "    qproperty-gridColor: %s;\n"
            "    qproperty-axisColor: %s;\n"
            "    qproperty-labelColor: %s;\n"
            "}\n" % (r("surface-muted"), r("outline"), r("on-surface")))


def radar_qss(tokens):
    """Feed token colours to the painted QCustomRadarChart."""
    r = tokens.role
    return ("QCustomRadarChart {\n"
            "    qproperty-gridColor: %s;\n"
            "    qproperty-axisColor: %s;\n"
            "    qproperty-labelColor: %s;\n"
            "}\n" % (r("surface-muted"), r("outline"), r("on-surface")))


def candlestick_qss(tokens):
    """Feed token colours to the painted QCustomCandlestickChart.

    Up/down are the success/destructive roles rather than raw green/red so a
    palette that redefines them (or a colour-blind-safe theme) carries through.
    """
    r = tokens.role
    return ("QCustomCandlestickChart {\n"
            "    qproperty-upColor: %s; qproperty-downColor: %s;\n"
            "    qproperty-wickColor: %s; qproperty-gridColor: %s;\n"
            "    qproperty-axisTextColor: %s;\n"
            "}\n" % (r("success"), r("destructive"), r("on-surface"),
                     r("outline"), r("on-surface")))


def radiogroup_qss(tokens):
    """Feed the token text colour to the painted QCustomRadioGroup title."""
    r = tokens.role
    return ("QCustomRadioGroup {\n"
            "    qproperty-titleColor: %s;\n"
            "}\n" % r("on-surface"))


def number_qss(tokens):
    """Generate QCustomNumberInput QSS (joined field + step buttons)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomNumberInput #numberField {\n"
               "    background-color: %s; color: %s;\n"
               "    border: 1px solid %s; border-left: none; border-right: none;\n"
               "    padding: %s %s;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"),
                        px("space.1"), px("space.2")))
    css.append("QCustomNumberInput #numberDown, QCustomNumberInput #numberUp {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    min-width: 26px; font-weight: %d; padding: %s;\n"
               "}\n" % (r("surface-muted"), r("on-surface"), r("outline"),
                        int(r("font.weight.semibold")), px("space.1")))
    css.append("QCustomNumberInput #numberDown {"
               " border-top-left-radius: %s; border-bottom-left-radius: %s; }\n"
               % (px("radius.md"), px("radius.md")))
    css.append("QCustomNumberInput #numberUp {"
               " border-top-right-radius: %s; border-bottom-right-radius: %s; }\n"
               % (px("radius.md"), px("radius.md")))
    css.append("QCustomNumberInput #numberDown:hover, QCustomNumberInput #numberUp:hover"
               " { background-color: %s; color: %s; }\n" % (r("accent"), r("on-primary")))
    css.append("QCustomNumberInput #numberDown:disabled, QCustomNumberInput #numberUp:disabled"
               " { color: %s; }\n" % r("outline"))
    return "".join(css)


def alert_qss(tokens):
    """Generate QCustomAlert QSS: a base card + a coloured left bar / icon /
    title per semantic variant (info / success / warning / destructive)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomAlert {\n"
               "    background-color: %s; border: 1px solid %s; border-radius: %s;\n"
               "}\n" % (r("surface"), r("outline"), px("radius.md")))
    css.append("QCustomAlert #alertTitle { font-weight: %d; background: transparent; }\n"
               % int(r("font.weight.semibold")))
    css.append("QCustomAlert #alertText { color: %s; background: transparent; }\n"
               % r("on-surface"))
    css.append("QCustomAlert #alertIcon { font-size: %s; background: transparent; }\n"
               % px("font.size.lg"))
    css.append("QCustomAlert #alertClose { background: transparent; border: none; color: %s; }\n"
               % r("outline"))
    css.append("QCustomAlert #alertClose:hover { color: %s; }\n" % r("on-surface"))
    for name in ("info", "success", "warning", "destructive"):
        css.append('QCustomAlert[variant="%s"] {'
                   ' border-color: %s; border-left: 4px solid %s; }\n'
                   % (name, r(name), r(name)))
        css.append('QCustomAlert[variant="%s"] #alertIcon { color: %s; }\n'
                   % (name, r(name)))
        css.append('QCustomAlert[variant="%s"] #alertTitle { color: %s; }\n'
                   % (name, r(name)))
    return "".join(css)


def statcard_qss(tokens):
    """Generate QCustomStatCard QSS (card + label/value/delta, trend colours)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomStatCard {\n"
               "    background-color: %s; border: 1px solid %s; border-radius: %s;\n"
               "}\n" % (r("surface"), r("outline"), px("radius.md")))
    css.append("QCustomStatCard #statLabel { color: %s; font-size: %s;"
               " background: transparent; }\n" % (r("outline"), px("font.size.sm")))
    css.append("QCustomStatCard #statValue { color: %s; font-size: %s;"
               " font-weight: %d; background: transparent; }\n"
               % (r("on-surface"), px("font.size.2xl"), int(r("font.weight.bold"))))
    css.append("QCustomStatCard #statCaption { color: %s; font-size: %s;"
               " background: transparent; }\n" % (r("outline"), px("font.size.sm")))
    css.append("QCustomStatCard #statDelta { font-size: %s; font-weight: %d;"
               " background: transparent; }\n"
               % (px("font.size.sm"), int(r("font.weight.medium"))))
    css.append('QCustomStatCard[trend="up"] #statDelta { color: %s; }\n' % r("success"))
    css.append('QCustomStatCard[trend="down"] #statDelta { color: %s; }\n' % r("destructive"))
    css.append('QCustomStatCard[trend="flat"] #statDelta { color: %s; }\n' % r("outline"))
    return "".join(css)


def progressring_qss(tokens):
    """Feed token colours to the painted QCustomProgressRing via qproperty."""
    r = tokens.role
    return ("QCustomProgressRing {\n"
            "    qproperty-ringColor: %s; qproperty-trackColor: %s;\n"
            "    qproperty-textColor: %s;\n"
            "}\n" % (r("accent"), r("surface-muted"), r("on-surface")))


def card_qss(tokens):
    """Generate QCustomCard QSS (surface panel + header title/subtitle)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomCard {\n"
               "    background-color: %s; border: 1px solid %s; border-radius: %s;\n"
               "}\n" % (r("surface"), r("outline"), px("radius.lg")))
    css.append("QCustomCard #cardTitle { color: %s; font-size: %s; font-weight: %d;"
               " background: transparent; }\n"
               % (r("on-surface"), px("font.size.lg"), int(r("font.weight.semibold"))))
    css.append("QCustomCard #cardSubtitle { color: %s; font-size: %s;"
               " background: transparent; }\n" % (r("outline"), px("font.size.sm")))
    css.append("QCustomCard #cardBody { background: transparent; }\n")
    return "".join(css)


def badge_qss(tokens):
    """Generate QCustomBadge QSS: a pill whose colour comes from the semantic
    `variant`, plus sizes and a dot mode."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomBadge {\n"
               "    border-radius: %s; padding: 1px %s;\n"
               "    font-weight: %d; font-size: %s;\n"
               "}\n" % (px("radius.full"), px("space.2"),
                        int(r("font.weight.medium")), px("font.size.sm")))
    fills = {"default": ("surface-muted", "on-surface"),
             "primary": ("primary", "on-primary"),
             "secondary": ("secondary", "on-secondary"),
             "success": ("success", "on-success"),
             "warning": ("warning", "on-warning"),
             "destructive": ("destructive", "on-destructive"),
             "info": ("info", "on-info")}
    for name, (bg, fg) in fills.items():
        css.append('QCustomBadge[variant="%s"] { background-color: %s; color: %s; }\n'
                   % (name, r(bg), r(fg)))
    css.append('QCustomBadge[variant="outline"] {'
               ' background-color: transparent; color: %s; border: 1px solid %s; }\n'
               % (r("on-surface"), r("outline")))
    # sizes
    css.append('QCustomBadge[sizeVariant="sm"] { padding: 0 %s; font-size: %s; }\n'
               % (px("space.1"), px("font.size.sm")))
    css.append('QCustomBadge[sizeVariant="lg"] { padding: 2px %s; font-size: %s; }\n'
               % (px("space.2"), px("font.size.md")))
    # dot mode: no padding (size is fixed in code)
    css.append('QCustomBadge[dot="true"] { padding: 0; min-width: 0; }\n')
    return "".join(css)


def kbd_qss(tokens):
    """Generate QCustomKbd QSS: small keycaps + '+' separators."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomKbd #kbdKey {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s; padding: 1px %s; min-width: %s;\n"
               "    font-family: monospace; font-size: %s; font-weight: %d;\n"
               "}\n" % (r("surface-muted"), r("on-surface"), r("outline"),
                        px("radius.sm"), px("space.2"), px("space.3"),
                        px("font.size.sm"), int(r("font.weight.medium"))))
    css.append("QCustomKbd #kbdPlus { color: %s; background: transparent;"
               " font-size: %s; }\n" % (r("outline"), px("font.size.sm")))
    return "".join(css)


def splitter_qss(tokens):
    """Generate QCustomSplitter QSS: a subtle handle that accents on hover."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomSplitter::handle { background-color: %s;"
               " border-radius: %s; }\n" % (r("surface-muted"), px("radius.sm")))
    css.append("QCustomSplitter::handle:hover { background-color: %s; }\n"
               % r("accent"))
    css.append("QCustomSplitter::handle:pressed { background-color: %s; }\n"
               % r("accent"))
    return "".join(css)


def carousel_qss(tokens):
    """Generate QCustomCarousel QSS: nav buttons + dot indicators (active dot
    uses the accent). The dot radius is a concrete half-size (not radius.full,
    which Qt renders square instead of a circle)."""
    r = tokens.role
    px = tokens.px
    css = []
    css.append("QCustomCarousel #carouselNav {\n"
               "    background-color: %s; color: %s; border: 1px solid %s;\n"
               "    border-radius: %s; font-size: %s; font-weight: %d;\n"
               "}\n" % (r("surface"), r("on-surface"), r("outline"),
                        px("radius.md"), px("font.size.lg"),
                        int(r("font.weight.semibold"))))
    css.append("QCustomCarousel #carouselNav:hover { background-color: %s; }\n"
               % r("surface-muted"))
    css.append("QCustomCarousel #carouselNav:disabled { color: %s; }\n"
               % r("outline"))
    css.append("QCustomCarousel #carouselDot { background-color: %s;"
               " border: none; border-radius: 5px; }\n" % r("outline"))
    css.append('QCustomCarousel #carouselDot[active="true"] {'
               " background-color: %s; }\n" % r("accent"))
    return "".join(css)


def build_component_qss(tokens):
    """All token-driven component QSS. Extend as more widgets adopt tokens."""
    return (button_qss(tokens) + datatable_qss(tokens) + toast_qss(tokens)
            + combobox_qss(tokens) + datetime_qss(tokens)
            + commandpalette_qss(tokens) + tabs_qss(tokens) + accordion_qss(tokens)
            + tree_qss(tokens) + drawer_qss(tokens) + stepper_qss(tokens)
            + richtext_qss(tokens) + colorpicker_qss(tokens)
            + breadcrumbs_qss(tokens) + rating_qss(tokens) + chip_qss(tokens)
            + skeleton_qss(tokens) + avatargroup_qss(tokens) + timeline_qss(tokens)
            + pagination_qss(tokens) + popover_qss(tokens) + segmented_qss(tokens)
            + emptystate_qss(tokens) + dropzone_qss(tokens) + tagedit_qss(tokens)
            + chat_qss(tokens)
            + rangeslider_qss(tokens)
            + switch_qss(tokens) + radio_qss(tokens) + radiogroup_qss(tokens)
            + candlestick_qss(tokens) + radar_qss(tokens)
            + scatter_qss(tokens) + funnel_qss(tokens)
            + rangebar_qss(tokens) + radialbars_qss(tokens)
            + sankey_qss(tokens) + chrome_qss(tokens)
            + motion_qss(tokens)
            + textarea_qss(tokens)
            + verificationcode_qss(tokens) + multiselect_qss(tokens)
            + imagepicker_qss(tokens) + gradientpicker_qss(tokens)
            + number_qss(tokens) + alert_qss(tokens)
            + statcard_qss(tokens) + progressring_qss(tokens) + card_qss(tokens)
            + badge_qss(tokens) + kbd_qss(tokens) + splitter_qss(tokens)
            + carousel_qss(tokens))


_MARK_START = "/* >>> custom-widgets design tokens >>> */"
_MARK_END = "/* <<< custom-widgets design tokens <<< */"
_MARK_RE = re.compile(re.escape(_MARK_START) + ".*?" + re.escape(_MARK_END), re.DOTALL)


########################################################################
## SCSS engine integration - expose token() to SCSS/QtSASS
########################################################################
def _token_string(tokens, name):
    """QSS-ready string for a token name: colours as hex, font weights
    unitless, other numerics (space/radius/size) as px."""
    val = tokens.role(name)
    if isinstance(val, str):        # colour hex
        return val
    if "weight" in name:
        return str(int(val))
    return "%dpx" % int(val)


def sass_functions(tokens):
    """qtsass/libsass custom functions exposing ``token()`` to SCSS.

    In SCSS:  background-color: token('primary');  padding: token('space.2');
    qtsass keys custom functions by ``fn.__name__``, so the callable must be
    named ``token``.
    """
    def token(name):
        raw = getattr(name, "value", name)      # SassString -> its .value
        return _token_string(tokens, str(raw))
    return [token]


_IMPORT_RE = re.compile(r"""@import\s+['"]([^'"]+)['"]""")


def _resolve_scss_import(name, base_dir, include_paths):
    """Resolve a single ``@import '<name>'`` the way libsass does: to
    ``<name>.scss`` or the ``_<name>.scss`` partial, searched under the
    importing file's directory then the include paths. Returns the absolute
    path, or ``None`` when nothing matches."""
    stem = name[:-5] if name.lower().endswith(".scss") else name
    head, tail = os.path.split(stem)
    for root in [base_dir, *include_paths]:
        for cand in (os.path.join(root, head, tail + ".scss"),
                     os.path.join(root, head, "_" + tail + ".scss")):
            if os.path.isfile(cand):
                return os.path.normpath(cand)
    return None


def find_unresolved_imports(root_file, include_paths=()):
    """Walk the ``@import`` graph from ``root_file`` and return a list of
    ``(importing_file, import_name)`` for every import that resolves to no
    file on disk.

    A dangling ``@import`` (e.g. a leftover ``@import 'custom'`` after the
    partial was deleted) makes qtsass/libsass fail with an OPAQUE error
    (``CompileError``/``TypeError: expected str ... not NoneType``). Call this
    to turn that into an actionable message naming the file and the missing
    import. Pure/Qt-free so it is unit-testable.
    """
    include_paths = [os.path.abspath(p) for p in include_paths]
    problems, visited = [], set()

    def walk(path):
        path = os.path.normpath(os.path.abspath(path))
        if path in visited or not os.path.isfile(path):
            return
        visited.add(path)
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                src = f.read()
        except OSError:
            return
        base_dir = os.path.dirname(path)
        for name in _IMPORT_RE.findall(src):
            # CSS / URL imports are passed through to Qt untouched, not resolved.
            if name.lower().endswith(".css") or \
                    name.startswith(("http://", "https://", "url(")):
                continue
            resolved = _resolve_scss_import(name, base_dir, include_paths)
            if resolved is None:
                problems.append((path, name))
            else:
                walk(resolved)

    walk(root_file)
    return problems


def describe_scss_compile_error(root_file, include_paths=(), original=None):
    """Return a clear, single-line diagnosis for a failed SCSS compile of
    ``root_file``, or ``None`` when no unresolved import explains it (so the
    caller can fall back to the raw error). Names the importing file and the
    missing partial so the fix is obvious."""
    try:
        problems = find_unresolved_imports(root_file, include_paths)
    except Exception:
        return None
    if not problems:
        return None
    importer, name = problems[0]
    extra = f" (+{len(problems) - 1} more)" if len(problems) > 1 else ""
    return (f"SCSS @import '{name}' in {os.path.basename(importer)} could not "
            f"be resolved{extra} - expected '{name}.scss' or '_{name}.scss' in "
            f"the scss folder / include paths. Create the file or remove the "
            f"@import.")


def compile_scss(source, tokens=None, theme="light", is_filename=False,
                 output_file=None, **kwargs):
    """Compile QtSASS/SCSS with the ``token()`` function registered.

    source       SCSS string, or a file path when is_filename=True.
    tokens/theme DesignTokens to expose (or a theme name to build one).
    Returns the compiled QSS string.
    """
    import qtsass
    if tokens is None:
        tokens = DesignTokens(theme=theme)
    fns = list(kwargs.pop("custom_functions", [])) + sass_functions(tokens)
    if is_filename:
        return qtsass.compile_filename(source, output_file,
                                       custom_functions=fns, **kwargs)
    return qtsass.compile(source, custom_functions=fns, **kwargs)


def scss_tokens_partial(tokens):
    """A SCSS partial exposing semantic roles as a map + ``token()`` function
    and as ``$role`` variables. For editors and compilers without custom-
    function support; the runtime path uses the Python token() above."""
    lines = ["// AUTO-GENERATED from Custom_Widgets design tokens - do not edit.",
             "$__design_tokens: ("]
    for name in sorted(tokens._semantic.keys()):
        lines.append('    "%s": %s,' % (name, _token_string(tokens, name)))
    lines.append(");")
    lines.append("@function token($name) { @return map-get($__design_tokens, $name); }")
    for name in sorted(tokens._semantic.keys()):
        lines.append("$%s: %s;" % (name.replace("-", "_"), _token_string(tokens, name)))
    return "\n".join(lines) + "\n"


#: The token set most recently handed to applyDesignTokens, or None if the
#: application does not use the token system at all. Widgets that cannot style
#: themselves through QSS — anything painting into a QGraphicsScene, such as
#: the QtCharts family — need to read the roles directly, and otherwise have no
#: way to find out which theme is live.
_activeTokens = None


def activeDesignTokens():
    """The DesignTokens currently applied, or None if none ever were.

    Prefer QSS and the semantic roles. This exists for the cases QSS cannot
    reach; treat None as "the app is not token-themed" and fall back rather
    than assuming a default, or you will force light onto a dark app.
    """
    return _activeTokens


def applyDesignTokens(target, tokens=None, theme="light"):
    """Generate token QSS and apply it to a QApplication or widget.

    Idempotent: the token block is delimited by markers and replaced in place,
    so calling this again (e.g. on a light/dark switch) never accumulates.
    Returns the DesignTokens used.
    """
    global _activeTokens
    if tokens is None:
        tokens = DesignTokens(theme=theme)
    block = _MARK_START + "\n" + build_component_qss(tokens) + "\n" + _MARK_END
    existing = target.styleSheet() or ""
    if _MARK_RE.search(existing):
        new = _MARK_RE.sub(lambda _m: block, existing)
    else:
        new = (existing + "\n" + block) if existing else block
    target.setStyleSheet(new)
    _activeTokens = tokens
    return tokens
