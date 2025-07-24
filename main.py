from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from product_dialog import ProductDialog
from database_manager import DatabaseManager
import sys

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Stok Takip Sistemi")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Ürün Adı", "Kategori", "Stok Miktarı", "Satış Fiyatı"])
        layout.addWidget(self.table)

        self.add_product_button = QPushButton("Yeni Ürün Ekle")
        self.add_product_button.clicked.connect(self.open_add_product_dialog)
        layout.addWidget(self.add_product_button)

        central_widget.setLayout(layout)
        self.load_products()

    def load_products(self):
        try:
            products = self.db_manager.get_products()
            self.table.setRowCount(len(products))
            for row_idx, product in enumerate(products):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(product[0])))  # urun_adi
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(product[1])))  # kategori
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(product[2])))  # stok_miktari
                self.table.setItem(row_idx, 3, QTableWidgetItem(f"{float(product[3]):.2f}"))  # satis_fiyat
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürünler yüklenirken hata oluştu:\n{str(e)}")

    def open_add_product_dialog(self):
        dialog = ProductDialog(self.db_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    main_window = MainWindow(db_manager)
    main_window.show()
    sys.exit(app.exec_())
