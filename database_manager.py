import sqlite3

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("stoktakip.db")
            self.cursor = self.conn.cursor()
            self.create_tables_if_not_exists()
        except sqlite3.Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")
            self.conn = None

    def create_tables_if_not_exists(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barkod_no TEXT,
            urun_adi TEXT,
            kategori TEXT,
            stok_miktari INTEGER,
            kritik_stok INTEGER,
            birim TEXT,
            alis_fiyat REAL
        )
        """)
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT id, barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat FROM Products")
        return self.cursor.fetchall()

    def add_product(self, barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat):
        try:
            self.cursor.execute(
                "INSERT INTO Products (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, alis_fiyat)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ürün eklenirken hata oluştu: {e}")
            raise
