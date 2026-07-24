"""Async remote image loading for the chat demo.

Pulls REAL pictures from free, no-API-key providers (faces from
thispersondoesnotexist / randomuser, media from picsum.photos), fully async via
QNetworkAccessManager (never blocks the GUI), with an on-disk cache and a
graceful fallback: if the network is unavailable the caller's existing
placeholder (initials avatar / gradient tile) simply stays.
"""

import os
import hashlib

from qtpy.QtCore import QObject, QUrl, QStandardPaths, Qt
from qtpy.QtGui import QPixmap, QPainter, QPainterPath, QColor
from qtpy.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


# ---- free providers ------------------------------------------------------- #
def avatar_url(index, gender="men", size=200):
    """A distinct real portrait per contact (randomuser.me — free, direct JPEG)."""
    return "https://randomuser.me/api/portraits/%s/%d.jpg" % (gender, index % 100)


def face_url(seed, size=400):
    """A single AI face (thispersondoesnotexist — one random face per request)."""
    return "https://thispersondoesnotexist.com/"


def media_url(seed, w=200, h=200):
    """A deterministic stock photo (Lorem Picsum — free, direct JPEG)."""
    return "https://picsum.photos/seed/%s/%d/%d" % (seed, w, h)


# ---- pixmap shaping ------------------------------------------------------- #
def rounded_pixmap(pm, radius):
    if pm.isNull():
        return pm
    size = pm.size()
    out = QPixmap(size)
    out.setDevicePixelRatio(pm.devicePixelRatio())
    out.fill(QColor(0, 0, 0, 0))
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing, True)
    path = QPainterPath()
    path.addRoundedRect(0, 0, size.width(), size.height(), radius, radius)
    p.setClipPath(path)
    p.drawPixmap(0, 0, pm)
    p.end()
    return out


class RemoteImageLoader(QObject):
    """Loads image URLs asynchronously, caches them on disk, and hands the
    finished QPixmap to a per-request callback. Safe to call for many images at
    once; a failed load just never fires its callback (placeholder stays)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._nam = QNetworkAccessManager(self)
        self._callbacks = {}
        base = QStandardPaths.writableLocation(QStandardPaths.CacheLocation) or ""
        self._cache_dir = os.path.join(base, "AuroraChat", "images")
        try:
            os.makedirs(self._cache_dir, exist_ok=True)
        except Exception:
            self._cache_dir = None
        self._nam.finished.connect(self._on_finished)

    def _cache_file(self, url):
        if not self._cache_dir:
            return None
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()
        return os.path.join(self._cache_dir, h + ".img")

    def load(self, url, callback):
        """Fetch `url` and call `callback(QPixmap)` when ready. Serves from the
        disk cache instantly when present."""
        cache = self._cache_file(url)
        if cache and os.path.exists(cache):
            pm = QPixmap()
            if pm.load(cache) and not pm.isNull():
                self._safe_call(callback, pm)
                return
        req = QNetworkRequest(QUrl(url))
        # Qt6's QNetworkAccessManager follows redirects by default, so no
        # explicit redirect-policy attribute is needed (and the old
        # FollowRedirectsAttribute was removed in Qt6).
        req.setHeader(QNetworkRequest.UserAgentHeader, "AuroraChat/1.0")
        reply = self._nam.get(req)
        self._callbacks[reply] = (callback, cache)

    def _on_finished(self, reply):
        callback, cache = self._callbacks.pop(reply, (None, None))
        try:
            if callback is not None and reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                pm = QPixmap()
                if pm.loadFromData(data) and not pm.isNull():
                    if cache:
                        try:
                            with open(cache, "wb") as fh:
                                fh.write(bytes(data))
                        except Exception:
                            pass
                    self._safe_call(callback, pm)
        finally:
            reply.deleteLater()

    @staticmethod
    def _safe_call(callback, pm):
        # The target widget may have been rebuilt/deleted (theme recolour)
        # between issuing the request and its completion — swallow that.
        try:
            callback(pm)
        except RuntimeError:
            pass
