# Custom_Widgets/CMD.py
import argparse
import textwrap

from Custom_Widgets.ProjectMaker import create_project
from Custom_Widgets.FileMonitor import start_file_listener, start_ui_conversion
from Custom_Widgets.Designer import start_designer

def run_command():
    parser = argparse.ArgumentParser(description='Custom Widgets CLI')
    parser.add_argument('--monitor-ui', dest='file_to_monitor', help='Monitor changes made to UI file and generate new .py file and other necessary files for the custom widgets.')
    parser.add_argument('--convert-ui', dest='file_to_convert', help='Generate new .py file and other necessary files for the custom widgets.')
    parser.add_argument('--qt-library', dest='qt_library', help='Specify the Qt library (e.g., "PySide6")')
    parser.add_argument('--create-project', action='store_true', help='Create a new project')
    
    # --- Designer launcher ---
    parser.add_argument('--start-designer', action='store_true', help='Start Qt Designer')
    parser.add_argument('--plugins', dest='plugins', action='store_true', help='Register Custom_Widgets plugins in Designer (used with --start-designer)')

    args = parser.parse_args()

    if args.file_to_monitor:
        start_file_listener(args.file_to_monitor, args.qt_library)
    
    elif args.file_to_convert:
        start_ui_conversion(args.file_to_convert, args.qt_library)

    elif args.create_project:
        create_project()

    elif args.start_designer:
        start_designer(load_plugins=args.plugins)

    else:
        print(textwrap.dedent(
            "Use:\n"
            "'Custom_Widgets --monitor-ui ui-path'\n"
            "'Custom_Widgets --convert-ui ui-path'\n"
            "'Custom_Widgets --create-project'\n"
            "'Custom_Widgets --start-designer [--plugins]'"
        ))
