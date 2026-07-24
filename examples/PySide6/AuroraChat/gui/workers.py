"""Background workers — run off the GUI thread and only emit Qt signals
(Worker -> Signal -> GUI slot). Never touch widgets from here.

TypingWorker simulates the other participant's presence: it periodically flips
between "Online" and "typing…" so the thread header animates like a real
messenger, demonstrating the correct threaded pattern."""

from qtpy.QtCore import QObject, Signal
import time


class TypingWorker(QObject):
    presenceChanged = Signal(bool)          # True -> typing, False -> online

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        typing = False
        # slow, gentle cadence so the demo reads as "alive" without flicker
        steps = 0
        while self._running:
            time.sleep(0.25)
            steps += 1
            if steps >= 14:                 # ~3.5s per phase
                steps = 0
                typing = not typing
                self.presenceChanged.emit(typing)

    def stop(self):
        self._running = False
