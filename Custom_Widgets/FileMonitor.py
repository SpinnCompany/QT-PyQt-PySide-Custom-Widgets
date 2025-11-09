import sys
import os
import json
from qtpy.QtCore import QObject, QFileSystemWatcher
from qtpy.QtWidgets import QApplication
from termcolor import colored
import xml.etree.ElementTree as ET
from lxml import etree
import re

import qtpy

from Custom_Widgets.QAppSettings import QAppSettings
# from Custom_Widgets.QCustomTheme import QCustomTheme
from Custom_Widgets.Utils import replace_url_prefix, SharedData, is_in_designer, uiToPy
from Custom_Widgets.Log import *

class FileMonitor(QObject):
    def __init__(self, files_to_monitor, refresh=False):
        super().__init__()
        file_folder = os.path.join(os.getcwd(), "generated-files")
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        file_folder = os.path.join(os.getcwd(), "generated-files/ui")
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        file_folder = os.path.join(os.getcwd(), "generated-files/json")
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        file_folder = os.path.join(os.getcwd(), "src")
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)

        self.files_to_monitor = files_to_monitor
        self.refresh = refresh
        self.fileSystemWatchers = []
        
        # Create a QFileSystemWatcher for folder monitoring
        if refresh:
            self.monitor_folders()
        else:
            # Monitor files if no refresh argument
            self.monitor_files(files_to_monitor)

    def monitor_folders(self):
        # Monitor the folder for changes (e.g., new .ui files added)
        folder_to_monitor = os.path.dirname(self.files_to_monitor[0]) if self.files_to_monitor else os.getcwd()
        self.folder_watcher = QFileSystemWatcher([folder_to_monitor])
        self.folder_watcher.directoryChanged.connect(self.on_folder_change)
        
        # Initially monitor the files already in the folder
        self.monitor_files(self.files_to_monitor)

    def monitor_files(self, files_to_monitor):
        # Clear any existing file watchers
        for watcher in self.fileSystemWatchers:
            watcher.fileChanged.disconnect(self.on_file_change)
        self.fileSystemWatchers.clear()

        # Create a QFileSystemWatcher for each file
        self.fileSystemWatchers = [QFileSystemWatcher([file]) for file in files_to_monitor]

        # Connect the fileChanged signal for each watcher
        for watcher in self.fileSystemWatchers:
            watcher.fileChanged.connect(self.on_file_change)

        print(f"Monitoring {len(self.files_to_monitor)} files...")

    def on_file_change(self, path):
        print(f"File {path} has been changed!")
        # Handle file modification event
        self.update_file_list()
        convert_file(path)

    def on_folder_change(self, path):
        # Refresh the list of .ui files to monitor if a folder is updated
        self.update_file_list()

    def update_file_list(self):
        # Find all .ui files in the folder
        folder_path = os.path.dirname(self.files_to_monitor[0]) if self.files_to_monitor else os.getcwd()
        ui_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".ui")]

        # Update the list of monitored files if there are new files or missing files
        new_files = set(ui_files) - set(self.files_to_monitor)
        removed_files = set(self.files_to_monitor) - set(ui_files)

        if new_files or removed_files:
            print(f"Updating monitored files: {len(new_files)} new files, {len(removed_files)} removed files")
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

