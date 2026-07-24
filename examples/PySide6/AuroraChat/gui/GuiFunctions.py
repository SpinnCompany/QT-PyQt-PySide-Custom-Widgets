"""Aurora Chat — GUI orchestration (the CORRECT Custom_Widgets way, normalized).

Design lives in Designer + QSS; Python only handles LOGIC. The whole chat UI is
assembled from reusable Custom_Widgets in ``ui/ChatComponent.ui``
(QCustomChatList, QCustomChatThread, QCustomChatInput, QCustomMediaGrid,
QCustomActionButton, …). Icons are set in QSS via ``theme-icons``; colours come
from the token-driven ChatPalette. This manager just feeds those widgets DATA
and connects their signals — it never builds or paints a row/bubble/tile.
"""

import os

from qtpy.QtCore import QObject, QTimer, QByteArray, Qt, QThread
from qtpy.QtGui import QColor, QPainter, QPixmap, QIcon, QBrush
from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets
from Custom_Widgets.QCustomEmojiPicker import QCustomEmojiPicker
from Custom_Widgets.QCustomImageViewer import QCustomImageViewer

from gui import theme as T
from gui import data as D
from gui import net
from gui.workers import TypingWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _feather_pixmap(name, color, size=20, stroke=2.1):
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path):
        svg = open(path, "r", encoding="utf-8").read()
        svg = (svg.replace('stroke="#ffffff"', 'stroke="%s"' % color)  # noqa: hardcoded-hex — recolour placeholder in source SVG, not chrome
                  .replace('stroke-width="3"', 'stroke-width="%s"' % stroke))
        r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        from qtpy.QtCore import QRectF
        r.render(p, QRectF(0, 0, pm.width(), pm.height()))
        p.end()
    pm.setDevicePixelRatio(2.0)
    return pm


def _badge_pixmap(accent, size=20):
    pm = QPixmap(size * 2, size * 2)
    pm.setDevicePixelRatio(2.0)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(accent)))
    p.drawEllipse(0, 0, size * 2, size * 2)
    p.end()
    check = _feather_pixmap("check", "#ffffff", int(size * 0.66), stroke=3.2)  # noqa: hardcoded-hex — white tick on accent badge is intentional, theme-independent
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    off = (size * 2 - check.width() / check.devicePixelRatio()) / 2.0
    p.drawPixmap(int(off), int(off), check)
    p.end()
    return pm


# --------------------------------------------------------------------------- #
# Data adapters — tuples in gui/data.py -> the dict shapes the widgets expect.
# --------------------------------------------------------------------------- #
def _conversations():
    out = []
    for name, preview, tm, unread, online, muted in D.CONVERSATIONS:
        out.append({"name": name, "preview": preview, "time": tm,
                    "unread": unread, "online": online, "muted": muted})
    return out


def _thread_messages(active_name):
    out = []
    for row in D.THREAD:
        kind = row[0]
        # a trailing dict carries per-message extras (status ticks / reactions)
        extras = row[-1] if isinstance(row[-1], dict) else {}
        if kind == "date":
            out.append({"kind": "date", "text": row[1]})
            continue
        if kind == "voice":
            msg = {"kind": "voice", "side": row[1], "duration": row[2],
                   "time": row[3], "wave": D.VOICE_WAVE}
        elif kind in ("in", "out"):
            msg = {"kind": "text", "side": kind, "text": row[1], "time": row[2]}
        elif kind == "outcost":
            msg = {"kind": "text", "side": "out", "text": row[1],
                   "time": row[3], "foot": row[2] + "  |  " + row[3]}
        else:
            continue
        if extras.get("status"):
            msg["status"] = extras["status"]
        if extras.get("reactions"):
            msg["reactions"] = extras["reactions"]
        out.append(msg)
    return out


