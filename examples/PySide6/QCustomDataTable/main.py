########################################################################
## QCustomDataTable - basic (free core) example
##
## Demonstrates columns, typed values, client-side filtering, pagination
## and selection signals. Run:
##     python main.py
########################################################################
import sys
from PySide6 import QtCore, QtWidgets

from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
from Custom_Widgets.JSonStyles.tokens import DesignTokens, applyDesignTokens


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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomDataTable Example")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # search box -> live filter
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Filter rows (matches any column)...")
        layout.addWidget(self.search)

        # the table
        self.table = QCustomDataTable()
        self.table.setColumns([
            DataTableColumn("id", "ID", type="number", width=60),
            DataTableColumn("name", "Product", type="text"),
            DataTableColumn("category", "Category", type="text"),
            DataTableColumn("price", "Price", type="number",
                            formatter=lambda v: "$%.2f" % v),
            DataTableColumn("in_stock", "In stock", type="bool"),
        ])
        self.table.setData(SAMPLE_ROWS)
        self.table.pageSize = 12          # enable pagination
        layout.addWidget(self.table)

        # status line reflecting selection / clicks
        self.status = QtWidgets.QLabel("Select a row...")
        layout.addWidget(self.status)

        # wire signals (all indices are source-model rows)
        self.search.textChanged.connect(self.table.setFilterText)
        self.table.rowSelected.connect(self._onRowSelected)
        self.table.cellClicked.connect(self._onCellClicked)
        self.table.pageChanged.connect(
            lambda p: self.statusBar().showMessage("Page %d of %d" %
                                                   (p + 1, self.table.pageCount())))

        # NOTE: the table's own styling (view, header, selection, footer) comes
        # entirely from the design-token system (applied app-wide in __main__).

    def _onRowSelected(self, source_row):
        row = SAMPLE_ROWS[source_row]
        self.status.setText("Selected: #%d  %s  (%s)" %
                            (row["id"], row["name"], row["category"]))

    def _onCellClicked(self, source_row, column):
        self.status.setText("Clicked row %d, column %d -> %r" %
                            (source_row, column, SAMPLE_ROWS[source_row]["name"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # design tokens style the table; add window/line-edit chrome from the
    # same tokens so everything is consistent
    tokens = DesignTokens(theme="light")
    app.setStyleSheet(
        "QMainWindow, QWidget { background-color: %s; color: %s; }\n"
        "QLineEdit { padding: 6px 10px; border: 1px solid %s; border-radius: 6px;"
        " background: %s; }" % (tokens.role("surface"), tokens.role("on-surface"),
                                tokens.role("outline"), tokens.role("surface")))
    applyDesignTokens(app, tokens=tokens)

    window = MainWindow()
    window.resize(680, 460)
    window.show()
    sys.exit(app.exec())
