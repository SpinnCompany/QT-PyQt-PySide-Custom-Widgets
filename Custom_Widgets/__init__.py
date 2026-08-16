## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
import os
import sys
import __main__
import importlib

# Must run before anything below imports a widget by its flat name. The widget
# implementations now live in subpackages, but Custom_Widgets.<Module> stays
# published API — it is baked into every Designer-authored .ui file as
# <header>Custom_Widgets.QCustomX</header>. See _legacy_paths.py.
from Custom_Widgets import _legacy_paths as _legacy_paths
_legacy_paths.install()

# The package root deliberately does NOT import the Qt/widget stack eagerly.
# `import Custom_Widgets` is the cheapest thing tools (design linter, stubgen,
# docs generators) need — dragging in qtsass + every widget here cost ~1.1s
# and required the full Qt GUI libraries even when all you wanted was to parse
# a file. Every public name is resolved lazily by __getattr__ (PEP 562); the
# heavy imports happen on first use. `from Custom_Widgets import *` still
# works because __all__ lists them and the star-import machinery calls
# getattr() for each name.
from Custom_Widgets.Log import *
from Custom_Widgets.Project import projectRoot, setProjectRoot  # noqa: E402
script_dir = projectRoot().replace("\\", "/")

_LAZY_EXPORTS = {
    "QCustomMainWindow": ("Custom_Widgets.QCustomMainWindow", "QCustomMainWindow"),
    "loadJsonStyle": ("Custom_Widgets.JSonStyles", "loadJsonStyle"),
    "enable_hot_reload": ("Custom_Widgets.HotReload", "enable_hot_reload"),
    "QCustomTheme": ("Custom_Widgets.QCustomTheme", "QCustomTheme"),
    "is_in_designer": ("Custom_Widgets.Utils", "is_in_designer"),
    "SharedData": ("Custom_Widgets.Utils", "SharedData"),
    "recolor_icon": ("Custom_Widgets.Utils", "recolor_icon"),
    "themed_icon": ("Custom_Widgets.Utils", "themed_icon"),
    "resolve_icon_path": ("Custom_Widgets.Utils", "resolve_icon_path"),
    "set_state": ("Custom_Widgets.Utils", "set_state"),
    "load_image": ("Custom_Widgets.ImageLoader", "load_image"),
    "rounded_pixmap": ("Custom_Widgets.ImageLoader", "rounded_pixmap"),
    "ImageLoader": ("Custom_Widgets.ImageLoader", "ImageLoader"),
    "QCustomComponentLoader": ("Custom_Widgets.QCustomComponentLoader",
                               "QCustomComponentLoader"),
    "QCustomHamburgerMenu": ("Custom_Widgets.QCustomHamburgerMenu",
                             "QCustomHamburgerMenu"),
    "QSsFileMonitor": ("Custom_Widgets.FileMonitor", "QSsFileMonitor"),
}


def __getattr__(name):
    """Resolve a public name on demand so the package root stays import-light."""
    mapping = _LAZY_EXPORTS.get(name)
    if mapping is None:
        raise AttributeError(
            f"module 'Custom_Widgets' has no attribute {name!r}")
    module_name, attr = mapping
    import importlib
    module = importlib.import_module(module_name)
    value = getattr(module, attr)
    globals()[name] = value
    return value


import types  # noqa: E402


class _LazyRootModule(types.ModuleType):
    """Stop the import machinery from clobbering a lazily-exported name with
    the submodule object. ``import Custom_Widgets.QCustomTheme`` (or the legacy
    alias ``Custom_Widgets.QCustomTheme``) makes importlib run
    ``setattr(Custom_Widgets, 'QCustomTheme', <module>)`` as the import
    finishes. The published API value is the CLASS/function the module holds,
    so any such set is redirected to the intended value instead. Without this,
    ``from Custom_Widgets import *`` hands callers the module - ``'module'
    object is not callable``."""

    def __setattr__(self, name, value):
        if name in _LAZY_EXPORTS and isinstance(value, types.ModuleType):
            mapping = _LAZY_EXPORTS[name]
            module = importlib.import_module(mapping[0])
            value = getattr(module, mapping[1])
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _LazyRootModule


__all__ = [n for n in globals() if not n.startswith("_")]
__all__ += list(_LAZY_EXPORTS)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_EXPORTS))
