"""Static demo data for the crypto dashboard (a real app would fetch this)."""

# Sidebar rail: objectName -> feather icon name (painted in the manager).
NAV_ICONS = {
    "navDashboard": "home",
    "navMarkets": "pie-chart",
    "navWallet": "credit-card",
    "navReports": "clipboard",
    "navExchange": "repeat",
    "navStats": "bar-chart-2",
    "navContacts": "users",
    "navDocs": "book-open",
    "navSettings": "settings",
}

# ------------------------------------------------------------------ overview --
# "Overview of all wallets" area chart — a BTC micro price series (USD). The
# x-axis time labels are painted as a separate row under the chart.
OVERVIEW_SERIES = [
    69.34, 69.31, 69.37, 69.33, 69.40, 69.36, 69.44, 69.41, 69.38, 69.46,
    69.43, 69.52, 69.49, 69.58, 69.71, 69.66, 69.79, 69.94, 70.02, 69.97,
    70.12, 70.28, 70.19, 70.36, 70.31, 70.44, 70.52, 70.47, 70.55, 70.60,
    70.57, 70.62, 70.66, 70.63, 70.71,
]
OVERVIEW_TIMES = ["10 AM", "1 PM", "4 PM", "6 PM", "8 PM",
                  "1 AM", "3 AM", "4 AM", "6 AM"]

RANGE_SEGMENTS = ["1D", "1W", "1M", "6M"]

BIG_BTC = "0.00263788 BTC"
BIG_USD = "≈ $69.82"
BIG_CHANGE = "8.89%"

# -------------------------------------------------------------------- market --
MARKET_TABS = ["Holding", "Top Gainers", "Hot"]

# (ticker, name, amount, price, change%, sign)  — sign drives the up/down colour.
MARKET = [
    ("BTC", "Bitcoin",  "0.00000462", "$26,551.00", "+0.39%", "up"),
    ("ETH", "Ethereum", "0.000023",   "$1,846.04",  "+0.39%", "up"),
    ("SOL", "Solana",   "0.00000462", "$18.77",     "-0.79%", "down"),
    ("ADA", "Cardano",  "0.00000462", "$0.3232",    "-0.68%", "down"),
    ("USDT", "Tether",  "0.0001583",  "$0.3232",    "+0.02%", "up"),
]

# --------------------------------------------------------------------- promo --
PROMO_TITLE = "Unlimited access to\n130+ assets"
PROMO_SUB = "Start earning today with\nMy Container and avg. APY of 10%"
PROMO_COINS = ["BTC", "ETH", "SOL", "ADA", "USDT", "XRP", "BNB", "DOT"]

# --------------------------------------------------------------------- trade --
TRADE_TABS = ["Buy", "Sell", "Exchange"]
TRADE_COIN_NAME = "Ethereum"
TRADE_COIN_TICKER = "ETH"
TRADE_AMOUNT = "34994"
TRADE_CURRENCY = "USD"
TRADE_RATE = "Exchange rate, 1 ETH = 1844.29"
TRADE_FEE = "2322.40"
TRADE_RECEIVED = "$33831.90"

# ---------------------------------------------------------------------- user --
USER_NAME = "Anna cathcart"
USER_ID = "ID: 32324254"
