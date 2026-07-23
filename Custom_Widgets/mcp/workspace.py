########################################################################
## CUSTOM WIDGETS MCP - WORKSPACE REGISTRY + PER-PROJECT SERIALIZATION
##
## The MCP server is a thin forwarder: the real singletons it drives - Qt
## Designer and the running app - are separate processes, each addressed by a
## per-project QLocalServer socket whose name derives from the project folder
## (see DesignerBridge.bridgeServerName / AppControl.appControlServerName).
##
## Two projects therefore never collide (different sockets). But two agents /
## sessions driving the SAME project would interleave commands against the one
## Designer/app and race. This module removes that race:
##
##   ProjectWorker   - one daemon thread + FIFO queue per project. Every mutating
##                     bridge/app command for that project is submitted here and
##                     runs strictly one-at-a-time, so concurrent MCP clients
##                     (e.g. a shared HTTP transport) are serialized by project.
##   ProjectRegistry - resolves a per-call `project` argument to an absolute dir
##                     and hands out the (lazily created) worker for it.
##
## Nothing here imports Qt: it is pure stdlib so it stays cheap and testable.
########################################################################
import os
import queue
import threading
import time
from concurrent.futures import Future


class ProjectWorker:
    """Single-thread FIFO command queue for one project's Designer/app singletons.

    Submit a zero-arg callable; it runs on this worker's thread, one at a time,
    in submission order. ``submit`` blocks until the callable finishes and
    returns its result (or re-raises its exception), so callers keep their
    natural request/reply shape while the underlying singleton is accessed
    serially. ``status`` reports queue depth and the in-flight command so a
    discovery tool can show who is driving what.
    """

    def __init__(self, project_dir):
        self.project_dir = os.path.abspath(project_dir)
        self._q = queue.Queue()
        self._lock = threading.Lock()
        self._depth = 0                 # jobs queued but not yet started
        self._current = None            # (owner, label, monotonic_start) while running
        self._thread = threading.Thread(
            target=self._run, name="cw-mcp-worker:%s" % os.path.basename(self.project_dir),
            daemon=True)
        self._thread.start()

    def submit(self, fn, owner=None, label=None, timeout=None):
        """Run ``fn()`` on this project's worker thread and return its result.

        Blocks up to ``timeout`` seconds (None = forever). Re-raises whatever
        ``fn`` raises. ``owner``/``label`` tag the job for status reporting.
        """
        fut = Future()
        with self._lock:
            self._depth += 1
        self._q.put((fn, fut, owner, label))
        return fut.result(timeout=timeout)

    def _run(self):
        while True:
            fn, fut, owner, label = self._q.get()
            with self._lock:
                self._depth -= 1
                self._current = (owner, label, time.monotonic())
            try:
                result = fn()
            except BaseException as exc:  # noqa: BLE001 - propagate to submitter
                fut.set_exception(exc)
            else:
                fut.set_result(result)
            finally:
                with self._lock:
                    self._current = None
                self._q.task_done()

    def status(self):
        """{queue_depth, busy, current:{owner,label,held_s}|None} - a snapshot
        of this project's serialization queue for workspaces_status."""
        with self._lock:
            cur = self._current
            current = None
            if cur is not None:
                owner, label, started = cur
                current = {"owner": owner, "label": label,
                           "held_s": round(time.monotonic() - started, 2)}
            return {"queue_depth": self._depth, "busy": current is not None,
                    "current": current}


class ProjectRegistry:
    """Resolves per-call ``project`` arguments to absolute dirs and owns one
    ``ProjectWorker`` per project (created on first use).

    ``default_provider`` is a zero-arg callable returning the current default
    project dir (the ``--project-dir`` the server was started with). It is read
    lazily on every ``resolve`` so the default can be repointed at runtime and
    so tests that monkeypatch it keep working.
    """

    def __init__(self, default_provider):
        self._default_provider = default_provider
        self._workers = {}
        self._lock = threading.Lock()

    def default_dir(self):
        return os.path.abspath(self._default_provider())

    def resolve(self, project=None):
        """Resolve a project argument to an absolute dir.

        Empty/None -> the current default. Absolute paths pass through.
        Relative paths resolve against the default dir (so an agent can name a
        sibling example folder without knowing the absolute path).
        """
        if not project:
            return self.default_dir()
        if os.path.isabs(project):
            return os.path.abspath(project)
        return os.path.abspath(os.path.join(self.default_dir(), project))

    def worker(self, project_dir):
        """The (lazily created) serialization worker for an absolute dir."""
        project_dir = os.path.abspath(project_dir)
        with self._lock:
            worker = self._workers.get(project_dir)
            if worker is None:
                worker = ProjectWorker(project_dir)
                self._workers[project_dir] = worker
            return worker

    def known(self):
        """Absolute dirs that have a worker (i.e. have been touched this run)."""
        with self._lock:
            return sorted(self._workers)

    def statuses(self):
        """{project_dir: worker.status()} for every known project."""
        with self._lock:
            workers = dict(self._workers)
        return {d: w.status() for d, w in workers.items()}
