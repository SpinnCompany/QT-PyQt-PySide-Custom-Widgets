"""Background workers — the Worker -> Signal -> GUI pattern from the guide.

A worker runs on its own QThread and only ever EMITS Qt signals; it never
touches widgets directly. The GUI thread receives the signal (queued) and
updates the widgets.
"""

import time

from qtpy.QtCore import QObject, Signal


class MarketWorker(QObject):
    """Simulates fetching the market snapshot off-thread, then emits it once.

    A real app would poll an exchange API on this loop; here it just delivers
    the static snapshot after a short delay so the table population is driven
    by the Worker -> Signal -> GUI path rather than the GUI thread.
    """

    rowsReady = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._run = True

    def stop(self):
        self._run = False

    def run(self):
        # brief simulated fetch latency
        slept = 0.0
        while self._run and slept < 0.4:
            time.sleep(0.1)
            slept += 0.1
        if self._run:
            self.rowsReady.emit([])       # payload merged with palette in the GUI
