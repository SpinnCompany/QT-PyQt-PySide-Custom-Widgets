########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################
"""QCustomBeeswarm — a Custom Widgets **Pro** widget.

The implementation ships compiled in the `QT-PyQt-PySide-Custom-Widgets-Pro`
wheel, not in this GPLv3 package. This stub stays here on purpose: the import
path `Custom_Widgets.QCustomBeeswarm` is baked into every Qt Designer .ui file that uses
the widget, so removing the module outright would fail at .ui load time with an
error pointing at the form instead of at the missing licence.

With Pro installed every public name is re-exported transparently and existing
code keeps working unchanged. Without it, asking for one raises a message that
says what to do.
"""
_PRO_MODULE = "custom_widgets_pro.widgets.charts.QCustomBeeswarm"

_MESSAGE = (
    "QCustomBeeswarm is part of Custom Widgets Pro and is not included in the free "
    "GPLv3 package.\n"
    "Pro is licensed software and is NOT installable from PyPI - the name\n"
    "there is only a pointer. Licence holders download the wheel:\n"
    "    https://portal.customwidgets.org/downloads\n"
    "    pip install <the downloaded .whl>\n"
    "Plans and licence: https://customwidgets.org/pricing/"
)


def __getattr__(name):
    # PEP 562. Forward EVERY public name, not just the headline class: these
    # modules also export helpers (QCustomSyntaxHighlighter, delegates, enums)
    # that callers and tests import directly. Resolving lazily keeps a bare
    # `import` working, which Qt Designer and the widget scanner both rely on.
    if name.startswith("__"):
        raise AttributeError(name)
    try:
        import importlib
        return getattr(importlib.import_module(_PRO_MODULE), name)
    except ImportError as exc:
        raise ImportError(_MESSAGE) from exc
    except AttributeError:
        raise AttributeError(
            "%r is not exported by %s" % (name, _PRO_MODULE))


__all__ = ["QCustomBeeswarm"]
