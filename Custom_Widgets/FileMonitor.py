import sys
import os
import json
from qtpy.QtCore import QObject, QFileSystemWatcher
from qtpy.QtWidgets import QApplication
import xml.etree.ElementTree as ET
from lxml import etree
import re

import qtpy

from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.Utils import replace_url_prefix, SharedData, is_in_designer, uiToPy
from Custom_Widgets.Project import projectRoot
from Custom_Widgets.Log import *

class FileMonitor(QObject):
    """Monitors UI files for changes and automatically regenerates Python source files."""
    
    def __init__(self, files_to_monitor, refresh=False, src_output_dir="src"):
        super().__init__()
        
        # Store source output directory
        self.src_output_dir = src_output_dir
        
        # Create necessary directories
        self._create_directories()
        
        # Log startup information
        logInfo("=" * 60)
        logInfo("File Monitor Initialized")
        logInfo("=" * 60)
        logInfo(f"Source output directory: {os.path.abspath(src_output_dir)}")
        logInfo(f"UI files output: {os.path.abspath(os.path.join('generated-files', 'ui'))}")
        logInfo(f"JSON files output: {os.path.abspath(os.path.join('generated-files', 'json'))}")
        logInfo("=" * 60)

        self.files_to_monitor = files_to_monitor
        self.refresh = refresh
        self.fileSystemWatchers = []
        
        # Create a QFileSystemWatcher for folder monitoring
        if refresh:
            self.monitor_folders()
        else:
            # Monitor files if no refresh argument
            self.monitor_files(files_to_monitor)

    def _create_directories(self):
        """Create all required directories if they don't exist."""
        directories = [
            os.path.join(projectRoot(), "generated-files"),
            os.path.join(projectRoot(), "generated-files/ui"),
            os.path.join(projectRoot(), "generated-files/json"),
            self.src_output_dir
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logDebug(f"Created directory: {directory}")

    def monitor_folders(self):
        """Monitor the folder for changes (e.g., new .ui files added)."""
        folder_to_monitor = os.path.dirname(self.files_to_monitor[0]) if self.files_to_monitor else projectRoot()
        self.folder_watcher = QFileSystemWatcher([folder_to_monitor])
        self.folder_watcher.directoryChanged.connect(self.on_folder_change)
        
        logInfo(f" Monitoring folder: {folder_to_monitor}")
        
        # Initially monitor the files already in the folder
        self.monitor_files(self.files_to_monitor)

    def monitor_files(self, files_to_monitor):
        """Set up file watchers for individual UI files."""
        # Clear any existing file watchers
        for watcher in self.fileSystemWatchers:
            try:
                watcher.fileChanged.disconnect(self.on_file_change)
            except Exception:
                pass
        self.fileSystemWatchers.clear()

        if not files_to_monitor:
            logWarning("No files to monitor")
            return

        # Create a QFileSystemWatcher for each file
        self.fileSystemWatchers = [QFileSystemWatcher([file]) for file in files_to_monitor]

        # Connect the fileChanged signal for each watcher
        for watcher in self.fileSystemWatchers:
            watcher.fileChanged.connect(self.on_file_change)

        logSuccess(f" Monitoring {len(self.files_to_monitor)} UI files:")
        for file in self.files_to_monitor:
            logInfo(f"   • {os.path.basename(file)}")

    def on_file_change(self, path):
        """Handle file modification events."""
        logInfo("")
        logInfo(" " + "=" * 50)
        logInfo(f" FILE CHANGE DETECTED: {os.path.basename(path)}")
        logInfo(" " + "=" * 50)
        
        # Handle file modification event - pass source output directory
        convert_file(path, self.src_output_dir)
        
        logSuccess(f" Successfully regenerated files from {os.path.basename(path)}")
        logInfo(" " + "=" * 50 + "\n")
        
        self.update_file_list()

    def on_folder_change(self, path):
        """Handle folder changes (files added/removed)."""
        logInfo(f" Folder change detected in: {path}")
        # Refresh the list of .ui files to monitor if a folder is updated
        self.update_file_list(fresh=True)

    def update_file_list(self, fresh=False):
        """Update the list of monitored UI files."""
        # Find all .ui files in the folder
        folder_path = os.path.dirname(self.files_to_monitor[0]) if self.files_to_monitor else projectRoot()
        ui_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".ui")]

        # Update the list of monitored files if there are new files or missing files
        new_files = set(ui_files) - set(self.files_to_monitor)
        removed_files = set(self.files_to_monitor) - set(ui_files)

        if not (new_files or removed_files) and fresh:
            return
            
        if new_files:
            logInfo(f" New UI files detected: {len(new_files)}")
            for file in new_files:
                logInfo(f"   + {os.path.basename(file)}")
                
        if removed_files:
            logInfo(f" Removed UI files: {len(removed_files)}")
            for file in removed_files:
                logInfo(f"   - {os.path.basename(file)}")
            
        self.files_to_monitor = ui_files
        self.monitor_files(self.files_to_monitor)

