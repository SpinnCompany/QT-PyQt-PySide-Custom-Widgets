########################################################################
## QCustomImagePicker example
##
## An avatar-and-cover form: a circular avatar picker, a wide cover picker in
## cover mode, and the same image in contain mode so the difference is visible.
## Drag an image file onto any of them, or click to browse. The status line
## shows the rejection reason when a file is refused.
## Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtWidgets

from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
from Custom_Widgets.JSonStyles.tokens import applyDesignTokens


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomImagePicker")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        self._theme = "light"

        top = QtWidgets.QHBoxLayout()
        top.setSpacing(20)

        avatarBox = QtWidgets.QVBoxLayout()
        avatarBox.addWidget(self._heading("Avatar"))
        self.avatar = QCustomImagePicker(placeholder="Drop a photo")
        self.avatar.shape = "circle"
        self.avatar.setFixedSize(130, 130)
        avatarBox.addWidget(self.avatar)
        avatarBox.addStretch(1)
        top.addLayout(avatarBox)

        coverBox = QtWidgets.QVBoxLayout()
        coverBox.addWidget(self._heading("Cover (cover / contain)"))
        self.cover = QCustomImagePicker(placeholder="Drop a wide image")
        self.cover.setMinimumHeight(130)
        coverBox.addWidget(self.cover)
        self.contain = QCustomImagePicker(placeholder="same image, contain")
        self.contain.fitMode = "contain"
        self.contain.setMinimumHeight(130)
        coverBox.addWidget(self.contain)
        top.addLayout(coverBox, 1)

        layout.addLayout(top)

        # Mirror whatever the cover picker accepts into the contain one, so the
        # two fit modes can be compared on the same file.
        self.cover.imageSelected.connect(self.contain.setImagePath)
        self.cover.imageCleared.connect(self.contain.clearImage)

        for picker, name in ((self.avatar, "avatar"), (self.cover, "cover")):
            picker.imageSelected.connect(
                lambda path, n=name: self.status.setText("%s: %s" % (n, path)))
            picker.selectionRejected.connect(
                lambda why, n=name: self.status.setText("%s rejected — %s" % (n, why)))
            picker.imageCleared.connect(
                lambda n=name: self.status.setText("%s cleared" % n))

        row = QtWidgets.QHBoxLayout()
        for text, slot in (("Browse avatar", self.avatar.browse),
                           ("Clear all", self._clearAll),
                           ("Light / dark", self._toggleTheme)):
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(slot)
            row.addWidget(btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.status = QtWidgets.QLabel(
            "Drop an image, or click a field to browse. "
            "Non-images and files over 5 MB are refused.")
        layout.addWidget(self.status)
        layout.addStretch(1)
        self.resize(640, 480)

    @staticmethod
    def _heading(text):
        label = QtWidgets.QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def _clearAll(self):
        for picker in (self.avatar, self.cover, self.contain):
            picker.clearImage()

    def _toggleTheme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        applyDesignTokens(QtWidgets.QApplication.instance(), theme=self._theme)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    applyDesignTokens(app, theme="light")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
