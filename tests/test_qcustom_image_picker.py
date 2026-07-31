"""QCustomImagePicker — byte-level validation, selection, preview, Designer."""
import os
import struct
import zlib

import pytest


def _png(path, w=64, h=48):
    # A gradient, not a flat fill: a uniform image makes crop and stretch
    # produce identical pixels, so a flat fixture would let a broken fitMode
    # pass its own test.
    rows = b"".join(
        b"\x00" + b"".join(bytes(((x * 255) // max(1, w - 1),
                                  (y * 255) // max(1, h - 1),
                                  180)) for x in range(w))
        for y in range(h))

    def chunk(tag, data):
        payload = tag + data
        return (struct.pack(">I", len(data)) + payload
                + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF))

    blob = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows))
            + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(blob)
    return str(path)


@pytest.fixture
def image(tmp_path):
    return _png(tmp_path / "real.png")


class TestImagePickerValidation:
    def test_accepts_a_real_png(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        assert p.validationError(image) is None
        assert p.canAccept(image) is True

    def test_rejects_a_missing_file(self, qapp, tmp_path):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        assert "does not exist" in p.validationError(str(tmp_path / "nope.png"))

    def test_rejects_non_image_bytes_despite_png_extension(self, qapp, tmp_path):
        """The whole point of validating: trust the bytes, not the name."""
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        fake = tmp_path / "evil.png"
        fake.write_text("<?php echo 1; ?>")
        p = QCustomImagePicker()
        assert p.canAccept(str(fake)) is False
        assert "not a readable image" in p.validationError(str(fake))

    def test_rejects_oversize_file(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.maxBytes = 10                      # bytes
        assert "exceeds" in p.validationError(image)

    def test_rejects_oversize_dimensions(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.maxPixels = 10
        assert "dimensions exceed" in p.validationError(image)

    def test_zero_limits_disable_the_checks(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.maxBytes = 0
        p.maxPixels = 0
        assert p.validationError(image) is None


class TestImagePickerSelection:
    def test_set_image_path_emits_and_previews(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        seen = []
        p.imageSelected.connect(seen.append)
        assert p.setImagePath(image) is True
        assert p.hasImage() is True and seen == [image]
        assert p.pixmap().width() == 64 and p.pixmap().height() == 48

    def test_rejected_file_emits_reason_and_keeps_state(self, qapp, tmp_path):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        fake = tmp_path / "bad.png"
        fake.write_text("not an image")
        p = QCustomImagePicker()
        reasons = []
        p.selectionRejected.connect(reasons.append)
        assert p.setImagePath(str(fake)) is False
        assert p.hasImage() is False
        assert p.state == "error" and len(reasons) == 1

    def test_clear_emits_once(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        seen = []
        p.imageCleared.connect(lambda: seen.append(True))
        p.clearImage()
        assert p.hasImage() is False and seen == [True]
        p.clearImage()                       # already empty
        assert seen == [True]

    def test_empty_path_clears(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        p.setImagePath("")
        assert p.hasImage() is False

    def test_successful_selection_clears_error_state(self, qapp, image, tmp_path):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        bad = tmp_path / "bad.png"
        bad.write_text("nope")
        p = QCustomImagePicker()
        p.setImagePath(str(bad))
        assert p.state == "error"
        p.setImagePath(image)
        assert p.state == "default" and p.hasImage() is True


class TestImagePickerPainting:
    def test_empty_and_filled_render_differently(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        empty = QCustomImagePicker()
        empty.resize(240, 160)
        filled = QCustomImagePicker(path=image)
        filled.resize(240, 160)
        assert empty.grab().toImage() != filled.grab().toImage()

    def test_cover_and_contain_differ(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        cover = QCustomImagePicker(path=image)
        cover.resize(240, 80)                 # aspect very different from source
        contain = QCustomImagePicker(path=image)
        contain.fitMode = "contain"
        contain.resize(240, 80)
        assert cover.grab().toImage() != contain.grab().toImage()

    def test_cover_source_rect_preserves_aspect(self, qapp, image):
        from qtpy.QtCore import QRectF
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        rect = QRectF(0, 0, 200, 100)         # 2:1 target, 4:3 source
        src = p._sourceRect(rect)
        assert abs(src.width() / src.height() - 2.0) < 0.01
        assert src.width() <= p.pixmap().width()

    def test_contain_source_is_the_whole_image(self, qapp, image):
        from qtpy.QtCore import QRectF
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        p.fitMode = "contain"
        src = p._sourceRect(QRectF(0, 0, 200, 100))
        assert src.width() == 64 and src.height() == 48

    def test_circle_shape_differs(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        rounded = QCustomImagePicker(path=image)
        rounded.resize(160, 160)
        circle = QCustomImagePicker(path=image)
        circle.shape = "circle"
        circle.resize(160, 160)
        assert rounded.grab().toImage() != circle.grab().toImage()

    def test_clear_button_only_when_allowed(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        p.resize(240, 160)
        p.grab()
        assert not p._clearRect.isEmpty()
        p.allowClear = False
        p.grab()
        assert p._clearRect.isEmpty()

    def test_clicking_clear_button_removes_the_image(self, qapp, image):
        from qtpy.QtCore import QEvent, QPointF, Qt
        from qtpy.QtGui import QMouseEvent
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker(path=image)
        p.resize(240, 160)
        p.grab()
        ev = QMouseEvent(QEvent.MouseButtonRelease,
                         QPointF(p._clearRect.center()),
                         Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        p.mouseReleaseEvent(ev)
        assert p.hasImage() is False


class TestImagePickerDesigner:
    def test_image_path_property_roundtrip(self, qapp, image):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.imagePath = image
        assert p.imagePath == image

    def test_enum_properties_fall_back(self, qapp):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.shape = "nonsense"
        assert p.shape == "rounded"
        p.fitMode = "nonsense"
        assert p.fitMode == "cover"

    def test_numeric_properties_clamp(self, qapp):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        p = QCustomImagePicker()
        p.maxBytes = -5
        p.maxPixels = -5
        p.cornerRadius = -5
        assert p.maxBytes == 0 and p.maxPixels == 0 and p.cornerRadius == 0

    def test_placeholder_shows_when_empty(self, qapp):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        a = QCustomImagePicker()
        a.resize(240, 160)
        b = QCustomImagePicker()
        b.placeholderText = "Totally different wording here"
        b.resize(240, 160)
        assert a.grab().toImage() != b.grab().toImage()

    def test_colors_via_qproperty(self, qapp):
        from Custom_Widgets.QCustomImagePicker import QCustomImagePicker
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        p = QCustomImagePicker()
        p.ensurePolished()
        assert p.borderErrorColor.name().lower() == "#dc2626"     # destructive
        assert p.borderActiveColor.name().lower() == "#2563eb"    # accent
        qapp.setStyleSheet("")