def find_parent_with_class(widget):
    """
    Traverse up the XML tree from the given widget until an element with a non-None class attribute is found.
    
    Parameters:
        widget (Element): The starting widget (XML element).
        
    Returns:
        Element or None: The found parent element with a non-None class attribute, or None if not found.
    """
    current_element = widget
    while current_element is not None:
        # Check if the current element has a non-None class attribute
        if current_element.get('class') is not None:
            return current_element
        # Move up to the parent element
        current_element = current_element.getparent()
    
    # Return None if no matching parent is found
    return None

def convert_file(path, src_output_dir="src"):
    """
    Convert a UI file to generate JSON metadata and modified UI file.
    
    Parameters:
        path (str): Path to the UI file
        src_output_dir (str): Directory for output Python source files
    """
    logInfo(f" Processing: {os.path.basename(path)}")
    
    # Load the UI file
    try:
        tree = etree.parse(path)
        root = tree.getroot()
        logDebug(f"Successfully parsed UI file: {path}")
    except Exception as e:
        logError(f"Failed to parse UI file: {e}")
        return

    # Initialize counters and data structures
    widget_info = {}
    table_items = 0
    tree_items = 0
    processed_widgets = 0

    # Iterate through each element in the UI file
    for element in root.iter():
        # Get the widget class and name
        widget_class = element.attrib.get('class')
        widget_name = element.attrib.get('name')
        
        if widget_class == 'QComboBox':
            # Initialize a list to hold combo box items
            combo_items = []

            # Find all items within the QComboBox
            for item_element in element.findall("item"):
                item_data = {}

                # Get the item text
                text_element = item_element.find("property[@name='text']/string")
                if text_element is not None:
                    item_data['name'] = text_element.text

                # Get the item icon
                icon_element = item_element.find("property[@name='icon']/iconset/normaloff")
                if icon_element is not None:
                    icon_path = icon_element.text
                    qrc_file_path = icon_element.attrib['resource']
                    qrc_folder = os.path.dirname(qrc_file_path)
                    item_data['icon'] = replace_url_prefix(icon_path, qrc_folder)

                combo_items.append(item_data)

            # Save the combo box items in the widget_info dictionary
            widget_info["QComboBox"] = widget_info.get("QComboBox", [])
            widget_info["QComboBox"].append({"name": widget_name, "items": combo_items})
            processed_widgets += 1
            logDebug(f"Processed QComboBox: {widget_name} with {len(combo_items)} items")

        if 'name' in element.attrib and (element.attrib['name'] == 'icon' or element.attrib['name'] == "windowIcon"):
            widget = element.getparent()  # Get the parent widget
            widget_class = widget.get('class')  
            parent_widget = widget.getparent()
            
            if widget.get('class') is None:
                parent_with_class = find_parent_with_class(widget)
                if parent_with_class is not None:
                    widget_class = parent_with_class.get('class')  
                    parent_widget = parent_with_class
            
            widget_name = widget.get('name')  

            iconset_element = element.find('iconset')

            if iconset_element is not None:
                icon_url = None
                
                if 'resource' in iconset_element.attrib:
                    # Extract the QRC file path from the 'resource' attribute
                    qrc_file_path = iconset_element.attrib['resource']
                    # Extract the folder name containing the QRC file
                    qrc_folder = os.path.dirname(qrc_file_path)
                    # Combine with the relative path within the <iconset> tag
                    relative_path = iconset_element.find("normaloff").text
                    icon_url = replace_url_prefix(relative_path, qrc_folder)
                else:
                    # Handle case without resource attribute
                    relative_path = iconset_element.find("normaloff").text
                    if relative_path.startswith(':/'):
                        # QRC resource path
                        resource_parts = relative_path.split('/')
                        if len(resource_parts) > 2:
                            icon_url = os.path.join(*resource_parts[2:])
                        else:
                            icon_url = relative_path
                    else:
                        # Regular file path
                        ui_dir = os.path.dirname(path)
                        abs_path = os.path.abspath(os.path.join(ui_dir, relative_path))
                        project_root = projectRoot()
                        try:
                            icon_url = os.path.relpath(abs_path, project_root)
                        except ValueError:
                            icon_url = abs_path
                
                # Clear the original icon text
                iconset_element.find("normaloff").text = ""

                # Handle different parent widget types
                if parent_widget.tag == 'widget' and widget_class == 'QWidget' and parent_widget.get('class') == "QTabWidget":
                    tab_name = parent_widget.get('name')
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QTabWidget": tab_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QTabWidget": tab_name, "name": widget_name, "icon": icon_url}]
                    logDebug(f"Processed QTabWidget item: {tab_name} -> {widget_name}")
                
                elif parent_widget.tag == 'widget' and widget_class == 'QTableWidget':
                    table_name = parent_widget.get('name')
                    if table_items > 0:
                        widget_name = "__qtablewidgetitem" + str(table_items)
                    else:
                        widget_name = "__qtablewidgetitem"
                    widget.set('name', widget_name)

                    table_items = table_items + 1

                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QTableWidget": table_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QTableWidget": table_name, "name": widget_name, "icon": icon_url}]
                    logDebug(f"Processed QTableWidget item: {table_name} -> {widget_name}")
                
                elif parent_widget.tag == 'widget' and widget_class == 'QTreeWidget':
                    tree_name = parent_widget.get('name')
                    if tree_items > 0:
                        widget_name = "qtreewidgetitem" + str(tree_items)
                    else:
                        widget_name = "qtreewidgetitem"

                    tree_items += 1
                    
                    widget.set('name', widget_name)
                    
                    if "QTreeWidget" in widget_info:
                        widget_info["QTreeWidget"].append({"QTreeWidget": tree_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info["QTreeWidget"] = [{"QTreeWidget": tree_name, "name": widget_name, "icon": icon_url}]
                    logDebug(f"Processed QTreeWidget item: {tree_name} -> {widget_name}")

                elif parent_widget.tag == 'widget' and widget_class == 'QToolBox':
                    tab_name = parent_widget.get('name')
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QToolBox": tab_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QToolBox": tab_name, "name": widget_name, "icon": icon_url}]
                    logDebug(f"Processed QToolBox item: {tab_name} -> {widget_name}")

                else:
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"name": widget_name, "icon": icon_url}]
                    logDebug(f"Processed icon for: {widget_class} - {widget_name}")
                
                processed_widgets += 1
        
        if widget_class == 'QCustomThemeDarkLightToggle':
            dark_theme_icon_element = element.find("property[@name='darkThemeIcon']/iconset")
            light_theme_icon_element = element.find("property[@name='lightThemeIcon']/iconset")

            # Extract resource paths for darkThemeIcon
            dark_theme_icon_url = None
            if dark_theme_icon_element is not None:
                if 'resource' in dark_theme_icon_element.attrib:
                    resource_path = dark_theme_icon_element.attrib.get('resource')
                    qrc_folder = os.path.dirname(resource_path)
                    if qrc_folder:
                        relative_path = dark_theme_icon_element.find("normaloff").text
                        dark_theme_icon_url = replace_url_prefix(relative_path, qrc_folder)
                else:
                    relative_path = dark_theme_icon_element.find("normaloff").text
                    if relative_path.startswith(':/'):
                        resource_parts = relative_path.split('/')
                        if len(resource_parts) > 2:
                            dark_theme_icon_url = os.path.join(*resource_parts[2:])
                        else:
                            dark_theme_icon_url = relative_path
                    else:
                        ui_dir = os.path.dirname(path)
                        abs_path = os.path.abspath(os.path.join(ui_dir, relative_path))
                        project_root = projectRoot()
                        try:
                            dark_theme_icon_url = os.path.relpath(abs_path, project_root)
                        except ValueError:
                            dark_theme_icon_url = abs_path

            # Extract resource paths for lightThemeIcon
            light_theme_icon_url = None
            if light_theme_icon_element is not None:
                if 'resource' in light_theme_icon_element.attrib:
                    resource_path = light_theme_icon_element.attrib.get('resource')
                    qrc_folder = os.path.dirname(resource_path)
                    if qrc_folder:
                        relative_path = light_theme_icon_element.find("normaloff").text
                        light_theme_icon_url = replace_url_prefix(relative_path, qrc_folder)
                else:
                    relative_path = light_theme_icon_element.find("normaloff").text
                    if relative_path.startswith(':/'):
                        resource_parts = relative_path.split('/')
                        if len(resource_parts) > 2:
                            light_theme_icon_url = os.path.join(*resource_parts[2:])
                        else:
                            light_theme_icon_url = relative_path
                    else:
                        ui_dir = os.path.dirname(path)
                        abs_path = os.path.abspath(os.path.join(ui_dir, relative_path))
                        project_root = projectRoot()
                        try:
                            light_theme_icon_url = os.path.relpath(abs_path, project_root)
                        except ValueError:
                            light_theme_icon_url = abs_path

            # Append dark and light theme icons
            if widget_class in widget_info:
                widget_info[widget_class].append({
                    "name": widget_name,
                    "darkThemeIcon": dark_theme_icon_url,
                    "lightThemeIcon": light_theme_icon_url
                })
            else:
                widget_info[widget_class] = [{
                    "name": widget_name,
                    "darkThemeIcon": dark_theme_icon_url,
                    "lightThemeIcon": light_theme_icon_url
                }]
            processed_widgets += 1
            logDebug(f"Processed QCustomThemeDarkLightToggle: {widget_name}")

        if 'name' in element.attrib and element.attrib['name'] == 'pixmap':
            widget = element.getparent()
            widget_class = widget.get('class')
            widget_name = widget.get('name')
            
            pixmap_element = element.find('pixmap')
            
            if pixmap_element is not None:
                pixmap_url = None
                
                if 'resource' in pixmap_element.attrib:
                    qrc_file_path = pixmap_element.attrib['resource']
                    qrc_folder = os.path.dirname(qrc_file_path)
                    relative_path = pixmap_element.text
                    pixmap_url = replace_url_prefix(relative_path, qrc_folder)
                else:
                    relative_path = pixmap_element.text
                    if relative_path.startswith(':/'):
                        resource_parts = relative_path.split('/')
                        if len(resource_parts) > 2:
                            pixmap_url = os.path.join(*resource_parts[2:])
                        else:
                            pixmap_url = relative_path
                    else:
                        ui_dir = os.path.dirname(path)
                        abs_path = os.path.abspath(os.path.join(ui_dir, relative_path))
                        project_root = projectRoot()
                        try:
                            pixmap_url = os.path.relpath(abs_path, project_root)
                        except ValueError:
                            pixmap_url = abs_path

                if widget_class in widget_info:
                    widget_info[widget_class].append({"name": widget_name, "pixmap": pixmap_url})
                else:
                    widget_info[widget_class] = [{"name": widget_name, "pixmap": pixmap_url}]
                processed_widgets += 1
                logDebug(f"Processed pixmap for: {widget_class} - {widget_name}")

    # Generate JSON file
    base_name, _ = os.path.splitext(os.path.basename(path))
    json_file_name = f"{base_name}.json"
    json_path = os.path.join(projectRoot(), "generated-files/json", json_file_name)
    
    with open(json_path, "w") as json_file:
        json.dump(widget_info, json_file, indent=2)
    
    logDebug(f"Generated JSON: {json_file_name} with {processed_widgets} widgets")

    replacements_list = []  # Can be configured as needed

    # Create modified UI file
    base_name, extension = os.path.splitext(os.path.basename(path))
    new_file_name = "new_{}{}".format(base_name, extension)
    new_file_path = os.path.join(projectRoot(), "generated-files/ui", new_file_name)
    
    tree.write(new_file_path, encoding="utf-8", xml_declaration=True)
    logDebug(f"Generated modified UI: {new_file_name}")

    # Generate Python source
    replace_attributes_values(path, replacements_list, src_output_dir=src_output_dir)
    
    logSuccess(f" Completed processing {os.path.basename(path)}")
    logInfo(f"   ├─ JSON: {json_file_name}")
    logInfo(f"   ├─ UI:   {new_file_name}")
    logInfo(f"   └─ Python: ui_{base_name}.py")

