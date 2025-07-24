from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from PyQt5.QtGui import QDoubleValidator, QIntValidator

class ProductDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Yeni Ürün Ekle")
        self.setFixedSize(300, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.barcode_input = QLineEdit()
        form_layout.addRow("Barkod No:", self.barcode_input)

        self.name_input = QLineEdit()
        form_layout.addRow("Ürün Adı:", self.name_input)

        self.category_input = QLineEdit()
        form_layout.addRow("Kategori:", self.category_input)

        self.stock_input = QLineEdit()
        self.stock_input.setValidator(QIntValidator(0, 99999))
        form_layout.addRow("Stok Miktarı:", self.stock_input)

        self.critical_stock_input = QLineEdit()
        self.critical_stock_input.setValidator(QIntValidator(0, 99999))
        form_layout.addRow("Kritik Stok:", self.critical_stock_input)

        self.unit_input = QLineEdit()
        form_layout.addRow("Birim:", self.unit_input)

        self.price_input = QLineEdit()
        self.price_input.setValidator(QDoubleValidator(0.0, 99999.99, 2))
        form_layout.addRow("Satış Fiyatı:", self.price_input)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_product)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def save_product(self):
        barcode = self.barcode_input.text().strip()
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        stock = self.stock_input.text().strip()
        critical_stock = self.critical_stock_input.text().strip()
        unit = self.unit_input.text().strip()
        price = self.price_input.text().strip()

        if not barcode or not name or not category or not stock or not critical_stock or not unit or not price:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurunuz.")
            return

        try:
            self.db_manager.add_product(
                barcode, name, category, int(stock), int(critical_stock), unit, float(price)
            )
            QMessageBox.information(self, "Başarılı", "Ürün başarıyla eklendi.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ürün eklenirken hata oluştu:\n{str(e)}")
