########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## ImageLoader — async, cached image loading for Custom_Widgets.
##
## Widgets should NOT hand-roll `urllib` + threads + disk caching to show a
## remote avatar or cover; that belongs here. Point any widget at a local PATH
## or an http(s) URL and get a `QPixmap` back on the GUI thread:
##
##     from Custom_Widgets.ImageLoader import load_image
##     load_image("https://…/cover.jpg", self._onPixmap)   # async, cached
##     load_image("/abs/cover.png",      self._onPixmap)   # sync fast-path
##
## URLs are downloaded ONCE on a background thread, cached to disk (keyed by a
## hash of the URL) and reused forever after; the QPixmap is always built and
## delivered on the GUI thread (Qt requirement). Failures are swallowed and the
## callback simply never fires, so the widget keeps its fallback.
########################################################################
import os
import hashlib
import tempfile

from qtpy.QtCore import QObject, Signal, QRunnable, QThreadPool, Qt
from qtpy.QtGui import QPixmap, QPainter, QPainterPath, QColor


def default_cache_dir():
    d = os.path.join(tempfile.gettempdir(), "customwidgets_images")
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        pass
    return d


def _is_url(source):
    s = str(source).lower()
    return s.startswith("http://") or s.startswith("https://")


def _cache_path(url, cache_dir):
    ext = os.path.splitext(url.split("?")[0])[1]
    if len(ext) > 5 or not ext:
        ext = ".img"
    return os.path.join(cache_dir, hashlib.md5(url.encode()).hexdigest() + ext)


class _TaskSignals(QObject):
    done = Signal(str, str)     # source, local_path ("" on failure)


class _DownloadTask(QRunnable):
    def __init__(self, source, path, signals):
        super().__init__()
        self._source = source
        self._path = path
        self._signals = signals

    def run(self):
        ok = False
        try:
            if os.path.exists(self._path) and os.path.getsize(self._path) > 256:
                ok = True
            else:
                import urllib.request
                req = urllib.request.Request(self._source,
                                             headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = r.read()
                if data:
                    with open(self._path, "wb") as f:
                        f.write(data)
                    ok = os.path.getsize(self._path) > 256
        except Exception:
            ok = False
        try:
            self._signals.done.emit(self._source, self._path if ok else "")
        except RuntimeError:
            # signals object torn down (interpreter/app shutdown) — nothing to do
            pass


class ImageLoader(QObject):
    """Process-wide singleton. Use the module-level ``load_image`` instead of
    touching this directly."""

    ready = Signal(str, object)     # source, QPixmap (or None)
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ImageLoader()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._pool = QThreadPool.globalInstance()
        self._cache_dir = default_cache_dir()
        self._pm_cache = {}        # source -> QPixmap
        self._pending = {}         # source -> [callbacks]
        self._signals = _TaskSignals()
        self._signals.done.connect(self._on_downloaded)

    def load(self, source, callback=None, cache_dir=None):
        """Resolve ``source`` (path or URL) to a QPixmap and invoke ``callback``
        with it on the GUI thread. Returns a cached QPixmap immediately when one
        is available, else None (the callback fires later)."""
        source = str(source)
        if not source:
            return None
        if source in self._pm_cache:
            pm = self._pm_cache[source]
            if callback:
                callback(pm)
            return pm

        # local file → load now, on the GUI thread
        if not _is_url(source):
            if os.path.exists(source):
                pm = QPixmap(source)
                if not pm.isNull():
                    self._pm_cache[source] = pm
                    if callback:
                        callback(pm)
                    return pm
            return None

        # URL → cached file fast-path, else queue a download
        cdir = cache_dir or self._cache_dir
        path = _cache_path(source, cdir)
        if os.path.exists(path) and os.path.getsize(path) > 256:
            pm = QPixmap(path)
            if not pm.isNull():
                self._pm_cache[source] = pm
                if callback:
                    callback(pm)
                return pm

        self._pending.setdefault(source, [])
        if callback:
            self._pending[source].append(callback)
        # only one in-flight download per source
        if len(self._pending[source]) <= 1:
            self._pool.start(_DownloadTask(source, path, self._signals))
        return None

    def _on_downloaded(self, source, path):
        pm = None
        if path and os.path.exists(path):
            loaded = QPixmap(path)
            if not loaded.isNull():
                pm = loaded
                self._pm_cache[source] = pm
        for cb in self._pending.pop(source, []):
            try:
                if pm is not None:
                    cb(pm)
            except Exception:
                pass
        self.ready.emit(source, pm)


def load_image(source, callback=None, cache_dir=None):
    """Module-level convenience: load a local path or http(s) URL and deliver a
    QPixmap to ``callback`` on the GUI thread (cached; async for URLs)."""
    return ImageLoader.instance().load(source, callback, cache_dir)


def rounded_pixmap(pixmap, size, fallback_color=None):
    """Return ``pixmap`` centre-cropped into a circle of ``size`` px (2x for
    crispness). If ``pixmap`` is null/None, paint a flat ``fallback_color`` disc
    (or transparent)."""
    s = int(size * 2)
    out = QPixmap(s, s)
    out.fill(QColor(0, 0, 0, 0))
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing, True)
    path = QPainterPath()
    path.addEllipse(0, 0, s, s)
    p.setClipPath(path)
    if pixmap is not None and not pixmap.isNull():
        sc = pixmap.scaled(s, s, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        p.drawPixmap(int((s - sc.width()) / 2), int((s - sc.height()) / 2), sc)
    elif fallback_color is not None:
        p.fillRect(0, 0, s, s, QColor(fallback_color))
    p.end()
    out.setDevicePixelRatio(2.0)
    return out