def update_json(data, json_file_name):
    """Save JSON data to file."""
    json_path = os.path.join(projectRoot(), "generated-files/json", json_file_name)
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=2)
    logDebug(f"JSON file updated: {json_file_name}")

def start_file_listener(file_or_folder, qt_binding="PySide6", src_output_dir="src"):
    """Start file listener with specified source output directory."""
    if qt_binding is None:
        qt_binding = "PySide6"
    if qt_binding not in ["PySide6", "PyQt6"]:
        logError(f" {qt_binding} is not a supported Qt binding "
                 "(Custom_Widgets supports PySide6 and PyQt6)")
        return

    qtpy.API_NAME = qt_binding
    os.environ['QT_API'] = qt_binding.lower()

    logInfo("")
    logInfo(" " + "=" * 60)
    logInfo(" STARTING CUSTOM WIDGETS FILE MONITOR")
    logInfo(" " + "=" * 60)
    logInfo(f"Qt Binding: {qt_binding}")
    logInfo(f"Source output: {os.path.abspath(src_output_dir)}")

    # Create source output directory if it doesn't exist
    if not os.path.exists(src_output_dir):
        os.makedirs(src_output_dir)
        logDebug(f"Created source directory: {src_output_dir}")

    files_to_monitor = []

    if os.path.isfile(file_or_folder):
        # If the provided path is a file, check if it's a .ui file
        if not file_or_folder.lower().endswith(".ui"):
            raise ValueError("The file to monitor must be a .ui file.")
        if not os.path.exists(file_or_folder):
            raise FileNotFoundError(f"The file {file_or_folder} does not exist.")

        files_to_monitor.append(file_or_folder)
        logSuccess(f" Monitoring single file: {file_or_folder}")

    elif os.path.isdir(file_or_folder):
        # If the provided path is a directory, get all .ui files in the folder
        ui_files = [f for f in os.listdir(file_or_folder) if f.lower().endswith(".ui")]

        if not ui_files:
            logWarning(" No .ui files found in the specified folder.")
            return

        logSuccess(f" Monitoring folder: {file_or_folder}")
        logInfo(f"Found {len(ui_files)} UI files:")
        for ui_file in ui_files:
            logInfo(f"   • {ui_file}")
            file_path = os.path.join(file_or_folder, ui_file)
            files_to_monitor.append(file_path)

    else:
        logError(" Invalid path. Please provide a valid .ui file or folder.")
        return

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create a FileMonitor instance with source output directory
    file_monitor = FileMonitor(files_to_monitor, refresh=True, src_output_dir=src_output_dir)

    logInfo("")
    logInfo(" File monitor is running. Press Ctrl+C to stop.")
    logInfo("⏳ Waiting for file changes...")
    logInfo("")

    sys.exit(app.exec())

