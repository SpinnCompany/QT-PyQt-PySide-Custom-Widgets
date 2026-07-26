"""Node Studio — GuiFunctions orchestrator.

LOGIC only (the .ui carries structure, chrome.scss carries chrome). This:
  * feeds the QCustomNodeGraph the IDEAS -> SETTINGS -> REFERENCES -> MODELS
    graph, coloured from the token-driven NodePalette (flips on theme switch),
  * feeds the QCustomMediaTimeline the clip + waveform tracks,
  * fills the QCustomCodeEditor "Thoughts" panel,
  * paints a self-contained 3D-preview placeholder,
  * wires the theme toggle + the play button (animates the playhead).
"""

import math

from qtpy.QtCore import Qt, QTimer, QRectF, QPointF, QObject, QEvent
from qtpy.QtGui import (QPixmap, QPainter, QColor, QBrush, QPen, QLinearGradient,
                        QRadialGradient, QPainterPath, QFont)

from . import theme as T

# Button ICONS are NOT set here — they live in Qss/scss/chrome.scss as
# `qproperty-icon: url(theme-icons:...)` so the theme engine recolours + refreshes
# them on every theme flip (the icons-via-QSS rule). This module is logic only.

# exclusive selectable control groups (name list, default-checked)
TABS = ["tabNew", "tabFramer", "tabUntitled"]
LEFT_TOOLS = ["rlText", "rlLayers", "rlPen", "rlBrush", "rlGrid", "rlAttach"]
RIGHT_TOOLS = ["rrCursor", "rrStar", "rrDrop", "rrLock", "rrBulb"]
DURATIONS = [10, 15, 30, 5]

# clicking a SETTINGS row cycles through these; Voice/Mode actually drive the
# 3D preview, so the graph is wired to the render (functional, not cosmetic).
SETTINGS_OPTIONS = {
    "Mode": ["Fun", "Serious", "Playful", "Cinematic"],
    "Trim": ["Auto", "Manual"],
    "Think": ["Fast", "Balanced", "Deep"],
    "Voice": ["Happy", "Calm", "Bright", "Warm"],
    "Music": ["Piano", "Lofi", "Synth", "None"],
}
VOICE_SHIRT = {"Happy": "#4ade80", "Calm": "#38bdf8",
               "Bright": "#f2a63b", "Warm": "#f472b6"}
MODE_GLOW = {"Fun": "#6c7bff", "Serious": "#64748b",
             "Playful": "#f472b6", "Cinematic": "#a855f7"}


class _ResizeRelay(QObject):
    """Repaints the preview whenever its host label is resized."""

    def __init__(self, cb, parent=None):
        super().__init__(parent)
        self._cb = cb

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self._cb()
        return False

THOUGHTS_CODE = '''import { CuteBoy } from "./components/3dcuteboy-animation";

export default function App() {
  return (
    <div className="size-full">
      <CuteBoy />
    </div>
  );
}
'''


