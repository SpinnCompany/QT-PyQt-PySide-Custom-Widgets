########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## QCustomEmojiPicker - a modern emoji picker popover.
##
## A QCustomTipOverlay that shows a searchable, category-navigable grid of
## emojis. On top of the original picker it adds:
##   * a themed CATEGORY quick-nav bar (real SVG icons, scroll-to-group),
##   * a persisted "Recently used" section (QSettings),
##   * an `emojiSelected(str)` signal + optional close-on-select,
##   * clean, palette-driven styling (no per-button inline hacks / % radius),
##   * ONLINE UPDATING: when the bundled set is outdated it can fetch the
##     latest emoji dataset (GitHub gemoji) off the GUI thread, cache it to a
##     writable location, and rebuild the grid live — falling back to the
##     bundled JSON when offline.
##
## Back-compatible: existing callers
##   QCustomEmojiPicker(target=w, parent=p, itemsPerRow=16).show()
## keep working; the emoji is still inserted into a QLineEdit/QTextEdit target.
########################################################################
import typing
import os
import json
import datetime

from qtpy import QtCore, QtWidgets
from qtpy.QtCore import (Qt, Signal, QObject, QThread, QTimer, QSize, QRectF,
                         QByteArray, QStandardPaths, QSettings)
from qtpy.QtGui import QIcon, QPixmap, QPainter, QColor
from qtpy.QtSvg import QSvgRenderer

from Custom_Widgets.components.python.ui_emojiPicker import Ui_Form
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay

_PKG = os.path.dirname(os.path.realpath(__file__))
_BUNDLED_JSON = os.path.join(_PKG, "components", "json", "emojis.json")
_MD_ICONS = os.path.join(_PKG, "Qss", "icons", "material_design")
_FEATHER = os.path.join(_PKG, "Qss", "icons", "feather")

# Canonical group order + the SVG icon each gets in the quick-nav bar.
_GROUP_ORDER = ["Smileys & People", "Animals & Nature", "Food & Drink",
                "Activity", "Travel & Places", "Objects", "Symbols", "Flags"]
# Clean feather LINE icons for the category quick-nav (crisp at small sizes,
# consistent with modern pickers — not heavy filled glyphs).
_GROUP_ICON = {
    "Recent":            (_FEATHER, "clock.svg"),
    "Smileys & People":  (_FEATHER, "smile.svg"),
    "Animals & Nature":  (_FEATHER, "feather.svg"),
    "Food & Drink":      (_FEATHER, "coffee.svg"),
    "Activity":          (_FEATHER, "award.svg"),
    "Travel & Places":   (_FEATHER, "map-pin.svg"),
    "Objects":           (_FEATHER, "briefcase.svg"),
    "Symbols":           (_FEATHER, "heart.svg"),
    "Flags":             (_FEATHER, "flag.svg"),
}
# GitHub gemoji category -> our group name.
_GEMOJI_MAP = {
    "Smileys & Emotion": "Smileys & People",
    "People & Body":     "Smileys & People",
    "Animals & Nature":  "Animals & Nature",
    "Food & Drink":      "Food & Drink",
    "Activities":        "Activity",
    "Travel & Places":   "Travel & Places",
    "Objects":           "Objects",
    "Symbols":           "Symbols",
    "Flags":             "Flags",
}


