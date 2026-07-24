"""Static demo data for the Cash Flow dashboard (a real app would fetch this)."""

# ── Top banner ──────────────────────────────────────────────────────────────
BALANCE = {"value": "€ 320.845,20", "delta": "15.8%", "dir": "up"}

# ── Cash Flow diverging bar chart ───────────────────────────────────────────
# Income bars point UP (positive, dark teal); expense bars point DOWN
# (negative, green). Rendered by QCustomBarChart in two grouped series so the
# y-axis straddles zero. Only a few buckets carry an x-axis date label.
CASHFLOW_INCOME = [1.2, 3.1, 2.4, 0.9, 1.1, 1.3, 4.2, 4.8, 3.0, 1.4, 2.0, 1.6,
                   2.1, 3.4, 1.5, 1.2]          # €K, up
CASHFLOW_EXPENSE = [-0.9, -1.4, -2.6, -0.7, -0.9, -1.1, -1.7, -2.0, -1.2, -0.8,
                    -1.3, -1.0, -1.9, -1.5, -1.1, -0.9]   # €K, down
CASHFLOW_LABELS = ["", "18 Oct", "", "", "", "", "25 Oct", "", "", "",
                   "2 Nov", "", "", "", "9 Nov", ""]
CASHFLOW_YRANGE = (-3.0, 5.0)                    # €K, matches €3K / €0 / €5K axis

# Income / Expense side panel next to the chart.
CASHFLOW_SIDE = [
    ("income", "Income", "€ 12.378,20", "45.0%", "up", "arrow-down-left"),
    ("expense", "Expense", "€ 5.788,21", "12.5%", "down", "arrow-up-right"),
]

# ── KPI cards row ───────────────────────────────────────────────────────────
# (icon, title, value, delta, dir, "vs. … Last Period")
KPIS = [
    ("briefcase", "Business account", "€ 8.672,20", "16.0%", "up", "vs. 7.120,14 Last Period"),
    ("dollar-sign", "Total Saving", "€ 3.765,35", "8.2%", "down", "vs. 4.116,50 Last Period"),
    ("shield", "Tax Reserve", "€ 14.376,16", "35.2%", "up", "vs. 10.236,46 Last Period"),
]

# ── Recent Activity table ───────────────────────────────────────────────────
# (icon, name, type, date, amount, sub, status, method, last4, sign)
ACTIVITY = [
    ("plus", "Theo Lawrence", "Add", "Oct 18, 2024", "€ 500,00", "120 USD",
     "Success", "Credit Card", "3560", "pos"),
    ("arrow-up-right", "Amy March", "Sent", "May 24, 2024", "- € 250,00", "80 USD",
     "Pending", "Bank Transfer", "2285", "neg"),
]

# ── My Cards (interactive stack) ─────────────────────────────────────────────
MY_CARDS = [
    {"brand": "VISA", "amount": "€ 4.540,20", "number": "2104", "fullNumber": "4539 8843 0117 2104"},
    {"brand": "Mastercard", "amount": "€ 12.980,00", "number": "8821", "fullNumber": "5218 4471 9930 8821"},
    {"brand": "VISA", "amount": "€ 640,75", "number": "3390", "fullNumber": "4024 0071 3355 3390"},
]

# ellipsis (…) menu actions: (icon, label, key, danger)
MORE_MENU = [
    ("file-text", "Account statement", "statement", False),
    ("download", "Export data", "export", False),
    ("settings", "Card settings", "settings", False),
    ("__sep__", "", "", False),
    ("trash-2", "Close account", "close_acct", True),
]
ACTIVITY_MENU = [
    ("download", "Export CSV", "export_csv", False),
    ("filter", "Filter rows", "filter", False),
    ("check-circle", "Mark all reviewed", "mark", False),
]
