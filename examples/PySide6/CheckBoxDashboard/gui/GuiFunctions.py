"""Check Box dashboard — GUI orchestration (the CORRECT Custom_Widgets way).

The window shell (ui/MainWindow.ui) hosts one QCustomComponentContainer per
region; each loads a granular component .ui (TopNav, LeftRail, Header, and the
four cards) and exposes it as ``container.component``. This orchestrator reaches
each component by objectName and fills in runtime data + the painted data-viz
(line chart, dot matrix, beeswarm, gantt) and every icon.

Colours come from the token-driven ChartPalette in json-styles/style.json, so
they flip when the theme switches (CheckBox Dark / CheckBox Light) — no
hard-coded hex in Python.
"""

import os

from qtpy.QtCore import QObject, Qt, QByteArray, QThread, QTimer, QPointF
from qtpy.QtGui import (QColor, QPainter, QPixmap, QIcon, QBrush, QPen,
                        QPolygonF, QFont)
from qtpy.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout
from qtpy.QtSvg import QSvgRenderer

import Custom_Widgets

from gui import theme as T
from gui import data as D
from gui.workers import ClockWorker, AvatarWorker

_ICON_DIR = os.path.join(os.path.dirname(Custom_Widgets.__file__), "Qss", "icons", "feather")
_PM_CACHE = {}


# --------------------------------------------------------------------------- #
# Painted helpers (feather icons, composed markers, small primitives)
# --------------------------------------------------------------------------- #
def feather_pixmap(name, color, size=22, stroke=2.2):
    key = ("f", name, color, size, stroke)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    path = os.path.join(_ICON_DIR, name + ".svg")
    pm = QPixmap(int(size * 2), int(size * 2))
    pm.fill(QColor(0, 0, 0, 0))
    if os.path.exists(path):
        svg = open(path, "r", encoding="utf-8").read()
        svg = svg.replace('stroke="#ffffff"', 'stroke="%s"' % color)
        svg = svg.replace('stroke="#000000"', 'stroke="%s"' % color)
        svg = svg.replace('stroke-width="3"', 'stroke-width="%s"' % stroke)
        r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        r.render(p)
        p.end()
    pm.setDevicePixelRatio(2.0)
    _PM_CACHE[key] = pm
    return pm


def feather_icon(name, color, size=22, stroke=2.2):
    return QIcon(feather_pixmap(name, color, size, stroke))


def marker_pixmap(name, bg, fg, size=26, glyph=15):
    """A filled circle (bg) with a centred feather glyph (fg) — the leading
    badge that sits at the start of each timeline bar."""
    key = ("m", name, bg, fg, size, glyph)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    s = size * 2
    pm = QPixmap(s, s)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(bg)))
    p.drawEllipse(0, 0, s, s)
    gp = feather_pixmap(name, fg, glyph, 2.4)
    gx = (s - gp.width() / gp.devicePixelRatio()) / 2.0
    gy = (s - gp.height() / gp.devicePixelRatio()) / 2.0
    p.drawPixmap(int(gx), int(gy), gp)
    p.end()
    pm.setDevicePixelRatio(2.0)
    _PM_CACHE[key] = pm
    return pm


def triangle_pixmap(up, color, size=12):
    key = ("t", up, color, size)
    if key in _PM_CACHE:
        return _PM_CACHE[key]
    s = size * 2
    pm = QPixmap(s, s)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(color)))
    if up:
        poly = QPolygonF([QPointF(s / 2.0, s * 0.15), QPointF(s * 0.85, s * 0.8),
                          QPointF(s * 0.15, s * 0.8)])
    else:
        poly = QPolygonF([QPointF(s * 0.15, s * 0.2), QPointF(s * 0.85, s * 0.2),
                          QPointF(s / 2.0, s * 0.85)])
    p.drawPolygon(poly)
    p.end()
    pm.setDevicePixelRatio(2.0)
    _PM_CACHE[key] = pm
    return pm


def dot_pixmap(color, size=10):
    s = size * 2
    pm = QPixmap(s, s)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(color)))
    p.drawEllipse(0, 0, s, s)
    p.end()
    pm.setDevicePixelRatio(2.0)
    return pm


