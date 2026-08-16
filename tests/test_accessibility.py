"""Screen-reader surface for the custom-painted interactive widgets.

Qt gives QAbstractButton / QSlider subclasses roles and state for free, but
these widgets subclass plain QWidget and paint their own chrome, so without an
accessible name a screen reader announces them as an anonymous pane. Every one
must expose a meaningful name (its text, tooltip, or a sensible default).
Qt 6.4+ removed setAccessibleRole, so roles are only asserted on bindings that
still support them; the names are the portable guarantee.
"""
from qtpy.QtGui import QAccessible

ROLE = {
    "QCustomSwitch": "CheckBox",
    "QCustomRadioButton": "RadioButton",
    "QCustomRating": "Slider",
    "QCustomRangeSlider": "Slider",
    "QCustomSegmentedControl": "Grouping",
    "QCustomButtonGroup": "Grouping",
    "QCustomSocialButton": "Button",
    "QCustomRainbowButton": "Button",
    "QCustomCopyButton": "Button",
    "QCustomPagination": "Grouping",
    "QCustomBreadcrumbs": "Grouping",
    "QCustomCoverFlow": "List",
}

_MODULES = {
    "QCustomSwitch": "QCustomSwitch",
    "QCustomRadioButton": "QCustomRadioButton",
    "QCustomRating": "QCustomRating",
    "QCustomRangeSlider": "QCustomRangeSlider",
    "QCustomSegmentedControl": "QCustomSegmentedControl",
    "QCustomButtonGroup": "QCustomButtonGroup",
    "QCustomSocialButton": "QCustomSocialButton",
    "QCustomRainbowButton": "QCustomRainbowButton",
    "QCustomCopyButton": "QCustomCopyButton",
    "QCustomPagination": "QCustomPagination",
    "QCustomBreadcrumbs": "QCustomBreadcrumbs",
    "QCustomCoverFlow": "QCustomCoverFlow",
}


def _role_int(name):
    return int(getattr(QAccessible, name))


def _classes():
    import importlib
    out = {}
    for cls, mod in _MODULES.items():
        out[cls] = getattr(importlib.import_module("Custom_Widgets." + mod), cls)
    return out


def test_interactive_widgets_expose_an_accessible_name(qapp):
    classes = _classes()
    kwargs = {"QCustomRadioButton": {"text": "Choice A"}}
    for name in ROLE:
        widget = classes[name](**kwargs.get(name, {}))
        # Every interactive widget gets a name: its text, its tooltip, or a
        # sensible default. A blank name means an anonymous pane to AT.
        assert widget.accessibleName(), "%s should have an accessible name" % name
        widget.deleteLater()


def test_roles_when_binding_supports_them(qapp):
    classes = _classes()
    if not hasattr(classes["QCustomSwitch"], "setAccessibleRole"):
        return  # Qt 6.4+ removed the role setter — names are the guarantee
    kwargs = {"QCustomRadioButton": {"text": "Choice A"}}
    for name, role in ROLE.items():
        widget = classes[name](**kwargs.get(name, {}))
        assert int(widget.accessibleRole()) == _role_int(role), (
            "%s should be announced as %s" % (name, role))
        widget.deleteLater()


def test_buttons_carry_their_text_as_accessible_name(qapp):
    classes = _classes()
    assert classes["QCustomSocialButton"](text="Sign in with GitHub").accessibleName() == "Sign in with GitHub"
    assert classes["QCustomRainbowButton"](text="Launch").accessibleName() == "Launch"
    assert classes["QCustomCopyButton"](text="Copy").accessibleName() == "Copy"


def test_toggle_and_selection_widgets_have_fallback_names(qapp):
    classes = _classes()
    assert classes["QCustomSwitch"]().accessibleName() == "Toggle switch"
    assert classes["QCustomRating"]().accessibleName() == "Rating"
    assert classes["QCustomRangeSlider"]().accessibleName() == "Range slider"
    assert classes["QCustomPagination"]().accessibleName() == "Pagination"
    assert classes["QCustomBreadcrumbs"]().accessibleName() == "Breadcrumbs"
    assert classes["QCustomCoverFlow"]().accessibleName() == "Cover flow"


def test_group_widgets_expose_names(qapp):
    classes = _classes()
    assert classes["QCustomSegmentedControl"]().accessibleName() == "Segmented control"
    assert classes["QCustomButtonGroup"]().accessibleName() == "Button group"