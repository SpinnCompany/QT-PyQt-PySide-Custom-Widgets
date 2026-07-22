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
    },
    "space": {"1": 4, "2": 8, "3": 12, "4": 16, "6": 24},
    "radius": {"sm": 4, "md": 8, "lg": 12, "full": 9999},
    "font": {
        "size": {"sm": 13, "md": 14, "lg": 16},
        "weight": {"regular": 400, "medium": 500, "semibold": 600},
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


def build_component_qss(tokens):
    """All token-driven component QSS. Extend as more widgets adopt tokens."""
    return button_qss(tokens) + datatable_qss(tokens)


_MARK_START = "/* >>> custom-widgets design tokens >>> */"
_MARK_END = "/* <<< custom-widgets design tokens <<< */"
_MARK_RE = re.compile(re.escape(_MARK_START) + ".*?" + re.escape(_MARK_END), re.DOTALL)


def applyDesignTokens(target, tokens=None, theme="light"):
    """Generate token QSS and apply it to a QApplication or widget.

    Idempotent: the token block is delimited by markers and replaced in place,
    so calling this again (e.g. on a light/dark switch) never accumulates.
    Returns the DesignTokens used.
    """
    if tokens is None:
        tokens = DesignTokens(theme=theme)
    block = _MARK_START + "\n" + build_component_qss(tokens) + "\n" + _MARK_END
    existing = target.styleSheet() or ""
    if _MARK_RE.search(existing):
        new = _MARK_RE.sub(lambda _m: block, existing)
    else:
        new = (existing + "\n" + block) if existing else block
    target.setStyleSheet(new)
    return tokens
