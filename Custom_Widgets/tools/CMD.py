# Custom_Widgets/CMD.py
import argparse
import textwrap

from Custom_Widgets.ProjectMaker import create_project, create_ui_file
from Custom_Widgets.FileMonitor import start_file_listener, start_ui_conversion
from Custom_Widgets.Designer import start_designer

def run_command():
    parser = argparse.ArgumentParser(description='Custom Widgets CLI')
    parser.add_argument('--monitor-ui', dest='file_to_monitor', help='Monitor changes made to UI file and generate new .py file and other necessary files for the custom widgets.')
    parser.add_argument('--convert-ui', dest='file_to_convert', help='Generate new .py file and other necessary files for the custom widgets.')
    parser.add_argument('--qt-library', dest='qt_library', help='Specify the Qt library (e.g., "PySide6")')
    parser.add_argument('--create-project', action='store_true', help='Create a new project')
    parser.add_argument('--new-ui', dest='new_ui_name', help='Create a new .ui form in ./ui with the theme icons resource (Qss/icons/_icons.qrc) pre-loaded')
    parser.add_argument('--dev', dest='dev', nargs='?', const='main.py',
                        metavar='SCRIPT',
                        help='Run the app under the dev server: .ui saves '
                             'regenerate + restart, .py saves restart, '
                             'scss/json restyle live (default script: main.py)')
    
    # --- Python source output directory ---
    parser.add_argument('--src-output-dir', dest='src_output_dir', default='src',
                       help='Directory for generated Python source files (default: src)')
    
    # --- Designer launcher ---
    parser.add_argument('--start-designer', action='store_true', help='Start Qt Designer')
    parser.add_argument('--plugins', dest='plugins', action='store_true', help='Register Custom_Widgets plugins in Designer (used with --start-designer)')
    parser.add_argument('--process-mode', dest='process_mode', choices=['normal', 'qprocess'], default='normal',
                       help='Process mode for launching Designer: "normal" uses subprocess, "qprocess" uses QProcess (default: normal)')

    args = parser.parse_args()

    if args.file_to_monitor:
        start_file_listener(
            args.file_to_monitor, 
            args.qt_library,
            src_output_dir=args.src_output_dir
        )
    
    elif args.file_to_convert:
        start_ui_conversion(
            args.file_to_convert, 
            args.qt_library,
            src_output_dir=args.src_output_dir
        )

    elif args.create_project:
        create_project()

    elif args.new_ui_name:
        create_ui_file(args.new_ui_name)

    elif args.dev:
        from Custom_Widgets.DevServer import run_dev
        raise SystemExit(run_dev(
            script=args.dev,
            qt_binding=args.qt_library or "PySide6",
            src_output_dir=args.src_output_dir,
        ))

    elif args.start_designer:
        start_designer(load_plugins=args.plugins, process_mode=args.process_mode)

    else:
        print(textwrap.dedent("""
        ╔══════════════════════════════════════════════════════════════╗
        ║                 Custom Widgets CLI - Help                    ║
        ╚══════════════════════════════════════════════════════════════╝
        
        USAGE:
            Custom_Widgets COMMAND [OPTIONS]
        
        COMMANDS:
            Dev loop:
                --dev [SCRIPT]           Run the app with everything hot:
                                        .ui saves regenerate + restart the app,
                                        .py saves restart, scss/json restyle
                                        live (default SCRIPT: main.py)

            Monitor & Convert:
                --monitor-ui PATH       Monitor UI file/folder and auto-generate files on changes
                --convert-ui PATH        Convert UI file/folder once and exit
            
            Project:
                --create-project         Create a new project structure
                --new-ui NAME            Create ui/NAME.ui with the theme icons
                                        resource (SVG) ready for Qt Designer
            
            Designer:
                --start-designer         Launch Qt Designer with custom widgets
                [--plugins]             Register Custom_Widgets plugins
                [--process-mode MODE]    Process mode: 'normal' (subprocess) or 'qprocess'
        
        OPTIONS:
            General:
                --qt-library LIB         Qt binding to use (PySide6, PyQt6)
                                        (default: PySide6)
            
            Output:
                --src-output-dir DIR     Directory for generated Python source files
                                        (default: ./src)
        
        EXAMPLES:
            # Monitor a single UI file
            Custom_Widgets --monitor-ui path/to/mainwindow.ui
            
            # Monitor all UI files in a folder with custom output
            Custom_Widgets --monitor-ui ./ui_files --src-output-dir ./generated
            
            # Convert UI files once
            Custom_Widgets --convert-ui ./ui_files --qt-library PyQt6
            
            # Launch Designer with plugins
            Custom_Widgets --start-designer --plugins
            
            # Create a new project
            Custom_Widgets --create-project
        
        NOTES:
            • The monitor mode continuously watches for changes and regenerates files
            • Convert mode processes files once and exits
            • Generated JSON and modified UI files are stored in ./generated-files/
            • Python source files are stored in the directory specified by --src-output-dir
            • If no --qt-library is specified, PySide6 is used by default
        """))

if __name__ == "__main__":
    run_command()