def replace_attributes_values(ui_file_path, replacements, root=None, tree=None, src_output_dir="src"):
    """
    Replace attributes in UI file and generate Python output.
    
    Parameters:
        ui_file_path (str): Path to the UI file
        replacements (list): List of replacement specifications
        root, tree: XML root and tree (optional)
        src_output_dir (str): Directory for output Python source files
    """
    logDebug(f"Generating Python source in: {src_output_dir}")
    
    # Parse the XML file
    if root is None:
        tree = ET.parse(ui_file_path)
        root = tree.getroot()

    # Find and remove the <resources> element
    resources_elements = root.findall(".//resources")
    for resources_element in resources_elements:
        root.remove(resources_element)
        logDebug("Removed <resources> tag")

    # Iterate over the replacement specifications
    for tag, attribute, old_value, new_value in replacements:
        elements = root.findall(".//{}".format(tag))
        for element in elements:
            if attribute in element.attrib and element.attrib[attribute] == old_value:
                element.attrib[attribute] = new_value
                logDebug(f"Replaced {tag}.{attribute}: {old_value} -> {new_value}")

    # Create modified UI file
    base_name, extension = os.path.splitext(os.path.basename(ui_file_path))
    new_file_name = "new_{}{}".format(base_name, extension)
    new_file_path = os.path.join(projectRoot(), "generated-files/ui", new_file_name)

    # Save the modified XML
    tree.write(new_file_path, encoding="utf-8", xml_declaration=True)

    # Append custom widgets
    widget_list = [
        ("QPushButton", "QPushButton", "Custom_Widgets.Theme.h", 1),
        ("QLabel", "QLabel", "Custom_Widgets.Theme.h", 1)
    ]
    append_custom_widgets(new_file_path, widget_list)

    # Generate Python output
    ui_output_py_path = os.path.join(src_output_dir, "ui_"+base_name.replace(".ui", "")+".py")
    uiToPy(new_file_path, ui_output_py_path)
    assign_private_vars_to_instance_in_file(ui_output_py_path)
    
    logDebug(f"Python source generated: {ui_output_py_path}")

    return root

