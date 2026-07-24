"""Static demo data for the My Home smart-home dashboard. Icons are feather
names (resolved + recoloured in GuiFunctions). Runtime data lives here, not in
the .ui."""

USER = {"name": "My Home", "members": "3 MEMBERS", "greet": "Ana"}

# top-bar navigation (feather icon names)
NAV = ["home", "folder", "zap", "target", "calendar", "share-2", "settings", "log-out"]

WELCOME = ("Welcome home, Ana. Lorem ipsum dolor sit amet nonummy sed diam "
           "consectetuer nibh et adipiscing elit.")

# Hello-card weather tiles: (icon, value, label)
WEATHER = [
    ("cloud",       "15°",  "Weather\nPart Cloudy"),
    ("droplet",     "45%",  "Outdoor Humidity"),
    ("thermometer", "22°",  "Indoor Temperature\n(C°)"),
    ("plus",        "",     "Add Data"),
]

# gauges: (title, icon, value, min, max, text, suffix, gradient-key, status-icon, status)
GAUGES = [
    {"title": "Temperature", "icon": "thermometer", "value": 22, "min": 0, "max": 40,
     "text": "22", "suffix": "C°", "grad": "temp", "sicon": "clock", "status": "24° in 20 min"},
    {"title": "Power", "icon": "zap", "value": 68, "min": 0, "max": 100,
     "text": "135", "suffix": "Kwh", "grad": "power", "sicon": "trending-down", "status": "Saving 187€"},
]

# device tiles: (icon, caption) — first is active
DEVICES = [
    ("zap", "Lights"), ("thermometer", "Heating"), ("wind", "Air Conditioner"), ("video", "Cameras"),
    ("lock", "Doors"), ("shield", "Alarm"), ("truck", "Garage"), ("home", "Garden"),
]
DEVICE_ACTIVE = 0

LIGHTING = {"room": "Studio", "brightness": 62}
SECURITY = {"door": "Front Door", "locked": True}
