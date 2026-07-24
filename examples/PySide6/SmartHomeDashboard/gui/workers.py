"""Background workers. AvatarWorker fetches a real portrait (best-effort,
async) from a free no-key provider; failures are swallowed so the fallback
avatar stays."""

from qtpy.QtCore import QObject, Signal


class AvatarWorker(QObject):
    loaded = Signal(bytes)

    def __init__(self, url):
        super().__init__()
        self._url = url

    def run(self):
        try:
            import urllib.request
            req = urllib.request.Request(self._url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as r:
                data = r.read()
            if data:
                self.loaded.emit(data)
        except Exception:
            pass
