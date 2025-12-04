# 📊 Dashboard Analisis Penjualan Produk - Dokumentasi Lengkap

## Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Persyaratan File CSV](#persyaratan-file-csv)
3. [Cara Menggunakan Dashboard](#cara-menggunakan-dashboard)
4. [Penjelasan Analisis](#penjelasan-analisis)
5. [Interpretasi Hasil](#interpretasi-hasil)
6. [Panduan Instalasi Lokal](#panduan-instalasi-lokal)

---

## Pengenalan

**Dashboard Analisis Penjualan Produk** adalah aplikasi web interaktif yang membantu Anda menganalisis data penjualan tahunan dengan segmentasi produk otomatis menggunakan algoritma **K-Means Clustering**. Aplikasi ini dirancang dengan antarmuka yang ramah pengguna dan menggunakan **Bahasa Indonesia** serta **Mata Uang Rupiah** untuk kemudahan penggunaan di Indonesia.

### Fitur Utama:
- **Upload File CSV**: Unggah data penjualan tahunan Anda dengan mudah.
- **Pembersihan Data Otomatis**: Menghapus nilai yang hilang, harga negatif, dan outlier.
- **Segmentasi Produk**: Mengelompokkan produk ke dalam 4 kategori berdasarkan performa penjualan.
- **Visualisasi Interaktif**: Melihat hasil clustering melalui grafik yang mudah dipahami.
- **Laporan Top 5 Produk**: Menampilkan produk terbaik di setiap cluster.
- **Export Hasil**: Mengunduh hasil analisis dalam format CSV atau Excel.

---

## Persyaratan File CSV

File CSV yang Anda unggah **harus memiliki kolom-kolom berikut** dengan nama yang tepat:

| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `Item Name` | Teks | Nama produk atau item yang dijual |
| `Qty` | Angka | Jumlah kuantitas yang terjual (harus > 0) |
| `Price` | Angka | Harga satuan produk dalam Rupiah (harus > 0) |
| `Amount Price Item` | Angka | Total pendapatan dari item (Qty × Price, harus > 0) |
| `Invoice Number` | Teks/Angka | Nomor transaksi atau faktur (digunakan untuk menghitung frekuensi penjualan) |

### Contoh Format CSV:

```csv
Item Name,Qty,Price,Amount Price Item,Invoice Number
Laptop Dell XPS 13,2,15000000,30000000,INV-001
Mouse Logitech MX,5,500000,2500000,INV-001
Keyboard Mechanical,3,1200000,3600000,INV-002
Monitor LG 27",1,3500000,3500000,INV-002
Laptop Dell XPS 13,1,15000000,15000000,INV-003
```

### Catatan Penting:
- Semua kolom **wajib ada** dan harus menggunakan nama yang **tepat sama** (case-sensitive).
- Nilai pada kolom `Qty`, `Price`, dan `Amount Price Item` **harus positif** (> 0).
- Jangan ada baris kosong di tengah data.
- Gunakan pemisah koma (`,`) untuk CSV.

---

## Cara Menggunakan Dashboard

### Langkah 1: Akses Dashboard
Buka URL dashboard di browser Anda:
```
https://8501-io2u6rlujhanw9bxr0q4x-d4a31053.manus-asia.computer
```

### Langkah 2: Unggah File CSV
1. Klik tombol **"1. Unggah File CSV Penjualan"** di sidebar sebelah kiri.
2. Pilih file CSV yang berisi data penjualan tahunan Anda.
3. Tunggu hingga file berhasil diunggah (akan muncul pesan "File berhasil diunggah!").

### Langkah 3: Lihat Pratinjau Data
Setelah file diunggah, dashboard akan menampilkan **5 baris pertama** dari data Anda untuk verifikasi.

### Langkah 4: Proses Analisis Otomatis
Dashboard akan secara otomatis melakukan:
- **Pembersihan Data**: Menghapus nilai yang hilang, harga 0, dan outlier.
- **Rekayasa Fitur**: Menghitung metrik penting seperti total penjualan, frekuensi, dan rata-rata revenue.
- **Transformasi Logaritmik**: Menstabilkan varians data untuk clustering yang lebih baik.
- **Segmentasi K-Means**: Mengelompokkan produk ke dalam cluster.

### Langkah 5: Sesuaikan Jumlah Cluster (Opsional)
Anda dapat mengubah jumlah cluster (K) menggunakan slider **"Pilih Jumlah Cluster (K)"** untuk melihat hasil dengan jumlah cluster yang berbeda. Nilai default adalah **4 cluster**.

### Langkah 6: Analisis Hasil
Dashboard akan menampilkan:
- **Grafik Elbow Method**: Membantu menentukan jumlah cluster optimal.
- **Skor Silhouette**: Mengukur kualitas clustering.
- **Ringkasan Cluster**: Rata-rata metrik untuk setiap cluster.
- **Visualisasi Scatter Plot**: Menampilkan distribusi produk di setiap cluster.
- **Pie Chart**: Menunjukkan persentase produk di setiap cluster.
- **Top 5 Produk**: Produk dengan revenue tertinggi di setiap cluster.

### Langkah 7: Unduh Hasil
Klik tombol **"Unduh Hasil Analisis (CSV)"** atau **"Unduh Hasil Analisis (Excel)"** untuk menyimpan hasil analisis ke komputer Anda.

---

## Penjelasan Analisis

### 1. Pembersihan Data (Data Cleaning)
Dashboard menghapus:
- **Baris dengan nilai yang hilang** pada kolom Item Name, Qty, atau Amount Price Item.
- **Data dengan harga/jumlah negatif atau nol** karena tidak valid untuk analisis penjualan.
- **Outlier** menggunakan metode **Interquartile Range (IQR)** untuk menghapus nilai ekstrem yang mungkin merupakan kesalahan data.

### 2. Rekayasa Fitur (Feature Engineering)
Dashboard menghitung metrik penting untuk setiap produk:

| Metrik | Rumus | Penjelasan |
|--------|-------|-----------|
| **Total Quantity** | SUM(Qty) | Total kuantitas produk yang terjual sepanjang tahun |
| **Total Revenue** | SUM(Amount Price Item) | Total pendapatan dari produk tersebut dalam Rupiah |
| **Sales Frequency** | COUNT(Invoice Number) | Berapa kali produk muncul di transaksi yang berbeda |
| **Avg Revenue Per Transaction** | Total Revenue / Sales Frequency | Rata-rata pendapatan per transaksi |
| **Revenue Share** | Total Revenue / Total Revenue Semua Produk | Persentase kontribusi produk terhadap total pendapatan |

### 3. Transformasi Logaritmik
Dashboard menerapkan transformasi logaritmik pada metrik numerik:
- **Total Revenue Log** = log(1 + Total Revenue)
- **Total Quantity Log** = log(1 + Total Quantity)
- **Avg Revenue Log** = log(1 + Avg Revenue Per Transaction)

Transformasi ini membantu **menstabilkan varians** dan membuat distribusi data lebih normal, sehingga clustering lebih akurat.

### 4. Standardisasi Data (Scaling)
Sebelum clustering, semua fitur distandardisasi menggunakan **StandardScaler** sehingga setiap fitur memiliki mean = 0 dan standard deviation = 1. Ini penting karena K-Means sensitif terhadap skala data.

### 5. K-Means Clustering
Dashboard menggunakan **K-Means Clustering** untuk mengelompokkan produk berdasarkan performa penjualan:
- **Elbow Method**: Menentukan jumlah cluster optimal dengan melihat "siku" pada grafik inertia.
- **Silhouette Score**: Mengukur seberapa baik setiap data point cocok dengan clusternya (nilai 0-1, semakin tinggi semakin baik).
- **Default K = 4**: Dashboard menggunakan 4 cluster secara default, yang mewakili kategori performa: Top Performer, High Performer, Medium Performer, dan Low Performer.

---

## Interpretasi Hasil

### Kategori Cluster
Setelah clustering, produk diklasifikasikan ke dalam 4 kategori berdasarkan performa penjualan:

| Kategori | Karakteristik | Strategi |
|----------|---------------|----------|
| **Top Performer** | Revenue tertinggi, frekuensi penjualan tinggi, rata-rata revenue per transaksi tinggi | Pertahankan stok, tingkatkan promosi, pertimbangkan ekspansi |
| **High Performer** | Revenue tinggi, frekuensi penjualan sedang, performa stabil | Jaga ketersediaan, monitor kompetitor, pertahankan kualitas |
| **Medium Performer** | Revenue sedang, frekuensi penjualan rendah hingga sedang | Analisis pasar, pertimbangkan bundling, promosi targeted |
| **Low Performer** | Revenue rendah, frekuensi penjualan rendah, potensi improvement | Evaluasi demand, pertimbangkan diskon, atau discontinue |

### Membaca Grafik

**Elbow Method**: Cari titik "siku" pada grafik. Jumlah cluster di titik tersebut adalah optimal. Jika tidak ada siku yang jelas, gunakan Silhouette Score sebagai panduan.

**Silhouette Score**: Semakin tinggi skor (mendekati 1), semakin baik clustering. Skor < 0.4 menunjukkan clustering yang lemah.

**Scatter Plot**: Setiap titik mewakili satu produk. Warna berbeda menunjukkan cluster berbeda. Produk yang berjauhan dari cluster lain menunjukkan karakteristik unik.

**Pie Chart**: Menunjukkan persentase produk di setiap cluster. Jika satu cluster mendominasi, mungkin perlu menyesuaikan jumlah cluster.

---

## Panduan Instalasi Lokal

Jika Anda ingin menjalankan dashboard di komputer lokal Anda:

### Prasyarat:
- **Python 3.8+** (download dari https://www.python.org/)
- **pip** (biasanya sudah termasuk dengan Python)

### Langkah Instalasi:

#### 1. Buat Virtual Environment (Opsional tapi Direkomendasikan)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2. Instal Dependencies
```bash
pip install streamlit pandas numpy scikit-learn matplotlib openpyxl
```

#### 3. Jalankan Aplikasi
```bash
streamlit run app.py
```

#### 4. Akses Dashboard
Dashboard akan otomatis terbuka di browser pada URL:
```
http://localhost:8501
```

### Troubleshooting:

**Masalah**: "Module not found" error
- **Solusi**: Pastikan Anda sudah mengaktifkan virtual environment dan menginstal semua dependencies.

**Masalah**: Port 8501 sudah digunakan
- **Solusi**: Gunakan port lain dengan perintah:
```bash
streamlit run app.py --server.port 8502
```

**Masalah**: Locale Rupiah tidak berfungsi
- **Solusi**: Ini adalah keterbatasan sistem operasi. Aplikasi akan tetap menampilkan format Rupiah sebagai fallback (Rp X.XXX,XX).

---

## Tips & Trik

1. **Persiapkan Data dengan Baik**: Pastikan data CSV sudah bersih sebelum upload. Hapus kolom yang tidak perlu dan pastikan format konsisten.

2. **Gunakan Data Tahunan**: Dashboard dirancang untuk analisis data penjualan tahunan. Jika Anda punya data bulanan, gabungkan terlebih dahulu.

3. **Eksperimen dengan K**: Coba berbagai nilai K (2-10) untuk melihat mana yang paling masuk akal untuk bisnis Anda.

4. **Ekspor Hasil**: Selalu ekspor hasil analisis untuk dokumentasi dan analisis lebih lanjut di Excel atau tools lainnya.

5. **Analisis Mendalam**: Gunakan hasil clustering sebagai dasar untuk analisis lebih mendalam, seperti:
   - Analisis margin keuntungan per cluster
   - Analisis tren penjualan per cluster
   - Analisis kompetitor untuk produk di cluster tertentu

---

## Dukungan & Feedback

Jika Anda mengalami masalah atau memiliki saran untuk improvement, silakan hubungi tim pengembang atau buat issue di repository proyek ini.

---

**Selamat menggunakan Dashboard Analisis Penjualan Produk!** 🚀

Semoga aplikasi ini membantu Anda membuat keputusan bisnis yang lebih baik berdasarkan data yang akurat dan analisis yang mendalam.
