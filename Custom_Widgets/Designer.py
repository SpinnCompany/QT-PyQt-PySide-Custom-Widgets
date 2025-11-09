#!/usr/bin/env python3
import sys
import os
import subprocess
import pathlib

import qtpy

def start_designer(load_plugins: bool = False):
    """Launch Qt Designer from current venv, auto-detecting PySide6/PySide2/PyQt6/PyQt5."""

    # --- Determine library and designer executable ---
    qt_lib = qtpy.API_NAME  # 'PySide6', 'PyQt6', 'PySide2', 'PyQt5'

    if qt_lib == "PySide6":
        designer_exe = pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside6-designer"
        try:
            import PySide6
            qt_plugins_base = pathlib.Path(PySide6.__file__).parent / "designer" / "plugins"
        except ImportError:
            sys.exit("❌ PySide6 not found in current venv.")

    elif qt_lib == "PySide2":
        designer_exe = pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside2-designer"
        try:
            import PySide2
            qt_plugins_base = pathlib.Path(PySide2.__file__).parent / "designer" / "plugins"
        except ImportError:
            sys.exit("❌ PySide2 not found in current venv.")

    elif qt_lib == "PyQt6":
        designer_exe = pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt6-designer"
        try:
            import PyQt6
            qt_plugins_base = None  # PyQt6 does not include internal Python Designer plugins
        except ImportError:
            sys.exit("❌ PyQt6 not found in current venv.")

    elif qt_lib == "PyQt5":
        designer_exe = pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt5-designer"
        try:
            import PyQt5
            qt_plugins_base = None  # PyQt5 does not include internal Python Designer plugins
        except ImportError:
            sys.exit("❌ PyQt5 not found in current venv.")

    else:
        sys.exit(f"❌ Unsupported Qt library: {qt_lib}")

    if not designer_exe.exists():
        sys.exit(f"❌ Designer executable not found: {designer_exe}")

    # --- Setup environment variables ---
    env = os.environ.copy()

    # Set internal plugins if available
    if qt_plugins_base and qt_plugins_base.exists():
        env["PYSIDE_DESIGNER_PLUGINS"] = str(qt_plugins_base)
    else:
        env["PYSIDE_DESIGNER_PLUGINS"] = ""

    # Add Custom_Widgets path to PYTHONPATH
    import Custom_Widgets
    env["PYTHONPATH"] = os.path.dirname(Custom_Widgets.__file__)

    # --- Add Custom_Widgets Plugins folder if requested ---
    if load_plugins:
        plugins_dir = pathlib.Path(Custom_Widgets.__file__).parent / "Plugins"
        if plugins_dir.exists():
            if env.get("PYSIDE_DESIGNER_PLUGINS"):
                env["PYSIDE_DESIGNER_PLUGINS"] += os.pathsep + str(plugins_dir)
            else:
                env["PYSIDE_DESIGNER_PLUGINS"] = str(plugins_dir)

    # --- Launch Designer from current working directory ---
    subprocess.run([str(designer_exe)], cwd=os.getcwd(), env=env)
