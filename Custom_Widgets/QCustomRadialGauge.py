########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomRadialGauge - a modern painted gauge (the gauge FAMILY in one widget).
##
## Two looks, switched with `gaugeStyle`:
##   gaugeStyle="needle" (default) - a thick coloured value arc over a muted
##       track + a drawn needle pointer, big centre value, min/max scale labels
##       at the arc ends and an optional coloured status badge below. Covers the
##       speedometer / threshold / "Threat Level" semicircle gauges. Colour the
##       value arc by ZONES (green/amber/red) so the arc + badge track the band
##       the value falls in, or by a two-stop gradient.
##   gaugeStyle="tick"   - a sweep of tick marks: the passed ticks use a
##       gradient (e.g. pink->purple), the rest a muted track. Covers the
##       radial-tick timer ("17 Sec"). Drive it as a countdown with start()/stop().
##
## Painted directly with QPainter so it stays crisp at ANY size and recolours on
## a theme switch (all colours are qproperties). Give it a value in code via
## setValue(...) / setRange(...) or the Designer properties; feed zones via
## setZones([...]) or the `zonesCsv` property ("lo:hi:#hex, ...").
##
## Angles use the Qt convention (degrees, 0 at 3 o'clock, positive = CCW), so a
## downward-opening semicircle is startAngle=180, spanAngle=-180 and a 270-deg
## timer with a gap at the bottom is startAngle=225, spanAngle=-270.
########################################################################
import math

from qtpy.QtCore import (Qt, Property, Signal, QRectF, QPointF, QTimer,
                         QVariantAnimation, QEasingCurve)
from qtpy.QtGui import (QColor, QPainter, QPen, QBrush, QFont, QPainterPath,
                        QLinearGradient, QPixmap)
from qtpy.QtWidgets import QWidget, QSizePolicy


