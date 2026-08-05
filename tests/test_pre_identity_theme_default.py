"""Regression: pre-identity QSettings neutralized Default-Theme machine-wide.

configure_settings used to read QSettings() while parsing CustomThemes, BEFORE
the app's org/app names were set — resolving the shared fallback store
(~/.config/Unknown Organization/main.py.conf). Any stale THEME there stripped
the Default-Theme flag from every other app's first run, and currentTheme then
fell back to whichever theme was literally named "Light".
"""
import types

from qtpy.QtCore import QCoreApplication, QSettings


def _redirect_qsettings(tmp_path, monkeypatch):
    """Route every QSettings() in the process into tmp_path for this test."""
    previous_format = QSettings.defaultFormat()
    QSettings.setDefaultFormat(QSettings.IniFormat)
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, str(tmp_path))
    monkeypatch.setattr(QSettings, "defaultFormat",
                        staticmethod(lambda: QSettings.IniFormat), raising=False)
    return previous_format


def test_foreign_pre_identity_theme_does_not_kill_default(qapp, theme, tmp_path,
                                                          monkeypatch):
    from Custom_Widgets.JSonStyles import configure_settings

    previous_format = _redirect_qsettings(tmp_path, monkeypatch)
    saved_identity = (QCoreApplication.organizationName(),
                      QCoreApplication.applicationName(),
                      QCoreApplication.organizationDomain())
    saved_defaults = [(t, getattr(t, "defaultTheme", False)) for t in theme.themes]
    try:
        # 1. Simulate the polluted shared pre-identity store.
        QCoreApplication.setOrganizationName("Unknown Organization")
        QCoreApplication.setApplicationName("main.py")
        polluted = QSettings()
        polluted.setValue("THEME", "Glass Dusk")  # some OTHER app's theme
        polluted.sync()
        del polluted

        # 2. Parse a style.json equivalent declaring its own identity and a
        #    dark Default-Theme. Before the fix, the foreign THEME above
        #    stripped the default flag during this call.
        host = types.SimpleNamespace(themeEngine=theme)
        configure_settings(host, {
            "QSettings": {
                "AppSettings": {
                    "OrganizationName": "CustomWidgetsTests",
                    "ApplicationName": "PreIdentityRegression",
                },
                "ThemeSettings": {
                    "CustomThemes": [
                        {"Theme-name": "RegDark2026", "Background-color": "#10131a",
                         "Text-color": "#e6e9ef", "Accent-color": "#7ab3f0",
                         "Icons-color": "#9ca3af", "Default-Theme": True,
                         "Create-icons": False},
                        {"Theme-name": "RegLight2026", "Background-color": "#f5f6f8",
                         "Text-color": "#1a1d24", "Accent-color": "#2f6fce",
                         "Icons-color": "#5b6270", "Create-icons": False},
                    ],
                },
            },
        })

        # Fix 1: parsing applied the app's own identity before reading settings.
        assert QCoreApplication.organizationName() == "CustomWidgetsTests"
        assert QCoreApplication.applicationName() == "PreIdentityRegression"

        # Fix 2: the foreign THEME did not neutralize the declared default.
        regDark = next(t for t in theme.themes if t.name == "RegDark2026")
        assert regDark.defaultTheme is True

        # Fix 3: with a stored THEME naming no registered theme, currentTheme
        # resolves to the declared default — not a theme named "Light".
        for t, _ in saved_defaults:
            t.defaultTheme = False
        own = QSettings()
        own.setValue("THEME", "GhostTheme")
        own.sync()
        theme._theme = "GhostTheme"
        assert theme.currentTheme is regDark
    finally:
        for t, flag in saved_defaults:
            t.defaultTheme = flag
        # Remove this test's themes from the session-singleton engine — a
        # leftover defaultTheme=True entry changes currentTheme for every
        # later test (it broke the icon-generation suite once).
        theme._themes[:] = [t for t in theme._themes
                            if t.name not in ("RegDark2026", "RegLight2026")]
        QCoreApplication.setOrganizationName(saved_identity[0])
        QCoreApplication.setApplicationName(saved_identity[1])
        QCoreApplication.setOrganizationDomain(saved_identity[2])
        QSettings.setDefaultFormat(previous_format)
