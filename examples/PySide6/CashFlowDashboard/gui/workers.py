"""Background workers — the Worker -> Signal -> GUI pattern from the guide.

A worker runs on its own QThread and only ever EMITS Qt signals; it never
touches widgets directly. The GUI thread receives the signal (queued) and
updates the widgets.
"""

import time
from datetime import datetime

from qtpy.QtCore import QObject, Signal


class ClockWorker(QObject):
    """Emits a formatted 'HH:MM, DD Month YYYY' string once a second, off-thread."""

    tick = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._run = True

    def stop(self):
        self._run = False

    def run(self):
        while self._run:
            now = datetime.now()
            self.tick.emit(now.strftime("%H:%M, %d %B %Y"))
            slept = 0.0
            while self._run and slept < 1.0:
                time.sleep(0.1)
                slept += 0.1
