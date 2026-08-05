"""QCustomDataTable — basic (free core) example.

Demonstrates columns, typed values, client-side filtering, pagination and
selection signals. Chrome comes from Qss/scss + json-styles; the columns and
data are seeded in code (Designer cannot author data config)."""

import json
import os, sys

# Force PySide6 to match compiled ui files
os.environ.setdefault("QT_API", "pyside6")

from Custom_Widgets.Project import setProjectRoot
setProjectRoot(__file__)

from Custom_Widgets import *
from Custom_Widgets.QCustomDataTable import DataTableColumn
from qtpy.QtCore import QCoreApplication, QSettings
from qtpy.QtWidgets import QApplication


# ---- sample data -----------------------------------------------------------
_CATEGORIES = ["Laptops", "Phones", "Audio", "Cameras", "Wearables"]
SAMPLE_ROWS = [
    {
        "id": i + 1,
        "name": "Product %02d" % (i + 1),
        "category": _CATEGORIES[i % len(_CATEGORIES)],
        "price": round(19.99 + (i * 37) % 950, 2),
        "in_stock": (i % 3 != 0),
    }
    for i in range(43)   # 43 rows -> several pages
]


class MainWindow(QCustomMainWindow):
    def __init__(self, parent=None):
        QCustomMainWindow.__init__(self)
        from src.ui_MainWindow import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})

        self.show()
        themeEngine = self.themeEngine
        org = getattr(themeEngine, "organizationName", "")
        if org:
            QCoreApplication.setOrganizationName(str(org))
        appn = getattr(themeEngine, "applicationName", "")
        if appn:
            QCoreApplication.setApplicationName(str(appn))
        orgd = getattr(themeEngine, "organizationDomain", "")
        if orgd:
            QCoreApplication.setOrganizationDomain(str(orgd))
        s = QSettings()
        init_set = s.value("INIT-THEME-SET")
        if s.value("THEME") is None or not init_set:
            for t in themeEngine.themes:
                if getattr(t, "defaultTheme", False) and (init_set is None or not init_set):
                    s.setValue("THEME", t.name)
                    s.setValue("INIT-THEME-SET", True)
        if s.value("THEME") is None:
            # A stray QSettings file (written before QApplication got its real
            # names) strips every theme's default flag — seed explicitly.
            s.setValue("THEME", "Graphite")
            s.setValue("INIT-THEME-SET", True)
        s.setValue("THEMES-LIST", themeEngine.themes)
        themeEngine.reloadJsonStyles(update=False)
        themeEngine.applyCompiledSass(generateIcons=False, paintEntireApp=True)

        from Custom_Widgets.AppControl import maybe_start_app_control
        try:
            maybe_start_app_control()
        except Exception:
            pass

        self._seed_table()
        self._wire()

    def _seed_table(self):
        table = self.ui.table
        table.setColumns([
            DataTableColumn("id", "ID", type="number", width=60),
            DataTableColumn("name", "Product", type="text"),
            DataTableColumn("category", "Category", type="text"),
            DataTableColumn("price", "Price", type="number",
                            formatter=lambda v: "$%.2f" % v),
            DataTableColumn("in_stock", "In stock", type="bool"),
        ])
        table.setData(SAMPLE_ROWS)
        table.pageSize = 12          # enable pagination

        # Row separators are painted by the delegate (not QSS) — hue comes
        # from the ChartPalette section of style.json so it flips with theme.
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "json-styles", "style.json")) as f:
            chartPalette = json.load(f).get("ChartPalette", {})
        theme = str(QSettings().value("THEME") or "")
        separator = chartPalette.get(theme, {}).get("rowSeparator")
        if separator:
            table.setRowSeparatorColor(separator)

    def _wire(self):
        ui = self.ui
        ui.searchEdit.textChanged.connect(ui.table.setFilterText)
        ui.table.rowSelected.connect(self._onRowSelected)
        ui.table.cellClicked.connect(self._onCellClicked)
        ui.table.pageChanged.connect(
            lambda p: self.statusBar().showMessage(
                "Page %d of %d" % (p + 1, ui.table.pageCount())))

    def _onRowSelected(self, source_row):
        row = SAMPLE_ROWS[source_row]
        self.ui.statusLabel.setText("Selected: #%d  %s  (%s)" %
                                    (row["id"], row["name"], row["category"]))

    def _onCellClicked(self, source_row, column):
        self.ui.statusLabel.setText("Clicked row %d, column %d -> %r" %
                                    (source_row, column,
                                     SAMPLE_ROWS[source_row]["name"]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
