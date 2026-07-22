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
    """Launch Qt Designer from current venv, auto-detecting PySide6/PySide2/PyQt6/PyQt5."""
    
    # --- Determine library and designer executable ---
    qt_lib = qtpy.API_NAME
    
    # Initialize variables
    qt_plugins_base = None
    possible_paths = []
    designer_cmd = None

    if qt_lib == "PySide6":
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside6-designer"
        )
        designer_cmd = "pyside6-designer"
        
        try:
            import PySide6
            pyside6_dir = pathlib.Path(PySide6.__file__).parent
            
            if sys.platform.startswith("win"):
                possible_paths.append(pyside6_dir / "designer.exe")
            else:
                possible_paths.append(pyside6_dir / "designer")
            
            if sys.platform.startswith("win"):
                possible_paths.append(pyside6_dir / "Qt" / "bin" / "designer.exe")
            else:
                possible_paths.append(pyside6_dir / "Qt" / "bin" / "designer")
            
            qt_plugins_base = pyside6_dir / "designer" / "plugins"
        except ImportError:
            sys.exit(" PySide6 not found in current venv.")

    elif qt_lib == "PySide2":
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside2-designer"
        )
        designer_cmd = "pyside2-designer"
        
        try:
            import PySide2
            pyside2_dir = pathlib.Path(PySide2.__file__).parent
            
            if sys.platform.startswith("win"):
                possible_paths.append(pyside2_dir / "designer.exe")
            else:
                possible_paths.append(pyside2_dir / "designer")
            
            qt_plugins_base = pyside2_dir / "designer" / "plugins"
        except ImportError:
            sys.exit(" PySide2 not found in current venv.")

    elif qt_lib == "PyQt6":
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt6-designer"
        )
        designer_cmd = "pyqt6-designer"
        
        try:
            import PyQt6
            pyqt6_dir = pathlib.Path(PyQt6.__file__).parent
            
            if sys.platform.startswith("win"):
                possible_paths.append(pyqt6_dir / "designer.exe")
            else:
                possible_paths.append(pyqt6_dir / "designer")
            
            qt_plugins_base = None
        except ImportError:
            sys.exit(" PyQt6 not found in current venv.")

    elif qt_lib == "PyQt5":
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt5-designer"
        )
        designer_cmd = "pyqt5-designer"
        
        try:
            import PyQt5
            pyqt5_dir = pathlib.Path(PyQt5.__file__).parent
            
            if sys.platform.startswith("win"):
                possible_paths.append(pyqt5_dir / "designer.exe")
            else:
                possible_paths.append(pyqt5_dir / "designer")
            
            qt_plugins_base = None
        except ImportError:
            sys.exit(" PyQt5 not found in current venv.")

    else:
        sys.exit(f" Unsupported Qt library: {qt_lib}")

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

    # Add Custom_Widgets path to PYTHONPATH
    custom_widgets_dir = pathlib.Path(Custom_Widgets.__file__).parent
    env["PYTHONPATH"] = str(custom_widgets_dir.parent) + os.pathsep + env.get("PYTHONPATH", "")

    # Pin qtpy to the binding this Designer belongs to. Without this, with
    # several bindings installed qtpy may resolve to a different one (e.g.
    # PyQt5) inside Designer's embedded interpreter and every plugin import
    # crashes (pyqtProperty(notify=None) TypeError).
    env["QT_API"] = qt_lib.lower()

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
        designer_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
        
        print(f" Launching Qt Designer using QProcess: {designer_cmd}")
        
        # On Windows, use the full path if available
        if sys.platform.startswith("win") and designer_exe:
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