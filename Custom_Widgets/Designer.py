#!/usr/bin/env python3
import sys
import os
import subprocess
import pathlib

import qtpy
from qtpy.QtCore import QProcess, QProcessEnvironment
from qtpy.QtWidgets import QApplication

import Custom_Widgets

def start_designer(load_plugins: bool = False, process_mode: str = "normal"):
    """Launch Qt Designer from the current venv.

    Designer integration (custom-widget plugins, bridge, tool docks) is
    PySide6-only: the Python plugin loader (PYSIDE_DESIGNER_PLUGINS /
    QPyDesignerCustomWidgetCollection) exists only in PySide6, and PyQt
    wheels do not ship a designer binary at all. Use PyQt6 for widgets and
    ui conversion; design forms with pyside6-designer."""

    qt_lib = qtpy.API_NAME

    if qt_lib != "PySide6":
        sys.exit(
            f" Qt Designer integration requires PySide6 (current binding: "
            f"{qt_lib}).\n"
            " PyQt6 is supported for widgets and ui conversion, but Designer\n"
            " plugins are a PySide6-only feature - install PySide6 and rerun.")

    possible_paths = [
        pathlib.Path(sys.prefix)
        / ("Scripts" if sys.platform.startswith("win") else "bin")
        / "pyside6-designer"
    ]
    designer_cmd = "pyside6-designer"

    try:
        import PySide6
        pyside6_dir = pathlib.Path(PySide6.__file__).parent
        exe = "designer.exe" if sys.platform.startswith("win") else "designer"
        possible_paths.append(pyside6_dir / exe)
        possible_paths.append(pyside6_dir / "Qt" / "bin" / exe)
        qt_plugins_base = pyside6_dir / "designer" / "plugins"
    except ImportError:
        sys.exit(" PySide6 not found in current venv.")

    # Find designer executable
    designer_exe = None
    for path in possible_paths:
        if path.exists():
            designer_exe = path
            print(f" Found designer at: {designer_exe}")
            break
    
    if not designer_exe and process_mode == "normal":
        paths_str = "\n  ".join(str(p) for p in possible_paths)
        sys.exit(f" Designer executable not found in any of these locations:\n  {paths_str}")

    # --- Setup environment variables ---
    env = os.environ.copy()

    # Add Custom_Widgets path to PYTHONPATH, plus THIS interpreter's
    # site-packages: Designer's embedded Python only inherits the venv's
    # packages when VIRTUAL_ENV is set (activated shell) - launched from a
    # script/IDE without activation, qtpy and friends would be missing.
    import sysconfig
    custom_widgets_dir = pathlib.Path(Custom_Widgets.__file__).parent
    python_path = [str(custom_widgets_dir.parent),
                   sysconfig.get_paths().get("purelib", "")]
    if env.get("PYTHONPATH"):
        python_path.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(p for p in python_path if p)

    # Pin qtpy to the binding this Designer belongs to. Without this, with
    # several bindings installed qtpy may resolve to a different one (e.g.
    # PyQt5) inside Designer's embedded interpreter and every plugin import
    # crashes (pyqtProperty(notify=None) TypeError).
    env["QT_API"] = qt_lib.lower()

    # Pin the project root to the folder this command was CALLED from, for
    # the whole Designer session. Everything inside Designer (UI Workspace,
    # bridge socket name, theme/icon paths) resolves via projectRoot(),
    # whose cwd fallback breaks the moment anything chdirs the Designer
    # process (its own file dialogs can) - the env var can't be moved.
    env["CUSTOM_WIDGETS_PROJECT_ROOT"] = os.getcwd()

    # Build plugins paths
    plugins_paths = []
    if qt_plugins_base and qt_plugins_base.exists():
        plugins_paths.append(str(qt_plugins_base))
    
    # Add Custom_Widgets Plugins folder if requested
    if load_plugins:
        plugins_dir = custom_widgets_dir / "Plugins"
        print(f"Plugins dir: {plugins_dir}")
        if plugins_dir.exists():
            plugins_paths.append(str(plugins_dir))
            print(f" Found Custom_Widgets plugins at: {plugins_dir}")
        else:
            print(f" Plugins directory not found: {plugins_dir}")
    
    # CRITICAL: Set PYSIDE_DESIGNER_PLUGINS for Windows
    if plugins_paths:
        plugins_env = os.pathsep.join(plugins_paths)
        env["PYSIDE_DESIGNER_PLUGINS"] = plugins_env
        print(f" PYSIDE_DESIGNER_PLUGINS set to: {plugins_env}")
    else:
        print(" No plugin paths found - custom widgets may not appear")

    # --- Launch Designer based on process mode ---
    if process_mode == "qprocess":
        # Use QProcess mode (better for Windows)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        qenv = QProcessEnvironment.systemEnvironment()
        
        # Set all environment variables for QProcess
        for key, value in env.items():
            qenv.insert(key, value)
        
        designer_process = QProcess()
        designer_process.setProcessEnvironment(qenv)
        designer_process.setWorkingDirectory(os.getcwd())
        designer_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
        
        print(f" Launching Qt Designer using QProcess: {designer_cmd}")
        
        # Always prefer the resolved executable - the bare command name on
        # PATH can belong to a different Python installation entirely.
        if designer_exe:
            designer_process.start(str(designer_exe), [])
        else:
            designer_process.start(designer_cmd, [])
        
        if not designer_process.waitForStarted(30000):
            error_string = designer_process.errorString()
            print(f" Designer process failed to start: {error_string}")
            sys.exit(1)
        
        print(" Qt Designer started successfully")
        designer_process.waitForFinished(-1)
        sys.exit(designer_process.exitCode())
        
    else:
        # Use normal subprocess mode
        print(f" Launching Qt Designer using subprocess from: {designer_exe}")
        
        # On Windows, environment variables need to be passed explicitly
        if sys.platform.startswith("win"):
            # Windows-specific: Use shell=True for better environment handling
            result = subprocess.run(
                [str(designer_exe)], 
                cwd=os.getcwd(), 
                env=env,
                shell=True  # Helps with Windows path resolution
            )
        else:
            subprocess.run([str(designer_exe)], cwd=os.getcwd(), env=env)