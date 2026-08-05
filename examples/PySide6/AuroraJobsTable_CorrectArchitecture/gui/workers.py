"""Background workers — the Worker -> Signal -> GUI pattern from the guide.

The worker runs on its own QThread and only EMITS a signal with the loaded rows;
it never touches widgets. The manager receives `rowsLoaded` (queued to the GUI
thread) and fills the table. This mirrors how a real app fetches jobs from a DB
or API without blocking the UI.
"""

import time

from qtpy.QtCore import QObject, Signal

from gui import data as D


class JobsLoaderWorker(QObject):
    rowsLoaded = Signal(list)      # list[dict] of job rows

    def __init__(self, count=14, delay=0.35, parent=None):
        super().__init__(parent)
        self._count = count
        self._delay = delay
        self._run = True

    def stop(self):
        self._run = False

    def run(self):
        # simulate a short fetch, then hand the rows to the GUI thread
        slept = 0.0
        while self._run and slept < self._delay:
            time.sleep(0.05)
            slept += 0.05
        if self._run:
            self.rowsLoaded.emit(D.sample_rows(self._count))