def convert_file(path):
    # Load the UI file
    tree = etree.parse(path)
    root = tree.getroot()

    # Initialize an empty dictionary to store widget names and their icons
    widget_info = {}
    table_items = 0
    tree_items = 0

    # Iterate through each element in the UI file
    for element in root.iter():
        # Get the widget class and name
        widget_class = element.attrib.get('class')
        widget_name = element.attrib.get('name')
        
        # Print for debugging
        # print(f"Widget Class: {widget_class}, Widget Name: {widget_name}")

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
                if 'resource' in iconset_element.attrib:
                    # Extract the QRC file path from the 'resource' attribute
                    qrc_file_path = iconset_element.attrib['resource']
                    # Extract the folder name containing the QRC file
                    qrc_folder = os.path.dirname(qrc_file_path)
                    # Combine with the relative path within the <iconset> tag
                    relative_path = iconset_element.find("normaloff").text
                    
                    icon_url = replace_url_prefix(relative_path, qrc_folder)

                else:
                    icon_url = generate_relative_path(path, iconset_element.find("normaloff").text)
                
                iconset_element.find("normaloff").text = ""

                if parent_widget.tag == 'widget' and widget_class == 'QWidget' and parent_widget.get('class') == "QTabWidget":
                    # Get the tab name
                    tab_name = parent_widget.get('name')
                    # Add the widget info to the dictionary
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QTabWidget": tab_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QTabWidget": tab_name, "name": widget_name, "icon": icon_url}]
                
                elif parent_widget.tag == 'widget' and widget_class == 'QTableWidget':
                    table_name = parent_widget.get('name')
                    if table_items > 0:
                        widget_name = "__qtablewidgetitem" + str(table_items)
                    else:
                        widget_name = "__qtablewidgetitem"
                    # set parent name
                    widget.set('name', widget_name)

                    table_items = table_items + 1

                    # Add the widget info to the dictionary
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QTableWidget": table_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QTableWidget": table_name, "name": widget_name, "icon": icon_url}]
                
                elif parent_widget.tag == 'widget' and widget_class == 'QTreeWidget':
                    tree_name = parent_widget.get('name')
                    if tree_items > 0:
                        widget_name = "qtreewidgetitem" + str(tree_items)
                    else:
                        widget_name = "qtreewidgetitem"

                    tree_items += 1
                    
                    # Set parent name
                    widget.set('name', widget_name)
                    
                    # Add the widget info to the dictionary
                    if "QTreeWidget" in widget_info:
                        widget_info["QTreeWidget"].append({"QTreeWidget": tree_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info["QTreeWidget"] = [{"QTreeWidget": tree_name, "name": widget_name, "icon": icon_url}]

                elif parent_widget.tag == 'widget' and widget_class == 'QToolBox':
                    # Get the tab name
                    tab_name = parent_widget.get('name')
                    # Add the widget info to the dictionary
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"QToolBox": tab_name, "name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"QToolBox": tab_name, "name": widget_name, "icon": icon_url}]

                else:
                    # Add the widget info to the dictionary
                    if widget_class in widget_info:
                        widget_info[widget_class].append({"name": widget_name, "icon": icon_url})
                    else:
                        widget_info[widget_class] = [{"name": widget_name, "icon": icon_url}]
        
        if widget_class == 'QCustomThemeDarkLightToggle':
            dark_theme_icon_element = element.find("property[@name='darkThemeIcon']/iconset")
            light_theme_icon_element = element.find("property[@name='lightThemeIcon']/iconset")

            # Extract resource paths from the property tag for darkThemeIcon
            dark_theme_icon_url = None
            if dark_theme_icon_element is not None:
                resource_path = dark_theme_icon_element.attrib.get('resource')
                qrc_folder = os.path.dirname(resource_path)
                if qrc_folder:
                    relative_path = dark_theme_icon_element.find("normaloff").text
                    dark_theme_icon_url = replace_url_prefix(relative_path, qrc_folder)

            # Extract resource paths from the property tag for lightThemeIcon
            light_theme_icon_url = None
            if light_theme_icon_element is not None:
                resource_path = light_theme_icon_element.attrib.get('resource')
                qrc_folder = os.path.dirname(resource_path)
                if qrc_folder:
                    relative_path = light_theme_icon_element.find("normaloff").text
                    light_theme_icon_url = replace_url_prefix(relative_path, qrc_folder)

            # Append dark and light theme icons to the widget_info
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

        if 'name' in element.attrib and element.attrib['name'] == 'pixmap':
            widget = element.getparent()  # Get the parent widget
            widget_class = widget.get('class')  # Get the widget class
            widget_name = widget.get('name')  # Get the widget name
            
            pixmap_element = element.find('pixmap')
            
            if pixmap_element is not None:
                if 'resource' in pixmap_element.attrib:
                    # Extract the QRC file path from the 'resource' attribute
                    qrc_file_path = pixmap_element.attrib['resource']
                    # Extract the folder name containing the QRC file
                    qrc_folder = os.path.dirname(qrc_file_path)
                    # Combine with the relative path within the <pixmap> tag
                    relative_path = pixmap_element.text
                    pixmap_url = replace_url_prefix(relative_path, qrc_folder)
                else:
                    pixmap_url = generate_relative_path(path, pixmap_element.text)

                # Add the widget info to the dictionary
                if widget_class in widget_info:
                    widget_info[widget_class].append({"name": widget_name, "pixmap": pixmap_url})
                else:
                    widget_info[widget_class] = [{"name": widget_name, "pixmap": pixmap_url}]


    # Generate JSON file name from UI name
    base_name, _ = os.path.splitext(os.path.basename(path))
    json_file_name = f"{base_name}.json"

    # Update JSON data for the specific file
    update_json(widget_info, json_file_name)

    replacements_list = [
        # ("widget", "class", "QPushButton", "QPushButtonThemed"),
        # ("widget", "class", "QLabel", "QLabelThemed"),
    ]

    # Create a new file name
    base_name, extension = os.path.splitext(os.path.basename(path))
    new_file_name = "new_{}{}".format(base_name, extension)
    new_file_path = os.path.join(os.getcwd(), "generated-files/ui/"+new_file_name)
    # print(new_file_name)
    # Save the modified XML to the new file
    tree.write(new_file_path, encoding="utf-8", xml_declaration=True)

    replace_attributes_values(path, replacements_list)

def update_json(data, json_file_name):
    # Save the JSON data back to the file
    json_path = os.path.join(os.getcwd(), "generated-files/json/"+json_file_name)
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=2)

def generate_relative_path(ui_path, relative_url):
    # Determine the directory of the UI file
    ui_dir = os.path.dirname(ui_path)
    
    # Combine UI directory with the relative URL
    abs_path = os.path.abspath(os.path.join(ui_dir, relative_url))
    
    return abs_path
    
def start_file_listener(file_or_folder, qt_binding="PySide6"):
    if qt_binding is None:
        qt_binding = "PySide6"
    if qt_binding not in ["PySide6", "PySide2", "PyQt6", "PyQt5"]:
        print(colored((str(qt_binding) + " is not a valid Qt binding/API Name"), "red"))
        return

    qtpy.API_NAME = qt_binding
    os.environ['QT_API'] = qt_binding.lower()

    files_to_monitor = []

    if os.path.isfile(file_or_folder):
        # If the provided path is a file, check if it's a .ui file
        if not file_or_folder.lower().endswith(".ui"):
            raise ValueError("The file to monitor must be a .ui file.")
        if not os.path.exists(file_or_folder):
            raise FileNotFoundError(f"The file {file_or_folder} does not exist.")

        files_to_monitor.append(file_or_folder)
        print(f"Monitoring file: {file_or_folder}")

    elif os.path.isdir(file_or_folder):
        # If the provided path is a directory, get all .ui files in the folder
        ui_files = [f for f in os.listdir(file_or_folder) if f.lower().endswith(".ui")]

        if not ui_files:
            print("No .ui files found in the specified folder.")
            return

        print(f"Monitoring files in folder: {file_or_folder}")
        print(f".ui files found: {', '.join(ui_files)}")
        for ui_file in ui_files:
            file_path = os.path.join(file_or_folder, ui_file)
            files_to_monitor.append(file_path)

    else:
        print("Invalid path. Please provide a valid .ui file or folder.")
        return

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create a FileMonitor instance with the list of files to monitor
    file_monitor = FileMonitor(files_to_monitor, refresh=True)

    sys.exit(app.exec_())  # Start the application event loop

def replace_attributes_values(ui_file_path, replacements, root=None, tree=None):
    # Parse the XML file
    if root is None:
        tree = ET.parse(ui_file_path)
        root = tree.getroot()

    # Find and remove the <resources> element
    resources_elements = root.findall(".//resources")
    for resources_element in resources_elements:
        root.remove(resources_element)

    # Iterate over the replacement specifications
    for tag, attribute, old_value, new_value in replacements:
        # Find all elements with the specified tag
        elements = root.findall(".//{}".format(tag))

        # Replace the attribute value for each matching element
        for element in elements:
            if attribute in element.attrib and element.attrib[attribute] == old_value:
                element.attrib[attribute] = new_value

    # Create a new file name
    base_name, extension = os.path.splitext(os.path.basename(ui_file_path))
    new_file_name = "new_{}{}".format(base_name, extension)
    new_file_path = os.path.join(os.getcwd(), "generated-files/ui/"+new_file_name)

    # Save the modified XML to the new file
    tree.write(new_file_path, encoding="utf-8", xml_declaration=True)

    # Append custom widgets
    widget_list = [
        ("QPushButton", "QPushButton", "Custom_Widgets.Theme.h", 1),
        ("QLabel", "QLabel", "Custom_Widgets.Theme.h", 1)
    ]
    append_custom_widgets(new_file_path, widget_list)

    ui_output_py_path = os.path.join(os.getcwd(), "src/ui_"+base_name.replace(".ui", "")+".py")
    uiToPy(new_file_path, ui_output_py_path)
    assign_private_vars_to_instance_in_file(ui_output_py_path)

    return root  # Return the root element after modification

def assign_private_vars_to_instance_in_file(py_file_path):
    # Read the contents of the generated Python file
    with open(py_file_path, 'r') as file:
        content = file.read()

    # Find all private variable names with 2 to 3 leading underscores (e.g., __qtreewidgetitem, ___qtreewidgetitem)
    private_vars = set(re.findall(r'(__+\w+)', content))

    # Replace each private variable instance with `self.<variable_name>` for the first 2 underscores only
    for var_name in private_vars:
        # Only replace if there are 2 underscores (i.e., convert __ to self.)
        if var_name.startswith('__'):
            new_var_name = 'self.' + var_name[2:]  # Strip only the first two underscores manually
            content = re.sub(rf'\b{var_name}\b', new_var_name, content)

    # Write the modified content back to the .py file
    with open(py_file_path, 'w') as file:
        file.write(content)

def append_custom_widgets(ui_file_path, widget_list):
    # Parse the existing XML file
    tree = ET.parse(ui_file_path)
    root = tree.getroot()

    # Find the customwidgets section or create it if it doesn't exist
    customwidgets_section = root.find(".//customwidgets")
    if customwidgets_section is None:
        customwidgets_section = ET.Element("customwidgets")
        root.append(customwidgets_section)

    for widget_spec in widget_list:
        widget_class, widget_extends, widget_header, widget_container = widget_spec

        # Check if a customwidget with the specified class already exists
        existing_customwidgets = customwidgets_section.findall(".//customwidget[class='{}']".format(widget_class))
        if existing_customwidgets:
            # Custom widget with the specified class already exists, skip
            continue

        # Create a new customwidget element
        customwidget = ET.Element("customwidget")

        # Add class, extends, header, and container elements to the customwidget
        class_element = ET.SubElement(customwidget, "class")
        class_element.text = widget_class

        extends_element = ET.SubElement(customwidget, "extends")
        extends_element.text = widget_extends

        header_element = ET.SubElement(customwidget, "header", location="global")
        header_element.text = widget_header

        container_element = ET.SubElement(customwidget, "container")
        container_element.text = str(widget_container)

        # Append the new customwidget to the customwidgets section
        customwidgets_section.append(customwidget)

    # Save the modified XML back to the file
    tree.write(ui_file_path, encoding="utf-8", xml_declaration=True)


def remove_resources_tag(ui_file_path):
    # Parse the XML file
    tree = ET.parse(ui_file_path)
    root = tree.getroot()

    # Find and remove the <resources> element
    resources_elements = root.findall(".//resources")
    for resources_element in resources_elements:
        parent = resources_element.getparent()
        parent.remove(resources_element)

    # Create a new file name
    base_name, extension = os.path.splitext(os.path.basename(ui_file_path))
    new_file_name = "generated-files/ui/new_{}{}".format(base_name, extension)
    new_file_path = os.path.join(os.path.dirname(ui_file_path), new_file_name)

    # Save the modified XML to the new file
    tree.write(new_file_path, encoding="utf-8", xml_declaration=True)

    return root  # Return the root element after modification


def start_ui_conversion(file_or_folder, qt_binding="PySide6"):
    if qt_binding is None:
        qt_binding = "PySide6"
    if qt_binding not in ["PySide6", "PySide2", "PyQt6", "PyQt5"]:
        print(colored((str(qt_binding) + " is not a valid Qt binding/API Name"), "red"))
        return

    qtpy.API_NAME = qt_binding
    os.environ['QT_API'] = qt_binding.lower()

    files_to_convert = []

    if os.path.isfile(file_or_folder):
        # If the provided path is a file, check if it's a .ui file
        if not file_or_folder.lower().endswith(".ui"):
            raise ValueError("The file to monitor must be a .ui file.")
        if not os.path.exists(file_or_folder):
            raise FileNotFoundError(f"The file {file_or_folder} does not exist.")

        files_to_convert.append(file_or_folder)
        print(f"Converting file: {file_or_folder}")

    elif os.path.isdir(file_or_folder):
        # If the provided path is a directory, get all .ui files in the folder
        ui_files = [f for f in os.listdir(file_or_folder) if f.lower().endswith(".ui")]

        if not ui_files:
            print("No .ui files found in the specified folder.")
            return

        print(f"Converting files in folder: {file_or_folder}")
        print(f".ui files found: {', '.join(ui_files)}")
        for ui_file in ui_files:
            file_path = os.path.join(file_or_folder, ui_file)
            files_to_convert.append(file_path)

    else:
        print("Invalid path. Please provide a valid .ui file or folder.")
        return
    
    file_folder = os.path.join(os.getcwd(), "src")
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    file_folder = os.path.join(os.getcwd(), "generated-files/ui")
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    file_folder = os.path.join(os.getcwd(), "generated-files/json")
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    
    [convert_file(file) for file in files_to_convert]

    print("Done converting!")


class QSsFileMonitor():
    def __init__(self, parent=None):
        super(QSsFileMonitor, self).__init__(parent)

    def start_qss_file_listener(self):
        if self.liveCompileQss:
            default_sass_path = os.path.abspath(os.path.join(os.getcwd(), 'Qss/scss/defaultStyle.scss'))

            if os.path.isfile(default_sass_path):
                # Monitor defaultStyle.scss file for changes
                if not hasattr(self, "qss_watcher"):
                    self.qss_watcher = QFileSystemWatcher()
                    self.shared_data = SharedData()
                if self.qss_watcher is None:
                    self.qss_watcher = QFileSystemWatcher()
                if not self.shared_data.url_exists(default_sass_path):
                    self.qss_watcher.addPath(default_sass_path)
                    self.shared_data.add_file_url(default_sass_path)

                # Monitor JSON style sheets for changes
                for json_file in self.jsonStyleSheets:
                    json_file_path = os.path.abspath(os.path.join(os.getcwd(), json_file))
                    if os.path.isfile(json_file_path):
                        self.qss_watcher.addPath(json_file_path)

                        logInfo(f"Live monitoring {json_file} for changes")
                    else:
                        logError(f"Error: JSON file {json_file_path} not found")
                
                self.qss_watcher.fileChanged.connect(lambda path=default_sass_path: QSsFileMonitor.qss_file_changed(self, path))
                logInfo("Live monitoring Qss/scss/defaultStyle.scss file for changes")

            else:
                logError("Error: Qss/scss/defaultStyle.scss file not found")


    def qss_file_changed(self, file_path):
        if self.liveCompileQss:
            logInfo(f"File changed: {file_path}")

            # # Check if the file extension is '.json'
            if file_path.endswith('.json'):
                # reload jsons
                # self.reloadJsonStyles(update = True)
                QAppSettings.updateAppSettings(self, generateIcons = False, reloadJson = True)
            else:
                # Apply compiled stylesheet
                QAppSettings.updateAppSettings(self, generateIcons = False, reloadJson = False)
        else:
            logInfo(f"File changes ignored. Reason: Live compilation disabled")

    def stop_qss_file_listener(self):
        if hasattr(self, 'qss_watcher'):
            # Disconnect the fileChanged signal from the qss_file_changed slot
            self.qss_watcher.fileChanged.disconnect(QSsFileMonitor.qss_file_changed)
            self.qss_watcher.deleteLater()
            del self.qss_watcher



    
