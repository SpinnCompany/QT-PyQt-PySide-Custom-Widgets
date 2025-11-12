########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
# EMAIL: info@spinncode.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import os
import sys
from subprocess import call
import shutil
import json
from urllib.parse import urlparse
import argparse
import subprocess
import platform

from termcolor import colored  # Install termcolor using: pip install termcolor
import textwrap

import qtpy
from qtpy.QtCore import Signal, QObject
from qtpy.QtGui import QColor

from Custom_Widgets.QCustomTheme import QCustomTheme

class ProjectMaker(QObject):
    progress = Signal(int)

    def __init__(self):
        super().__init__()

def print_header(title):
    """Print formatted header"""
    print(colored(f"\n{'='*60}", "cyan"))
    print(colored(f" {title}", "cyan", attrs=['bold']))
    print(colored(f"{'='*60}", "cyan"))

def print_success(message):
    """Print success message"""
    print(colored(f"✓ {message}", "green"))

def print_warning(message):
    """Print warning message"""
    print(colored(f"⚠ {message}", "yellow"))

def print_error(message):
    """Print error message"""
    print(colored(f"✗ {message}", "red"))

def print_info(message):
    """Print info message"""
    print(colored(f"ℹ {message}", "blue"))

def print_command(command, description):
    """Print command with description"""
    print(colored(f"  $ {command}", "yellow"))
    print(colored(f"    # {description}", "white"))

def progress(count, status='Processing'):
    """Display progress bar"""
    bar_len = 30
    total = 100
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '░' * (bar_len - filled_len)

    sys.stdout.write(f'[{bar}] {percents}% {status}\r')
    sys.stdout.flush() 

def query_yes_no(question, default="yes"):
    """Ask a yes/no question and return the answer"""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(colored(question + prompt, "yellow"))
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print_warning("Please respond with 'yes' or 'no' (or 'y' or 'n').")

def create_requirements_file(required_packages, file_path="requirements.txt"):
    """
    Create a requirements.txt file with the specified package names and versions.
    """
    with open(file_path, "w") as file:
        for package in required_packages:
            file.write(package + "\n")
    print_success(f"Created {file_path}")

def is_directory_empty_or_only_logs(directory):
    """Check if directory is empty or only contains logs folder"""
    entries = list(os.scandir(directory))
    for entry in entries:
        if entry.name != "logs" and (entry.is_file() or entry.is_dir()):
            return False
    return True

def get_user_choice_for_non_empty_dir():
    """Get user choice when directory is not empty"""
    print_header("DIRECTORY NOT EMPTY")
    print_warning("The current directory is not empty!")
    print_info("Contents of current directory:")
    
    for entry in os.scandir():
        if entry.is_file():
            print(f"  📄 {entry.name}")
        elif entry.is_dir():
            print(f"  📁 {entry.name}")
    
    print("\nChoose an option:")
    print("1. Overwrite existing project files (recommended for new projects)")
    print("2. Exit and choose a different directory")
    
    while True:
        choice = input(colored("Enter your choice (1 or 2): ", "yellow")).strip()
        if choice == "1":
            return "overwrite"
        elif choice == "2":
            return "exit"
        else:
            print_warning("Please enter 1 or 2")

def register_custom_widgets():
    """Register custom widgets with Qt Designer"""
    print_header("REGISTERING CUSTOM WIDGETS")
    print_info("Registering custom widgets with Qt Designer...")
    
    try:
        # Find the site-packages directory
        result = subprocess.run([sys.executable, "-m", "site", "--user-site"], 
                              capture_output=True, text=True)
        site_packages = result.stdout.strip()
        
        if site_packages:
            plugins_path = os.path.join(site_packages, "Custom_Widgets", "Plugins", "registerMyWidget.py")
            if os.path.exists(plugins_path):
                print_info("Running widget registration script...")
                subprocess.run([sys.executable, plugins_path])
                print_success("Custom widgets registered successfully!")
            else:
                print_warning(f"Registration script not found at: {plugins_path}")
                print_info("You can manually register widgets later using:")
                print_command("Custom_Widgets --register-widgets", "Register custom widgets with Qt Designer")
        else:
            print_warning("Could not find site-packages directory")
            
    except Exception as e:
        print_error(f"Failed to register widgets: {e}")
        print_info("You can manually register widgets later")

def start_file_monitoring(ui_path="ui", qt_binding="PySide6"):
    """Start monitoring UI files for changes"""
    print_header("STARTING FILE MONITORING")
    print_info("Starting file monitoring service...")
    
    try:
        command = ["Custom_Widgets", "--monitor-ui", ui_path, "--qt-library", qt_binding]
        print_info(f"Monitoring UI files in: {ui_path}")
        print_info("File monitor started! Changes to .ui files will be automatically converted.")
        print_info("Press Ctrl+C to stop monitoring")
        
        # Start monitoring in background
        if platform.system() == "Windows":
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            subprocess.Popen(command, start_new_session=True)
            
        return True
    except Exception as e:
        print_error(f"Failed to start file monitoring: {e}")
        return False