def assign_private_vars_to_instance_in_file(py_file_path):
    """Convert private variables to instance variables in generated Python file."""
    logDebug(f"Processing Python file: {os.path.basename(py_file_path)}")
    
    with open(py_file_path, 'r') as file:
        content = file.read()

    # Find all private variable names
    private_vars = set(re.findall(r'(__+\w+)', content))
    
    vars_converted = 0
    for var_name in private_vars:
        if var_name.startswith('__'):
            new_var_name = 'self.' + var_name[2:]
            content = re.sub(rf'\b{var_name}\b', new_var_name, content)
            vars_converted += 1

    with open(py_file_path, 'w') as file:
        file.write(content)
    
    if vars_converted > 0:
        logDebug(f"Converted {vars_converted} private variables to instance variables")

def append_custom_widgets(ui_file_path, widget_list):
    """Append custom widget definitions to UI file."""
    logDebug(f"Appending custom widgets to: {os.path.basename(ui_file_path)}")
    
    tree = ET.parse(ui_file_path)
    root = tree.getroot()

    # Find or create customwidgets section
    customwidgets_section = root.find(".//customwidgets")
    if customwidgets_section is None:
        customwidgets_section = ET.Element("customwidgets")
        root.append(customwidgets_section)
        logDebug("Created new <customwidgets> section")

    widgets_added = 0
    for widget_spec in widget_list:
        widget_class, widget_extends, widget_header, widget_container = widget_spec

        # Check if custom widget already exists
        existing = customwidgets_section.findall(".//customwidget[class='{}']".format(widget_class))
        if existing:
            logDebug(f"Custom widget {widget_class} already exists, skipping")
            continue

        # Create new customwidget element
        customwidget = ET.Element("customwidget")
        
        ET.SubElement(customwidget, "class").text = widget_class
        ET.SubElement(customwidget, "extends").text = widget_extends
        ET.SubElement(customwidget, "header", location="global").text = widget_header
        ET.SubElement(customwidget, "container").text = str(widget_container)

        customwidgets_section.append(customwidget)
        widgets_added += 1
        logDebug(f"Added custom widget: {widget_class}")

    tree.write(ui_file_path, encoding="utf-8", xml_declaration=True)
    
    if widgets_added > 0:
        logDebug(f"Added {widgets_added} custom widgets to UI file")

