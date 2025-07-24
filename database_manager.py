import pyodbc

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=MERI\\SQLEXPRESS;"
                "DATABASE=StokTakipDB;"
                "Trusted_Connection=yes;"
            )
            self.cursor = self.conn.cursor()
            print("[VERİTABANI] Bağlantı başarılı!")
        except pyodbc.Error as e:
            print(f"[VERİTABANI HATASI] Bağlantı hatası: {e}")
            raise

    def get_products(self):
        try:
            query = """
            SELECT id, barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, satis_fiyat
            FROM Products
            """
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            return products
        except pyodbc.Error as e:
            print(f"[VERİTABANI HATASI] Ürünler alınamadı: {e}")
            return []

    def add_product(self, barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, satis_fiyat):
        try:
            query = """
            INSERT INTO Products (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, satis_fiyat)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (barkod_no, urun_adi, kategori, stok_miktari, kritik_stok, birim, satis_fiyat))
            self.conn.commit()
            print("[VERİTABANI] Ürün eklendi.")
        except pyodbc.Error as e:
            print(f"[VERİTABANI HATASI] Ürün eklenemedi: {e}")
            raise
