"""Static demo data for the RhythmoTune music dashboard. Icon names are feather
names (resolved + recoloured in GuiFunctions). Cover / avatar imagery is pulled
async from free no-key providers (see workers.ImageWorker)."""

USER = {"name": "Molly Hunter", "plan": "Premium", "avatar": "https://i.pravatar.cc/120?img=45"}

# Sidebar nav: (label, feather-icon)
NAV = [
    ("Home", "home"),
    ("Categories", "grid"),
    ("Artists", "user"),
]

# Sidebar playlists: (name, pravatar image index or None for no thumbnail)
PLAYLISTS = [
    ("Vibes & Chill", 12),
    ("Morning Boost", 32),
    ("Rhythm & Energy", None),
]

# Hero cover-flow items: (title, artist, accent, pravatar image index)
HERO = [
    ("Sunset Drive", "Leah Cole", "#c0432a", 1),
    ("Neon Bloom", "Ivy Sound", "#2f6f8f", 15),
    ("Echoes of Midnight", "Jon Hickman", "#1f7a5a", 68),
    ("Golden Hour", "Mia Lowell", "#d79a2b", 44),
    ("Crimson Bass", "The Verge", "#a12f4b", 51),
]
HERO_ACTIVE = 2

CATEGORIES = ["All", "Relax", "Sad", "Party", "Romance", "Energetic",
              "Relaxing", "Jazz", "Alternative"]

# Popular songs: (title, artist, accent, pravatar image index)
POPULAR = [
    ("Golden Days", "Felix Carter", "#e0592f", 3),
    ("Fading Horizon", "Ella Hunt", "#1f7a5a", 9),
    ("Waves of Time", "Lana Rivers", "#26418f", 20),
    ("Electric Dreams", "Mia Lowell", "#d79a2b", 25),
    ("Echoes of Midnight", "Jon Hickman", "#a12f4b", 68),
    ("Shadows & Light", "Ryan Miles", "#2f6f8f", 60),
]

NOW_PLAYING = {"title": "Echoes of Midnight", "artist": "Jon Hickman",
               "elapsed": "0:53", "total": "3:58", "position": 0.22, "cover": 68}