def _clear_layout(lay):
    if lay is None:
        return
    while lay.count():
        it = lay.takeAt(0)
        w = it.widget()
        if w is not None:
            w.setParent(None)
            w.deleteLater()


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #
class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui
        self._built = False

    # -- lifecycle -------------------------------------------------------- #
    def initialize(self):
        self.themeEngine = getattr(self.win, "themeEngine", None)
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._onThemeReady)
            except Exception:
                pass
        self._populateWhenReady()
        self._watchSources()

    def _watchSources(self):
        """Re-apply the code-populated content (icons + data) after a component
        hot-reload. Editing a component .ui regenerates src/ui_<name>.py and the
        container rebuilds that component's widget subtree BLANK — so we watch
        src/ and debounce a full re-populate onto the fresh widgets. This is what
        makes the live-reload dev loop actually keep the data/icons."""
        try:
            from qtpy.QtCore import QFileSystemWatcher, QTimer
            src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
            self._srcWatcher = QFileSystemWatcher(self.win)
            if os.path.isdir(src):
                self._srcWatcher.addPath(src)
            for f in os.listdir(src) if os.path.isdir(src) else []:
                if f.endswith(".py"):
                    self._srcWatcher.addPath(os.path.join(src, f))
            self._srcDir = src
            self._reapplyTimer = QTimer(self.win)
            self._reapplyTimer.setSingleShot(True)
            self._reapplyTimer.timeout.connect(self._reapply)
            self._srcWatcher.directoryChanged.connect(lambda _p: self._reapplyTimer.start(800))
            self._srcWatcher.fileChanged.connect(lambda _p: self._reapplyTimer.start(800))
        except Exception:
            pass

    def _reapply(self):
        # Re-arm watch paths that Qt drops when the converter rewrites files,
        # then re-populate the (freshly hot-reloaded) components.
        try:
            src = getattr(self, "_srcDir", None)
            if src and os.path.isdir(src):
                have = set(self._srcWatcher.files())
                for f in os.listdir(src):
                    p = os.path.join(src, f)
                    if f.endswith(".py") and p not in have:
                        self._srcWatcher.addPath(p)
        except Exception:
            pass
        self._populateWhenReady()

    def _theme_name(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_DARK)

    def _palette(self):
        return T.chart_palette(self._theme_name())

    _NEED = ["topNavContainer", "railContainer", "headerContainer",
             "customerContainer", "productContainer", "beeswarmContainer",
             "timelineContainer"]

    def _c(self, name):
        # Read the loader's LIVE ui. After a component hot-reload the container's
        # cached `.component` points at the deleted old Ui instance, whereas
        # `container.form.ui` is always the freshly-built one.
        cont = getattr(self.ui, name, None)
        if cont is None:
            return None
        live = getattr(getattr(cont, "form", None), "ui", None)
        return live if live is not None else getattr(cont, "component", None)

    def _components_ready(self):
        return all(self._c(n) is not None for n in self._NEED)

    def _populateWhenReady(self, tries=0):
        if not self._components_ready():
            if tries < 40:
                QTimer.singleShot(60, lambda: self._populateWhenReady(tries + 1))
            return
        self._buildAll()

    # -- build everything ------------------------------------------------- #
    def _buildAll(self):
        pal = self._palette()
        jobs = [("topNavContainer", self._topnav), ("railContainer", self._rail),
                ("headerContainer", self._header), ("customerContainer", self._customer),
                ("productContainer", self._product), ("beeswarmContainer", self._beeswarm),
                ("timelineContainer", self._timeline)]
        stale = False
        for name, fn in jobs:
            try:
                fn(self._c(name), pal)
            except RuntimeError:
                # a component was mid hot-reload (C++ child deleted) — retry soon
                stale = True
            except Exception:
                import traceback
                traceback.print_exc()
        if stale:
            QTimer.singleShot(250, self._populateWhenReady)

        if not self._built:
            self._built = True
            self._startClock()
            self._loadAvatar()

    def _onThemeReady(self):
        try:
            self._buildAll()
        except Exception:
            import traceback
            traceback.print_exc()

    # -- top nav ---------------------------------------------------------- #
    def _topnav(self, c, pal):
        icol = T.icon_color(self._theme_name())
        c.navBtn0.setIcon(feather_icon("box", pal["accentText"] if c.navBtn0.isChecked() else icol, 18))
        c.navBtn1.setIcon(feather_icon("bar-chart-2", icol, 18))
        c.navBtn2.setIcon(feather_icon("message-square", icol, 18))
        for b in (c.navBtn0, c.navBtn1, c.navBtn2):
            b.setIconSize(_qsize(18))
        c.searchBtn.setIcon(feather_icon("search", icol, 20))
        c.searchBtn.setIconSize(_qsize(20))
        self._avatarFallback(c, pal)

    def _avatarFallback(self, c, pal):
        self._paintAvatar(c.avatar, pal, self._initialsPixmap(pal))
        self._placeBadge(c.avatar, pal)

    def _initialsPixmap(self, pal, size=46):
        s = size * 2
        pm = QPixmap(s, s)
        pm.fill(QColor(0, 0, 0, 0))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(pal["accent"])))
        p.drawEllipse(0, 0, s, s)
        p.setPen(QColor(pal["accentText"]))
        f = QFont(); f.setPointSize(int(size * 0.42)); f.setBold(True)
        p.setFont(f)
        p.drawText(pm.rect(), Qt.AlignCenter, "BN")
        p.end()
        pm.setDevicePixelRatio(2.0)
        return pm

    def _paintAvatar(self, label, pal, pm):
        label.setPixmap(pm)
        label.setScaledContents(True)

    def _placeBadge(self, avatar, pal):
        badge = getattr(self, "_badge", None)
        if badge is None or badge.parent() is not avatar:
            badge = QLabel(avatar)
            self._badge = badge
        badge.setText(str(D.PROFILE["notifications"]))
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedSize(18, 18)
        badge.setStyleSheet(
            "background:%s; color:#ffffff; border-radius:9px; font-size:10px; "
            "font-weight:700;" % pal["badge"])
        badge.move(avatar.width() - 16, -2)
        badge.raise_()
        badge.show()

    # -- left rail -------------------------------------------------------- #
    def _rail(self, c, pal):
        icol = T.icon_color(self._theme_name())
        for i, name in enumerate(D.RAIL):
            btn = getattr(c, "railBtn%d" % i)
            active = btn.isChecked()
            btn.setIcon(feather_icon(name, pal["accent"] if active else icol, 20))
            btn.setIconSize(_qsize(20))
        c.addBtn.setIcon(feather_icon("plus", pal["accentText"], 22, 2.6))
        c.addBtn.setIconSize(_qsize(22))

    # -- header ----------------------------------------------------------- #
    def _header(self, c, pal):
        icol = T.icon_color(self._theme_name())
        for i in range(3):
            btn = getattr(c, "filterBtn%d" % i)
            btn.setIcon(feather_icon("chevron-down", icol, 16))
            btn.setIconSize(_qsize(16))
        c.settingsBtn.setIcon(feather_icon("sliders", icol, 18))
        c.settingsBtn.setIconSize(_qsize(18))
        if not getattr(self, "_themeWired", False):
            self._themeWired = True
            c.settingsBtn.clicked.connect(self._toggleTheme)

    # -- CUSTOMER card ---------------------------------------------------- #
    def _customer(self, c, pal):
        cat = [pal["green"], pal["orange"]]
        # two overlaid trend lines: orange first, green second (per reference)
        c.customerLines.setSeries(D.CUSTOMER_LINES, [pal["orange"], pal["green"]])
        for i, (value, capn, direction, catidx) in enumerate(D.CUSTOMER_STATS):
            col = pal["green"] if catidx == 1 else pal["orange"]
            getattr(c, "custArrow%d" % i).setPixmap(triangle_pixmap(direction == "up", col, 12))
            getattr(c, "custArrow%d" % i).setScaledContents(False)
            getattr(c, "custValue%d" % i).setText(value)
            getattr(c, "custCap%d" % i).setText(capn)

    # -- PRODUCT (small) card --------------------------------------------- #
    def _product(self, c, pal):
        m = c.productMatrix
        # states 1=green, 2=orange, 3=white
        m.setColors([pal["green"], pal["orange"], pal["white"]])
        m.emptyColor = QColor(pal["dotEmpty"])
        m.setData(D.PRODUCT_MATRIX)
        for i, (value, capn, direction, catidx) in enumerate(D.PRODUCT_STATS):
            col = pal["green"] if catidx == 1 else pal["orange"]
            getattr(c, "prodArrow%d" % i).setPixmap(triangle_pixmap(direction == "up", col, 12))
            getattr(c, "prodValue%d" % i).setText(value)
            getattr(c, "prodCap%d" % i).setText(capn)

    # -- PRODUCT (large) beeswarm ----------------------------------------- #
    def _beeswarm(self, c, pal):
        b = c.beeswarm
        # categories: 0=white/Resources, 1=green/Valid, 2=orange/Invalid
        b.setColors([pal["white"], pal["green"], pal["orange"]],
                    [pal["onColorText"], pal["onColorText"], pal["onOrangeText"]])
        b.lineColor = QColor(pal["beeswarmLine"])
        b.setData(D.BEESWARM)
        self._legend(c.beeswarmLegend, D.BEESWARM_LEGEND, pal)
        c.beeswarmTotal.setText("Total: " + D.BEESWARM_TOTAL)

    # -- PROJECTS TIMELINE gantt ------------------------------------------ #
    def _timeline(self, c, pal):
        g = c.timeline
        self._gantt = g
        # category -> colour: 0=white/Web, 1=green/Customer, 2=orange/Product
        cat_colors = [pal["white"], pal["green"], pal["orange"]]
        g.setColors(cat_colors,
                    [pal["onColorText"], pal["onColorText"], pal["onOrangeText"]])
        g.gridColor = QColor(pal["gridLine"])
        g.labelColor = QColor(pal["muted"])
        g.axisTextColor = QColor(pal["muted"])
        g.xMax = 30.0
        g.gridStep = 5.0
        g.barHeight = 44
        if not hasattr(self, "_brandPix"):
            self._brandPix = {}     # row -> composed real-logo marker
            self._grpPix = {}       # row -> composed avatar-group marker
            self._grpParts = {}     # row -> {k: QPixmap} partial photos
            self._mkBusy = set()
        rows = []
        for i, r in enumerate(D.TIMELINE):
            base = {k: v for k, v in r.items() if k not in ("brand", "avatars")}
            if "brand" in r:
                glyph, bg = D.BRAND[r["brand"]]
                base["icon"] = self._brandPix.get(
                    i, marker_pixmap(glyph, bg, "#ffffff", 26, 14))
                self._loadBrandLogo(i, r["brand"], bg)
            else:
                base["icon"] = self._grpPix.get(
                    i, marker_pixmap("users", pal["faint"], pal["muted"], 26, 13))
                self._loadAvatarGroup(i, min(3, int(r.get("avatars", 3))))
            rows.append(base)
        self._tlRows = rows
        g.setData(rows)
        self._legend(c.timelineLegend, D.TIMELINE_LEGEND, pal, cat_colors)
        c.timelineTotal.setText("Total: " + D.TIMELINE_TOTAL)

    def _spawn(self, url, cb):
        th = QThread(self.win)
        wk = AvatarWorker(url)
        wk.moveToThread(th)
        th.started.connect(wk.run)
        wk.loaded.connect(cb)
        if not hasattr(self, "_tlThreads"):
            self._tlThreads = []
        self._tlThreads.append((th, wk))
        th.start()

    def _refreshGantt(self, index, pm):
        rows = getattr(self, "_tlRows", None)
        g = getattr(self, "_gantt", None)
        if rows and g is not None and index < len(rows):
            rows[index]["icon"] = pm
            g.setData(rows)

    # -- real brand logo (public simpleicons CDN, async) ------------------ #
    def _loadBrandLogo(self, index, slug, bg):
        key = ("brand", index)
        if index in self._brandPix or key in self._mkBusy:
            return
        self._mkBusy.add(key)
        # cdn.simpleicons.org returns a single-colour SVG; ask for white.
        self._spawn("https://cdn.simpleicons.org/%s/ffffff" % slug,
                    lambda raw, i=index, b=bg: self._onBrandLogo(i, b, raw))

    def _onBrandLogo(self, index, bg, raw):
        try:
            if raw and b"<svg" in raw[:400]:
                pm = self._composeBrand(raw, bg, 26)
                self._brandPix[index] = pm
                self._refreshGantt(index, pm)
        except Exception:
            pass
        finally:
            self._mkBusy.discard(("brand", index))

    def _composeBrand(self, svg_raw, bg, size=26, logo_frac=0.54):
        from qtpy.QtCore import QRectF
        s = size * 2
        pm = QPixmap(s, s); pm.fill(QColor(0, 0, 0, 0))
        p = QPainter(pm); p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen); p.setBrush(QBrush(QColor(bg)))
        p.drawEllipse(0, 0, s, s)
        r = QSvgRenderer(QByteArray(svg_raw))
        lw = s * logo_frac
        r.render(p, QRectF((s - lw) / 2.0, (s - lw) / 2.0, lw, lw))
        p.end(); pm.setDevicePixelRatio(2.0)
        return pm

    # -- real avatar GROUP (overlapping portraits, async) ----------------- #
    def _loadAvatarGroup(self, index, n):
        key = ("grp", index)
        if index in self._grpPix or key in self._mkBusy:
            return
        self._mkBusy.add(key)
        self._grpParts[index] = {}
        for k in range(n):
            gender = "women" if (index + k) % 2 else "men"
            url = "https://randomuser.me/api/portraits/%s/%d.jpg" % (gender, 12 + index * 5 + k)
            self._spawn(url, lambda raw, i=index, kk=k, tot=n: self._onGroupPart(i, kk, tot, raw))

    def _onGroupPart(self, index, k, total, raw):
        try:
            pm = QPixmap()
            if raw and pm.loadFromData(raw):
                self._grpParts.setdefault(index, {})[k] = pm
            parts = self._grpParts.get(index, {})
            if len(parts) >= total:
                photos = [parts[j] for j in sorted(parts)]
                grp = self._composeGroup(photos, 26)
                self._grpPix[index] = grp
                self._refreshGantt(index, grp)
                self._mkBusy.discard(("grp", index))
        except Exception:
            self._mkBusy.discard(("grp", index))

    def _composeGroup(self, photos, d=26, overlap=0.46):
        from qtpy.QtGui import QPainterPath
        s = 2
        dd = d * s
        step = dd * (1.0 - overlap)
        n = len(photos)
        W = int(dd + step * (n - 1)); H = int(dd)
        out = QPixmap(W, H); out.fill(QColor(0, 0, 0, 0))
        p = QPainter(out); p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        for i, ph in enumerate(photos):
            x = int(i * step)
            p.save()
            path = QPainterPath(); path.addEllipse(x, 0, dd, dd)
            p.setClipPath(path)
            sc = ph.scaled(dd, dd, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            p.drawPixmap(x, 0, sc)
            p.restore()
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor("#ffffff"), max(1.0, s * 1.4)))
            p.drawEllipse(x + 1, 1, dd - 2, dd - 2)
        p.end(); out.setDevicePixelRatio(2.0)
        return out

    # -- legend builder --------------------------------------------------- #
    def _legend(self, holder, items, pal, cat_colors=None):
        lay = holder.layout()
        _clear_layout(lay)
        default = [pal["white"], pal["green"], pal["orange"]]
        for text, catidx in items:
            colors = cat_colors or default
            col = colors[catidx] if catidx < len(colors) else pal["muted"]
            item = QWidget()
            h = QHBoxLayout(item); h.setContentsMargins(0, 0, 0, 0); h.setSpacing(7)
            dot = QLabel(); dot.setFixedSize(10, 10)
            dot.setPixmap(dot_pixmap(col, 10)); dot.setScaledContents(True)
            lbl = QLabel(text); lbl.setProperty("role", "legendText")
            h.addWidget(dot); h.addWidget(lbl)
            lay.addWidget(item)

    # -- background clock ------------------------------------------------- #
    def _startClock(self):
        self._thread = QThread(self.win)
        self._worker = ClockWorker()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._thread.start()
        QApplication.instance().aboutToQuit.connect(self._teardownClock)

    def _teardownClock(self):
        try:
            self._worker.stop(); self._thread.quit(); self._thread.wait(1200)
        except Exception:
            pass

    # -- avatar (real image, best-effort async) --------------------------- #
    def _loadAvatar(self):
        try:
            self._avThread = QThread(self.win)
            self._avWorker = AvatarWorker("https://i.pravatar.cc/96?img=12")
            self._avWorker.moveToThread(self._avThread)
            self._avThread.started.connect(self._avWorker.run)
            self._avWorker.loaded.connect(self._onAvatar)
            self._avThread.start()
        except Exception:
            pass

    def _onAvatar(self, raw):
        try:
            pm = QPixmap()
            if not pm.loadFromData(raw):
                return
            circ = self._circleClip(pm, 46)
            c = self._c("topNavContainer")
            self._paintAvatar(c.avatar, self._palette(), circ)
            self._placeBadge(c.avatar, self._palette())
        except Exception:
            pass
        finally:
            try:
                self._avThread.quit(); self._avThread.wait(800)
            except Exception:
                pass

    def _circleClip(self, pm, size):
        from qtpy.QtGui import QPainterPath
        s = size * 2
        out = QPixmap(s, s); out.fill(QColor(0, 0, 0, 0))
        p = QPainter(out)
        p.setRenderHint(QPainter.Antialiasing, True)
        path = QPainterPath(); path.addEllipse(0, 0, s, s)
        p.setClipPath(path)
        scaled = pm.scaled(s, s, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        p.drawPixmap(0, 0, scaled)
        p.end()
        out.setDevicePixelRatio(2.0)
        return out

    # -- theme ------------------------------------------------------------ #
    def _toggleTheme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_LIGHT if T.is_dark(self._theme_name()) else T.THEME_DARK
        self.themeEngine.setTheme(target)


def _qsize(n):
    from qtpy.QtCore import QSize
    return QSize(n, n)