def _recolor_svg_icon(path, color, size=20, stroke=2.2):
    """Load an SVG (feather `stroke=` or material `fill=`) recoloured to `color`.
    Feather icons default to a thick stroke-width of 3; `stroke` thins them so
    they read as clean, refined line icons at small sizes."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            svg = fh.read()
    except OSError:
        return QIcon()
    svg = (svg.replace('fill="#ffffff"', 'fill="%s"' % color)
              .replace('stroke="#ffffff"', 'stroke="%s"' % color)
              .replace('stroke-width="3"', 'stroke-width="%s"' % stroke))
    dim = size * 2
    pm = QPixmap(dim, dim)
    pm.fill(QColor(0, 0, 0, 0))
    r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    # Render into an explicit rect so the SVG (intrinsic size 100x100) SCALES to
    # fill the pixmap instead of being drawn at native size and clipped.
    r.render(p, QRectF(0, 0, dim, dim))
    p.end()
    pm.setDevicePixelRatio(2.0)
    return QIcon(pm)


def _parse_gemoji(data):
    """A gemoji list -> {group: {emoji: Name}} in canonical order."""
    groups = {g: {} for g in _GROUP_ORDER}
    for item in data:
        emoji = item.get("emoji")
        if not emoji:
            continue
        group = _GEMOJI_MAP.get(item.get("category", ""))
        if not group:
            continue
        desc = (item.get("description") or "").strip()
        groups[group][emoji] = desc.title() if desc else emoji
    return {g: v for g, v in groups.items() if v}


class _EmojiUpdateWorker(QObject):
    """Downloads + parses an online emoji dataset off the GUI thread."""
    finished = Signal(dict)     # {group: {emoji: name}}
    failed = Signal(str)

    def __init__(self, url, timeout=15):
        super().__init__()
        self._url = url
        self._timeout = timeout

    def run(self):
        try:
            import urllib.request
            req = urllib.request.Request(self._url, headers={"User-Agent": "QCustomEmojiPicker"})
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                raw = resp.read().decode("utf-8")
            groups = _parse_gemoji(json.loads(raw))
            if not groups:
                self.failed.emit("no emojis parsed from the online source")
                return
            self.finished.emit(groups)
        except Exception as e:                      # offline / parse / HTTP
            self.failed.emit(str(e))


class _EmojiButton(QtWidgets.QPushButton):
    """One emoji cell — updates the hover preview and reports picks."""

    def __init__(self, emoji, name, picker):
        super().__init__(emoji)
        self._emoji = emoji
        self._name = name
        self._picker = picker
        self.setObjectName("emojiPickerBtn")
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(34, 34)
        self.setToolTip(name)
        self.clicked.connect(lambda: self._picker._on_pick(self._emoji, self._name))

    def enterEvent(self, e):
        self._picker._set_preview(self._emoji, self._name)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._picker._set_preview("", "")
        super().leaveEvent(e)


class QCustomEmojiPicker(QCustomTipOverlay):
    """A modern, updatable emoji picker."""

    emojiSelected = Signal(str)
    emojisUpdated = Signal(int)
    updateFailed = Signal(str)

    GEMOJI_URL = "https://raw.githubusercontent.com/github/gemoji/master/db/emoji.json"

    def __init__(self, parent=None, target=None, tailPosition="top-center",
                 itemsPerRow=8, performanceSearch=True, howForm=None,
                 closeOnSelect=False, autoUpdate=False, updateMaxAgeDays=30,
                 onlineUrl=None, recentLimit=24):
        super().__init__(parent=parent, target=target, title='QCustom Emoji Picker',
                         description='', isClosable=True, tailPosition=tailPosition,
                         showForm=Ui_Form(), duration=-1)

        self.items_per_row = itemsPerRow
        self.performance_search = performanceSearch
        self.close_on_select = closeOnSelect
        self._online_url = onlineUrl or self.GEMOJI_URL
        self._update_max_age = updateMaxAgeDays
        self._recent_limit = recentLimit

        self.selected_emoji = None
        self.total_emojis = {}
        self._group_boxes = {}
        self._nav_buttons = {}
        self._recent_box = None
        self._status_timer = None
        self._thread = None
        self._worker = None
        self._settings = QSettings("Custom Widgets", "QCustomEmojiPicker")

        self._accent = self.palette().highlight().color().name()
        # A neutral mid-grey for idle category icons that reads on both a light
        # and a dark picker surface; the active category switches to the accent.
        self._icon_color = "#9aa1b3"
        self._nav_paths = {}        # group -> absolute svg path (for recolouring)

        self.emojis, self._meta = self._load_emoji_data()

        self._style_form()
        self._build_nav_bar()
        self._build_all_groups()

        self.form.ui.search_line_edit.textChanged.connect(self.on_input)

        if autoUpdate and self._is_outdated():
            QTimer.singleShot(400, self.updateEmojisOnline)

    # ------------------------------------------------------------------ #
    ## Public API
    # ------------------------------------------------------------------ #
    def select(self) -> typing.Union[str, None]:
        """The last selected emoji (or None)."""
        return self.selected_emoji

    def recentEmojis(self):
        return list(self._settings.value("recent", []) or [])

    def isLocalOutdated(self) -> bool:
        """True if the active dataset is the bundled one or older than the
        configured max age — i.e. a good moment to refresh online."""
        return self._is_outdated()

    def datasetInfo(self) -> dict:
        info = dict(self._meta or {})
        info["count"] = sum(len(v) for v in self.emojis.values())
        return info

    def updateEmojisOnline(self, force: bool = False):
        """Fetch the latest emoji dataset online (off the GUI thread) and, on
        success, cache + rebuild the grid. No-op if already updating."""
        if self._thread is not None:
            return
        if not force and not self._is_outdated():
            return
        self._set_status("Updating emojis…")
        self._thread = QThread(self)
        self._worker = _EmojiUpdateWorker(self._online_url)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_update_finished)
        self._worker.failed.connect(self._on_update_failed)
        self._thread.start()

    # ------------------------------------------------------------------ #
    ## Data loading / caching
    # ------------------------------------------------------------------ #
    def _cache_paths(self):
        base = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        if not base:
            base = os.path.join(_PKG, "components", "json")
        folder = os.path.join(base, "QCustomEmojiPicker")
        return os.path.join(folder, "emojis_online.json"), folder

    def _read_groups(self, path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict) and isinstance(data.get("emojis"), dict):
            data = data["emojis"]
        return {k: v for k, v in data.items()
                if not str(k).startswith("_") and isinstance(v, dict)}

    def _load_emoji_data(self):
        """Prefer a fresher online cache; else the bundled set."""
        bundled = self._read_groups(_BUNDLED_JSON)
        bundled_count = sum(len(v) for v in bundled.values())
        cache_file, _ = self._cache_paths()
        try:
            if os.path.exists(cache_file):
                with open(cache_file, encoding="utf-8") as fh:
                    payload = json.load(fh)
                groups = payload.get("emojis")
                meta = payload.get("_meta", {})
                if groups and sum(len(v) for v in groups.values()) >= bundled_count:
                    return groups, meta
        except Exception:
            pass
        return bundled, {"source": "bundled", "count": bundled_count}

    def _write_cache(self, groups, meta):
        try:
            cache_file, folder = self._cache_paths()
            os.makedirs(folder, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as fh:
                json.dump({"_meta": meta, "emojis": groups}, fh, ensure_ascii=False)
        except Exception:
            pass                                    # cache is best-effort

    def _is_outdated(self):
        meta = self._meta or {}
        if meta.get("source", "bundled") == "bundled":
            return True
        fetched = meta.get("fetched")
        if not fetched:
            return True
        try:
            age = (datetime.datetime.now() - datetime.datetime.fromisoformat(fetched)).days
            return age >= self._update_max_age
        except Exception:
            return True

    # ------------------------------------------------------------------ #
    ## Online-update result handlers
    # ------------------------------------------------------------------ #
    def _on_update_finished(self, groups):
        count = sum(len(v) for v in groups.values())
        self._teardown_thread()
        meta = {"source": self._online_url, "count": count,
                "fetched": datetime.datetime.now().isoformat(timespec="seconds")}
        self._write_cache(groups, meta)
        self.emojis, self._meta = groups, meta
        self._rebuild_groups()
        self._set_status("Updated — %d emojis" % count, transient=True)
        self.emojisUpdated.emit(count)

    def _on_update_failed(self, msg):
        self._teardown_thread()
        self._set_status("Update failed — using local set", transient=True)
        self.updateFailed.emit(msg)

    def _teardown_thread(self):
        try:
            if self._thread is not None:
                self._thread.quit()
                self._thread.wait(1500)
        except Exception:
            pass
        self._thread = None
        self._worker = None

    # ------------------------------------------------------------------ #
    ## Styling
    # ------------------------------------------------------------------ #
    def _style_form(self):
        accent = self._accent
        self.form.setStyleSheet(
            "QScrollArea{border:0; background:transparent;}"
            "#search_line_edit{border:1px solid rgba(128,128,128,0.35); border-radius:15px;"
            " padding:6px 12px; background:rgba(128,128,128,0.10);}"
            "#search_line_edit:focus{border:1px solid %s;}"
            "QGroupBox{border:0; margin-top:16px; font-size:11px; font-weight:700;"
            " color:rgba(128,128,128,0.95);}"
            "QGroupBox::title{subcontrol-origin:margin; left:4px; top:0px;"
            " text-transform:uppercase; letter-spacing:1px;}"
            "#emojiPickerBtn{font-size:20px; border:0; border-radius:9px; background:transparent;}"
            "#emojiPickerBtn:hover{background:rgba(128,128,128,0.20);}"
            "#emojiPickerBtn:pressed{background:%s;}"
            "#emojiNavBtn{border:0; border-radius:9px; background:transparent; padding:5px;}"
            "#emojiNavBtn:hover{background:rgba(128,128,128,0.20);}"
            "#emojiNavBtn:checked{background:rgba(128,128,128,0.16);}"
            "#emojiRefreshBtn{border:0; border-radius:9px; background:transparent; padding:5px;}"
            "#emojiRefreshBtn:hover{background:rgba(128,128,128,0.20);}"
            "#emoji_name_label{color:rgba(128,128,128,0.95); font-size:12px; font-weight:600;}"
            % (accent, accent))
        # a little more room than the default overlay
        self.form.ui.emoji_scroll_area.setMinimumSize(QSize(self.items_per_row * 38 + 24, 300))

    # ------------------------------------------------------------------ #
    ## Category quick-nav bar (real SVG icons)
    # ------------------------------------------------------------------ #
    def _build_nav_bar(self):
        bar = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(bar)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(2)
        order = ["Recent"] + _GROUP_ORDER
        for group in order:
            btn = QtWidgets.QPushButton()
            btn.setObjectName("emojiNavBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(30, 30)
            btn.setIconSize(QSize(18, 18))
            icdir, icname = _GROUP_ICON[group]
            path = os.path.join(icdir, icname)
            self._nav_paths[group] = path
            btn.setIcon(_recolor_svg_icon(path, self._icon_color, 18))
            btn.setToolTip(group)
            btn.clicked.connect(lambda _=False, g=group: self._scroll_to_group(g))
            row.addWidget(btn)
            self._nav_buttons[group] = btn
        row.addStretch(1)
        # refresh / update-online button
        refresh = QtWidgets.QPushButton()
        refresh.setObjectName("emojiRefreshBtn")
        refresh.setCursor(Qt.PointingHandCursor)
        refresh.setFixedSize(30, 30)
        refresh.setIconSize(QSize(17, 17))
        refresh.setIcon(_recolor_svg_icon(os.path.join(_FEATHER, "refresh-cw.svg"), self._icon_color, 17))
        refresh.setToolTip("Update emojis online")
        refresh.clicked.connect(lambda: self.updateEmojisOnline(force=True))
        row.addWidget(refresh)
        self._refresh_btn = refresh
        # insert the bar just under the search box
        self.form.ui.verticalLayout.insertWidget(1, bar)

    def _scroll_to_group(self, group):
        box = self._recent_box if group == "Recent" else self._group_boxes.get(group)
        for g, b in self._nav_buttons.items():
            active = (g == group)
            b.setChecked(active)
            # active category icon takes the accent colour, the rest stay muted
            col = self._accent if active else self._icon_color
            b.setIcon(_recolor_svg_icon(self._nav_paths[g], col, 18))
        if box is not None:
            self.form.ui.emoji_scroll_area.ensureWidgetVisible(box)

    # ------------------------------------------------------------------ #
    ## Grid building
    # ------------------------------------------------------------------ #
    def _make_group_box(self, title, pairs):
        # '&' is a QGroupBox mnemonic — escape it so "Smileys & People" shows literally.
        box = QtWidgets.QGroupBox(str(title).replace("&", "&&"))
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(2)
        grid.setContentsMargins(0, 4, 0, 4)
        for i, (emoji, name) in enumerate(pairs):
            grid.addWidget(_EmojiButton(emoji, name, self),
                           i // self.items_per_row, i % self.items_per_row)
            self.total_emojis[emoji] = name
        box.setLayout(grid)
        return box

    def _build_all_groups(self):
        vlayout = self.form.ui.emoji_scroll_area_vlayout
        self.total_emojis = {}
        self._group_boxes = {}
        self._refresh_recent()          # builds the Recent box at the top (if any)
        for group in _GROUP_ORDER:
            items = self.emojis.get(group)
            if not items:
                continue
            box = self._make_group_box(group, list(items.items()))
            self._group_boxes[group] = box
            vlayout.addWidget(box)

    def _clear_groups(self):
        vlayout = self.form.ui.emoji_scroll_area_vlayout
        while vlayout.count():
            item = vlayout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._group_boxes = {}
        self._recent_box = None

    def _rebuild_groups(self):
        self.form.ui.search_line_edit.clear()
        self._clear_groups()
        self._build_all_groups()

    # ------------------------------------------------------------------ #
    ## Recently used
    # ------------------------------------------------------------------ #
    def _refresh_recent(self):
        vlayout = self.form.ui.emoji_scroll_area_vlayout
        if self._recent_box is not None:
            self._recent_box.setParent(None)
            self._recent_box.deleteLater()
            self._recent_box = None
        recent = self.recentEmojis()
        if not recent:
            return
        pairs = [(e, self.total_emojis.get(e, self._name_for(e))) for e in recent]
        self._recent_box = self._make_group_box("Recent", pairs)
        vlayout.insertWidget(0, self._recent_box)

    def _name_for(self, emoji):
        for items in self.emojis.values():
            if emoji in items:
                return items[emoji]
        return ""

    def _push_recent(self, emoji):
        recent = self.recentEmojis()
        if emoji in recent:
            recent.remove(emoji)
        recent.insert(0, emoji)
        del recent[self._recent_limit:]
        self._settings.setValue("recent", recent)

    # ------------------------------------------------------------------ #
    ## Selection + preview
    # ------------------------------------------------------------------ #
    def _set_preview(self, emoji, name):
        self.form.ui.emoji_image_label.setText(emoji)
        self.form.ui.emoji_name_label.setText(name)

    def _set_status(self, text, transient=False):
        self.form.ui.emoji_name_label.setText(text)
        if self._status_timer is not None:
            self._status_timer.stop()
        if transient:
            self._status_timer = QTimer(self)
            self._status_timer.setSingleShot(True)
            self._status_timer.timeout.connect(lambda: self.form.ui.emoji_name_label.setText(""))
            self._status_timer.start(2600)

    def _on_pick(self, emoji, name):
        self.selected_emoji = emoji
        self._push_recent(emoji)
        self._insert_into_target(emoji)
        self.emojiSelected.emit(emoji)
        if self.close_on_select:
            self.close()
        else:
            self._refresh_recent()

    def _insert_into_target(self, emoji):
        target = getattr(self, "original_target", None)
        if isinstance(target, QtWidgets.QLineEdit):
            target.setText(target.text() + emoji)
        elif isinstance(target, (QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            target.textCursor().insertText(emoji)

    # ------------------------------------------------------------------ #
    ## Search
    # ------------------------------------------------------------------ #
    def on_input(self, text: str):
        vlayout = self.form.ui.emoji_scroll_area_vlayout
        for i in range(vlayout.count()):
            w = vlayout.itemAt(i).widget()
            if w is None:
                continue
            if w.title() == 'Search results':
                w.hide()
                w.deleteLater()
            elif not text and w.isHidden():
                w.show()
            elif text and not w.isHidden():
                w.hide()

        if not text:
            return
        lower = text.lower()
        if self.performance_search:
            matches = [(e, n) for e, n in self.total_emojis.items()
                       if n.lower().startswith(lower)]
        else:
            matches = [(e, n) for e, n in self.total_emojis.items()
                       if lower in n.lower()]
        box = self._make_group_box('Search results', matches)
        vlayout.insertWidget(0, box)

    # ------------------------------------------------------------------ #
    def closeEvent(self, e):
        self._teardown_thread()
        super().closeEvent(e)
