"""Demo content for the GlassHome dashboard (the reference screen's data).
Media sources (wallpaper / lamp / cover / avatar photos) live in the .ui files
as widget properties — only per-instance texts and states remain here."""

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
