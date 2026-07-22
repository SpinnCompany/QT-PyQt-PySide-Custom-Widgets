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

        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #f4f5f7; }
            QLineEdit {
                padding: 6px 10px; border: 1px solid #d0d3d9;
                border-radius: 6px; background: #ffffff;
            }
            QTableView {
                border: 1px solid #d0d3d9; border-radius: 6px;
                background: #ffffff; gridline-color: #e6e8eb;
                selection-background-color: #2563eb; selection-color: #ffffff;
            }
            QHeaderView::section {
                background: #eef0f3; padding: 6px; border: none;
                border-bottom: 1px solid #d0d3d9; font-weight: 600;
            }
            QPushButton {
                background: #2563eb; color: white; border: none;
                padding: 6px 14px; border-radius: 6px;
            }
            QPushButton:disabled { background: #b9c4da; }
            QLabel { color: #333; }
        """)

    def _onRowSelected(self, source_row):
        row = SAMPLE_ROWS[source_row]
        self.status.setText("Selected: #%d  %s  (%s)" %
                            (row["id"], row["name"], row["category"]))

    def _onCellClicked(self, source_row, column):
        self.status.setText("Clicked row %d, column %d -> %r" %
                            (source_row, column, SAMPLE_ROWS[source_row]["name"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(680, 460)
    window.show()
    sys.exit(app.exec())
