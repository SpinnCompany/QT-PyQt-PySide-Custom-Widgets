"""Static demo data for the Aurora Chat showcase.

Kept out of the .ui and out of the managers so the repeating content
(conversations, the message thread, the media grid) is data-driven — the
managers just turn these rows into Custom_Widgets.
"""

# A pleasant spread of avatar chip colours (initials on a solid fill).
AVATAR_COLORS = [
    "#f2704e", "#3d7bff", "#8b5cf6", "#12b8a6", "#e8477f",
    "#f0a92b", "#2fb673", "#5b74ff", "#ff7a5c", "#0ea5e9", "#a855f7",
]

# Conversation list — (name, preview, time, unread, online, muted).
CONVERSATIONS = [
    ("Ricky Smith",       "YOU: Okay, let's get the file over to the team", "1min ago",  0, True,  False),
    ("Stephanie Sharkey", "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("Rodger Struck",     "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("Jerry Helfer",      "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("James Hall",        "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("Lorri Warf",        "Let's go on a date tomorrow 💫",                 "2min ago",  2, True,  False),  # noqa: glyph-icons
    ("Frances Swann",     "YOU: Okay, let's get the file over…",            "1min ago",  0, False, True),
    ("Stephanie Nicol",   "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("Kathy Pacheco",     "YOU: Okay, let's get the file over…",            "1min ago",  0, False, False),
    ("Mary Freund",       "YOU: Okay, let's get the file over…",            "1min ago",  0, True,  False),
    ("Corina McCoy",      "YOU: Haha, I agree with you.",                   "Jan 01",    0, False, False),
    ("Judith Rodriguez",  "See you on a rift.",                            "Jan 01",    0, True,  False),
]

# Real portrait per contact — (gender, randomuser index). Parallel to CONVERSATIONS.
AVATAR_SPECS = [
    ("men", 32), ("women", 44), ("men", 51), ("men", 13), ("men", 75),
    ("women", 68), ("women", 21), ("women", 9), ("women", 90), ("women", 33),
    ("women", 57), ("women", 12),
]
USER_AVATAR = ("women", 65)     # Vivien (the signed-in user)

ACTIVE_INDEX = 0            # Ricky Smith is the open conversation

# The open thread — a list of message rows.
#   ("date",  label)                          -> a date divider pill
#   ("in",    text, time)                     -> incoming text bubble
#   ("out",   text, time)                     -> outgoing text bubble
#   ("voice", "in"/"out", duration, time)     -> a voice message bubble
#   ("outcost", text, cost, time)             -> outgoing bubble w/ credits foot
# A trailing dict on a row carries per-message extras: "status" (delivery ticks
# on outgoing messages: sent/delivered/read) and "reactions" (emoji + count).
THREAD = [
    ("date",  "YESTERDAY"),
    ("in",    "Hi! How are you? 🥰", "11:00 AM", {"reactions": [("👍", 2)]}),  # noqa: glyph-icons
    ("out",   "Hey Ricky! I'm feeling amazing, how about you?", "12:42 PM", {"status": "read", "reactions": [("❤️", 1)]}),  # noqa: glyph-icons
    ("voice", "in", "01:30", "12:00 PM"),
    # --- inline media (reuses the media widgets inside chat bubbles) ---
    ("album", "in",  "12:03 PM", {"images": ["chatA", "chatB", "chatC", "chatD"]}),
    ("link",  "in",  "12:04 PM", {"title": "Aurora Design System",
                                   "url": "https://dribbble.com/aurora",
                                   "desc": "Modern UI kit for chat apps"}),
    ("file",  "out", "12:05 PM", {"name": "Design Specs.pdf", "size": "3.1 MB",
                                   "date": "Today", "status": "read"}),
    ("video", "in",  "12:06 PM", {"poster": "chatVid", "duration": "1:24"}),
    ("outcost", "That's a cool idea! 😄", "Sent for 0 credits", "12:42 PM", {"status": "delivered"}),  # noqa: glyph-icons
    ("in",    "Hey, so happy you are down! ✨", "12:42 PM", {"reactions": [("😂", 1), ("🔥", 3)]}),  # noqa: glyph-icons
]

# Waveform bar heights for the voice message.
VOICE_WAVE = "3,6,10,14,9,16,20,12,7,18,22,14,8,12,6,10,16,9,5,12,18,10,6,14,8,13,7,17,11,6"

# Profile action buttons — (feather-icon, label).
PROFILE_ACTIONS = [
    ("user",   "Profile"),
    ("bell",   "Mute"),
    ("search", "Search"),
]

# Media grid thumbnails — gradient (top, bottom) pairs, painted as placeholders.
MEDIA_TILES = [
    ("#f6a94b", "#b5541e"), ("#8fd66f", "#2f7d3e"), ("#7fc7f5", "#2b6fb0"),
    ("#c58bf0", "#6a34b0"), ("#f28b8b", "#b53b52"), ("#8ad9c8", "#2f8f86"),
    ("#f5c86b", "#a9781f"), ("#7fa2f5", "#33489f"), ("#f28bbf", "#a83b7a"),
    ("#9be0a0", "#39833f"), ("#c0b2f0", "#5a45b0"), ("#f5b07f", "#a9531f"),
]

# Deterministic picsum seeds for the media grid (real photos; gradient = fallback).
MEDIA_SEEDS = ["aurora1", "aurora2", "aurora3", "aurora4", "aurora5", "aurora6",
               "aurora7", "aurora8", "aurora9", "aurora10", "aurora11", "aurora12"]

MEDIA_TABS = ["Media", "Files", "Links"]
