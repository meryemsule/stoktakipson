import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QLabel, QComboBox,
    QHBoxLayout, QHeaderView, QSizePolicy, QSpacerItem, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QFont
from datetime import datetime

from database_manager import DatabaseManager
from product_dialog import ProductDialog  # BURAYA EKLENDİ

class StokTakipMainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()

        if not self.db_manager.conn:
            QMessageBox.critical(self, "Veritabanı Bağlantı Hatası", "Veritabanı bağlantısı kurulamadı.")
            sys.exit(1)

        self.setWindowTitle("PyQt Stok Takip Sistemi")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.init_header()  # <-- Yeni fonksiyon
        self.init_ui()
        self.load_products()

    def init_header(self):
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)

        # Ortada başlıklar
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        valilik_label = QLabel("Yozgat Valiliği")
        valilik_label.setFont(QFont("Arial", 22, QFont.Bold))
        valilik_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(valilik_label)

        stok_label = QLabel("Stok Takip")
        stok_label.setFont(QFont("Arial", 16, QFont.Bold))
        stok_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(stok_label)

        # Ortalamak için önce boşluk, sonra başlıklar, sonra tekrar boşluk ekle
        header_layout.addStretch()
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Logo sağ üstte
        logo_label = QLabel()
        pixmap = QPixmap("Yozgat_Valiliği_logo.png")
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        header_layout.addWidget(logo_label)

        self.main_layout.addLayout(header_layout)

    def init_ui(self):
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Ara:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Barkod, Ürün Adı veya Kategoriye göre ara...")
        self.search_input.textChanged.connect(self.search_products)
        search_layout.addWidget(self.search_input)
        self.main_layout.addLayout(search_layout)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(7)
        self.product_table.setHorizontalHeaderLabels(['ID', 'Barkod No', 'Ürün Adı', 'Kategori', 'Stok Miktarı', 'Kritik Stok', 'Birim'])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.product_table.horizontalHeader().setStretchLastSection(True)
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.main_layout.addWidget(self.product_table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Yeni Ürün Ekle")
        self.add_btn.clicked.connect(self.show_add_edit_product_dialog)
        btn_layout.addWidget(self.add_btn)
        self.main_layout.addLayout(btn_layout)

    def load_products(self):
        try:
            products = self.db_manager.get_products()
            self.product_table.setRowCount(0)
            for row_idx, product_data in enumerate(products):
                self.product_table.insertRow(row_idx)
                for col_idx, data in enumerate(product_data[:7]):  # Sadece ilk 7 sütunu al
                    item = QTableWidgetItem(str(data))
                    if col_idx in [0, 4, 5]:
                        item.setTextAlignment(Qt.AlignCenter)
                    self.product_table.setItem(row_idx, col_idx, item)
            self.product_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Veri Yükleme Hatası", f"Ürünler yüklenirken bir hata oluştu: {e}")

    def search_products(self):
        search_text = self.search_input.text().lower().strip()
        for row_idx in range(self.product_table.rowCount()):
            hidden = True
            for col_idx in [0, 1, 2, 3]:
                item = self.product_table.item(row_idx, col_idx)
                if item and search_text in item.text().lower():
                    hidden = False
                    break
            self.product_table.setRowHidden(row_idx, hidden)

    def get_selected_product_id(self):
        selected_rows = self.product_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ürün seçin.")
            return None
        return int(self.product_table.item(selected_rows[0].row(), 0).text())

    def show_add_edit_product_dialog(self):
        dialog = ProductDialog(self.db_manager, self)  # <-- DÜZELTİLDİ!
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()

    def add_product(self, barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat=0):
        query = """
        INSERT INTO Products (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat))
        self.conn.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StokTakipMainApp()
    main_window.show()
    sys.exit(app.exec_())
