#!/usr/bin/env python3
"""Showcase captures for doc pages whose widgets sit OUTSIDE manifestRows().

gen_widget_docs.py drives free/pro manifest rows only, so four kinds of pages
never get a screenshot from it: legacy classes the manifest skips (Canvas),
container/framework classes tiered as internal (the QCustomComponent trio),
classes that never entered the manifest (QDragWidget), and Pro widgets that
live in the sibling repo (QCustomDataTablePro). This shoots them through the
same harness so their pages match everything else.

Usage:  python tools/shoot_extra_docs.py
Needs the Pro repo checked out as a sibling directory for the DataTablePro
shot; that one is skipped with a warning if the import fails.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO = os.path.join(os.path.dirname(ROOT), "QT-PyQt-PySide-Custom-Widgets-Pro")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
if os.path.isdir(PRO):
    sys.path.insert(0, PRO)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_API", "pyside6")

import gen_widget_docs as G


def _seedCanvas(w, theme):
    from qtpy.QtCore import Qt
    from qtpy.QtGui import QColor
    G_DOCS = os.path.join(os.path.dirname(ROOT),
                          "Docs-QT-PyQt-PySide-Custom-Widgets")
    w.setBackgroundImage(os.path.join(G_DOCS, "static", "img",
                                      "social-card.png"))
    # An annotation canvas with nothing annotated is just an image viewer:
    # box the logo and circle the tagline the way a labelling session would.
    w.shapes.append(("rectangle", QColor("#22c55e"), "logo",
                     [190, 360, 545, 650]))
    w.shapes.append(("ellipse", QColor("#f59e0b"), "tagline",
                     [180, 660, 1290, 760]))
    # update=False draws the committed shapes; update=True would also draw the
    # in-progress drag shape from start/end coords that are None at rest.
    w.updateCanvas()
    # QLabel copies the pixmap on setPixmap, so push it again AFTER the shapes
    # landed — and scale down, or the shot host inherits the full 1545px hint.
    w.setPixmap(w.pixmap.scaled(460, 305, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation))


def _seedDrag(w, theme):
    from qtpy.QtWidgets import QLabel, QVBoxLayout
    from Custom_Widgets.widgets.containers.QDraggableWidget import QDragItem
    lay = w.layout() or QVBoxLayout(w)
    for text in ("Ship the changelog", "Review PR #142", "Prepare 2.3.0 notes"):
        item = QDragItem()
        il = QVBoxLayout(item)
        label = QLabel(text)
        label.setStyleSheet("padding: 6px;")
        il.addWidget(label)
        lay.addWidget(item)
    lay.addStretch(1)
    w.setMinimumSize(300, 200)


def _seedDataTablePro(w, theme):
    G._seedDataTable(w, theme)
    w.groupBy(["plan"], aggregates={"mrr": "sum"})
    w.expandAllGroups()
    w.setMinimumSize(640, 300)


def main():
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    from Custom_Widgets.widgets.data.QCustomAnnotationWidget import Canvas
    from Custom_Widgets.widgets.containers.QDraggableWidget import QDragWidget

    G.SEEDS["Canvas"] = _seedCanvas
    G.SEEDS["QDragWidget"] = _seedDrag

    targets = [(Canvas, "annotationwidget"), (QDragWidget, "draggablewidget")]

    for name in ("QCustomComponent", "QCustomComponentContainer",
                 "QCustomComponentLoader"):
        cls = G.importWidget(
            name, "Custom_Widgets/widgets/containers/%s.py" % name)
        targets.append((cls, G.slugFor(name)))

    try:
        from custom_widgets_pro.datatable.datatable_pro import QCustomDataTablePro
        G.SEEDS["QCustomDataTablePro"] = _seedDataTablePro
        targets.append((QCustomDataTablePro, "datatablepro"))
    except Exception as exc:
        print("SKIP QCustomDataTablePro (Pro repo not importable: %s)" % exc)

    failed = []
    for cls, slug in targets:
        for theme in ("light", "dark"):
            made = G.shoot(cls, slug, theme)
            print("%s %s -> %s" % (slug, theme, made))
            if not made:
                failed.append("%s (%s)" % (slug, theme))
    if failed:
        print("FAILED %d: %s" % (len(failed), ", ".join(failed)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
