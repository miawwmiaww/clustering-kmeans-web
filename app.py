import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import io
import locale

# Set locale untuk format mata uang Rupiah
# Coba beberapa locale yang mungkin mendukung Rupiah/Indonesia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'id_ID')
    except locale.Error:
        st.warning("Locale 'id_ID.UTF-8' atau 'id_ID' tidak ditemukan. Format Rupiah mungkin tidak berfungsi.")

# Fungsi untuk format angka menjadi Rupiah
def format_rupiah(amount):
    # Menggunakan format bawaan Python jika locale berhasil diatur
    if 'id_ID' in locale.getlocale()[0]:
        return locale.currency(amount, grouping=True, symbol="Rp")
    # Fallback jika locale gagal
    return f"Rp {amount:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")

# Fungsi utama untuk menjalankan analisis data
def run_analysis(df):
    st.subheader("2. Pembersihan dan Pra-pemrosesan Data")

    # Kolom yang wajib ada
    required_cols = ['Item Name', 'Qty', 'Price', 'Amount Price Item', 'Invoice Number']
    if not all(col in df.columns for col in required_cols):
        st.error(f"File CSV harus memiliki kolom: {', '.join(required_cols)}")
        return None

    # Konversi tipe data
    try:
        df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df['Amount Price Item'] = pd.to_numeric(df['Amount Price Item'], errors='coerce')
    except Exception as e:
        st.error(f"Gagal mengkonversi kolom numerik: {e}")
        return None

    # Hapus baris dengan nilai yang hilang pada kolom kunci
    df.dropna(subset=['Item Name', 'Qty', 'Amount Price Item'], inplace=True)

    # Hapus data dengan harga/jumlah 0 atau negatif
    df = df[(df['Price'] > 0) & (df['Amount Price Item'] > 0) & (df['Qty'] > 0)]
    st.info(f"Jumlah baris setelah pembersihan: {len(df)}")

    # Fungsi untuk menghapus outlier (menggunakan IQR)
    def remove_outliers_iqr(data, column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        low = Q1 - 1.5 * IQR
        high = Q3 + 1.5 * IQR
        return data[(data[column] >= low) & (data[column] <= high)]

    # Hapus outlier pada kolom Price dan Amount Price Item
    df = remove_outliers_iqr(df, 'Price')
    df = remove_outliers_iqr(df, 'Amount Price Item')
    st.info(f"Jumlah baris setelah penghapusan outlier: {len(df)}")

    st.subheader("3. Rekayasa Fitur (Feature Engineering)")

    # Agregasi data per produk (Item Name)
    df_group = df.groupby(['Item Name']).agg({
        'Qty': 'sum',
        'Amount Price Item': 'sum',
        'Invoice Number': 'nunique'
    }).reset_index()

    df_group.rename(columns={
        'Qty': 'Total_Quantity',
        'Amount Price Item': 'Total_Revenue',
        'Invoice Number': 'Sales_Frequency'
    }, inplace=True)

    df_group['Avg_Revenue_Per_Transaction'] = df_group['Total_Revenue'] / df_group['Sales_Frequency']

    # Transformasi Logaritmik (untuk menstabilkan varians)
    df_group['Total_Revenue_Log'] = np.log1p(df_group['Total_Revenue'])
    df_group['Total_Quantity_Log'] = np.log1p(df_group['Total_Quantity'])
    df_group['Avg_Revenue_Log'] = np.log1p(df_group['Avg_Revenue_Per_Transaction'])

    st.dataframe(df_group.head(), use_container_width=True)

    st.subheader("4. Segmentasi Produk dengan K-Means Clustering")

    # Pilih fitur untuk clustering
    features = df_group[['Total_Quantity_Log',
                         'Total_Revenue_Log',
                         'Sales_Frequency',
                         'Avg_Revenue_Log']]

    # Standardisasi data
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    df_scaled = pd.DataFrame(scaled, columns=features.columns)

    # Menentukan jumlah cluster (K)
    K_range = range(2, 11)
    inertia = []
    silhouette_scores = {}

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)
        clusters = kmeans.predict(df_scaled)
        if k > 1:
            silhouette_scores[k] = silhouette_score(df_scaled, clusters)

    # Plot Elbow Method
    fig_elbow, ax_elbow = plt.subplots(figsize=(8, 4))
    ax_elbow.plot(K_range, inertia, marker='o')
    ax_elbow.set_title("Metode Siku (Elbow Method)")
    ax_elbow.set_xlabel("Jumlah Cluster (K)")
    ax_elbow.set_ylabel("Inertia")
    st.pyplot(fig_elbow)

    # Tampilkan Silhouette Scores
    st.write("Skor Silhouette:")
    st.dataframe(pd.Series(silhouette_scores, name="Skor Silhouette").sort_values(ascending=False), use_container_width=True)

    # Asumsi K terbaik adalah 4 (berdasarkan kode asli dan praktik umum)
    best_k = st.slider("Pilih Jumlah Cluster (K)", min_value=2, max_value=10, value=4)

    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df_group['Cluster'] = kmeans.fit_predict(df_scaled)

    st.info(f"Segmentasi berhasil dengan {best_k} cluster.")
    st.dataframe(df_group['Cluster'].value_counts().sort_index().rename("Jumlah Produk"), use_container_width=True)

    st.subheader("5. Interpretasi Hasil Clustering")

    # Hitung rata-rata metrik per cluster
    cluster_summary = df_group.groupby('Cluster').agg({
        'Total_Quantity': 'mean',
        'Total_Revenue': 'mean',
        'Sales_Frequency': 'mean',
        'Avg_Revenue_Per_Transaction': 'mean'
    }).reset_index()

    # Tentukan label cluster (ini bisa disesuaikan berdasarkan hasil)
    # Labeling sederhana berdasarkan Total_Revenue rata-rata
    cluster_summary = cluster_summary.sort_values(by='Total_Revenue', ascending=False).reset_index(drop=True)
    cluster_summary['Label'] = [
        "Top Performer" if i == 0 else
        "High Performer" if i == 1 else
        "Medium Performer" if i == 2 else
        "Low Performer"
        for i in cluster_summary.index
    ]

    # Gabungkan label kembali ke df_group
    label_map = cluster_summary.set_index('Cluster')['Label'].to_dict()
    df_group['Label'] = df_group['Cluster'].map(label_map)

    st.write("Ringkasan Rata-rata Metrik per Cluster:")
    # Format Rupiah untuk Total_Revenue dan Avg_Revenue_Per_Transaction
    summary_display = cluster_summary.copy()
    summary_display['Total_Revenue'] = summary_display['Total_Revenue'].apply(format_rupiah)
    summary_display['Avg_Revenue_Per_Transaction'] = summary_display['Avg_Revenue_Per_Transaction'].apply(format_rupiah)
    st.dataframe(summary_display[['Label', 'Total_Quantity', 'Total_Revenue', 'Sales_Frequency', 'Avg_Revenue_Per_Transaction']], use_container_width=True)

    # Visualisasi Cluster (Scatter Plot)
    fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
    scatter = ax_scatter.scatter(df_group['Total_Revenue_Log'], df_group['Total_Quantity_Log'],
                                 c=df_group['Cluster'], cmap='viridis', alpha=0.6)
    ax_scatter.set_title("Visualisasi Cluster (Log Transform)")
    ax_scatter.set_xlabel("Log(Total Revenue)")
    ax_scatter.set_ylabel("Log(Total Quantity)")
    legend1 = ax_scatter.legend(*scatter.legend_elements(), title="Cluster")
    ax_scatter.add_artist(legend1)
    st.pyplot(fig_scatter)

    # Pie Chart Distribusi Produk per Cluster
    fig_pie, ax_pie = plt.subplots(figsize=(7, 7))
    cluster_counts = df_group['Label'].value_counts()
    ax_pie.pie(cluster_counts,
               labels=cluster_counts.index,
               autopct='%1.1f%%',
               startangle=90)
    ax_pie.set_title("Distribusi Jumlah Produk per Cluster")
    st.pyplot(fig_pie)

    # Tampilkan Top 5 Produk per Cluster
    st.subheader("6. Top 5 Produk per Cluster")
    for cluster_id, label in label_map.items():
        st.markdown(f"#### {label} (Cluster {cluster_id})")
        top5 = df_group[df_group['Cluster'] == cluster_id].sort_values(
            by="Total_Revenue", ascending=False
        ).head(5)

        # Format Rupiah untuk tampilan
        top5_display = top5[['Item Name', 'Total_Quantity', 'Total_Revenue', 'Sales_Frequency']].copy()
        top5_display['Total_Revenue'] = top5_display['Total_Revenue'].apply(format_rupiah)
        st.dataframe(top5_display, use_container_width=True)

        # Bar Chart Revenue Top 5
        fig_bar, ax_bar = plt.subplots(figsize=(10, 4))
        ax_bar.bar(top5["Item Name"], top5["Total_Revenue"])
        ax_bar.set_xticks(top5["Item Name"])
        ax_bar.set_xticklabels(top5["Item Name"], rotation=45, ha='right')
        ax_bar.set_title(f"Top 5 Produk Berdasarkan Revenue - {label}")
        ax_bar.set_xlabel("Nama Item")
        ax_bar.set_ylabel("Total Revenue")
        fig_bar.tight_layout()
        st.pyplot(fig_bar)

    # Sediakan file hasil untuk diunduh
    csv_export = df_group.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Unduh Hasil Analisis (CSV)",
        data=csv_export,
        file_name='hasil_analisis_penjualan.csv',
        mime='text/csv',
    )

    excel_export = io.BytesIO()
    df_group.to_excel(excel_export, index=False, engine='xlsxwriter')
    st.download_button(
        label="Unduh Hasil Analisis (Excel)",
        data=excel_export.getvalue(),
        file_name='hasil_analisis_penjualan.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Penjualan CSV",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard Analisis Penjualan Produk")
st.markdown("Aplikasi ini membantu Anda mengupload data penjualan tahunan (CSV) dan melakukan segmentasi produk menggunakan algoritma K-Means Clustering.")

st.sidebar.header("Pengaturan Data")
uploaded_file = st.sidebar.file_uploader("1. Unggah File CSV Penjualan", type=["csv"])

if uploaded_file is not None:
    try:
        # Baca file CSV
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("File berhasil diunggah!")

        # Tampilkan 5 baris pertama
        st.subheader("1. Pratinjau Data yang Diunggah")
        st.dataframe(df.head(), use_container_width=True)

        # Jalankan analisis
        run_analysis(df)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
        st.info("Pastikan file Anda adalah CSV yang valid dan memiliki kolom yang diperlukan.")

else:
    st.info("Silakan unggah file CSV Anda di sidebar untuk memulai analisis.")
    st.markdown("""
    **Format Kolom yang Diperlukan:**
    - `Item Name`: Nama produk/item.
    - `Qty`: Jumlah kuantitas yang terjual.
    - `Price`: Harga satuan produk.
    - `Amount Price Item`: Total pendapatan dari item tersebut (Qty * Price).
    - `Invoice Number`: Nomor transaksi/faktur (digunakan untuk menghitung frekuensi penjualan).
    """)
