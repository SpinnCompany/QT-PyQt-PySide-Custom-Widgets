"""RhythmoTune music dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

This orchestrator is DELIBERATELY thin: the framework does the heavy lifting.
  - Colours come from the ACTIVE theme's Other-variables via
    ``themeEngine.customColors()`` (they flip on a theme switch, no style.json
    reading here).
  - Icons are set in the .ui (QCustomQPushButton/QCustomQLabel `iconName` + size)
    and recoloured from QSS (`qproperty-iconColor`, incl. `:checked` states) —
    no icon code here at all.
  - Cover / avatar imagery is loaded straight from URLs by the WIDGETS
    themselves (QCustomAvatar.imageSource, QCustomCoverCard/CoverFlow/PlayerBar
    cover sources) via Custom_Widgets.ImageLoader — no ImageWorker here.
  - Theme flips with ``themeEngine.toggleTheme()`` (no target computed here).
The window shell hosts one QCustomComponentContainer per region; this fills each
region's live ``container.form.ui`` with data + icons and re-applies on
``onThemeChangeComplete``.
"""

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QHBoxLayout, QLabel, QWidget, QButtonGroup

from Custom_Widgets.QCustomAvatar import QCustomAvatar
from gui import data as D

_THEME_DARK = "RhythmoTune Dark"
_THEME_LIGHT = "RhythmoTune Light"


def _face(idx, size):
    return "https://i.pravatar.cc/%d?img=%d" % (size, idx)


