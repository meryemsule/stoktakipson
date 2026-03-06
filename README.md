# 📦 Inventory Management System (Python & PyQt)

Bu proje, bir kurumda kullanılan ürünlerin stok durumunu takip etmek amacıyla geliştirilmiş **masaüstü stok takip uygulamasıdır**.

Uygulama **Python**, **PyQt** ve **SQLite veritabanı** kullanılarak geliştirilmiştir.  
Sistem; ürün ekleme, stok miktarı görüntüleme ve kritik stok seviyelerini takip etmeyi sağlar.

---

# 🚀 Features

- 📦 Ürün ekleme
- 🔎 Ürün listeleme
- ⚠️ Kritik stok takibi
- 🏷 Barkod numarası ile ürün yönetimi
- 💾 Yerel veritabanı (SQLite)

---

# 🛠 Tech Stack

| Teknoloji | Açıklama |
|-----------|----------|
| Python | Ana programlama dili |
| PyQt | Masaüstü arayüz geliştirme |
| SQLite | Yerel veritabanı |
| sqlite3 | Python SQLite veritabanı kütüphanesi |

---

# 📂 Database Structure

Uygulama **SQLite** veritabanı kullanmaktadır.

### Products Table

| Alan | Açıklama |
|-----|----------|
| id | Ürün ID |
| barkod_no | Barkod numarası |
| urun_adi | Ürün adı |
| kategori | Ürün kategorisi |
| stok_miktari | Mevcut stok |
| kritik_stok | Kritik stok seviyesi |
| birim | Ürün birimi |
| alis_fiyat | Alış fiyatı |

---

# 📂 Project Structure

stok-takip-sistemi
│
├── database.py
├── main.py
├── ui
│ └── interface files
│
└── stoktakip.db


---

# 🚦 Installation

Projeyi çalıştırmak için:

### 1️⃣ Repoyu klonlayın

git clone https://github.com/kullaniciadi/stok-takip-sistemi.git


### 2️⃣ Gerekli kütüphaneleri yükleyin

pip install PyQt5


### 3️⃣ Uygulamayı çalıştırın

python main.py


---

# 📝 Notes

- Veriler **SQLite veritabanında (stoktakip.db)** saklanmaktadır.
- Veritabanı ilk çalıştırmada otomatik olarak oluşturulur.
- Kritik stok seviyesine düşen ürünler sistem tarafından tespit edilebilir.

---
