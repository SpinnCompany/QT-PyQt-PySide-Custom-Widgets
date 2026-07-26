import os
import sys
import re
import shutil
import subprocess
import qtpy
from qtpy.QtGui import QIcon
from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QApplication

try:
    # Not available in every binding/deployment (e.g. PyQt6 wheels without
    # the designer module); is_in_designer degrades gracefully without it.
    from qtpy.QtDesigner import QDesignerFormWindowInterface
except Exception:
    QDesignerFormWindowInterface = None

# Import custom logging module
from Custom_Widgets.Log import *

def get_absolute_path(relative_path):
    """Convert a relative path to an absolute path based on the script's directory."""
    import __main__
    from Custom_Widgets.Project import projectRoot, hasExplicitRoot

    # Try multiple methods to find the main script directory
    possible_dirs = []

    # Method 0: an explicitly configured project root always wins
    if hasExplicitRoot():
        possible_dirs.append(projectRoot())
    
    # Method 1: __main__.__file__
    if hasattr(__main__, '__file__'):
        possible_dirs.append(os.path.dirname(os.path.abspath(__main__.__file__)))
    
    # Method 2: sys.argv[0] (your original approach)
    if sys.argv[0]:
        possible_dirs.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    # Method 3: Current working directory
    possible_dirs.append(os.path.abspath(os.getcwd()))
    
    # Use the first valid directory that contains the relative path when joined
    for main_dir in possible_dirs:
        test_path = os.path.join(main_dir, relative_path)
        if os.path.exists(test_path):
            return os.path.normpath(test_path)
    
    # If no existing path found, use the first method and hope for the best
    main_dir = possible_dirs[0] if possible_dirs else os.path.abspath(os.getcwd())
    return os.path.normpath(os.path.join(main_dir, relative_path))

def replace_url_prefix(url, new_prefix):
    pattern = re.compile(r':/[^/]+/')
    return pattern.sub( new_prefix + '/', url, 1)

def get_icon_path(icon: QIcon | str) -> str:
    """Return the correct path for a themed icon. Handle both QIcon and string paths."""
    settings = QSettings()
    # Check if the 'ICONS-COLOR' setting is defined
    if settings.value("ICONS-COLOR") is not None:
        # Get the normal color and derive the icon folder name from it
        normal_color = settings.value("ICONS-COLOR")
        icons_folder = normal_color.replace("#", "")  # Strip the '#' for folder naming

        # Regular expression to remove the old prefix in the icon path
        prefix_to_remove = re.compile(r'^Qss/icons/[^/]+/')

        if isinstance(icon, QIcon):
            # Handle QIcon by converting to the appropriate icon path
            icon_url = icon.name()  # Assuming the QIcon has a name or can be represented
            return icon.addFile(re.sub(prefix_to_remove, f'Qss/icons/{icons_folder}/', replace_url_prefix(icon_url, "Qss/icons")))

        elif isinstance(icon, str):
            # If the input is a string (file path), process it directly
            return re.sub(prefix_to_remove, f'Qss/icons/{icons_folder}/', replace_url_prefix(icon, "Qss/icons"))

    return icon 

def is_in_designer(self):
    """Check if running in Qt Designer."""
    try:
        # Method 1: Check for QDesignerFormWindowInterface (if widget is in a form)
        if QDesignerFormWindowInterface is not None and \
                QDesignerFormWindowInterface.findFormWindow(self) is not None:
            return True
    except Exception:
        pass
    
    try:
        # Method 2: Check for QApplication's applicationName (Designer sets this)
        app = QApplication.instance()
        if app is not None:
            app_name = app.applicationName().lower()
            if app_name and 'designer' in app_name:
                return True
    except Exception as e:
        pass
    
    # Method 3: Check command line arguments
    if len(sys.argv) > 0:
        exe_name = sys.argv[0].lower()
        if 'designer' in exe_name or 'pyqt5-tools' in exe_name or 'pyqt6-tools' in exe_name:
            return True
    
    # Method 4: Check if we're being imported by designer (parent chain check)
    # This works if the theme object has a parent widget that's in designer
    parent = self.parent()
    while parent is not None:
        try:
            if QDesignerFormWindowInterface is not None and \
                    QDesignerFormWindowInterface.findFormWindow(parent) is not None:
                return True
        except Exception:
            pass
        parent = parent.parent()
    
    return False


