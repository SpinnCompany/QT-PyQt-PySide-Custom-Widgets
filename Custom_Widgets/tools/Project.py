########################################################################
## PROJECT ROOT
##
## Single source of truth for "where is the user's project". Historically
## the pipeline mixed THREE roots - os.getcwd(), dirname(sys.argv[0]) and
## __main__.__file__ - so an app launched from anywhere but its own folder
## silently wrote icons/css/json elsewhere. Every path in the styling and
## tooling pipeline now funnels through projectRoot().
##
## Resolution order:
##   1. setProjectRoot(path)            - explicit, wins everywhere
##   2. CUSTOM_WIDGETS_PROJECT_ROOT env - explicit, e.g. set by tooling
##   3. os.getcwd()                     - legacy behavior (launch from the
##                                        project folder), still the default
##
## App entry points should call setProjectRoot(__file__'s folder) first
## (the generated main.py template does), which makes the app fully
## location-independent.
########################################################################
import os

_explicit_root = None


def setProjectRoot(path):
    """Pin the project root explicitly. Pass a directory, or a file (its
    directory is used - so setProjectRoot(__file__) works)."""
    global _explicit_root
    path = os.path.abspath(path)
    if os.path.isfile(path):
        path = os.path.dirname(path)
    _explicit_root = path
    return _explicit_root


def clearProjectRoot():
    """Forget the explicit root (falls back to env var / cwd)."""
    global _explicit_root
    _explicit_root = None


def hasExplicitRoot():
    """True when a root was pinned via setProjectRoot or the
    CUSTOM_WIDGETS_PROJECT_ROOT environment variable."""
    return bool(_explicit_root or os.environ.get("CUSTOM_WIDGETS_PROJECT_ROOT"))


def projectRoot():
    """The project root directory (see module docstring for resolution)."""
    if _explicit_root:
        return _explicit_root
    env = os.environ.get("CUSTOM_WIDGETS_PROJECT_ROOT")
    if env:
        return os.path.abspath(env)
    return os.getcwd()


def projectPath(*parts):
    """A path inside the project, e.g. projectPath('Qss', 'scss')."""
    return os.path.join(projectRoot(), *parts)


# -- Well-known project locations ---------------------------------------
def scssDir():
    return projectPath("Qss", "scss")


def iconsDir():
    return projectPath("Qss", "icons")


def generatedDir(*parts):
    return projectPath("generated-files", *parts)


def styleJsonPath():
    """The default style.json location (json-styles/style.json, falling
    back to a root-level style.json)."""
    preferred = projectPath("json-styles", "style.json")
    if os.path.isfile(preferred):
        return preferred
    legacy = projectPath("style.json")
    if os.path.isfile(legacy):
        return legacy
    return preferred
