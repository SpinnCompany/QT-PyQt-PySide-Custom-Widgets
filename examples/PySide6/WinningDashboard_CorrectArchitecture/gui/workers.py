"""Background workers — the Worker -> Signal -> GUI pattern from the guide.

A worker runs on its own QThread and only ever EMITS Qt signals; it never
touches widgets directly. The GUI thread receives the signal (queued) and
updates the widgets. This keeps the UI responsive even if data fetching is slow.
"""

import math
import time

from qtpy.QtCore import QObject, Signal

from gui import data as D


class LiveMetricsWorker(QObject):
    """Emits nudged KPI values + fresh sparkline points on a timer, off-thread."""

    tick = Signal(dict)     # {"values": {key: float}, "spark": {key: [floats]}}

    def __init__(self, interval=2.0, parent=None):
        super().__init__(parent)
        self._interval = interval
        self._run = True

    def stop(self):
        self._run = False

    def run(self):
        i = 0
        # seed rolling sparkline buffers from the static series
        buffers = {key: list(series)[-16:] for key, _l, series, _c, _a in
                   [(k, l, s, c, a) for k, l, s, c, a in D.KPIS]}
        while self._run:
            i += 1
            values = {}
            for key, base in D.KPI_BASE.items():
                swing = base * 0.01
                values[key] = base + swing * math.sin(i / 3.0 + hash(key) % 7)
            spark = {}
            for key in buffers:
                buf = buffers[key]
                nxt = buf[-1] + (buf[-1] * 0.06) * math.sin(i / 2.0 + len(buf))
                buf.append(max(0.0, nxt))
                if len(buf) > 24:
                    del buf[0]
                spark[key] = list(buf)
            self.tick.emit({"values": values, "spark": spark})
            # sleep in slices so stop() is responsive
            slept = 0.0
            while self._run and slept < self._interval:
                time.sleep(0.1)
                slept += 0.1