class GuiFunctions:
    def __init__(self, win):
        self.win = win
        self.ui = win.ui
        self.themeEngine = getattr(win, "themeEngine", None)

    # ------------------------------------------------------------------ #
    def initialize(self):
        self._dur_idx = 0
        self._playing = False
        self._built = False
        self._shirt_color = None     # set by the Voice setting
        self._glow_color = None      # set by the Mode setting
        self._setup_controls()      # tabs + rails live in the shell (self.ui.*)
        self._resolve_and_build()   # canvas/thoughts/preview/timeline are components
        if self.themeEngine is not None:
            try:
                self.themeEngine.onThemeChangeComplete.connect(self._on_theme_ready)
            except Exception:
                pass

    # ------------------------------------------------------------------ #
    ## Component resolution (containers load their .ui asynchronously)
    # ------------------------------------------------------------------ #
    def _find(self, container, name):
        """Resolve a child widget by objectName inside an embedded component."""
        from qtpy.QtWidgets import QWidget
        comp = getattr(container, "component", None)
        if comp is not None and hasattr(comp, name):
            return getattr(comp, name)
        for w in container.findChildren(QWidget):
            if w.objectName() == name:
                return w
        return None

    def _resolve_and_build(self, tries=0):
        ng = self._find(self.ui.canvasContainer, "nodeGraph")
        ce = self._find(self.ui.thoughtsContainer, "codeEditor")
        pv = self._find(self.ui.previewContainer, "previewImage")
        tl = self._find(self.ui.timelineContainer, "mediaTimeline")
        if None in (ng, ce, pv, tl):
            if tries < 50:                       # containers embed on a later tick
                QTimer.singleShot(60, lambda: self._resolve_and_build(tries + 1))
            return
        self._nodeGraph, self._codeEditor = ng, ce
        self._previewImage, self._timeline = pv, tl
        self._build_graph()
        self._build_timeline()
        self._build_thoughts()
        self._build_preview()
        self._wire()
        self._built = True

    def _theme_name(self):
        return str(getattr(self.themeEngine, "theme", "") or T.THEME_DARK)

    def _pal(self):
        return T.node_palette(self._theme_name())

    # ------------------------------------------------------------------ #
    ## Node graph
    # ------------------------------------------------------------------ #
    def _build_graph(self):
        g = self._nodeGraph
        p = self._pal()
        g.bgColor = p["canvasBg"]
        g.gridColor = p["gridColor"]
        g.nodeColor = p["nodeColor"]
        g.nodeHeaderColor = p["nodeHeaderColor"]
        g.nodeBorderColor = p["nodeBorderColor"]
        g.textColor = p["text"]
        g.mutedColor = p["muted"]
        g.portColor = p["ideas"]
        g.edgeColor = p["cableWarm"]
        g.selectedColor = p["settings"]

        g.setGraph({
            "nodes": [
                {"nid": "ideas", "title": "Ideas", "x": 30, "y": 40,
                 "w": 220, "h": 150, "accent": p["ideas"],
                 "text": "3D stylized cartoon boy character, slightly short "
                         "proportions, full body, big round glasses, spiky "
                         "dark brown hair",
                 "outputs": ["out"]},
                {"nid": "refs", "title": "References", "x": 30, "y": 250,
                 "w": 220, "h": 170, "accent": p["refs"],
                 "image": self._ref_thumb_path(), "outputs": ["out"]},
                {"nid": "settings", "title": "Settings", "x": 360, "y": 70,
                 "w": 250, "h": 230, "accent": p["settings"],
                 "inputs": ["in"], "outputs": ["out"],
                 "rows": [
                     {"label": "Mode", "value": "Fun", "dot": p["ideas"]},
                     {"label": "Trim", "value": "Auto", "dot": p["refs"]},
                     {"label": "Think", "value": "Fast", "dot": p["settings"]},
                     {"label": "Voice", "value": "Happy", "dot": p["voice"]},
                     {"label": "Music", "value": "Piano", "dot": p["music"]},
                 ]},
                {"nid": "models", "title": "AI Models", "x": 680, "y": 150,
                 "w": 210, "h": 120, "accent": p["models"],
                 "inputs": ["in"], "chips": ["Gemini", "Seedance2"]},
            ],
            "edges": [
                {"src": "ideas", "srcPort": 0, "dst": "settings", "dstPort": 0,
                 "color": p["cableWarm"]},
                {"src": "refs", "srcPort": 0, "dst": "settings", "dstPort": 0,
                 "color": p["cableViolet"]},
                {"src": "settings", "srcPort": 0, "dst": "models", "dstPort": 0,
                 "color": p["cableIndigo"]},
            ],
        })
        QTimer.singleShot(0, g.fitToView)

    def _ref_thumb_path(self):
        # the references node reuses the painted preview as its thumbnail
        path = "/tmp/claude-1000/nodestudio_ref.png"
        try:
            self._make_character_pixmap(220, 150).save(path)
            return path
        except Exception:
            return ""

    # ------------------------------------------------------------------ #
    ## Timeline
    # ------------------------------------------------------------------ #
    def _build_timeline(self):
        tl = self._timeline
        p = self._pal()
        tl.bgColor = p["canvasBg"]
        tl.trackBgColor = p["nodeColor"]
        tl.rulerColor = p["muted"]
        tl.playheadColor = p["text"]
        tl.clipColor = p["clip"]
        tl.waveColor = p["wave"]
        wave = [math.sin(i * 0.35) * (0.35 + 0.65 * abs(math.sin(i * 0.09)))
                for i in range(120)]
        tl.setTimeline({
            "duration": 9,
            "position": 1.4,
            "tracks": [
                {"name": "Clip", "kind": "clips",
                 "clips": [{"start": 0.25, "end": 8.6, "color": p["clip"],
                            "label": "3D Character Animation"}]},
                {"name": "Audio", "kind": "wave", "values": wave},
            ],
        })

    # ------------------------------------------------------------------ #
    ## Thoughts code panel
    # ------------------------------------------------------------------ #
    def _build_thoughts(self):
        ed = self._codeEditor
        try:
            ed.setTheme("one-dark" if not T.is_light(self._theme_name()) else "one-light")
            ed.setLang("javascript")
            ed.editor.setPlainText(THOUGHTS_CODE)
            f = QFont("monospace")
            f.setPointSize(10)
            ed.editor.setFont(f)
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    ## Preview
    # ------------------------------------------------------------------ #
    def _build_preview(self):
        self._paint_preview()

    def _paint_preview(self, force=False):
        lbl = self._previewImage
        # The pixmap must NOT drive the label's sizeHint, or setPixmap ->
        # layout grows -> resize -> setPixmap loops forever. Ignored policy +
        # a size guard keep it stable. `force` repaints on a state change
        # (setting tweak / theme flip) even when the size is unchanged.
        w = max(300, lbl.width())
        h = max(360, lbl.height())
        if not force and getattr(self, "_prev_size", None) == (w, h):
            return
        self._prev_size = (w, h)
        lbl.setPixmap(self._make_character_pixmap(w, h))

    def _make_character_pixmap(self, w, h):
        p = self._pal()
        dpr = 2
        pm = QPixmap(w * dpr, h * dpr)
        pm.setDevicePixelRatio(dpr)
        pm.fill(QColor(0, 0, 0, 0))
        pt = QPainter(pm)
        pt.setRenderHint(QPainter.Antialiasing, True)

        # stage background gradient + soft spotlight
        bg = QLinearGradient(0, 0, 0, h)
        light = T.is_light(self._theme_name())
        bg.setColorAt(0.0, QColor("#2a2140" if not light else "#e7e3f6"))
        bg.setColorAt(1.0, QColor("#14121e" if not light else "#f6f4fb"))
        pt.fillRect(QRectF(0, 0, w, h), QBrush(bg))
        glow = QRadialGradient(w / 2, h * 0.42, w * 0.55)
        glow_base = self._glow_color or QColor(p["settings"])   # driven by Mode
        glow.setColorAt(0.0, QColor(glow_base).lighter(140))
        glow.setColorAt(0.35, QColor(0, 0, 0, 0))
        pt.setOpacity(0.30)
        pt.fillRect(QRectF(0, 0, w, h), QBrush(glow))
        pt.setOpacity(1.0)

        # --- character laid out in a CENTERED portrait box so proportions are
        #     stable regardless of the panel's aspect ratio ------------------
        cx = w / 2.0
        u = min(h * 0.80, w * 1.25)          # overall character height (unit)
        top = (h - u) / 2.0
        skin = QColor("#f0c39c")
        hair = QColor("#3a2a22")
        shirt = QColor(self._shirt_color or p["refs"]).lighter(105)   # driven by Voice
        line_w = max(2.0, u * 0.012)

        hr = u * 0.15                        # head radius
        hy = top + u * 0.28                  # head centre y
        body_top = hy + hr * 1.15
        body_h = u * 0.50
        body_w = u * 0.44
        body_bottom = body_top + body_h

        # ground shadow
        pt.setPen(Qt.NoPen)
        pt.setBrush(QColor(0, 0, 0, 60))
        pt.drawEllipse(QPointF(cx, body_bottom + u * 0.02), body_w * 0.62, u * 0.022)

        # neck
        pt.setBrush(skin)
        pt.drawRoundedRect(QRectF(cx - u * 0.055, hy + hr * 0.5, u * 0.11, hr * 1.0),
                           6, 6)

        # body / shirt
        body = QPainterPath()
        body.addRoundedRect(QRectF(cx - body_w / 2, body_top, body_w, body_h),
                            body_w * 0.34, body_w * 0.34)
        pt.setBrush(shirt)
        pt.drawPath(body)
        # bag strap across the torso
        pt.setPen(QPen(QColor(p["ideas"]), max(3.0, u * 0.022)))
        pt.drawLine(QPointF(cx - body_w * 0.34, body_top + body_h * 0.10),
                    QPointF(cx + body_w * 0.30, body_top + body_h * 0.62))
        pt.setPen(Qt.NoPen)

        # head
        pt.setBrush(skin)
        pt.drawEllipse(QPointF(cx, hy), hr, hr * 1.05)

        # hair cap + spikes
        pt.setBrush(hair)
        cap = QPainterPath()
        cap.addEllipse(QPointF(cx, hy - hr * 0.28), hr * 1.02, hr * 0.82)
        pt.drawPath(cap)
        for i in range(-2, 3):
            sx = cx + i * hr * 0.38
            spike = QPainterPath()
            spike.moveTo(sx - hr * 0.17, hy - hr * 0.55)
            spike.lineTo(sx, hy - hr * 1.15)
            spike.lineTo(sx + hr * 0.17, hy - hr * 0.55)
            spike.closeSubpath()
            pt.drawPath(spike)

        # glasses + eyes
        gy = hy + hr * 0.10
        gr = hr * 0.44
        pt.setBrush(QColor(0, 0, 0, 0))
        pt.setPen(QPen(QColor("#2b2b2b"), line_w))
        pt.drawEllipse(QPointF(cx - hr * 0.46, gy), gr, gr)
        pt.drawEllipse(QPointF(cx + hr * 0.46, gy), gr, gr)
        pt.drawLine(QPointF(cx - hr * 0.02, gy), QPointF(cx + hr * 0.02, gy))
        pt.setPen(Qt.NoPen)
        pt.setBrush(QColor("#2b2b2b"))
        pt.drawEllipse(QPointF(cx - hr * 0.46, gy), gr * 0.30, gr * 0.30)
        pt.drawEllipse(QPointF(cx + hr * 0.46, gy), gr * 0.30, gr * 0.30)

        pt.end()
        return pm

    # ------------------------------------------------------------------ #
    ## Interactive controls
    # ------------------------------------------------------------------ #
    def _setup_controls(self):
        """Make the tabs + both tool rails behave as exclusive selectable
        controls, so a click gives an immediate active-state (:checked QSS)."""
        from qtpy.QtWidgets import QButtonGroup
        self._groups = []
        for names, default in ((TABS, "tabNew"),
                               (LEFT_TOOLS, "rlLayers"),
                               (RIGHT_TOOLS, "rrCursor")):
            grp = QButtonGroup(self.win)
            grp.setExclusive(True)
            for n in names:
                btn = getattr(self.ui, n, None)
                if btn is None:
                    continue
                btn.setCheckable(True)
                grp.addButton(btn)
                if n == default:
                    btn.setChecked(True)
            self._groups.append(grp)

    def _wire(self):
        from qtpy.QtWidgets import QSizePolicy
        self.ui.playBtn.setCheckable(True)   # :checked swaps play->pause icon (QSS)
        self.ui.themeToggle.clicked.connect(self._toggle_theme)
        self.ui.playBtn.clicked.connect(self._toggle_play)
        self.ui.durationBtn.clicked.connect(self._cycle_duration)
        self.ui.fabAdd.clicked.connect(self._add_node)
        self.ui.tabAdd.clicked.connect(lambda: self._toast("info", "New project tab"))
        self.ui.exportBtn.clicked.connect(lambda: self._toast("success", "Exporting animation…"))
        self.ui.shareBtn.clicked.connect(lambda: self._toast("info", "Share link copied"))
        self.ui.codeBtn.clicked.connect(lambda: self._toast("info", "View source"))
        self.ui.navPrev.clicked.connect(lambda: self._nudge_playhead(-1))
        self.ui.navNext.clicked.connect(lambda: self._nudge_playhead(1))
        # tapping a SETTINGS row cycles its value and drives the render
        self._nodeGraph.rowClicked.connect(self._on_row_clicked)
        # the preview label must never push the layout (its pixmap is drawn to
        # fit the label, not the other way round)
        lbl = self._previewImage
        lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        lbl.setMinimumSize(0, 0)
        self._relay = _ResizeRelay(self._paint_preview, self.win)
        lbl.installEventFilter(self._relay)
        QTimer.singleShot(0, self._paint_preview)

    def _toast(self, kind, msg):
        try:
            from Custom_Widgets.QCustomToast import QCustomToast
            getattr(QCustomToast, kind, QCustomToast.info)(self.win, msg)
        except Exception:
            pass

    def _toggle_play(self):
        # the timeline animates its OWN playhead now (play/pause); just drive it.
        self._timeline.togglePlay()
        self.ui.playBtn.setChecked(self._timeline.isPlaying())

    def _cycle_duration(self):
        self._dur_idx = (self._dur_idx + 1) % len(DURATIONS)
        d = DURATIONS[self._dur_idx]
        self.ui.durationBtn.setText("%ds" % d)
        self._timeline.setDuration(d)

    def _nudge_playhead(self, direction):
        tl = self._timeline
        tl.setPosition(tl.positionSeconds() + direction)

    def _on_row_clicked(self, node_id, idx):
        """Cycle a SETTINGS row to its next option and apply it to the render."""
        if node_id != "settings":
            return
        rows = self._nodeGraph.nodeRows(node_id)
        if idx >= len(rows):
            return
        label = rows[idx].get("label", "")
        opts = SETTINGS_OPTIONS.get(label)
        if not opts:
            return
        cur = rows[idx].get("value", opts[0])
        nxt = opts[(opts.index(cur) + 1) % len(opts)] if cur in opts else opts[0]
        self._nodeGraph.setRowValue(node_id, idx, nxt)
        if label == "Voice":
            self._shirt_color = QColor(VOICE_SHIRT.get(nxt, "#4ade80"))
            self._paint_preview(force=True)
        elif label == "Mode":
            self._glow_color = QColor(MODE_GLOW.get(nxt, "#6c7bff"))
            self._paint_preview(force=True)
        self._toast("info", "%s: %s" % (label, nxt))

    def _add_node(self):
        p = self._pal()
        k = getattr(self, "_added", 0)
        self._added = k + 1
        # drop into the empty band below the existing nodes, stepping right then
        # wrapping to a new row so fresh nodes never land on top of each other
        col, row = k % 3, k // 3
        self._nodeGraph.addNode(
            title="Layer %d" % (k + 1), x=40 + col * 250, y=470 + row * 110,
            w=200, h=92, accent=p["models"], inputs=["in"], outputs=["out"],
            text="New node — drag me, wire my ports.")
        self._toast("info", "Node added")

    # -- theme ---------------------------------------------------------- #
    def _toggle_theme(self):
        if self.themeEngine is None:
            return
        target = T.THEME_LIGHT if not T.is_light(self._theme_name()) else T.THEME_DARK
        self.themeEngine.setTheme(target)

    def _on_theme_ready(self):
        # icons recolour automatically (QSS theme-icons); only the PAINTED
        # widgets (node graph / timeline / preview) need re-tinting from the
        # new theme's NodePalette.
        self._build_graph()
        self._build_timeline()
        self._build_thoughts()
        self._paint_preview()