def createQrcFile(contents, filePath):
    # Ensure the directory for the filePath exists
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    
    # Save QRC content to a file
    with open(filePath, 'w', encoding='utf-8') as qrc_file:
        qrc_file.write(contents)

    # print(f'QRC file generated: {filePath}')

def _qtToolPath(tool):
    """Resolve a Qt CLI tool (pyside6-uic, pyside6-rcc, ...) preferring the
    running interpreter's environment over whatever is first on PATH - the
    PATH copy may belong to a different Python without the binding."""
    exe_dir = os.path.dirname(sys.executable)
    for candidate in (os.path.join(exe_dir, tool),
                      os.path.join(exe_dir, tool + ".exe")):
        if os.path.isfile(candidate):
            return candidate
    return tool  # fall back to PATH


def qrcToPy(qrcFile, pyFile):
    """
    Convert a Qt Resource Collection (qrc) file to a Python file.

    Parameters:
    - qrc_file (str): Path to the input qrc file.
    - py_file (str): Path to the output py file.
    """
    try:
        if qtpy.API_NAME == "PySide6":
            rcc_command = 'pyside6-rcc'
        elif qtpy.API_NAME == "PyQt6":
            rcc_command = 'pyrcc6'
        else:
            raise RuntimeError(
                f"Unsupported Qt binding '{qtpy.API_NAME}': Custom_Widgets "
                "supports PySide6 and PyQt6")

        logInfo(f'{rcc_command} "{qrcFile}" -o "{pyFile}"')
        subprocess.run([_qtToolPath(rcc_command), qrcFile, "-o", pyFile], check=True)

    except Exception as e:
        logError(f"Error converting qrc to py: {e}")

def uiToPy(uiFile, pyFile):
    """
    Convert a Qt UI file to a Python file.

    Parameters:
    - uiFile (str): Path to the input UI file.
    - pyFile (str): Path to the output Python file.
    """
    try:
        if qtpy.API_NAME == "PySide6":
            pyuic_command = 'pyside6-uic'
        elif qtpy.API_NAME == "PyQt6":
            pyuic_command = 'pyuic6'
        else:
            raise RuntimeError(
                f"Unsupported Qt binding '{qtpy.API_NAME}': Custom_Widgets "
                "supports PySide6 and PyQt6")

        subprocess.run([_qtToolPath(pyuic_command), uiFile, "-o", pyFile], check=True)

    except Exception as e:
        logError(f"Error converting ui to py: {e}")

def renameFolder(old_name, new_name):
    try:
        # Check if the destination directory exists
        if os.path.exists(new_name):
            # Remove the destination directory if it exists
            shutil.rmtree(new_name)

        # Rename the folder
        os.rename(old_name, new_name)
    except Exception as e:
        pass


class SharedData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedData, cls).__new__(cls)
            cls._instance.file_urls = []  # Initialize an empty list for file URLs
        return cls._instance

    def add_file_url(self, file_url):
        """Add a new file URL to the list."""
        if file_url not in self.file_urls:  # Prevent duplicates
            self.file_urls.append(file_url)

    def get_file_urls(self):
        """Return the list of file URLs."""
        return self.file_urls

    def clear_file_urls(self):
        """Clear the list of file URLs."""
        self.file_urls.clear()

    def url_exists(self, file_url):
        """Check if a file URL exists in the list."""
        return file_url in self.file_urls