def start_qt_designer_with_plugins():
    """Start Qt Designer with custom widgets plugins"""
    print_header("STARTING QT DESIGNER")
    
    try:
        # Use the Custom_Widgets CLI command to start Qt Designer with plugins
        print_info("Starting Qt Designer with custom widgets plugins...")
        command = ["Custom_Widgets", "--start-designer", "--plugins"]
        
        if platform.system() == "Windows":
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            subprocess.Popen(command, start_new_session=True)
            
        print_success("Qt Designer started with custom widgets plugins!")
        return True
        
    except Exception as e:
        print_error(f"Failed to start Qt Designer with plugins: {e}")
        print_info("Trying alternative method...")
        
        # Fallback: Try to find and start Qt Designer directly
        designer_commands = [
            "designer",
            "qt5-designer",
            "qt6-designer",
            "pyside6-designer",
            "pyside2-designer",
            "pyqt5-designer"
        ]
        
        designer_found = False
        for cmd in designer_commands:
            try:
                print_info(f"Trying to start: {cmd}")
                if platform.system() == "Windows":
                    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen(cmd, start_new_session=True)
                print_success(f"Qt Designer started with: {cmd}")
                designer_found = True
                break
            except (FileNotFoundError, OSError):
                continue
        
        if not designer_found:
            print_warning("Could not automatically find Qt Designer")
            print_info("Please start Qt Designer manually using:")
            print_command("Custom_Widgets --start-designer", "Launch Qt Designer with plugins")
            print_command("Custom_Widgets --start-designer --no-plugins", "Launch Qt Designer without plugins")
            print_info("Or install it using your package manager:")
            if platform.system() == "Windows":
                print_command("winget install Qt.QtDesigner", "Install Qt Designer on Windows")
            elif platform.system() == "Darwin":  # macOS
                print_command("brew install qt", "Install Qt on macOS")
            else:  # Linux
                print_command("sudo apt install qttools5-dev-tools", "Install Qt Designer on Ubuntu/Debian")
        
        return designer_found

def show_workflow_instructions(appQtBinding):
    """Show workflow instructions to the user"""
    print_header("NEXT STEPS - WORKFLOW INSTRUCTIONS")
    
    print_info("🎯 RECOMMENDED WORKFLOW:")
    print("1. Design your interface in Qt Designer (with custom widgets)")
    print("2. Save .ui files in the 'ui' folder")
    print("3. Automatically convert .ui to .py when changes occur")
    print("4. Run your app to see live updates")
    
    print_header("AUTOMATED FILE MONITORING")
    print_info("The file monitor automatically converts .ui files to Python when you save changes.")
    print("This means you can:")
    print("  • Design in Qt Designer")
    print("  • Save your .ui file") 
    print("  • See changes immediately in your running app")
    
    print_command(f"Custom_Widgets --monitor-ui ui --qt-library {appQtBinding}", 
                 "Monitor UI folder for changes")
    print_command(f"Custom_Widgets --convert-ui ui/main_window.ui --qt-library {appQtBinding}",
                 "Convert specific UI file to Python")
    
    print_header("QT DESIGNER WITH CUSTOM WIDGETS")
    print_info("Your custom widgets are now available in Qt Designer!")
    print("Look for these widget groups in the widget box:")
    print("  • MainWindow - Custom main windows")
    print("  • Sidebar - Navigation sidebars") 
    print("  • Progressbars - Animated progress indicators")
    print("  • Component Container - Layout containers")
    
    print_info("If widgets don't appear in Qt Designer:")
    print_command("Custom_Widgets --register-widgets", "Re-register widgets with Qt Designer")
    
    print_header("QUICK START COMMANDS")
    print_info("After project setup, you can use these commands anytime:")
    print_command("python main.py", "Run your application")
    print_command(f"Custom_Widgets --monitor-ui ui --qt-library {appQtBinding}", "Start UI file monitoring")
    print_command(f"Custom_Widgets --convert-ui ui --qt-library {appQtBinding}", "Convert all UI files once")
    print_command("Custom_Widgets --start-designer --plugins", "Launch Qt Designer with custom widgets plugins")
    print_command("Custom_Widgets --start-designer", "Launch Qt Designer without plugins")

project_maker = ProjectMaker()

