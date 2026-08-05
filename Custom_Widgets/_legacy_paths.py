########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## Keep the flat `Custom_Widgets.<Module>` import paths working after the
## package was regrouped into subpackages.
##
## `Custom_Widgets.QCustomRadioButton` is not merely where a file happens to
## live - it is published API in two places at once:
##
##   1. user code:  from Custom_Widgets.QCustomRadioButton import QCustomRadioButton
##   2. every .ui file Qt Designer has ever written for these widgets, which
##      bakes the module in as <header>Custom_Widgets.QCustomRadioButton</header>
##
## 213 .ui files in this repo alone do (2), and every user project with a
## Designer-authored form does the same. Moving the files without this layer
## would break all of them at load time, with an error pointing at the .ui file
## rather than at the rename that actually caused it.
##
## So the files move for maintainability and the old names keep resolving. The
## alias table is derived from the tree at import time rather than written out
## by hand, so it cannot drift out of step with a later move.
########################################################################
import importlib
import importlib.abc
import importlib.util
import os
import sys

PACKAGE = "Custom_Widgets"
_ROOT = os.path.dirname(os.path.abspath(__file__))

# Subpackages whose modules keep a flat alias at the top level. Anything not
# listed here is reachable only at its real path, which is what we want for
# genuinely internal groupings.
GROUPS = ("widgets", "tools", "designer", "theming")

# Whole packages that moved under widgets/. Unlike the flat aliases these are
# derived from an explicit table, because the old *package* name is itself
# published: .ui files carry headers like
#     <header>Custom_Widgets.QCustomCharts.QCustomAreaChart</header>
# and user code does `from Custom_Widgets.ProgressBars.X import X`, so the
# whole prefix has to keep resolving, not just the leaf module.
PACKAGE_ALIASES = {
    "Custom_Widgets.ProgressBars": "Custom_Widgets.widgets.progressbars",
    "Custom_Widgets.LoadingIndicators": "Custom_Widgets.widgets.loading",
    "Custom_Widgets.QCustomCharts": "Custom_Widgets.widgets.charts.qtcharts",
}


def build_aliases():
    """Map legacy flat name -> real dotted module path.

    Walks the tree; does not import anything, so this stays cheap at startup.
    """
    aliases = {}
    collisions = {}
    for group in GROUPS:
        base = os.path.join(_ROOT, group)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            rel = os.path.relpath(dirpath, _ROOT).replace(os.sep, ".")
            for filename in filenames:
                if not filename.endswith(".py") or filename == "__init__.py":
                    continue
                stem = filename[:-3]
                legacy = "%s.%s" % (PACKAGE, stem)
                real = "%s.%s.%s" % (PACKAGE, rel, stem)
                if legacy in aliases and aliases[legacy] != real:
                    collisions.setdefault(legacy, [aliases[legacy]]).append(real)
                    continue
                aliases[legacy] = real
    if collisions:
        # Two files with the same basename in different groups would make the
        # flat alias ambiguous. Fail loudly at import rather than silently
        # resolving to whichever the walk happened to reach first.
        detail = "; ".join("%s -> %s" % (k, " and ".join(v))
                           for k, v in sorted(collisions.items()))
        raise ImportError("ambiguous legacy module aliases: %s" % detail)
    return aliases


class _AliasLoader(importlib.abc.Loader):
    """Registers the real module under the legacy name.

    The obvious implementation - return the real module from create_module -
    is subtly wrong. importlib then calls _init_module_attrs(override=True) on
    whatever create_module hands back, which rewrites __name__, __spec__ and
    __package__ on the *real* module object to the alias's. Any relative
    import inside that package afterwards resolves against the wrong parent,
    so `from .X import Y` silently binds the submodule instead of the class
    it contains.

    Returning None lets importlib build a throwaway shim, and exec_module then
    swaps the real module into sys.modules. _load() re-reads sys.modules after
    exec_module, so callers get the real object with its own identity intact.
    """

    def __init__(self, real_name):
        self._real_name = real_name

    def create_module(self, spec):
        return None                      # default shim; never handed to callers

    def exec_module(self, module):
        real = importlib.import_module(self._real_name)
        sys.modules[module.__name__] = real


class LegacyPathFinder(importlib.abc.MetaPathFinder):
    """Resolves `Custom_Widgets.<Module>` to its new home."""

    def __init__(self, aliases, packages=None):
        self._aliases = aliases
        self._packages = dict(packages or {})

    def _packageAlias(self, fullname):
        """Rewrite an old package prefix, keeping the rest of the path."""
        for old, new in self._packages.items():
            if fullname == old:
                return new
            if fullname.startswith(old + "."):
                return new + fullname[len(old):]
        return None

    def find_spec(self, fullname, path=None, target=None):
        real = self._aliases.get(fullname) or self._packageAlias(fullname)
        if real is None:
            return None
        if fullname == real:                      # nothing to alias
            return None
        return importlib.util.spec_from_loader(fullname, _AliasLoader(real))


_installed = None


def install():
    """Install the finder once. Safe to call repeatedly."""
    global _installed
    if _installed is not None:
        return _installed
    finder = LegacyPathFinder(build_aliases(), PACKAGE_ALIASES)
    # Prepended, and it has to be. Once an aliased *package* resolves, its
    # __path__ is a real directory, so the stdlib PathFinder can find the
    # submodules underneath it and would import them a second time under the
    # legacy name - giving two module objects and two distinct classes for one
    # file, which quietly breaks isinstance across the two import paths.
    #
    # Prepending is safe because find_spec returns None for anything not in
    # the alias tables, and the tables only ever contain names that no longer
    # exist on disk at the top level.
    sys.meta_path.insert(0, finder)
    _installed = finder
    return finder
