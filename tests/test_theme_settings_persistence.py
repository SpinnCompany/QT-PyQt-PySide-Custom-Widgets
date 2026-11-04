"""Regressions for unreadable QSettings values and serializable theme lists."""
import importlib
import types

from qtpy.QtCore import QCoreApplication


def test_configure_settings_recovers_from_unreadable_theme(qapp, theme,
                                                           monkeypatch):
    styles = importlib.import_module("Custom_Widgets.JSonStyles")
    saved_identity = (QCoreApplication.organizationName(),
                      QCoreApplication.applicationName(),
                      QCoreApplication.organizationDomain())
    saved_themes = list(theme.themes)

    class BrokenSettings:
        def value(self, key):
            if key == "THEME":
                raise RuntimeError("invalid saved value")
            return None

    monkeypatch.setattr(styles, "QSettings", BrokenSettings)
    try:
        styles.configure_settings(types.SimpleNamespace(themeEngine=theme), {
            "QSettings": {
                "AppSettings": {
                    "OrganizationName": "CustomWidgetsTests",
                    "ApplicationName": "UnreadableThemeRegression",
                },
                "ThemeSettings": {
                    "CustomThemes": [{
                        "Theme-name": "UnreadableThemeRegression",
                        "Default-Theme": True,
                        "Create-icons": False,
                    }],
                },
            },
        })
        recovered = next(t for t in theme.themes
                         if t.name == "UnreadableThemeRegression")
        assert recovered.defaultTheme is True
    finally:
        theme._themes[:] = saved_themes
        QCoreApplication.setOrganizationName(saved_identity[0])
        QCoreApplication.setApplicationName(saved_identity[1])
        QCoreApplication.setOrganizationDomain(saved_identity[2])


def test_qapp_settings_recovers_and_stores_theme_names(monkeypatch):
    settings_module = importlib.import_module("Custom_Widgets.tools.QAppSettings")
    writes = {}

    class BrokenSettings:
        def value(self, key):
            raise RuntimeError("invalid saved value")

        def setValue(self, key, value):
            writes[key] = value

    class Theme:
        name = "DefaultRegressionTheme"
        defaultTheme = True

    class ThemeEngine:
        organizationName = ""
        applicationName = ""
        organizationDomain = ""
        themes = [Theme()]

        def applyCompiledSass(self, **kwargs):
            pass

    monkeypatch.setattr(settings_module, "QSettings", BrokenSettings)
    settings_module.QAppSettings.updateAppSettings(
        types.SimpleNamespace(themeEngine=ThemeEngine()), reloadJson=False)

    assert writes["THEME"] == "DefaultRegressionTheme"
    assert writes["INIT-THEME-SET"] is True
    assert writes["THEMES-LIST"] == ["DefaultRegressionTheme"]
