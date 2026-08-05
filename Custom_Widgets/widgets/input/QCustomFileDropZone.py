########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/@SpinnTV
# WEBSITE: customwidgets.org
########################################################################

########################################################################
## QCustomFileDropZone - drag-and-drop file input with click-to-browse.
##
## A dashed zone that accepts dropped files (filtered by extension) or opens
## a file dialog on click. Highlights while dragging (a `dragActive` property).
## Tokenized. Emits filesDropped / filesChanged.
########################################################################
import os

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog


class QCustomFileDropZone(QWidget):
    filesDropped = Signal(list)        # newly added paths
    filesChanged = Signal(list)        # full current list

    WIDGET_ICON = "components/icons/dropzone.png"
    WIDGET_TOOLTIP = "A drag-and-drop file input"
    WIDGET_MODULE = "Custom_Widgets.QCustomFileDropZone"
    WIDGET_DOM_XML = """
    <ui language='c++'>
        <widget class='QCustomFileDropZone' name='customFileDropZone'>
            <property name='geometry'><rect><x>0</x><y>0</y><width>320</width><height>140</height></rect></property>
        </widget>
    </ui>
    """
    __catalog__ = {
        "name": "QCustomFileDropZone",
        "props": {},
        "signals": ["filesDropped", "filesChanged"],
        "tokens_used": ["surface", "surface-muted", "on-surface", "outline", "accent"],
    }

    def __init__(self, parent=None, multiple=True, extensions=None):
        super().__init__(parent)
        self.setObjectName("QCustomFileDropZone")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAcceptDrops(True)
        self.setProperty("dragActive", False)
        self.setCursor(Qt.PointingHandCursor)
        self._multiple = multiple
        self._exts = self._normExts(extensions)
        self._files = []

        col = QVBoxLayout(self)
        col.setAlignment(Qt.AlignCenter)
        col.setSpacing(4)
        self._prompt = QLabel("Drop files here, or click to browse", self)
        self._prompt.setObjectName("dropPrompt")
        self._prompt.setAlignment(Qt.AlignCenter)
        self._prompt.setWordWrap(True)
        col.addWidget(self._prompt)
        self._detail = QLabel("", self)
        self._detail.setObjectName("dropDetail")
        self._detail.setAlignment(Qt.AlignCenter)
        self._detail.setWordWrap(True)
        col.addWidget(self._detail)

    @staticmethod
    def _normExts(exts):
        if not exts:
            return None
        out = set()
        for e in exts:
            e = str(e).lower().lstrip("*")
            if not e.startswith("."):
                e = "." + e
            out.add(e)
        return out

    def _accepts(self, path):
        if self._exts is None:
            return True
        return os.path.splitext(path)[1].lower() in self._exts

    def _setDragActive(self, active):
        self.setProperty("dragActive", bool(active))
        self.style().unpolish(self)
        self.style().polish(self)

    # ------------------------------------------------------------------ #
    ## Drag & drop
    # ------------------------------------------------------------------ #
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self._setDragActive(True)
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        self._setDragActive(False)

    def dropEvent(self, e):
        self._setDragActive(False)
        paths = [u.toLocalFile() for u in e.mimeData().urls() if u.isLocalFile()]
        self._addPaths(paths)
        e.acceptProposedAction()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._browse()
        super().mousePressEvent(e)

    def _browse(self):
        flt = "All files (*)"
        if self._exts:
            flt = "Accepted (%s)" % " ".join("*" + x for x in sorted(self._exts))
        if self._multiple:
            paths, _ = QFileDialog.getOpenFileNames(self, "Select files", "", flt)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", flt)
            paths = [path] if path else []
        self._addPaths(paths)

    def _addPaths(self, paths):
        added = []
        for p in paths:
            if p and self._accepts(p) and p not in self._files:
                if not self._multiple:
                    self._files = []
                self._files.append(p)
                added.append(p)
        if added:
            self._updateDetail()
            self.filesDropped.emit(added)
            self.filesChanged.emit(list(self._files))

    def _updateDetail(self):
        if not self._files:
            self._detail.setText("")
            return
        names = [os.path.basename(p) for p in self._files]
        self._detail.setText(", ".join(names) if len(names) <= 3
                             else "%d files: %s, ..." % (len(names), ", ".join(names[:3])))

    # ------------------------------------------------------------------ #
    ## API
    # ------------------------------------------------------------------ #
    def files(self):
        return list(self._files)

    def clear(self):
        self._files = []
        self._updateDetail()
        self.filesChanged.emit([])

    def setAcceptedExtensions(self, extensions):
        self._exts = self._normExts(extensions)

    def setMultiple(self, multiple):
        self._multiple = bool(multiple)
