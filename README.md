# UJIAN TENGAH SEMESTER (UTS)
# VISUALISASI DATA PENJUALAN

**Nama:** Sherly Saskia Rani  
**NIM:** 241051002
Link Demo: https://dashboard-uts-sherly.streamlit.app/ 

## Deskripsi Proyek

Proyek ini merupakan tugas Ujian Tengah Semester (UTS) mata kuliah Visualisasi Data. Proyek ini bertujuan untuk menganalisis dan memvisualisasikan data penjualan menggunakan Python melalui dashboard interaktif berbasis Streamlit.

Dataset yang digunakan adalah Sample Sales Data dari Kaggle. Data diolah untuk menghasilkan informasi mengenai pola dan tren penjualan berdasarkan beberapa kategori.

## Tujuan Visualisasi

- Mengetahui tren penjualan berdasarkan periode waktu.
- Menganalisis penjualan berdasarkan lini produk.
- Mengidentifikasi negara dengan penjualan tertinggi.
- Mengetahui proporsi penjualan berdasarkan ukuran transaksi.
- Menampilkan hubungan antara jumlah unit dan nilai penjualan.

## Fitur Dashboard

1. Total penjualan.
2. Jumlah order.
3. Rata-rata nilai per order.
4. Total unit terjual.
5. Jumlah data.
6. Grafik tren penjualan bulanan.
7. Grafik penjualan per lini produk.
8. Visualisasi 10 negara dengan penjualan tertinggi.
9. Diagram proporsi ukuran transaksi.
10. Heatmap pola penjualan berdasarkan bulan dan tahun.
11. Scatter plot jumlah unit terhadap nilai penjualan.
12. Filter tanggal, wilayah, lini produk, dan ukuran transaksi.

## Teknologi yang Digunakan

- Python
- Pandas
- Plotly
- Streamlit
- JupyterLab

## Struktur File

- `app.py` : File utama aplikasi dashboard.
- `clean.py` : File untuk proses pembersihan data.
- `requirements.txt` : Daftar library yang dibutuhkan.
- `sales_data_sample.csv` : Dataset mentah.
- `sales_clean.csv` : Dataset hasil pembersihan.

## Cara Menjalankan Aplikasi

Install library:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
streamlit run app.py
```

## Sumber Dataset

Kaggle - Sample Sales Data (kyanyoga).
