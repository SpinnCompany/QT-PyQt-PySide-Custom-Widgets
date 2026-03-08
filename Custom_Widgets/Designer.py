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
    qt_lib = qtpy.API_NAME  # 'PySide6', 'PyQt6', 'PySide2', 'PyQt5'
    
    # Initialize variables
    qt_plugins_base = None
    possible_paths = []
    designer_cmd = None  # Store just the command name for QProcess mode

    if qt_lib == "PySide6":
        # Standard Scripts/bin location
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside6-designer"
        )
        designer_cmd = "pyside6-designer"
        
        try:
            import PySide6
            pyside6_dir = pathlib.Path(PySide6.__file__).parent
            
            # Package root location
            if sys.platform.startswith("win"):
                possible_paths.append(pyside6_dir / "designer.exe")
            else:
                possible_paths.append(pyside6_dir / "designer")
            
            # Qt/bin location
            if sys.platform.startswith("win"):
                possible_paths.append(pyside6_dir / "Qt" / "bin" / "designer.exe")
            else:
                possible_paths.append(pyside6_dir / "Qt" / "bin" / "designer")
            
            qt_plugins_base = pyside6_dir / "designer" / "plugins"
        except ImportError:
            sys.exit("❌ PySide6 not found in current venv.")

    elif qt_lib == "PySide2":
        # Standard Scripts/bin location
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyside2-designer"
        )
        designer_cmd = "pyside2-designer"
        
        try:
            import PySide2
            pyside2_dir = pathlib.Path(PySide2.__file__).parent
            
            # Package root location
            if sys.platform.startswith("win"):
                possible_paths.append(pyside2_dir / "designer.exe")
            else:
                possible_paths.append(pyside2_dir / "designer")
            
            qt_plugins_base = pyside2_dir / "designer" / "plugins"
        except ImportError:
            sys.exit("❌ PySide2 not found in current venv.")

    elif qt_lib == "PyQt6":
        # Standard Scripts/bin location
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt6-designer"
        )
        designer_cmd = "pyqt6-designer"
        
        try:
            import PyQt6
            pyqt6_dir = pathlib.Path(PyQt6.__file__).parent
            
            # Package root location (less common for PyQt)
            if sys.platform.startswith("win"):
                possible_paths.append(pyqt6_dir / "designer.exe")
            else:
                possible_paths.append(pyqt6_dir / "designer")
            
            qt_plugins_base = None  # PyQt6 does not include internal Python Designer plugins
        except ImportError:
            sys.exit("❌ PyQt6 not found in current venv.")

    elif qt_lib == "PyQt5":
        # Standard Scripts/bin location
        possible_paths.append(
            pathlib.Path(sys.prefix) / ("Scripts" if sys.platform.startswith("win") else "bin") / "pyqt5-designer"
        )
        designer_cmd = "pyqt5-designer"
        
        try:
            import PyQt5
            pyqt5_dir = pathlib.Path(PyQt5.__file__).parent
            
            # Package root location (less common for PyQt)
            if sys.platform.startswith("win"):
                possible_paths.append(pyqt5_dir / "designer.exe")
            else:
                possible_paths.append(pyqt5_dir / "designer")
            
            qt_plugins_base = None  # PyQt5 does not include internal Python Designer plugins
        except ImportError:
            sys.exit("❌ PyQt5 not found in current venv.")

    else:
        sys.exit(f"❌ Unsupported Qt library: {qt_lib}")

    # Find first existing designer executable for normal mode
    designer_exe = None
    for path in possible_paths:
        if path.exists():
            designer_exe = path
            print(f"✅ Found designer at: {designer_exe}")
            break
    
    if not designer_exe and process_mode == "normal":
        paths_str = "\n  ".join(str(p) for p in possible_paths)
        sys.exit(f"❌ Designer executable not found in any of these locations:\n  {paths_str}")

    # --- Setup environment variables ---
    env = os.environ.copy()
    
    # Add Custom_Widgets path to PYTHONPATH
    custom_widgets_dir = pathlib.Path(Custom_Widgets.__file__).parent
    env["PYTHONPATH"] = str(custom_widgets_dir.parent)  # Add parent directory to Python path

    # Set internal plugins if available
    plugins_paths = []
    if qt_plugins_base and qt_plugins_base.exists():
        plugins_paths.append(str(qt_plugins_base))
    
    # --- Add Custom_Widgets Plugins folder if requested ---
    if load_plugins:
        plugins_dir = custom_widgets_dir / "Plugins"
        print(f"Plugins dir: {plugins_dir}")
        if plugins_dir.exists():
            plugins_paths.append(str(plugins_dir))
    
    # Set the PYSIDE_DESIGNER_PLUGINS environment variable
    if plugins_paths:
        env["PYSIDE_DESIGNER_PLUGINS"] = os.pathsep.join(plugins_paths)
        print(f"PYSIDE_DESIGNER_PLUGINS set to: {env['PYSIDE_DESIGNER_PLUGINS']}")

    # --- Launch Designer based on process mode ---
    if process_mode == "qprocess":
        # Use QProcess mode
        
        # Create QApplication (required for QProcess)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create QProcess environment
        qenv = QProcessEnvironment.systemEnvironment()
        
        # Set the plugins path using the same logic as normal mode
        if plugins_paths:
            qenv.insert('PYSIDE_DESIGNER_PLUGINS', os.pathsep.join(plugins_paths))
            print(f"PYSIDE_DESIGNER_PLUGINS set to: {os.pathsep.join(plugins_paths)}")
        
        # Also set PYTHONPATH if needed
        custom_widgets_dir = pathlib.Path(Custom_Widgets.__file__).parent
        qenv.insert("PYTHONPATH", str(custom_widgets_dir.parent))
        
        # Start Designer process
        designer_process = QProcess()
        designer_process.setProcessEnvironment(qenv)
        designer_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
        
        print(f"🚀 Launching Qt Designer using QProcess: {designer_cmd}")
        designer_process.start(designer_cmd, [])
        
        # Check if designer started
        if not designer_process.waitForStarted(30000):  # 30 second timeout
            error_string = designer_process.errorString()
            print(f"❌ Designer process failed to start: {error_string}")
            sys.exit(1)
        
        print("✅ Qt Designer started successfully")
        
        # Wait for designer to finish
        designer_process.waitForFinished(-1)  # -1 means wait indefinitely
        sys.exit(designer_process.exitCode())
        
    else:
        # Use normal subprocess mode
        print(f"🚀 Launching Qt Designer using subprocess from: {designer_exe}")
        subprocess.run([str(designer_exe)], cwd=os.getcwd(), env=env)