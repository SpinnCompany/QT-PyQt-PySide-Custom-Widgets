########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## Locate bundled resources relative to the package root.
##
## Widget modules live in subpackages (Custom_Widgets/widgets/<group>/) but the
## data they load - components/icons, components/json, Qss/ - sits at the
## package root. Anchoring on the module's own __file__ therefore resolves one
## or more directories too deep, which is how the 2026-07-31 regrouping broke
## every icon and theme lookup at once.
##
## Always resolve bundled data through here, never through a module-local
## dirname(__file__).
########################################################################
import os

_ROOT = os.path.dirname(os.path.abspath(__file__))


def packageDir():
    """Absolute path to the Custom_Widgets package root."""
    return _ROOT


def resourcePath(*parts):
    """Absolute path to a bundled resource, e.g. resourcePath("Qss", "icons")."""
    return os.path.join(_ROOT, *parts)
