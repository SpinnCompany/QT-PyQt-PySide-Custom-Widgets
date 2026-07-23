"""Static demo data for the finance dashboard (a real app would fetch this)."""

# Monthly-summary bar chart: (day label, height fraction 0..1, colour-key)
#   idle = muted grey, blue = accent, active = highlighted green (day 30).
MONTH_BARS = [
    ("23", 0.26, "barIdle"),
    ("23", 0.52, "barBlue"),
    ("23", 0.60, "barBlue"),
    ("24", 0.30, "barIdle"),
    ("25", 0.66, "barBlue"),
    ("26", 0.88, "barBlue"),
    ("27", 0.30, "barIdle"),
    ("28", 0.60, "barBlue"),
    ("29", 0.94, "barBlue"),
    ("30", 1.00, "barActive"),
    ("31", 0.66, "barBlue"),
]

# Latest transactions: (feather icon, name, category, amount, date, sign)
TRANSACTIONS = [
    ("shopping-bag", "Starbucks", "Shopping", "- $120.00", "31 Mar 2019", "neg"),
    ("dollar-sign", "Design Studio", "Salary", "+ $5000.00", "30 Mar 2019", "pos"),
]

# How many carousel dots each pager shows, and which one is active.
CARD_DOTS = (3, 0)          # (count, active index)
SUMMARY_DOTS = (3, 2)