# --------------------------------------------------------------------------- #
# Chat page manager — DATA + WIRING only.
#
# The chat screen is composed from many small component .ui files
# (ChatsList / Thread / ThreadHeader / Composer / Profile / MediaPanel),
# each loaded ASYNCHRONOUSLY into a QCustomComponentContainer. Rather than walk
# the nested container.component chains, this manager reaches every widget by
# its (globally-unique) objectName via findChild on the window, and simply waits
# until the widgets it needs exist before wiring them.
# --------------------------------------------------------------------------- #
class ChatManager(QObject):
    # widgets that must exist (across the loaded sub-components) before wiring
    _REQUIRED = ("chatList", "chatThread", "chatInput", "threadName",
                 "threadStatus", "threadAvatar", "profileName", "profileAvatar",
                 "profileVerified", "creditsBanner", "customizeChevron")

    def __init__(self, win):
        super().__init__(win)
        self.win = win
        self._loaded = False
        self.images = getattr(win, "_imageLoader", None)

    # widget lookup by objectName, resilient to however deep components nest
    def w(self, name):
        return self.win.findChild(QWidget, name)

    def onShown(self):
        if self._loaded:
            return
        if any(self.w(n) is None for n in self._REQUIRED):
            QTimer.singleShot(80, self.onShown)   # components still loading
            return
        try:
            self.setup()
            self._loaded = True
        except Exception:
            import traceback
            traceback.print_exc()

    def _theme(self):
        eng = getattr(self.win, "themeEngine", None)
        return str(getattr(eng, "theme", "") or T.THEME_LIGHT)

    def _palette(self):
        return T.chat_palette(self._theme())

    # -- build ------------------------------------------------------------- #
    def setup(self):
        self._active_row = D.ACTIVE_INDEX
        self._messages = _thread_messages(D.CONVERSATIONS[self._active_row][0])

        self._style_chrome()
        chatList = self.w("chatList")
        chatList.setConversations(_conversations())
        chatList.setCurrentIndex(self._active_row, emit=False)
        chatThread = self.w("chatThread")
        chatThread.setSenderName(D.CONVERSATIONS[self._active_row][0])
        chatThread.setMessages(self._messages)

        # signals
        chatList.currentChanged.connect(self._on_conversation)
        self.w("chatInput").sendMessage.connect(self._on_send)
        self.w("chatInput").emojiClicked.connect(self._open_emoji_picker)
        self.w("customizeChevron").clicked.connect(self._toggle_media_section)
        # reactions: clicking a chip adds one more; the "+" opens the emoji picker
        chatThread.reactionClicked.connect(chatThread.addReaction)
        chatThread.reactionAddRequested.connect(self._open_reaction_picker)

        # sync header + profile + thread to the active conversation deterministically
        self._on_conversation(self._active_row)
        self._load_avatars()
        # media/files/links live in the MediaPanelComponent sub-component, which
        # loads asynchronously — wire it once it is available.
        self._media_ready = False
        self._viewer = None
        self._media_pixmaps = [None] * len(D.MEDIA_SEEDS)
        self._setup_media()

        # presence worker (Worker -> Signal -> GUI)
        self._thread = QThread(self.win)
        self._worker = TypingWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.presenceChanged.connect(self._on_presence)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self.teardown)

    # -- the ONLY per-theme Python left: painted bits QSS can't express ----- #
    def _style_chrome(self):
        # Every colour/icon is driven by the app QSS (chrome.scss + theme-icons)
        # and auto-re-polished by the theme engine. Only two painted, theme-
        # dependent bits remain in code: the verified-badge pixmap and the
        # credits banner's dark-only visibility (colour read from ChatPalette —
        # the sanctioned painted-from-theme-role exception).
        pal = self._palette()
        self.w("profileVerified").setPixmap(_badge_pixmap(pal["verified"], 20))
        profileAvatar = self.w("profileAvatar")
        profileAvatar.ringColor = QColor(pal["accent"])
        profileAvatar.ringWidth = 3
        self.w("creditsBanner").setVisible(not T.is_light(self._theme()))

    # -- avatars / media (async, cached, offline-safe) --------------------- #
    def _load_avatars(self):
        if not self.images:
            return
        chatList = self.w("chatList")
        for i, (g, idx) in enumerate(D.AVATAR_SPECS):
            self.images.load(net.avatar_url(idx, g),
                             lambda pm, ix=i: chatList.setAvatarImageAt(ix, pm))
        self._load_header_avatars()

    def _load_header_avatars(self):
        if not self.images or self._active_row >= len(D.AVATAR_SPECS):
            return
        g, idx = D.AVATAR_SPECS[self._active_row]
        url = net.avatar_url(idx, g, size=400)
        for name in ("threadAvatar", "profileAvatar"):
            av = self.w(name)
            if av is not None:
                self.images.load(url, lambda pm, a=av: a.setImage(pm))

    # -- media / files / links sub-component (loads async) ----------------- #
    def _setup_media(self):
        grid = self.w("mediaGrid")
        tabs = self.w("mediaTabs")
        stack = self.w("mediaStack")
        if grid is None or tabs is None or stack is None:   # not loaded yet
            QTimer.singleShot(80, self._setup_media)
            return
        self._media_ready = True
        grid.setPlaceholders(D.MEDIA_TILES)
        # Tabs (Media/Files/Links) are defined in MediaPanelComponent.ui via the
        # segmented control's `segments` Designer property; here we only wire the
        # LOGIC: switch the stacked pages, and open the lightbox on a tile click.
        tabs.currentChanged.connect(stack.setCurrentIndex)
        grid.tileClicked.connect(self._open_lightbox)
        self._load_media()

    def _load_media(self):
        if not self.images or not self._media_ready:
            return
        for i, seed in enumerate(D.MEDIA_SEEDS):
            self.images.load(net.media_url(seed, 220, 150),
                             lambda pm, ix=i: self._on_media_pixmap(ix, pm))

    def _on_media_pixmap(self, index, pm):
        self._media_pixmaps[index] = pm
        grid = self.w("mediaGrid")
        if grid is not None:
            grid.setImageAt(index, net.rounded_pixmap(pm, 22))
        if self._viewer is not None:
            self._viewer.setImageAt(index, pm)

    def _open_lightbox(self, index):
        if self._viewer is None:
            self._viewer = QCustomImageViewer(parent=self.win)
        imgs = [pm for pm in self._media_pixmaps if pm is not None]
        # keep viewer index aligned with the grid's loaded tiles
        loaded = [i for i, pm in enumerate(self._media_pixmaps) if pm is not None]
        self._viewer.setImages(imgs)
        start = loaded.index(index) if index in loaded else 0
        self._viewer.openAt(start, self.win)

    # -- interactions ------------------------------------------------------ #
    def _on_conversation(self, idx):
        self._active_row = idx
        name = D.CONVERSATIONS[idx][0]
        self.w("threadName").setText(name)
        self.w("profileName").setText(name)
        color = D.AVATAR_COLORS[idx % len(D.AVATAR_COLORS)]
        for wname in ("threadAvatar", "profileAvatar"):
            av = self.w(wname)
            av.setText(name[:1])
            av.bgColor = QColor(color)
        self._messages = _thread_messages(name)
        chatThread = self.w("chatThread")
        chatThread.setSenderName(name)
        chatThread.setMessages(self._messages)
        self._load_header_avatars()

    def _on_send(self, text):
        self._messages.append({"kind": "text", "side": "out", "text": text, "time": "now"})
        self.w("chatThread").setMessages(self._messages)

    def _open_emoji_picker(self):
        picker = QCustomEmojiPicker(parent=self.win, target=self.w("chatInput").field(),
                                    tailPosition="bottom-right", itemsPerRow=9, autoUpdate=True)
        picker.show()

    def _open_reaction_picker(self, index, bar):
        # Pick an emoji to react to message `index`; apply it to the thread.
        picker = QCustomEmojiPicker(parent=self.win, target=bar,
                                    tailPosition="bottom-left", itemsPerRow=8,
                                    autoUpdate=False)
        thread = self.w("chatThread")

        def _apply(emoji):
            thread.addReaction(index, emoji)
            try:
                picker.close()
            except Exception:
                pass
        picker.emojiSelected.connect(_apply)
        picker.show()

    def _toggle_media_section(self):
        mc = self.w("mediaContainer")
        if mc is not None:
            mc.setVisible(not mc.isVisible())

    def _on_presence(self, typing):
        # Text only — colour is QSS-driven (a `typing` dynamic property could add
        # an accent colour via QSS, but green reads fine).
        ts = self.w("threadStatus")
        if ts is not None:
            ts.setText("typing…" if typing else "Online")

    # -- theme recolour ---------------------------------------------------- #
    def recolor(self):
        # The theme engine re-polishes every QSS-driven widget automatically on a
        # theme change; only the painted badge + credits visibility need a nudge.
        if not self._loaded:
            return
        self._style_chrome()

    def teardown(self):
        try:
            self._worker.stop()
            self._thread.quit()
            self._thread.wait(1200)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