class QCustomRadialGauge(QWidget):

    valueChanged = Signal(float)
    finished = Signal()          # countdown reached the minimum

    WIDGET_ICON = "components/icons/gauge.png"
    WIDGET_TOOLTIP = "A painted gauge (needle / tick / threshold / countdown)"
    WIDGET_MODULE = "Custom_Widgets.QCustomRadialGauge"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomRadialGauge' name='customRadialGauge'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>240</width><height>200</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomRadialGauge",
        "props": {
            "value": {"type": "float", "default": 55.0},
            "minimum": {"type": "float", "default": 0.0},
            "maximum": {"type": "float", "default": 100.0},
            "gaugeStyle": {"type": "enum", "values": ["needle", "tick"], "default": "needle"},
            "startAngle": {"type": "float", "default": 180.0},
            "spanAngle": {"type": "float", "default": -180.0},
            "tickCount": {"type": "int", "default": 44},
            "arcWidth": {"type": "int", "default": 16},
            "zonesCsv": {"type": "string", "default": "0:33:#33d17a,33:66:#f4c44e,66:100:#f2704e"},
            "gradientStart": {"type": "color", "default": "#7c5cff"},
            "gradientEnd": {"type": "color", "default": "#ff5c8a"},
            "trackColor": {"type": "color", "default": "#2a2e3a"},
            "needleColor": {"type": "color", "default": "#454b59"},
            "centerText": {"type": "string", "default": ""},
            "centerSuffix": {"type": "string", "default": "%"},
            "statusText": {"type": "string", "default": "Medium"},
            "statusColor": {"type": "color", "default": ""},
            "centerTextColor": {"type": "color", "default": "#f4f6fb"},
            "scaleColor": {"type": "color", "default": "#6b7280"},
            "showNeedle": {"type": "bool", "default": True},
            "showTicks": {"type": "bool", "default": False},
            "showHandle": {"type": "bool", "default": False},
            "handleColor": {"type": "color", "default": "#ffffff"},
            "centerIcon": {"type": "string", "default": ""},
            "iconColor": {"type": "color", "default": ""},
            "innerColor": {"type": "color", "default": ""},
            "showScaleLabels": {"type": "bool", "default": True},
            "showGuide": {"type": "bool", "default": True},
            "scaleLabelEvery": {"type": "float", "default": 0.0},
            "scaleLabelRadius": {"type": "float", "default": 0.0},
            "emphasizeActiveTick": {"type": "bool", "default": True},
            "activeTickExtend": {"type": "enum", "values": ["inward", "outward", "both"], "default": "inward"},
            "roundedCaps": {"type": "bool", "default": True},
            "animated": {"type": "bool", "default": False},
            "animationDuration": {"type": "int", "default": 600},
            "glow": {"type": "bool", "default": False},
            "glowStrength": {"type": "float", "default": 0.6},
            "glowRadius": {"type": "int", "default": 0},
        },
        "signals": ["valueChanged", "finished"],
        "tokens_used": ["accent", "up", "down"],
    }

    def __init__(self, parent=None, value=55.0, minimum=0.0, maximum=100.0,
                 gaugeStyle="needle"):
        super().__init__(parent)
        self.setObjectName("QCustomRadialGauge")
        self._min = float(minimum)
        self._max = float(maximum)
        self._value = float(value)
        self._style = "tick" if str(gaugeStyle) == "tick" else "needle"
        self._start = 180.0            # arc start angle (Qt convention)
        self._span = -180.0            # sweep; negative == clockwise
        self._tick_count = 44
        self._arc_w = 16
        # value-arc colouring: ZONES take priority, else a two-stop gradient
        self._zones = self._parse_zones("0:33:#33d17a,33:66:#f4c44e,66:100:#f2704e")
        self._grad_start = QColor("#7c5cff")
        self._grad_end = QColor("#ff5c8a")
        self._track = QColor("#2a2e3a")
        self._needle = QColor("#454b59")
        self._show_guide = True        # dashed inner guide arc (needle style)
        self._center_text = ""         # empty -> formatted value
        self._center_suffix = "%"
        self._status_text = "Medium"
        self._status_color = QColor()  # invalid -> derive from active zone
        self._center_color = QColor("#f4f6fb")
        self._scale_color = QColor("#6b7280")
        self._show_needle = True
        # ring-gauge extras (opt-in): an outer tick scale around the arc, an
        # end-cap handle knob at the value-arc tip, a centred icon above the
        # value, and a filled inner disc.
        self._show_ticks = False
        self._show_handle = False
        self._handle_color = QColor("#ffffff")
        self._center_icon = ""
        self._icon_color = QColor()    # invalid -> falls back to centerTextColor
        self._inner_color = QColor()   # invalid -> no inner disc
        self._pix_cache = {}
        self._show_scale = True        # min/max end labels (needle style)
        self._scale_every = 0.0        # >0 -> numeric scale labels every N units
        self._emphasize_tick = True    # draw the leading active tick longer/brighter
        self._active_extend = "inward"  # leading tick grows inward|outward|both
        self._scale_label_radius = 0.0  # 0 -> auto (by style)
        self._rounded_caps = True      # rounded arc/tick ends (arc "border radius")
        self._animated = False         # animate value transitions
        self._anim_ms = 600
        self._glow = False             # soft painted glow behind the arc / ticks
        self._glow_strength = 0.6      # 0..1
        self._glow_radius = 0          # px spread; 0 -> auto (by radius)
        self._disp_value = self._value  # the value the paint actually shows
        self._anim = None              # lazy QVariantAnimation
        self._timer = None             # lazy QTimer for countdown
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(120, 96)

    # ------------------------------------------------------------------ #
    ## Data API
    # ------------------------------------------------------------------ #
    def setValue(self, value):
        v = max(self._min, min(self._max, float(value)))
        if v == self._value:
            return
        self._value = v
        self.valueChanged.emit(v)
        if self._animated:
            self._animate_to(v)
        else:
            self._disp_value = v
            self.update()

    def stepBy(self, delta):
        """Nudge the value by ``delta`` (clamped to the range). With centerText
        unset the centre readout tracks the value automatically — a ± button
        pair is just clicked.connect(lambda: gauge.stepBy(±singleStep))."""
        self.setValue(self._value + float(delta))

    def stepUp(self):
        self.stepBy(getattr(self, "_single_step", 1.0))

    def stepDown(self):
        self.stepBy(-getattr(self, "_single_step", 1.0))

    @Property(float)
    def singleStep(self):
        return getattr(self, "_single_step", 1.0)

    @singleStep.setter
    def singleStep(self, v):
        self._single_step = float(v)

    def _animate_to(self, target):
        if self._anim is None:
            self._anim = QVariantAnimation(self)
            self._anim.setEasingCurve(QEasingCurve.OutCubic)
            self._anim.valueChanged.connect(self._on_anim)
        self._anim.stop()
        self._anim.setDuration(max(0, int(self._anim_ms)))
        self._anim.setStartValue(float(self._disp_value))
        self._anim.setEndValue(float(target))
        self._anim.start()

    def _on_anim(self, v):
        self._disp_value = float(v)
        self.update()

    def setRange(self, minimum, maximum):
        self._min = float(minimum)
        self._max = float(maximum)
        self._value = max(self._min, min(self._max, self._value))
        self._disp_value = max(self._min, min(self._max, self._disp_value))
        self.update()

    def setStyle(self, gaugeStyle):
        """Switch between the 'needle' and 'tick' looks."""
        self._style = "tick" if str(gaugeStyle) == "tick" else "needle"
        self.update()

    def setZones(self, zones):
        """zones: iterable of (lo, hi, colour) in value units (colours the arc)."""
        out = []
        for z in (zones or []):
            try:
                lo, hi, col = z
                out.append((float(lo), float(hi), QColor(col)))
            except Exception:
                pass
        self._zones = out
        self.update()

    def setGradient(self, start, end):
        self._grad_start = QColor(start)
        self._grad_end = QColor(end)
        self.update()

    def setStatusText(self, text):
        self._status_text = str(text)
        self.update()

    def setCenterText(self, text):
        self._center_text = str(text)
        self.update()

    # ---- countdown driver -------------------------------------------- #
    def start(self, seconds=None, interval_ms=1000, step=1.0):
        """Count the value down to the minimum, emitting finished() at the end."""
        if seconds is not None:
            self.setRange(0.0, float(seconds))
            self.setValue(float(seconds))
        self._cd_step = float(step)
        if self._timer is None:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._tick_down)
        self._timer.start(int(interval_ms))

    def stop(self):
        if self._timer is not None:
            self._timer.stop()

    def _tick_down(self):
        self.setValue(self._value - getattr(self, "_cd_step", 1.0))
        if self._value <= self._min:
            self.stop()
            self.finished.emit()

    # ------------------------------------------------------------------ #
    ## Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _parse_zones(text):
        out = []
        for tok in str(text).replace(";", ",").split(","):
            tok = tok.strip()
            if not tok:
                continue
            parts = tok.split(":")
            if len(parts) >= 3:
                try:
                    out.append((float(parts[0]), float(parts[1]),
                                QColor(":".join(parts[2:]).strip())))
                except Exception:
                    pass
        return out

    def _fraction(self):
        span = (self._max - self._min) or 1.0
        return max(0.0, min(1.0, (self._disp_value - self._min) / span))

    def _active_zone_color(self):
        for lo, hi, col in self._zones:
            if lo <= self._disp_value < hi:
                return QColor(col)
        if self._zones:
            return QColor(self._zones[-1][2])   # clamp to the top band
        return None

    @staticmethod
    def _lerp(c0, c1, t):
        t = max(0.0, min(1.0, t))
        return QColor(
            int(c0.red() + (c1.red() - c0.red()) * t),
            int(c0.green() + (c1.green() - c0.green()) * t),
            int(c0.blue() + (c1.blue() - c0.blue()) * t),
        )

    def _fill_colors(self):
        """(startColour, endColour) for the filled portion of the arc/ticks."""
        z = self._active_zone_color()
        if z is not None:
            return z.darker(135), z          # subtle dark->bright within the band
        return QColor(self._grad_start), QColor(self._grad_end)

    def _point(self, cx, cy, r, ang_deg):
        a = math.radians(ang_deg)
        return QPointF(cx + r * math.cos(a), cy - r * math.sin(a))

    def _labels_outside(self):
        """Needle gauges render their scale numbers OUTSIDE the arc (so the
        needle, which sweeps the interior, can never cross a number)."""
        return (self._style != "tick"
                and (self._show_scale or self._scale_every > 0))

    def _geometry(self):
        """Flex layout: size the radius so the WHOLE stack — outside label ring,
        arc, and the below-hub content (value + optional status badge) — fits the
        widget box, then place the hub. Nothing is a fixed fraction of the widget,
        so the badge/value never overflow when the card grows or shrinks."""
        w, h = self.width(), self.height()
        pad = 6.0
        full = abs(self._span) >= 320.0
        # outer ring the numbers/ticks need beyond the arc radius (× r)
        if self._labels_outside():
            top_ext = self._outside_ring()
        elif self._style == "tick":
            top_ext = 1.07                      # outward ticks / round caps
        else:
            top_ext = 1.02
        cx = w / 2.0
        # In ring / disc mode (an inner disc is drawn) the value sits INSIDE the
        # disc, not below the hub — so centre the circle and fill min(w,h) like a
        # full gauge (otherwise the below-hub reservation clips the disc bottom
        # and shrinks the gauge). Leave a little room for the handle knob that
        # pokes just outside the arc radius.
        disc_mode = self._inner_color.isValid()
        if full or disc_mode:
            ext = top_ext
            if disc_mode:
                ext = max(top_ext, 1.20 if self._show_ticks else 1.08)
            r = (min(w, h) / 2.0 - pad) / ext
            cy = h / 2.0
        else:
            # room reserved BELOW the hub for the value (+ badge), in units of r
            below = 0.66 + (0.42 if self._status_text else 0.10)
            r_w = (w / 2.0 - pad) / top_ext
            r_h = (h - 2 * pad) / (top_ext + below)
            r = min(r_w, r_h)
            cy = pad + top_ext * r              # leaves the top label ring room
        r = max(r, 8.0)
        return cx, cy, r

    def _outside_ring(self):
        """Radius factor (× r) where outside scale numbers sit."""
        if self._scale_label_radius > 0:
            return self._scale_label_radius
        return 1.15

    # ------------------------------------------------------------------ #
    ## Painting
    # ------------------------------------------------------------------ #
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        cx, cy, r = self._geometry()
        thickness = max(3.0, min(float(self._arc_w), r * 0.22))
        f = self._fraction()

        if self._style == "tick":
            # dashed inner scale ring sits inside the ticks
            if self._show_guide:
                self._paint_guide(p, cx, cy, r * 0.70)
            self._paint_ticks(p, cx, cy, r, f)
        else:
            if self._show_ticks:
                self._paint_outer_ticks(p, cx, cy, r, thickness, f)
            self._paint_arc(p, cx, cy, r, thickness, f)
            if self._show_guide:
                self._paint_guide(p, cx, cy, r - thickness - max(4.0, r * 0.07))
            if self._show_needle:
                self._paint_needle(p, cx, cy, r, f)

        # filled inner disc (drawn over the arc, under the centre readout)
        if self._inner_color.isValid():
            self._paint_inner_disc(p, cx, cy, r, thickness)

        if self._scale_every > 0:
            self._paint_value_scale(p, cx, cy, r)   # full numeric scale supersedes
        elif self._show_scale and self._style != "tick":
            self._paint_scale_labels(p, cx, cy, r)  # simple min/max end labels
        self._paint_center(p, cx, cy, r)

        # end-cap handle knob at the value-arc tip (drawn last, on top)
        if self._style != "tick" and self._show_handle and f > 0:
            self._paint_handle(p, cx, cy, r, thickness, f)
        p.end()

    def _paint_outer_ticks(self, p, cx, cy, r, thickness, f):
        """A ring of short radial ticks JUST OUTSIDE the arc — the outer scale.
        Ticks under the filled fraction take the gradient colour; the rest are a
        faint scale colour."""
        n = max(8, int(self._tick_count))
        r_in = r + thickness * 0.5 + max(2.0, r * 0.04)
        r_out = r_in + max(3.0, r * 0.07)
        full = abs(self._span) >= 359.9
        denom = n if full else (n - 1)
        c0, c1 = self._fill_colors()
        faint = QColor(self._scale_color)
        for i in range(n):
            tf = i / denom
            ang = self._start + self._span * tf
            if tf <= f + 1e-9 and f > 0:
                col = self._lerp(c0, c1, tf / f)
            else:
                col = QColor(faint); col.setAlpha(130)
            pen = QPen(col, max(1.6, r * 0.016))
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            p.drawLine(self._point(cx, cy, r_in, ang), self._point(cx, cy, r_out, ang))

    def _paint_inner_disc(self, p, cx, cy, r, thickness):
        r_in = r - thickness - max(4.0, r * 0.06)
        if r_in <= 2:
            return
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._inner_color))
        p.drawEllipse(QPointF(cx, cy), r_in, r_in)

    def _paint_handle(self, p, cx, cy, r, thickness, f):
        ang = self._start + self._span * f
        pt = self._point(cx, cy, r, ang)          # on the arc centreline
        kr = max(5.0, thickness * 0.72)
        _c0, c1 = self._fill_colors()
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._handle_color))
        p.drawEllipse(pt, kr, kr)
        p.setBrush(QBrush(c1))
        p.drawEllipse(pt, kr * 0.42, kr * 0.42)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(0, 0, 0, 28), 1))
        p.drawEllipse(pt, kr, kr)

    def _center_icon_pixmap(self, size):
        path = str(self._center_icon)
        col = self._icon_color if self._icon_color.isValid() else self._center_color
        key = (path, int(size), col.name())
        if key in self._pix_cache:
            return self._pix_cache[key]
        import os
        pm = QPixmap(int(size * 2), int(size * 2))
        pm.fill(QColor(0, 0, 0, 0))
        if os.path.exists(path):
            if path.lower().endswith(".svg"):
                from qtpy.QtSvg import QSvgRenderer
                from qtpy.QtCore import QByteArray
                svg = open(path, "r", encoding="utf-8").read()
                for old in ('stroke="#ffffff"', 'stroke="#000000"', 'stroke="currentColor"'):
                    svg = svg.replace(old, 'stroke="%s"' % col.name())
                svg = svg.replace('fill="currentColor"', 'fill="%s"' % col.name())
                rnd = QSvgRenderer(QByteArray(svg.encode("utf-8")))
                pr = QPainter(pm)
                pr.setRenderHint(QPainter.Antialiasing, True)
                rnd.render(pr)
                pr.end()
            else:
                src = QPixmap(path)
                if not src.isNull():
                    pm = src.scaled(int(size * 2), int(size * 2), Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        pm.setDevicePixelRatio(2.0)
        self._pix_cache[key] = pm
        return pm

    def _arc_rect(self, cx, cy, r):
        return QRectF(cx - r, cy - r, 2 * r, 2 * r)

    def _glow_specs(self, base_w, spread):
        """(width, alpha) passes for a soft painted glow — wide+faint down to
        narrow+brighter, an inexpensive bloom that reads like a blurred halo and
        (unlike QGraphicsDropShadowEffect) recolours with the theme."""
        passes = 5
        for k in range(passes, 0, -1):
            t = k / passes
            yield base_w + spread * 2.0 * t, self._glow_strength * 0.14 * (1.15 - t)

    def _paint_arc(self, p, cx, cy, r, thickness, f):
        rect = self._arc_rect(cx, cy, r)
        cap = Qt.RoundCap if self._rounded_caps else Qt.FlatCap
        # muted full-span track
        track = QPen(self._track, thickness)
        track.setCapStyle(cap)
        p.setPen(track)
        p.drawArc(rect, int(self._start * 16), int(self._span * 16))
        if f <= 0:
            return
        # filled value arc, drawn as small segments so the gradient follows the
        # sweep regardless of the span's sign.
        c0, c1 = self._fill_colors()
        filled_span = self._span * f
        # soft glow halo behind the filled arc, in the active colour
        if self._glow:
            spread = float(self._glow_radius) if self._glow_radius > 0 else max(6.0, r * 0.16)
            for gw, ga in self._glow_specs(thickness, spread):
                col = QColor(c1)
                col.setAlphaF(max(0.0, min(1.0, ga)))
                gp = QPen(col, gw)
                gp.setCapStyle(Qt.RoundCap)
                p.setPen(gp)
                p.drawArc(rect, int(self._start * 16), int(filled_span * 16))
        steps = max(2, int(abs(filled_span)))
        for i in range(steps):
            t0, t1 = i / steps, (i + 1) / steps
            a0 = self._start + filled_span * t0
            a1 = self._start + filled_span * t1
            pen = QPen(self._lerp(c0, c1, (t0 + t1) / 2.0), thickness)
            # round the outer ends only; flat internal joins avoid seams
            pen.setCapStyle(cap if (i == 0 or i == steps - 1) else Qt.FlatCap)
            p.setPen(pen)
            p.drawArc(rect, int(a0 * 16), int((a1 - a0) * 16))

    def _paint_ticks(self, p, cx, cy, r, f):
        n = max(2, int(self._tick_count))
        c0, c1 = self._fill_colors()
        tick_w = max(2.0, r * 0.03)
        # on a full circle the first and last tick coincide, so space over [0,1)
        full = abs(self._span) >= 359.9
        denom = n if full else (n - 1)
        last_passed = int(f * denom + 1e-9) if f > 0 else -1
        for i in range(n):
            tf = i / denom                         # 0..1 along the span
            ang = self._start + self._span * tf
            passed = tf <= f + 1e-9
            lead = self._emphasize_tick and i == last_passed and f > 0
            r_out = r
            if passed:
                col = self._lerp(c0, c1, (tf / f) if f > 0 else 0.0)
                r_in = r * 0.74
            else:
                col = QColor(self._track)
                r_in = r * 0.80
            if lead:
                col = col.lighter(135)             # brighter + longer leading tick
                w = tick_w * 1.5
                if self._active_extend in ("inward", "both"):
                    r_in = r * 0.64
                if self._active_extend in ("outward", "both"):
                    r_out = r * 1.05
            else:
                w = tick_w
            pt_in = self._point(cx, cy, r_in, ang)
            pt_out = self._point(cx, cy, r_out, ang)
            # soft glow behind each lit tick (blurred-halo look, theme-aware)
            if self._glow and passed:
                tspread = float(self._glow_radius) * 0.4 if self._glow_radius > 0 else max(3.0, w * 2.2)
                for gw, ga in self._glow_specs(w, tspread):
                    gcol = QColor(col)
                    gcol.setAlphaF(max(0.0, min(1.0, ga)))
                    gp = QPen(gcol, gw)
                    gp.setCapStyle(Qt.RoundCap)
                    p.setPen(gp)
                    p.drawLine(pt_in, pt_out)
            pen = QPen(col, w)
            pen.setCapStyle(Qt.RoundCap if self._rounded_caps else Qt.FlatCap)
            p.setPen(pen)
            p.drawLine(pt_in, pt_out)

    def _paint_guide(self, p, cx, cy, r_guide):
        """A faint dashed scale arc (inside the band / inside the ticks)."""
        if r_guide <= 2:
            return
        col = QColor(self._scale_color)
        col.setAlpha(150)
        pen = QPen(col, max(1.0, r_guide * 0.016))
        pen.setStyle(Qt.DashLine)
        pen.setDashPattern([1.6, 3.2])
        pen.setCapStyle(Qt.FlatCap)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawArc(self._arc_rect(cx, cy, r_guide),
                  int(self._start * 16), int(self._span * 16))

    def _paint_value_scale(self, p, cx, cy, r):
        """Numeric scale labels every `scaleLabelEvery` units along the arc."""
        step = self._scale_every
        span_units = (self._max - self._min) or 1.0
        f = QFont(self.font())
        f.setPointSizeF(max(6.5, r * 0.075))
        p.setFont(f)
        p.setPen(QPen(self._scale_color))
        fm = p.fontMetrics()
        # tick style has no needle -> labels sit INSIDE the ring; needle style
        # puts them OUTSIDE the arc entirely, so the needle can't cross a number.
        if self._scale_label_radius > 0:
            r_lbl = r * self._scale_label_radius
        elif self._style == "tick":
            r_lbl = r * 0.56
        else:
            r_lbl = r * self._outside_ring()
        v = self._min
        is_full = abs(self._span) >= 359.9    # endpoints coincide on a full circle
        # avoid an endless loop on a bad step
        n = int(span_units / step) + 1 if step > 0 else 0
        for _ in range(max(0, min(n, 200)) + 1):
            frac = (v - self._min) / span_units
            if not (is_full and frac >= 1.0 - 1e-9):   # skip the duplicate end label
                ang = self._start + self._span * frac
                pt = self._point(cx, cy, r_lbl, ang)
                p.drawText(QRectF(pt.x() - 18, pt.y() - fm.height() / 2.0, 36, fm.height()),
                           Qt.AlignCenter, "%g" % v)
            v += step
            if v > self._max + 1e-9:
                break

    def _paint_needle(self, p, cx, cy, r, f):
        ang = self._start + self._span * f
        tip = self._point(cx, cy, r * 0.72, ang)
        # a slim tapered needle; a length gradient (bright base -> dark tip) gives
        # it depth so a dark needle still reads on a dark card.
        base_w = max(3.0, r * 0.05)
        perp = ang + 90.0
        b1 = self._point(cx, cy, base_w, perp)
        b2 = self._point(cx, cy, base_w, perp + 180.0)
        path = QPainterPath()
        path.moveTo(b1)
        path.lineTo(tip)
        path.lineTo(b2)
        path.closeSubpath()
        grad = QLinearGradient(QPointF(cx, cy), tip)
        grad.setColorAt(0.0, self._needle.lighter(165))
        grad.setColorAt(1.0, self._needle)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(grad))
        p.drawPath(path)
        # hub: a ring in the needle colour with a bright pivot dot
        hub = max(4.0, r * 0.08)
        p.setBrush(QBrush(self._needle))
        p.drawEllipse(QPointF(cx, cy), hub, hub)
        p.setBrush(QBrush(self._needle.lighter(190)))
        p.drawEllipse(QPointF(cx, cy), hub * 0.42, hub * 0.42)

    def _paint_scale_labels(self, p, cx, cy, r):
        f = QFont(self.font())
        f.setPointSizeF(max(7.0, r * 0.09))
        p.setFont(f)
        p.setPen(QPen(self._scale_color))
        fm = p.fontMetrics()
        lo, hi = self._fmt_scale(self._min), self._fmt_scale(self._max)
        r_lbl = r * self._outside_ring()            # just outside the arc ends
        pt0 = self._point(cx, cy, r_lbl, self._start)
        pt1 = self._point(cx, cy, r_lbl, self._start + self._span)
        p.drawText(QRectF(pt0.x() - 20, pt0.y() - fm.height() / 2.0, 40, fm.height()),
                   Qt.AlignHCenter | Qt.AlignVCenter, lo)
        p.drawText(QRectF(pt1.x() - 20, pt1.y() - fm.height() / 2.0, 40, fm.height()),
                   Qt.AlignHCenter | Qt.AlignVCenter, hi)

    def _paint_center(self, p, cx, cy, r):
        # optional centred icon in the upper part of the disc (above the value).
        # Rendered as a PIXMAP (drawPixmap) at the real size, not a scaled QIcon.
        if self._center_icon:
            isz = r * 0.50
            ipm = self._center_icon_pixmap(isz)
            if not ipm.isNull():
                pr = ipm.devicePixelRatio() or 1.0
                iw, ih = ipm.width() / pr, ipm.height() / pr
                iy = cy - r * 0.27
                p.drawPixmap(QPointF(cx - iw / 2.0, iy - ih / 2.0), ipm)

        # big value + small suffix, centred just under the arc hub. Animates with
        # the displayed value; rounds so it doesn't jitter mid-transition.
        dv = self._disp_value
        if self._center_text:
            big = self._center_text
        elif (self._max - self._min) >= 10:
            big = "%d" % round(dv)
        else:
            big = "%g" % round(dv, 1)
        bf = QFont(self.font())
        bf.setBold(True)
        bf.setPointSizeF(max(11.0, r * 0.30))
        p.setFont(bf)
        bfm = p.fontMetrics()
        big_w = bfm.horizontalAdvance(big)

        suffix = self._center_suffix or ""
        sf = QFont(self.font())
        sf.setPointSizeF(max(8.0, r * 0.16))
        sfm_w = 0
        if suffix:
            from qtpy.QtGui import QFontMetrics
            sfm = QFontMetrics(sf)
            sfm_w = sfm.horizontalAdvance(suffix) + max(2.0, r * 0.03)

        total = big_w + sfm_w
        x = cx - total / 2.0
        # a full circle centres the text on the hub; an open (semicircle / wide)
        # gauge drops it into the empty area below the hub. When a needle is drawn,
        # push the number far enough down that its cap-top clears the needle hub.
        if abs(self._span) >= 320.0:
            center_y = cy
        else:
            center_y = cy + r * 0.20
            if self._show_needle and self._style != "tick":
                hub = max(4.0, r * 0.08)
                clear = cy + hub + max(3.0, r * 0.05) + bfm.height() / 2.0
                center_y = max(center_y, clear)
        baseline_y = center_y + (bfm.ascent() - bfm.descent()) / 2.0
        p.setFont(bf)
        p.setPen(QPen(self._center_color))
        p.drawText(QPointF(x, baseline_y), big)
        if suffix:
            p.setFont(sf)
            p.setPen(QPen(QColor(self._scale_color)))
            # bottom-align the small suffix to the big number's baseline
            p.drawText(QPointF(x + big_w + max(2.0, r * 0.03), baseline_y), suffix)

        if self._status_text:
            badge_top = baseline_y + bfm.descent() + max(4.0, r * 0.05)
            self._paint_status_badge(p, cx, badge_top, r)

    def _paint_status_badge(self, p, cx, top_y, r):
        col = self._status_color if self._status_color.isValid() else \
            (self._active_zone_color() or QColor(self._grad_end))
        bf = QFont(self.font())
        bf.setBold(True)
        bf.setPointSizeF(max(7.5, r * 0.10))
        p.setFont(bf)
        fm = p.fontMetrics()
        tw = fm.horizontalAdvance(self._status_text)
        pad_x, pad_y = max(8.0, r * 0.08), max(3.0, r * 0.03)
        bw, bh = tw + 2 * pad_x, fm.height() + 2 * pad_y
        rect = QRectF(cx - bw / 2.0, top_y, bw, bh)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(col))
        p.drawRoundedRect(rect, bh / 2.0, bh / 2.0)
        # readable text colour for the pill fill
        lum = 0.299 * col.red() + 0.587 * col.green() + 0.114 * col.blue()
        p.setPen(QPen(QColor("#10131a") if lum > 150 else QColor("#ffffff")))
        p.drawText(rect, Qt.AlignCenter, self._status_text)

    @staticmethod
    def _fmt_scale(v):
        return ("%g" % v)

    # ------------------------------------------------------------------ #
    ## Designer properties
    # ------------------------------------------------------------------ #
    @Property(float)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.setValue(v)

    @Property(float)
    def minimum(self):
        return self._min

    @minimum.setter
    def minimum(self, v):
        self.setRange(float(v), self._max)

    @Property(float)
    def maximum(self):
        return self._max

    @maximum.setter
    def maximum(self, v):
        self.setRange(self._min, float(v))

    @Property(str)
    def gaugeStyle(self):
        return self._style

    @gaugeStyle.setter
    def gaugeStyle(self, v):
        self.setStyle(v)

    @Property(float)
    def startAngle(self):
        return self._start

    @startAngle.setter
    def startAngle(self, v):
        self._start = float(v)
        self.update()

    @Property(float)
    def spanAngle(self):
        return self._span

    @spanAngle.setter
    def spanAngle(self, v):
        self._span = float(v)
        self.update()

    @Property(int)
    def tickCount(self):
        return self._tick_count

    @tickCount.setter
    def tickCount(self, v):
        self._tick_count = max(2, int(v))
        self.update()

    @Property(int)
    def arcWidth(self):
        return self._arc_w

    @arcWidth.setter
    def arcWidth(self, v):
        self._arc_w = max(1, int(v))
        self.update()

    @Property(str)
    def zonesCsv(self):
        return ",".join("%g:%g:%s" % (lo, hi, col.name())
                        for lo, hi, col in self._zones)

    @zonesCsv.setter
    def zonesCsv(self, text):
        self._zones = self._parse_zones(text)
        self.update()

    @Property(QColor)
    def gradientStart(self):
        return self._grad_start

    @gradientStart.setter
    def gradientStart(self, c):
        self._grad_start = QColor(c)
        self.update()

    @Property(QColor)
    def gradientEnd(self):
        return self._grad_end

    @gradientEnd.setter
    def gradientEnd(self, c):
        self._grad_end = QColor(c)
        self.update()

    @Property(QColor)
    def trackColor(self):
        return self._track

    @trackColor.setter
    def trackColor(self, c):
        self._track = QColor(c)
        self.update()

    @Property(QColor)
    def needleColor(self):
        return self._needle

    @needleColor.setter
    def needleColor(self, c):
        self._needle = QColor(c)
        self.update()

    @Property(str)
    def centerText(self):
        return self._center_text

    @centerText.setter
    def centerText(self, v):
        self.setCenterText(v)

    @Property(str)
    def centerSuffix(self):
        return self._center_suffix

    @centerSuffix.setter
    def centerSuffix(self, v):
        self._center_suffix = str(v)
        self.update()

    @Property(str)
    def statusText(self):
        return self._status_text

    @statusText.setter
    def statusText(self, v):
        self.setStatusText(v)

    @Property(QColor)
    def statusColor(self):
        return self._status_color

    @statusColor.setter
    def statusColor(self, c):
        self._status_color = QColor(c) if c else QColor()
        self.update()

    @Property(QColor)
    def centerTextColor(self):
        return self._center_color

    @centerTextColor.setter
    def centerTextColor(self, c):
        self._center_color = QColor(c)
        self.update()

    @Property(QColor)
    def scaleColor(self):
        return self._scale_color

    @scaleColor.setter
    def scaleColor(self, c):
        self._scale_color = QColor(c)
        self.update()

    @Property(bool)
    def showTicks(self):
        return self._show_ticks

    @showTicks.setter
    def showTicks(self, v):
        self._show_ticks = bool(v)
        self.update()

    @Property(bool)
    def showHandle(self):
        return self._show_handle

    @showHandle.setter
    def showHandle(self, v):
        self._show_handle = bool(v)
        self.update()

    @Property(QColor)
    def handleColor(self):
        return self._handle_color

    @handleColor.setter
    def handleColor(self, c):
        self._handle_color = QColor(c)
        self.update()

    @Property(str)
    def centerIcon(self):
        return self._center_icon

    @centerIcon.setter
    def centerIcon(self, path):
        self._center_icon = str(path)
        self._pix_cache.clear()
        self.update()

    @Property(QColor)
    def iconColor(self):
        return self._icon_color

    @iconColor.setter
    def iconColor(self, c):
        self._icon_color = QColor(c)
        self._pix_cache.clear()
        self.update()

    @Property(QColor)
    def innerColor(self):
        return self._inner_color

    @innerColor.setter
    def innerColor(self, c):
        self._inner_color = QColor(c)
        self.update()

    @Property(bool)
    def showNeedle(self):
        return self._show_needle

    @showNeedle.setter
    def showNeedle(self, v):
        self._show_needle = bool(v)
        self.update()

    @Property(bool)
    def showScaleLabels(self):
        return self._show_scale

    @showScaleLabels.setter
    def showScaleLabels(self, v):
        self._show_scale = bool(v)
        self.update()

    @Property(bool)
    def showGuide(self):
        return self._show_guide

    @showGuide.setter
    def showGuide(self, v):
        self._show_guide = bool(v)
        self.update()

    @Property(float)
    def scaleLabelEvery(self):
        return self._scale_every

    @scaleLabelEvery.setter
    def scaleLabelEvery(self, v):
        self._scale_every = max(0.0, float(v))
        self.update()

    @Property(bool)
    def emphasizeActiveTick(self):
        return self._emphasize_tick

    @emphasizeActiveTick.setter
    def emphasizeActiveTick(self, v):
        self._emphasize_tick = bool(v)
        self.update()

    @Property(str)
    def activeTickExtend(self):
        return self._active_extend

    @activeTickExtend.setter
    def activeTickExtend(self, v):
        v = str(v)
        self._active_extend = v if v in ("inward", "outward", "both") else "inward"
        self.update()

    @Property(float)
    def scaleLabelRadius(self):
        return self._scale_label_radius

    @scaleLabelRadius.setter
    def scaleLabelRadius(self, v):
        self._scale_label_radius = max(0.0, float(v))
        self.update()

    @Property(bool)
    def roundedCaps(self):
        return self._rounded_caps

    @roundedCaps.setter
    def roundedCaps(self, v):
        self._rounded_caps = bool(v)
        self.update()

    @Property(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        self._animated = bool(v)

    @Property(int)
    def animationDuration(self):
        return self._anim_ms

    @animationDuration.setter
    def animationDuration(self, v):
        self._anim_ms = max(0, int(v))

    @Property(bool)
    def glow(self):
        return self._glow

    @glow.setter
    def glow(self, v):
        self._glow = bool(v)
        self.update()

    @Property(float)
    def glowStrength(self):
        return self._glow_strength

    @glowStrength.setter
    def glowStrength(self, v):
        self._glow_strength = max(0.0, min(1.0, float(v)))
        self.update()

    @Property(int)
    def glowRadius(self):
        return self._glow_radius

    @glowRadius.setter
    def glowRadius(self, v):
        self._glow_radius = max(0, int(v))
        self.update()