def start_ui_conversion(file_or_folder, qt_binding="PySide6", src_output_dir="src"):
    """Start UI conversion with specified source output directory."""
    if qt_binding is None:
        qt_binding = "PySide6"
    if qt_binding not in ["PySide6", "PyQt6"]:
        logError(f" {qt_binding} is not a supported Qt binding "
                 "(Custom_Widgets supports PySide6 and PyQt6)")
        return

    qtpy.API_NAME = qt_binding
    os.environ['QT_API'] = qt_binding.lower()

    logInfo("")
    logInfo(" " + "=" * 60)
    logInfo(" CUSTOM WIDGETS UI CONVERSION")
    logInfo(" " + "=" * 60)
    logInfo(f"Qt Binding: {qt_binding}")
    logInfo(f"Source output: {os.path.abspath(src_output_dir)}")

    files_to_convert = []

    if os.path.isfile(file_or_folder):
        if not file_or_folder.lower().endswith(".ui"):
            raise ValueError("The file to convert must be a .ui file.")
        if not os.path.exists(file_or_folder):
            raise FileNotFoundError(f"The file {file_or_folder} does not exist.")

        files_to_convert.append(file_or_folder)
        logSuccess(f" Converting single file: {file_or_folder}")

    elif os.path.isdir(file_or_folder):
        ui_files = [f for f in os.listdir(file_or_folder) if f.lower().endswith(".ui")]

        if not ui_files:
            logWarning(" No .ui files found in the specified folder.")
            return

        logSuccess(f" Converting folder: {file_or_folder}")
        logInfo(f"Found {len(ui_files)} UI files:")
        for ui_file in ui_files:
            logInfo(f"   • {ui_file}")
            file_path = os.path.join(file_or_folder, ui_file)
            files_to_convert.append(file_path)

    else:
        logError(" Invalid path. Please provide a valid .ui file or folder.")
        return
    
    # Create necessary directories
    directories = [
        os.path.join(projectRoot(), "generated-files/ui"),
        os.path.join(projectRoot(), "generated-files/json"),
        src_output_dir
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logDebug(f"Created directory: {directory}")
    
    # Convert files
    logInfo("")
    logInfo("Starting conversion...")
    logInfo("-" * 40)
    
    successful = 0
    failed = 0
    
    for file in files_to_convert:
        try:
            convert_file(file, src_output_dir)
            successful += 1
        except Exception as e:
            logError(f"Failed to convert {os.path.basename(file)}: {e}")
            failed += 1

    logInfo("-" * 40)
    logSuccess(f" Conversion complete! Successful: {successful}, Failed: {failed}")
    logInfo(f" Output locations:")
    logInfo(f"   ├─ Python source: {os.path.abspath(src_output_dir)}")
    logInfo(f"   ├─ Modified UI:  {os.path.abspath(os.path.join('generated-files', 'ui'))}")
    logInfo(f"   └─ JSON data:    {os.path.abspath(os.path.join('generated-files', 'json'))}")

class QSsFileMonitor(QObject):
    """Monitors QSS/SCSS files for changes and auto-reloads styles."""
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QSsFileMonitor, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, "_initialized"):
            return
        super().__init__(parent)

        self.qss_watcher = QFileSystemWatcher()
        self.qss_watcher.connected = False
        self.shared_data = SharedData()
        self.liveCompileQss = True
        self.jsonStyleSheets = []
        self.themeEngine = None

        self.destroyed.connect(lambda: logWarning("Global QSsFileMonitor deleted."))
        self._initialized = True

    @staticmethod
    def instance():
        if QSsFileMonitor._instance is None:
            QSsFileMonitor()
        return QSsFileMonitor._instance

    def start_qss_file_listener(self, theme_engine):
        """Start monitoring QSS/SCSS files for changes."""
        if not self.themeEngine:
            self.themeEngine = theme_engine
            
        if not self.liveCompileQss:
            logInfo("Live QSS compile disabled.")
            return

        default_sass_path = os.path.abspath(os.path.join(projectRoot(), 'Qss/scss/defaultStyle.scss'))

        if os.path.isfile(default_sass_path):
            if not self.shared_data.url_exists(default_sass_path):
                self.qss_watcher.addPath(default_sass_path)
                self.shared_data.add_file_url(default_sass_path)
                logDebug(f"Added SASS file to watcher: {default_sass_path}")

            # Monitor JSON files
            for json_file in self.jsonStyleSheets:
                json_file_path = os.path.abspath(os.path.join(projectRoot(), json_file))
                if os.path.isfile(json_file_path):
                    self.qss_watcher.addPath(json_file_path)
                    logInfo(f" Live monitoring {json_file} for changes")
                else:
                    logError(f" JSON file not found: {json_file_path}")

            # Connect signal
            try:
                if self.qss_watcher.connected:
                    self.qss_watcher.fileChanged.disconnect()
            except Exception:
                pass

            self.qss_watcher.fileChanged.connect(self.qss_file_changed)
            self.qss_watcher.connected = True
            logSuccess(f" Live monitoring QSS/SCSS files")
            logInfo(f"   • {os.path.basename(default_sass_path)}")
            for json_file in self.jsonStyleSheets:
                logInfo(f"   • {json_file}")

        else:
            logError(f" SASS file not found: {default_sass_path}")

    def qss_file_changed(self, file_path, live_compile=False):
        """Handle QSS/SCSS file changes."""
        if not self.liveCompileQss and not live_compile:
            logInfo(f"File change ignored (liveCompileQss=False)")
            return

        logInfo("")
        logInfo(" " + "=" * 50)
        logInfo(f" STYLE FILE CHANGED: {os.path.basename(file_path)}")
        logInfo(" " + "=" * 50)

        if file_path.endswith('.json'):
            logInfo(" Reloading JSON settings...")
            QAppSettings.updateAppSettings(self, generateIcons=False, reloadJson=True)
            logSuccess(" JSON settings reloaded")
        else:
            logInfo(" Recompiling styles...")
            QAppSettings.updateAppSettings(self, generateIcons=False, reloadJson=False)
            logSuccess(" Styles recompiled")

    def stop_qss_file_listener(self):
        """Stop monitoring QSS/SCSS files."""
        try:
            self.qss_watcher.fileChanged.disconnect()
            logInfo("Stopped QSS file monitoring")
        except Exception:
            pass

        self.qss_watcher = QFileSystemWatcher()