class GuiFunctions:
    _NEED = ["sidebarContainer", "topBarContainer", "heroContainer",
             "categoriesContainer", "popularContainer", "playerContainer"]

    def __init__(self, win):
        self.win = win
        self.ui = win.ui
        self._activeNav = "Home"

    # -- lifecycle -------------------------------------------------------- #
    def initialize(self):
        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self._populateWhenReady()

    def _ui(self, name):
        cont = getattr(self.ui, name, None)
        if cont is None:
            return None
        live = getattr(getattr(cont, "form", None), "ui", None)
        return live if live is not None else getattr(cont, "component", None)

    def _root(self, name):
        return getattr(self.ui, name, None)   # the container widget (QSS cascades)

    def _components_ready(self):
        return all(self._ui(n) is not None for n in self._NEED)

    def _populateWhenReady(self, tries=0):
        if not self._components_ready():
            if tries < 50:
                QTimer.singleShot(60, lambda: self._populateWhenReady(tries + 1))
            return
        self._buildAll()
        # components can swap their live ui shortly after first load — re-apply
        # a few times so idempotent builders land on the final instances.
        n = getattr(self, "_settle", 0)
        if n < 4:
            self._settle = n + 1
            QTimer.singleShot(300 + n * 350, self._populateWhenReady)

    def _pal(self):
        pal = self.themeEngine.customColors() if self.themeEngine else {}
        return pal

    # -- build ------------------------------------------------------------ #
    def _buildAll(self):
        pal = self._pal()
        if not pal:                       # theme vars not ready yet — retry
            QTimer.singleShot(80, self._populateWhenReady)
            return
        for name, fn in [("sidebarContainer", self._sidebar),
                         ("topBarContainer", self._topbar),
                         ("heroContainer", self._hero),
                         ("categoriesContainer", self._categories),
                         ("popularContainer", self._popular),
                         ("playerContainer", self._player)]:
            try:
                fn(self._ui(name), self._root(name), pal)
            except Exception:
                import traceback
                traceback.print_exc()

    def _onThemeReady(self):
        try:
            self._repolishTree()   # force QSS qproperty-* colours to re-apply on switch
            self._buildAll()
        except Exception:
            import traceback
            traceback.print_exc()

    def _repolishTree(self):
        """Re-polish every widget so app-QSS `qproperty-*` values (painted-widget
        colours, container backgrounds) pick up the new theme. Qt caches qproperty
        from a stylesheet until the widget is unpolished/polished — only allowed
        Python here (polish/unpolish), no styling."""
        from qtpy.QtWidgets import QWidget
        widgets = self.win.findChildren(QWidget)
        widgets.append(self.win)
        for w in widgets:
            try:
                st = w.style()
                st.unpolish(w)
                st.polish(w)
                w.update()
            except Exception:
                pass

    # -- sidebar ---------------------------------------------------------- #
    # Icons (logo/nav/playlist) + their sizes are set in chrome.scss / the .ui —
    # Python only manages the nav CHECKED state and builds the playlist rows.
    def _sidebar(self, c, root, pal):
        if not hasattr(self, "_navGroup"):
            self._navGroup = QButtonGroup(self.win); self._navGroup.setExclusive(True)
        for obj, label in [("navHome", "Home"), ("navCategories", "Categories"),
                           ("navArtists", "Artists")]:
            b = getattr(c, obj)
            b.setChecked(label == self._activeNav)
            if self._navGroup.id(b) < 0:
                self._navGroup.addButton(b)
            if not getattr(b, "_wired", False):
                b._wired = True
                b.clicked.connect(lambda _c=False, l=label: self._navClicked(l))
        activeObj = {"Home": "navHome", "Categories": "navCategories",
                     "Artists": "navArtists"}.get(self._activeNav, "navHome")
        getattr(c, activeObj).setChecked(True)     # re-assert (exclusive group can steal it)
        self._buildPlaylists(c, pal)

    def _buildPlaylists(self, c, pal):
        lay = c.playlistsBox.layout()
        while lay.count():
            it = lay.takeAt(0)
            w = it.widget()
            if w is not None:
                w.setParent(None); w.deleteLater()
        for name, idx in D.PLAYLISTS:
            row = QWidget(); row.setObjectName("playlistRow")   # styled by chrome.scss
            rl = QHBoxLayout(row); rl.setContentsMargins(6, 5, 6, 5); rl.setSpacing(10)
            if idx is not None:
                av = QCustomAvatar(text=name[:1])        # reuse the avatar widget
                av.setFixedSize(26, 26)                  # layout only; colours/shape via chrome.scss
                av.setImageSource(_face(idx, 120))       # widget fetches + crops itself (content)
                rl.addWidget(av)
            else:
                spacer = QWidget(); spacer.setFixedSize(26, 26)
                rl.addWidget(spacer)                     # keep text aligned, no thumb
            lb = QLabel(name); lb.setObjectName("playlistLabel")
            lb.setProperty("muted", idx is None)         # dynamic prop → chrome.scss selector
            rl.addWidget(lb); rl.addStretch(1)
            lay.addWidget(row)

    def _navClicked(self, label):
        self._activeNav = label
        try:
            self._sidebar(self._ui("sidebarContainer"), self._root("sidebarContainer"), self._pal())
        except Exception:
            pass

    # -- top bar ---------------------------------------------------------- #
    # chrome (#searchFrame / #userName / #planBadge / #heartBtn …) is in chrome.scss
    def _topbar(self, c, root, pal):
        c.userName.setText(D.USER["name"])
        c.planBadge.setText(D.USER["plan"])
        c.userAvatar.setImageSource(D.USER["avatar"])     # content; bgColor via chrome.scss
        # per-button flag (NOT an instance flag): a component can swap its live
        # widgets during settle, so re-wire whichever settingsBtn is current.
        if not getattr(c.settingsBtn, "_wired", False):
            c.settingsBtn._wired = True
            c.settingsBtn.clicked.connect(self._toggleTheme)

    # -- hero ------------------------------------------------------------- #
    # coverFlow colours (title/artist/play) are set via chrome.scss qproperty.
    def _hero(self, c, root, pal):
        cf = c.coverFlow
        cf.setItems([{"title": t, "artist": a, "accent": ac, "coverPath": _face(idx, 500)}
                     for (t, a, ac, idx) in D.HERO])       # per-item data (title/artist/cover/fallback)
        cf.setCurrentIndex(D.HERO_ACTIVE, animate=False)
        if not getattr(self, "_heroWired", False):
            self._heroWired = True
            cf.playClicked.connect(self._playHero)

    def _playHero(self, i):
        try:
            t, a, _c, idx = D.HERO[i]
            pb = self._ui("playerContainer").playerBar
            pb.setTrack(title=t, artist=a, coverPath=_face(idx, 200))
            pb.setPlaying(True)
        except Exception:
            pass

    # -- categories ------------------------------------------------------- #
    # header/arrows/chip styling all live in chrome.scss (#categoriesTitle,
    # #prevCatBtn, QCustomChip[selected="true"] …)
    def _categories(self, c, root, pal):
        grp = c.chipGroup
        if grp.count() == 0:
            for i, name in enumerate(D.CATEGORIES):
                chip = grp.addChip(name, data=name)
                if i == 0:
                    try:
                        chip.setSelected(True)
                    except Exception:
                        pass

    # -- popular songs ---------------------------------------------------- #
    # header/arrows in chrome.scss; the CARDS are painted widgets configured via
    # their own Qt properties (setProperty), which is allowed.
    def _popular(self, c, root, pal):
        for b, dx in [(c.prevSongBtn, -396), (c.nextSongBtn, 396)]:
            if not getattr(b, "_wired", False):
                b._wired = True
                b.clicked.connect(lambda _c=False, d=dx: self._scrollSongs(d))
        # card colours (per-slot accent band, text colour, align, scale) all live
        # in chrome.scss (#song0…#song5 + QCustomCoverCard). Python only feeds data.
        for i, (title, artist, _accent, idx) in enumerate(D.POPULAR):
            getattr(c, "song%d" % i).setData(title=title, artist=artist,
                                             coverPath=_face(idx, 400))

    def _scrollSongs(self, dx):
        try:
            bar = self._ui("popularContainer").songsScroll.horizontalScrollBar()
            bar.setValue(bar.value() + dx)
        except Exception:
            pass

    # -- player ----------------------------------------------------------- #
    # playerBar colours are set via chrome.scss qproperty; Python feeds only data.
    def _player(self, c, root, pal):
        np = D.NOW_PLAYING
        c.playerBar.setTrack(title=np["title"], artist=np["artist"], elapsed=np["elapsed"],
                             total=np["total"], position=np["position"],
                             coverPath=_face(np["cover"], 200))

    # -- theme ------------------------------------------------------------ #
    def _toggleTheme(self):
        if self.themeEngine is not None:
            # explicit named pair — unambiguous vs any built-in Light/Dark themes
            self.themeEngine.toggleTheme(_THEME_DARK, _THEME_LIGHT)
