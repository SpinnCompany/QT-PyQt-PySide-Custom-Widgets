"""Static demo data for the Check Box dashboard. Runtime values live here (not
in the .ui). Category indices map to palette colours in GuiFunctions:
 0 = white / Resources / Web, 1 = green / Valid / Customer, 2 = orange / Invalid / Product.
"""

# --- top bar ------------------------------------------------------------- #
NAV = [("Check Box", "box"), ("Monitoring", "bar-chart-2"), ("Support", "message-square")]
PROFILE = {"name": "Bogdan Nikitin", "handle": "@Nixtio", "notifications": 2}

# --- left rail ----------------------------------------------------------- #
RAIL = ["heart", "calendar", "award", "settings"]

# --- filter pills -------------------------------------------------------- #
FILTERS = [("Date", "Now"), ("Product", "All"), ("Profile", "Bogdan")]

# --- CUSTOMER card ------------------------------------------------------- #
CUSTOMER_STATS = [("2,4%", "Web Surfing", "up", 1),      # green up
                  ("1,1%", "Radio Station", "down", 2)]  # orange down
# two overlaid trend lines (orange, green) sharing one scale
CUSTOMER_LINES = [
    [22, 30, 18, 34, 26, 40, 24, 30, 44, 33, 48, 36],   # orange
    [30, 24, 36, 20, 32, 26, 44, 30, 38, 50, 34, 46],   # green
]

# --- PRODUCT (small) card ----------------------------------------------- #
PRODUCT_STATS = [("2,8%", "Partners", "up", 1),          # green up
                 ("3,2%", "Owners", "down", 2)]          # orange down
# dot-matrix density grid — 0 empty, 1 green, 2 orange, 3 white
PRODUCT_MATRIX = [
    [0, 0, 0, 0, 0, 3, 0, 1, 0, 2, 1, 2, 1, 2],
    [0, 0, 1, 0, 2, 1, 2, 1, 3, 2, 1, 2, 1, 3],
    [0, 1, 0, 2, 1, 1, 2, 1, 2, 2, 1, 2, 3, 2],
    [1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 3, 2, 1],
    [2, 1, 2, 2, 1, 3, 2, 1, 3, 2, 1, 2, 1, 2],
    [1, 3, 1, 2, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3],
]

# --- PRODUCT (large) beeswarm ------------------------------------------- #
# each column = list of (value, category)
BEESWARM = [
    [(52, 0), (81, 2)],
    [(96, 1), (25, 0)],
    [(48, 1), (51, 0)],
    [(80, 1), (49, 2)],
    [(34, 2), (67, 1)],
    [(92, 1), (28, 0)],
    [(58, 1), (20, 2)],
    [(84, 2), (39, 1)],
    [(36, 0), (72, 2)],
]
BEESWARM_LEGEND = [("Resources", 0), ("Valid", 1), ("Invalid", 2)]
BEESWARM_TOTAL = "1,012"

# --- PROJECTS TIMELINE (gantt) ------------------------------------------ #
# Brand palette for the leading markers (brand identities, not theme chrome).
BRAND = {
    "shazam":   ("music",           "#3d8bff"),
    "x":        ("twitter",         "#1c1c22"),
    "dribbble": ("dribbble",        "#ea4c89"),
    "discord":  ("message-circle",  "#5865f2"),
    "facebook": ("facebook",        "#1877f2"),
    "twitter":  ("twitter",         "#1da1f2"),
}

# label(date), start, length, category, value, and EITHER brand=<key>
# (a colourful brand logo marker) OR avatars=<n> (a real photo avatar group).
TIMELINE = [
    {"label": "30.09", "start": 2,  "length": 8,  "category": 1, "value": 16, "brand": "shazam"},
    {"label": "29.09", "start": 18, "length": 8,  "category": 2, "value": 29, "brand": "x"},
    {"label": "28.09", "start": 8,  "length": 6,  "category": 0, "value": 15, "avatars": 3},
    {"label": "27.09", "start": 9,  "length": 9,  "category": 1, "value": 21, "brand": "dribbble"},
    {"label": "26.09", "start": 6,  "length": 4,  "category": 0, "value": 10, "brand": "discord"},
    {"label": "25.09", "start": 8,  "length": 5,  "category": 2, "value": 15, "brand": "facebook"},
    {"label": "25.09", "start": 12, "length": 9,  "category": 1, "value": 19, "avatars": 4},
    {"label": "24.09", "start": 6,  "length": 4,  "category": 0, "value": 8,  "brand": "twitter"},
]
TIMELINE_LEGEND = [("Customer", 1), ("Product", 2), ("Web", 0)]
TIMELINE_TOTAL = "284"
