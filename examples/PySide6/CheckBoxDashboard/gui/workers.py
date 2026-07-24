"""Background worker(s). A trivial clock worker demonstrates the correct
Worker -> Signal -> GUI (queued) pattern used across the Custom_Widgets
example apps."""

import time

from qtpy.QtCore import QObject, Signal


class ClockWorker(QObject):
    tick = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        while self._running:
            self.tick.emit(time.strftime("%H:%M:%S"))
            time.sleep(1.0)

    def stop(self):
        self._running = False


class AvatarWorker(QObject):
    """Fetch a real avatar image from a free, no-key provider (best-effort).
    Emits raw PNG/JPEG bytes; the GUI turns them into a pixmap. Any failure is
    swallowed so the seeded fallback avatar simply stays."""
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