class GuiFunctions:
    # sidebar widgets live in SidebarComponent/UserCardComponent (async-loaded)
    _SIDEBAR = ("navChat", "navPeople", "navShop", "navRequests", "navArchive",
                "themeToggle", "brandLogo", "sidebarAvatar")

    def __init__(self, win):
        self.win = win
        self.navButtons = {}
        self._active = "chat"
        self._theme_reasserted = False

    def w(self, name):
        return self.win.findChild(QWidget, name)

    def initialize(self):
        self.images = net.RemoteImageLoader(self.win)
        self.win._imageLoader = self.images
        self.chat = ChatManager(self.win)

        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self.win.toggleTheme = self.toggleTheme

        # The sidebar is a component that loads asynchronously — wire it (and the
        # chat page) once its widgets exist.
        self._wireWhenReady()
        # Boot applies the default (light) theme first; the persisted theme is
        # NOT re-applied after the async component tree (incl. the profile's
        # QCustomThemeList) finishes loading, so a persisted dark theme renders
        # light. Re-assert the persisted theme ONCE, after the deepest themed
        # component exists. Runtime setTheme fully re-applies palette+QSS.
        self._reassertThemeWhenReady()

    def _wireWhenReady(self):
        if any(self.w(n) is None for n in self._SIDEBAR):
            QTimer.singleShot(80, self._wireWhenReady)
            return
        self.navButtons = {"chat": self.w("navChat"), "people": self.w("navPeople"),
                           "shop": self.w("navShop"), "requests": self.w("navRequests"),
                           "archive": self.w("navArchive")}
        for name, btn in self.navButtons.items():
            btn.clicked.connect(lambda _=False, n=name: self.navigateTo(n))
        self.w("themeToggle").clicked.connect(self.toggleTheme)

        self._paintChrome()
        self.navigateTo("chat")

        # signed-in user portrait (async; initials stay if offline)
        try:
            g, idx = D.USER_AVATAR
            av = self.w("sidebarAvatar")
            self.images.load(net.avatar_url(idx, g, 200), lambda pm: av.setImage(pm))
        except Exception:
            pass

    def _reassertThemeWhenReady(self):
        if self._theme_reasserted or self.themeEngine is None:
            return
        # wait for the profile's theme list (deepest themed sub-component) to load
        if self.win.findChild(QWidget, "themeList") is None:
            QTimer.singleShot(90, self._reassertThemeWhenReady)
            return
        # let the theme list finish its own init, then force the persisted theme
        QTimer.singleShot(150, self._reassertTheme)

    def _reassertTheme(self):
        if self._theme_reasserted or self.themeEngine is None:
            return
        self._theme_reasserted = True
        try:
            self.themeEngine.setTheme(self._currentTheme())
        except Exception:
            import traceback
            traceback.print_exc()

    def _currentTheme(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_LIGHT)

    def toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_DARK if T.is_light(self._currentTheme()) else T.THEME_LIGHT
        self.themeEngine.setTheme(target)

    def _onThemeReady(self):
        # The theme engine + dev-server file listeners autocompile and apply the
        # stylesheet on any change; we only re-colour the token-driven chrome
        # (icons, chat-surface widget properties) that live outside the QSS.
        self._paintChrome()
        try:
            self.chat.recolor()
        except Exception:
            import traceback
            traceback.print_exc()

    def _paintChrome(self):
        # Nav icons + most chrome icons are QSS (theme-icons); Python only
        # re-asserts the active nav checked-state and the moon/sun toggle + brand.
        theme = self._currentTheme()
        pal = T.chat_palette(theme)
        for name, btn in self.navButtons.items():
            btn.setChecked(name == self._active)
        try:
            brandLogo = self.w("brandLogo")
            brandLogo.bgColor = QColor(pal["accent"])
            brandLogo.setText("A")
            sidebarAvatar = self.w("sidebarAvatar")
            sidebarAvatar.bgColor = QColor(D.AVATAR_COLORS[0])
            sidebarAvatar.statusColor = QColor(pal["onlineDot"])
            sidebarAvatar.statusBorderColor = QColor(pal["chipBg"])
            light = T.is_light(theme)
            themeToggle = self.w("themeToggle")
            themeToggle.setIcon(QIcon(_feather_pixmap("moon" if light else "sun",
                                                      T.icon_color(theme), 20)))
            themeToggle.labelText = "Dark mode" if light else "Light mode"
        except Exception:
            pass

    def navigateTo(self, name):
        self._active = name
        for n, btn in self.navButtons.items():
            btn.setChecked(n == name)
        if name == "chat":
            self.chat.onShown()
