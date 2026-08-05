"""Static demo data for the dashboard (a real app would fetch this)."""

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
          "Aug", "Sep", "Oct", "Nov", "Dec"]
ONLINE = [22, 19, 26, 23, 21, 25, 23, 17, 19, 19, 24, 26]      # $k
OFFLINE = [6.2, 4.6, 6.8, 5.8, 8.9, 5.6, 4.9, 4.2, 5.8, 6.4, 6.8, 2.2]

LOYAL = [1.1, 1.9, 1.5, 2.3, 1.8, 2.0, 1.9, 2.2, 2.0, 2.4, 2.3, 2.9]
NEWC = [0.9, 1.4, 2.1, 1.6, 1.5, 1.9, 1.5, 1.7, 1.6, 2.0, 1.7, 2.5]

# (label, value, colour-key in ChartPalette)
DISTRIBUTION = [("Online sales", 52, "online"),
                ("Offline sales", 33, "offline"),
                ("Returns", 15, "returns")]

# (initials, product, date, price, status, badge-variant)
ORDERS = [
    ("RL", "Rust Linen Blazer", "Jan 25, 2025", "$149.99", "Shipping", "warning"),
    ("CT", "Crop Tank", "Jan 25, 2025", "$49.99", "Received", "success"),
    ("OB", "Oversized Blazer", "Jan 24, 2025", "$185.99", "Received", "success"),
    ("SD", "Silk Slip Dress", "Jan 24, 2025", "$129.00", "Shipping", "warning"),
    ("WT", "Wide-Leg Trouser", "Jan 23, 2025", "$89.50", "Received", "success"),
]

# KPI cards: (key, label, sparkline series, colour-key, active?)
KPIS = [
    ("orders", "Total orders", ONLINE, "online", True),
    ("sales", "Total sales", [12, 15, 13, 18, 16, 22, 20, 24], "offline", False),
    ("sessions", "Online sessions", [30, 28, 33, 31, 36, 34, 40, 44], "returns", False),
    ("avg", "Average order", [22, 20, 24, 19, 23, 18, 21, 17], "down", False),
]

# Base values + formatter per KPI (the worker nudges these live).
KPI_BASE = {"orders": 947.0, "sales": 28407.0, "sessions": 54778.0, "avg": 89.99}


def fmt_kpi(key, v):
    if key == "orders":
        return "%d" % int(round(v))
    if key == "sessions":
        return "{:,}".format(int(round(v)))
    if key == "sales":
        return "${:,}".format(int(round(v)))
    if key == "avg":
        return "$%.2f" % v
    return str(v)