def download_font(url, cache_dir=None, timeout=20, force=False):
    """Download a remote font (TTF/OTF/TTC) to a local cache and return its path.

    Lets a Custom_Widgets app use a brand / web font by URL instead of bundling
    the binary. The file is cached by a hash of the URL under ``cache_dir``
    (default ``<projectRoot>/generated-files/fonts``) so it is fetched at most
    once. Network / HTTP failures are NON-FATAL: this logs and returns ``None``
    so the caller falls back to the bundled font. Stdlib only (urllib) — no new
    dependency. Note: QFontDatabase does not read WOFF/WOFF2, so point this at a
    TTF/OTF (variable TTFs are fine on Qt6).
    """
    import hashlib
    import urllib.request

    try:
        if cache_dir is None:
            from Custom_Widgets.Project import projectRoot
            cache_dir = os.path.join(projectRoot(), "generated-files", "fonts")
        os.makedirs(cache_dir, exist_ok=True)

        ext = os.path.splitext(url.split("?")[0])[1].lower()
        if ext not in (".ttf", ".otf", ".ttc"):
            ext = ".ttf"
        dest = os.path.join(cache_dir, hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext)

        if os.path.isfile(dest) and os.path.getsize(dest) > 0 and not force:
            return dest

        req = urllib.request.Request(url, headers={"User-Agent": "Custom_Widgets-font-loader"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if not data:
            logError(f"Remote font is empty: {url}")
            return None

        tmp = dest + ".part"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, dest)
        logInfo(f" Downloaded remote font ({len(data)} bytes) -> {dest}")
        return dest
    except Exception as e:
        logError(f"Failed to download remote font {url}: {e}")
        return None



########################################################################
## Icon helpers — recolour a themed SVG (feather / material / font_awesome)
## to ANY colour at ANY size, cached. Apps SHOULD use these instead of
## re-implementing QSvgRenderer tinting in every GuiFunctions. For a SINGLE
## theme colour prefer the QSS `theme-icons:` path; use these when a widget
## needs a specific colour (e.g. an ACTIVE nav item in the accent colour).
########################################################################
_ICONS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Qss", "icons")
_ICON_SETS = ("feather", "material_design", "font_awesome")
_ICON_PM_CACHE = {}


def resolve_icon_path(name_or_path):
    """Resolve a bare icon NAME (e.g. 'home') against the bundled icon sets
    (feather → material_design → font_awesome), or pass an absolute path
    through unchanged."""
    if not name_or_path:
        return ""
    if os.path.isabs(name_or_path) or os.path.exists(name_or_path):
        return name_or_path
    base = name_or_path[:-4] if name_or_path.lower().endswith(".svg") else name_or_path
    for pack in _ICON_SETS:
        p = os.path.join(_ICONS_ROOT, pack, base + ".svg")
        if os.path.exists(p):
            return p
    return os.path.join(_ICONS_ROOT, _ICON_SETS[0], base + ".svg")


def recolor_icon(name_or_path, color, size=22):
    """Return a `QPixmap` of the icon recoloured to `color` (any stroke- or
    fill-based SVG), rendered at 2x for crispness. Cached by (path, colour,
    size)."""
    from qtpy.QtGui import QPixmap, QPainter, QColor
    path = resolve_icon_path(name_or_path)
    key = (path, str(QColor(color).name()), int(size))
    if key in _ICON_PM_CACHE:
        return _ICON_PM_CACHE[key]
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    try:
        from qtpy.QtSvg import QSvgRenderer
    except Exception:
        QSvgRenderer = None
    if path and os.path.exists(path) and QSvgRenderer is not None:
        r = QSvgRenderer(path)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.setCompositionMode(QPainter.CompositionMode_SourceIn)
        p.fillRect(pm.rect(), QColor(color))
        p.end()
    pm.setDevicePixelRatio(2.0)
    _ICON_PM_CACHE[key] = pm
    return pm


def themed_icon(name_or_path, color, size=22):
    """Return a `QIcon` of the icon recoloured to `color` (see recolor_icon)."""
    return QIcon(recolor_icon(name_or_path, color, size))


def set_state(widget, prop, value, children=True):
    """Toggle a QSS dynamic-property state and RE-POLISH so `[prop="value"]`
    selectors (including qproperty-* rules) re-land — on the widget and, by
    default, its child widgets. The one-liner every manager needs instead of
    hand-rolled setProperty + unpolish/polish walks."""
    from qtpy.QtWidgets import QWidget

    if isinstance(value, bool):
        value = "true" if value else "false"
    widget.setProperty(prop, value)
    targets = [widget]
    if children:
        targets += widget.findChildren(QWidget)
    for w in targets:
        try:
            w.style().unpolish(w)
            w.style().polish(w)
        except Exception:
            pass
