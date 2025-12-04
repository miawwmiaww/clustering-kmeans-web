# 📊 Dashboard Analisis Penjualan Produk

Aplikasi web interaktif untuk menganalisis data penjualan tahunan dengan segmentasi produk otomatis menggunakan K-Means Clustering.

## 🚀 Fitur Utama

- ✅ **Upload File CSV**: Unggah data penjualan dengan mudah
- ✅ **Pembersihan Data Otomatis**: Menghapus nilai yang hilang, harga negatif, dan outlier
- ✅ **Segmentasi Produk**: Mengelompokkan produk ke dalam 4 kategori performa
- ✅ **Visualisasi Interaktif**: Grafik yang mudah dipahami dan informatif
- ✅ **Laporan Top 5 Produk**: Produk terbaik di setiap cluster
- ✅ **Export Hasil**: Unduh hasil dalam format CSV atau Excel
- ✅ **Bahasa Indonesia & Rupiah**: Interface dan format mata uang lokal

## 📋 Persyaratan File CSV

File CSV harus memiliki kolom berikut:
- `Item Name` - Nama produk
- `Qty` - Jumlah kuantitas terjual
- `Price` - Harga satuan (Rupiah)
- `Amount Price Item` - Total pendapatan item
- `Invoice Number` - Nomor transaksi

Lihat `contoh_data_penjualan.csv` untuk format yang benar.

## 🔧 Instalasi & Menjalankan

### Menggunakan Virtual Environment (Direkomendasikan)

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Instal dependencies
pip install streamlit pandas numpy scikit-learn matplotlib openpyxl

# 4. Jalankan aplikasi
streamlit run app.py
```

Dashboard akan terbuka di `http://localhost:8501`

### Tanpa Virtual Environment

```bash
pip install streamlit pandas numpy scikit-learn matplotlib openpyxl
streamlit run app.py
```

## 📁 Struktur File

```
.
├── app.py                          # Aplikasi Streamlit utama
├── contoh_data_penjualan.csv       # File CSV contoh untuk testing
├── DOKUMENTASI.md                  # Dokumentasi lengkap
├── README.md                       # File ini
└── requirements.txt                # Daftar dependencies (opsional)
```

## 📖 Dokumentasi

Untuk dokumentasi lengkap, cara penggunaan, dan penjelasan analisis, baca file **DOKUMENTASI.md**.

## 🎯 Cara Menggunakan

1. **Upload File CSV**: Klik tombol upload di sidebar dan pilih file CSV Anda
2. **Lihat Pratinjau**: Dashboard menampilkan 5 baris pertama data
3. **Proses Otomatis**: Analisis data dilakukan secara otomatis
4. **Sesuaikan K**: Gunakan slider untuk mengubah jumlah cluster (opsional)
5. **Analisis Hasil**: Lihat grafik, tabel, dan interpretasi hasil
6. **Unduh Hasil**: Ekspor hasil analisis dalam format CSV atau Excel

## 📊 Metodologi Analisis

1. **Data Cleaning**: Menghapus nilai yang hilang, harga negatif, dan outlier
2. **Feature Engineering**: Menghitung metrik penjualan penting
3. **Log Transformation**: Menstabilkan varians data
4. **Standardisasi**: Scaling fitur untuk clustering
5. **K-Means Clustering**: Segmentasi produk berdasarkan performa
6. **Interpretasi**: Labeling cluster dan analisis hasil

## 🏆 Kategori Cluster

- **Top Performer**: Revenue tertinggi, frekuensi tinggi
- **High Performer**: Revenue tinggi, performa stabil
- **Medium Performer**: Revenue sedang, potensi improvement
- **Low Performer**: Revenue rendah, perlu evaluasi

## ⚙️ Teknologi yang Digunakan

- **Streamlit**: Framework web interaktif
- **Pandas**: Manipulasi dan analisis data
- **NumPy**: Komputasi numerik
- **Scikit-learn**: Machine learning (K-Means, StandardScaler)
- **Matplotlib**: Visualisasi data

## 📝 Lisensi

Proyek ini tersedia untuk penggunaan pribadi dan komersial.

## 💬 Support

Jika Anda mengalami masalah atau memiliki pertanyaan, silakan buat issue atau hubungi tim pengembang.

---

**Selamat menggunakan Dashboard Analisis Penjualan Produk!** 🎉