def create_project():
    """Main function to create a new project"""
    
    # Print welcome banner
    print_header("PROJECT MAKER")
    print(colored("YouTube: https://www.youtube.com/spinnTv", "green"))
    print(colored("Website: spinncode.com", "green"))
    print(colored("Email: info@spinncode.com\n", "green"))
    
    # Current Directory
    currentDir = os.getcwd()
    print_info(f"Initializing new project in: {currentDir}")

    # Check if folder is empty (excluding logs folder)
    if not is_directory_empty_or_only_logs(currentDir):
        choice = get_user_choice_for_non_empty_dir()
        if choice == "exit":
            print_info("Exiting project creation. Please choose an empty directory.")
            return
        else:
            print_warning("Continuing with project creation. Existing files may be overwritten.")
    
    # Create UI directory and copy template if needed
    ui_dir = os.path.abspath(os.path.join(os.getcwd(), 'ui'))
    ui_path = os.path.join(ui_dir, 'QCustomQMainWindow.ui')
    
    if not os.path.exists(ui_dir):
        os.makedirs(ui_dir)
        print_success("Created UI directory")
    
    template_ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components/uis/QCustomQMainWindow.ui'))
    if not os.path.exists(ui_path) and os.path.exists(template_ui_path):   
        shutil.copy(template_ui_path, ui_path)
        print_success("Copied UI template file")

    # Get Qt binding
    print_header("QT BINDING SELECTION")
    print_info("Please enter your Qt binding/API name:")
    print("Options: PySide6, PySide2, PyQt6, PyQt5")
    print("Default: PySide6\n")

    global appQtBinding

    while True:
        appQtBinding = input(colored("Enter Qt binding/API name: ", "yellow")).strip()
        if not appQtBinding:
            appQtBinding = "PySide6"
            print_info(f"Using default Qt binding: {appQtBinding}")
            break
        
        if appQtBinding not in ["PySide6", "PySide2", "PyQt6", "PyQt5"]:
            print_error(f"'{appQtBinding}' is not a valid Qt binding")
            continue
            
        if query_yes_no(f"Use '{appQtBinding}' as Qt binding?"):
            break

    # Update Qt Binding
    qtpy.API_NAME = appQtBinding
    os.environ['QT_API'] = appQtBinding.lower()
    print_success(f"Qt binding set to: {appQtBinding}")

    # Copy main.py template if needed
    main_py = os.path.abspath(os.path.join(os.getcwd(), 'main.py'))
    template_main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components/python/main.py'))
    
    if not os.path.exists(main_py) and os.path.exists(template_main_path):   
        shutil.copy(template_main_path, main_py)
        print_success("Copied main.py template")

    # Get icons color
    print_header("ICONS COLOR")
    print_info("Enter icons color for your application:")
    print("You can use HEX values (#ffffff) or color names (white)")

    while True:
        iconsColor = input(colored("Enter icons color: ", "yellow")).strip()
        if not iconsColor:
            print_error("Icons color cannot be empty")
            continue
            
        if not QColor().isValidColor(iconsColor):
            print_error(f"'{iconsColor}' is not a valid color")
            continue
            
        if query_yes_no(f"Use '{iconsColor}' as icons color?"):
            break

    normal_color = QCustomTheme.colorToHex(None, iconsColor)

    # Get Qt Designer icons color
    print_header("QT DESIGNER ICONS COLOR")
    print_info("Enter icons color for Qt Designer:")
    print("For dark theme use light colors (white), for light theme use dark colors (black)")

    while True:
        qtIconsColor = input(colored("Enter Qt Designer icons color: ", "yellow")).strip()
        if not qtIconsColor:
            qtIconsColor = iconsColor
            print_info(f"Using same color as app icons: {qtIconsColor}")
            break
            
        if not QColor().isValidColor(qtIconsColor):
            print_error(f"'{qtIconsColor}' is not a valid color")
            continue
            
        if query_yes_no(f"Use '{qtIconsColor}' as Qt Designer icons color?"):
            break
    
    qt_normal_color = QCustomTheme.colorToHex(None, qtIconsColor)

    # Get app theme colors
    print_header("APP THEME COLORS")
    print_info("These colors will be used to create your app stylesheet")

    colors = {}
    for color_type in ["background", "text", "accent"]:
        while True:
            color = input(colored(f"Enter app {color_type} color: ", "yellow")).strip()
            if not color:
                print_error(f"{color_type.capitalize()} color cannot be empty")
                continue
                
            if not QColor().isValidColor(color):
                print_error(f"'{color}' is not a valid color")
                continue
                
            if query_yes_no(f"Use '{color}' as {color_type} color?"):
                colors[color_type] = QCustomTheme.colorToHex(None, color)
                break

    # Convert UI files
    print_info("Converting UI files...")
    call(["Custom_Widgets", "--convert-ui", "ui", "--qt-library", appQtBinding])
    print_success("UI files converted")

    # Get app name
    print_header("APPLICATION INFORMATION")
    default_app_name = os.path.basename(os.getcwd())
    print_info(f"Enter your application name (default: {default_app_name})")

    while True:
        appName = input(colored("Enter app name: ", "yellow")).strip()
        if not appName:
            appName = default_app_name
            print_info(f"Using directory name as app name: {appName}")
            
        if query_yes_no(f"Use '{appName}' as application name?"):
            break

    # Get organization details
    print_header("ORGANIZATION DETAILS")
    print_info("These values are used for QSettings configuration storage")

    default_org = f"{appName} Company"
    default_domain = f"{appName}.org"

    org_name = input(colored(f"Enter organization name (default: {default_org}): ", "yellow")).strip()
    if not org_name:
        org_name = default_org

    domain_name = input(colored(f"Enter domain name (default: {default_domain}): ", "yellow")).strip()
    if not domain_name:
        domain_name = default_domain

    # Create JSON styles directory and file
    json_dir = os.path.abspath(os.path.join(os.getcwd(), 'json-styles'))
    json_path = os.path.join(json_dir, 'style.json')
    
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
        print_success("Created JSON styles directory")

    template_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components/json/style.json'))
    if not os.path.exists(json_path) and os.path.exists(template_json_path):   
        shutil.copy(template_json_path, json_path)
        print_success("Copied JSON style template")

    # Update JSON configuration
    print_info("Updating project configuration...")
    with open(json_path, 'r+') as f:
        data = json.load(f)

        # Update basic settings
        data["QtBinding"] = appQtBinding
        data["CheckForMissingicons"] = True
        data["LiveCompileQss"] = True

        # Update QMainWindow title
        data["QMainWindow"] = {"title": appName}

        # Update QSettings
        data["QSettings"] = {
            "AppSettings": {
                "OrginizationName": org_name,
                "ApplicationName": appName,
                "OrginizationDormain": domain_name
            },
            "ThemeSettings": {
                "QtDesignerIconsColor": qt_normal_color,
                "CustomThemes": [{
                    "Background-color": colors["background"],
                    "Text-color": colors["text"],
                    "Accent-color": colors["accent"],
                    "Icons-color": normal_color,
                    "Theme-name": "Default-theme",
                    "Default-Theme": True
                }]
            }
        }

        f.seek(0)  
        json.dump(data, f, indent=4)
        f.truncate()

    print_success("Project configuration updated")

    # Create requirements file
    required_packages = [appQtBinding, "QT-PyQt-PySide-Custom-Widgets"]
    create_requirements_file(required_packages)

    # Copy README if needed
    readme_path = os.path.abspath(os.path.join(os.getcwd(), 'README.md'))
    template_readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components/md/README.md'))
    
    if not os.path.exists(readme_path) and os.path.exists(template_readme_path):   
        shutil.copy(template_readme_path, readme_path)
        print_success("Created README.md")

    # Register custom widgets
    register_custom_widgets()

    # Final summary
    print_header("PROJECT CREATION COMPLETE")
    print_success("Your project has been successfully created!")
    
    show_workflow_instructions(appQtBinding)

    # Post-creation options
    print_header("GET STARTED NOW!")
    print_info("Choose your next steps:")
    
    post_creation_actions = [
        ("Start Qt Designer with custom widgets", "Open Qt Designer to design your interface"),
        ("Start UI file monitoring", "Automatically convert UI files when changes occur"),
        ("Run the project", "Launch your application to see the result"),
        ("Show workflow instructions again", "Display workflow and commands"),
        ("Exit", "Close the project wizard")
    ]
    
    for i, (action, description) in enumerate(post_creation_actions, 1):
        print(f"{i}. {action}")
        print(f"   {description}")
    
    while True:
        try:
            choice = input(colored("\nEnter your choice (1-5): ", "yellow")).strip()
            if not choice:
                continue
                
            choice = int(choice)
            if choice == 1:
                start_qt_designer_with_plugins()
            elif choice == 2:
                if start_file_monitoring("ui", appQtBinding):
                    print_success("File monitoring started! Your UI changes will be automatically converted.")
                    print_info("Keep this terminal open to maintain monitoring.")
            elif choice == 3:
                print_info("Running your project...")
                call(["python", "main.py"])
            elif choice == 4:
                show_workflow_instructions(appQtBinding)
            elif choice == 5:
                print_info("Project creation complete! Happy coding! 🎉")
                break
            else:
                print_warning("Please enter a number between 1 and 5")
                
            # After each action, ask if user wants to do something else
            if choice != 5:
                if not query_yes_no("\nWould you like to do something else?"):
                    print_info("Project creation complete! Happy coding! 🎉")
                    break
                    
        except ValueError:
            print_warning("Please enter a valid number")
        except KeyboardInterrupt:
            print_info("\nProject creation complete! Happy coding! 🎉")
            break

if __name__ == "__main__":
    create_project()