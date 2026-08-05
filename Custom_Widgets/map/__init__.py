########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

"""Map support — an OPTIONAL extra, deliberately outside the core widgets.

Install with::

    pip install QT-PyQt-PySide-Custom-Widgets[map]

Nothing in the core library imports this package. That is the whole point:
docs/design/qcustommapview-project-plan.md decided a map must not sit in the
core because it drags in a mapping engine, tile providers, API keys and
provider ToS — config, secrets and legal surface an LGPL widget library should
not carry. Users who never need a map pay nothing for it.

The public face is `QCustomMapView`, an engine-agnostic facade. The engine
behind it is swappable; the shipped one uses QtLocation's `osm` plugin, which
is part of Qt and needs no Chromium and no API key.
"""
from .facade import QCustomMapView, MapEngineUnavailable, Marker, Route

__all__ = ["QCustomMapView", "MapEngineUnavailable", "Marker", "Route"]
