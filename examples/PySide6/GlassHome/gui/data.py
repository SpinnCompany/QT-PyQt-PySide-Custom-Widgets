"""Demo content for the GlassHome dashboard (the reference screen's data)."""

WALLPAPER_URL = "https://picsum.photos/seed/glasshome/1600/1000"
LAMP_URL = "https://picsum.photos/seed/glasslamp/256/432"
COVER_URL = "https://picsum.photos/seed/glasscover/128/128"
AVATAR_URL = "https://i.pravatar.cc/96?img=12"

STATS = [
    ("statCurrentContainer", "Current Consumption", "1,5 kWh"),
    ("statHumidityContainer", "Humidity", "48,2 %"),
    ("statTempContainer", "Temperature", "68° F"),
]

TILES = [
    ("tileHumidifierContainer", "Gaabor", "Gaabor Humidifier", True),
    ("tileSpeakerContainer", "Amazon", "Echo Speaker", False),
    ("tileLampContainer", "Bardi", "Bardi Smart Lamp", True),
    ("tileCameraContainer", "Xiaomi", "Xiaomi Camera", False),
]

MODE_ICONS = {
    "modeHot": "thermometer",
    "modeEco": "feather",
    "modeFan": "wind",
    "modeCold": "cloud-snow",
}

TRACK_SECONDS = 2 * 60 + 27          # 2:27
TRACK_START = 34                     # 0:34
