
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# ---------- Pengaturan halaman ----------
st.set_page_config(
    page_title="Dashboard Penjualan - Sherly Saskia Rani",
    page_icon="📊",
    layout="wide",
)

# ---------- Palet warna ----------
WARNA = [
    "#00C2A8", "#4EA8DE", "#FFB703",
    "#FB5607", "#B388EB", "#8AC926", "#FF70A6"
]
WARNA_UTAMA = "#00C2A8"
WARNA_SOROT = "#FFB703"
TEKS = "#E8EEF7"


# ---------- Fungsi tampilan grafik ----------
def gaya(fig, tinggi=360):
    fig.update_layout(
        height=tinggi,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEKS),
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        automargin=True
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        automargin=True
    )
    return fig


# ---------- CSS dashboard ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1426;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 20, 38, 0);
    }

    [data-testid="stSidebar"] {
        background-color: #14213D;
    }

    .block-container {
        padding-top: 2.5rem;
    }

    h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stWidgetLabel"] *,
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"] *,
    [data-testid="stExpander"] summary * {
        color: #E8EEF7 !important;
    }

    [data-testid="stCaptionContainer"] * {
        color: #A9B8D0 !important;
    }

    hr {
        border-color: #2B3A5C !important;
    }

    div[data-testid="stMetric"] {
        background-color: #14213D;
        border-left: 5px solid #00C2A8;
        padding: 12px 16px;
        border-radius: 8px;
    }

    [data-testid="stAlert"] {
        background-color: #14213D;
        border-left: 4px solid #FFB703;
        border-radius: 6px;
    }

    [data-testid="stMultiSelect"] .react-aria-ComboBox > [role="group"],
    [data-testid="stDateInputField"] {
        background-color: #0B1426 !important;
        border: 1px solid #2B3A5C !important;
    }

    [data-testid="stMultiSelect"] input,
    [data-testid="stDateInputField"] * {
        color: #E8EEF7 !important;
        -webkit-text-fill-color: #E8EEF7 !important;
    }

    [data-testid="stMultiSelect"] [role="group"] svg,
    [data-testid="stDateInputField"] svg {
        fill: #E8EEF7 !important;
    }

    [data-testid="stMultiSelect"] [data-tag] {
        background-color: #00C2A8 !important;
    }

    [data-testid="stMultiSelect"] [data-tag] * {
        color: #0B1426 !important;
        -webkit-text-fill-color: #0B1426 !important;
    }

    [data-testid="stMultiSelect"] [data-tag] svg {
        fill: #0B1426 !important;
    }

    [data-testid="stExpander"] {
        background-color: #14213D;
        border: 1px solid #2B3A5C;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Muat data ----------
@st.cache_data
def muat_data():

    # Mengambil lokasi folder utama aplikasi
    folder_proyek = Path(__file__).resolve().parent

    # Dua kemungkinan lokasi dataset
    lokasi_file = [
        folder_proyek / "sales_clean.csv",
        folder_proyek / "data" / "clean" / "sales_clean.csv"
    ]

    # Mencari file yang tersedia
    file_data = next(
        (file for file in lokasi_file if file.is_file()),
        None
    )

    # Jika file tidak ditemukan
    if file_data is None:
        raise FileNotFoundError(
            "File sales_clean.csv tidak ditemukan. "
            "Pastikan file sudah diunggah ke GitHub "
            "pada folder utama atau data/clean/."
        )

    # Membaca dataset
    df = pd.read_csv(file_data)

    # Memastikan kolom tanggal tersedia
    kolom_wajib = [
        "orderdate", "sales", "ordernumber",
        "quantityordered", "territory",
        "productline", "dealsize", "country"
    ]

    kolom_hilang = [
        kolom for kolom in kolom_wajib
        if kolom not in df.columns
    ]

    if kolom_hilang:
        raise ValueError(
            f"Kolom berikut tidak ditemukan dalam dataset: {kolom_hilang}"
        )

    # Mengubah format tanggal
    df["orderdate"] = pd.to_datetime(
        df["orderdate"], errors="coerce"
    )

    # Menghapus tanggal yang tidak valid
    df = df.dropna(subset=["orderdate"])

    # Membuat year_month jika belum tersedia
    if "year_month" not in df.columns:
        df["year_month"] = df["orderdate"].dt.to_period("M").dt.to_timestamp()
    else:
        df["year_month"] = pd.to_datetime(
            df["year_month"], errors="coerce"
        )

    # Membuat kolom tahun dan bulan jika belum tersedia
    if "year" not in df.columns:
        df["year"] = df["orderdate"].dt.year

    if "month" not in df.columns:
        df["month"] = df["orderdate"].dt.month

    # Memastikan kolom angka memiliki format numerik
    kolom_angka = [
        "sales", "ordernumber", "quantityordered",
        "year", "month"
    ]

    for kolom in kolom_angka:
        if kolom in df.columns:
            df[kolom] = pd.to_numeric(
                df[kolom], errors="coerce"
            )

    # Menghapus baris yang tidak memiliki nilai penjualan
    df = df.dropna(subset=["sales"])

    return df


# Menjalankan fungsi pemuatan data
try:
    df = muat_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()


# ---------- Sidebar: filter ----------
st.sidebar.header("Filter Data")

tgl_min = df["orderdate"].min().date()
tgl_maks = df["orderdate"].max().date()

rentang = st.sidebar.date_input(
    "Rentang tanggal order",
    value=(tgl_min, tgl_maks),
    min_value=tgl_min,
    max_value=tgl_maks,
)

wilayah = st.sidebar.multiselect(
    "Wilayah (territory)",
    options=sorted(df["territory"].dropna().unique()),
    default=sorted(df["territory"].dropna().unique()),
)

produk = st.sidebar.multiselect(
    "Lini produk",
    options=sorted(df["productline"].dropna().unique()),
    default=sorted(df["productline"].dropna().unique()),
)

ukuran = st.sidebar.multiselect(
    "Ukuran transaksi (deal size)",
    options=["Small", "Medium", "Large"],
    default=["Small", "Medium", "Large"],
)


# ---------- Pengolahan filter ----------
if isinstance(rentang, (tuple, list)) and len(rentang) == 2:
    awal, akhir = rentang
else:
    awal, akhir = tgl_min, tgl_maks

data = df[
    (df["orderdate"].dt.date >= awal)
    & (df["orderdate"].dt.date <= akhir)
    & (df["territory"].isin(wilayah))
    & (df["productline"].isin(produk))
    & (df["dealsize"].isin(ukuran))
].copy()


# ---------- Judul dashboard ----------
st.title(
    "Dashboard Penjualan: Sample Sales Data"
    "_Sherly Saskia Rani_241051002"
)

st.caption(
    "Sumber data: Kaggle, Sample Sales Data (kyanyoga). "
    "Nilai penjualan diasumsikan dalam USD. "
    "Gunakan filter di sebelah kiri untuk mengubah seluruh grafik."
)

if data.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter ini. "
        "Coba perluas rentang tanggal atau pilihan filter."
    )
    st.stop()


# ---------- KPI ----------
total_sales = data["sales"].sum()
jumlah_order = data["ordernumber"].nunique()

rata_order = (
    total_sales / jumlah_order
    if jumlah_order > 0 else 0
)

total_qty = data["quantityordered"].sum()
jumlah_data = len(data)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Total Penjualan",
    f"${total_sales / 1_000_000:,.2f}M",
    help=f"${total_sales:,.0f}"
)

k2.metric(
    "Jumlah Order",
    f"{jumlah_order:,}"
)

k3.metric(
    "Rata-rata Nilai per Order",
    f"${rata_order:,.0f}"
)

k4.metric(
    "Total Unit Terjual",
    f"{total_qty:,.0f}"
)

k5.metric(
    "Jumlah Data",
    f"{jumlah_data:,}"
)

st.divider()

# ---------- Baris 1: Tren dan lini produk ----------
c1, c2 = st.columns([3, 2])

with c1:
    st.subheader("Tren penjualan bulanan")

    tren = (
        data.groupby("year_month", as_index=False)["sales"]
        .sum()
        .sort_values("year_month")
    )

    fig = px.line(
        tren,
        x="year_month",
        y="sales",
        markers=True
    )

    fig.update_traces(line_color=WARNA_UTAMA)

    fig.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Penjualan (USD)"
    )

    gaya(fig, 360)
    st.plotly_chart(fig, width="stretch", theme=None)


with c2:
    st.subheader("Penjualan per lini produk")

    prod = (
        data.groupby("productline", as_index=False)["sales"]
        .sum()
        .sort_values("sales")
    )

    fig = px.bar(
        prod,
        x="sales",
        y="productline",
        orientation="h"
    )

    fig.update_traces(marker_color=WARNA_UTAMA)

    fig.update_layout(
        xaxis_title="Penjualan (USD)",
        yaxis_title=""
    )

    gaya(fig, 360)
    st.plotly_chart(fig, width="stretch", theme=None)


# ---------- Baris 2: Negara dan proporsi ----------
c3, c4 = st.columns([3, 2])

with c3:
    st.subheader("10 negara dengan penjualan tertinggi")

    neg = (
        data.groupby("country", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        neg,
        x="country",
        y="sales"
    )

    fig.update_traces(marker_color=WARNA_UTAMA)

    fig.update_layout(
        xaxis_title="Negara",
        yaxis_title="Penjualan (USD)"
    )

    gaya(fig, 360)
    st.plotly_chart(fig, width="stretch", theme=None)


with c4:
    st.subheader("Proporsi penjualan per ukuran transaksi")

    uk = (
        data.groupby("dealsize", as_index=False)["sales"]
        .sum()
    )

    fig = px.pie(
        uk,
        names="dealsize",
        values="sales",
        hole=0.5,
        color="dealsize",
        color_discrete_map={
            "Small": WARNA[1],
            "Medium": WARNA[0],
            "Large": WARNA_SOROT
        }
    )

    gaya(fig, 360)
    st.plotly_chart(fig, width="stretch", theme=None)


# ---------- Baris 3: Heatmap dan scatter ----------
c5, c6 = st.columns(2)

with c5:
    st.subheader("Pola musiman: penjualan per bulan dan tahun")

    pivot = data.pivot_table(
        index="year",
        columns="month",
        values="sales",
        aggfunc="sum"
    )

    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="Tealgrn",
        labels={
            "x": "Bulan",
            "y": "Tahun",
            "color": "Penjualan"
        }
    )

    fig.update_yaxes(type="category")
    fig.update_xaxes(dtick=1)

    gaya(fig, 340)
    st.plotly_chart(fig, width="stretch", theme=None)


with c6:
    st.subheader("Jumlah unit vs nilai penjualan")

    fig = px.scatter(
        data,
        x="quantityordered",
        y="sales",
        color="productline",
        color_discrete_sequence=WARNA,
        opacity=0.7,
        hover_data=["country", "dealsize"]
    )

    fig.update_layout(
        xaxis_title="Unit per baris order",
        yaxis_title="Penjualan (USD)",
        legend_title="Lini produk"
    )

    gaya(fig, 340)
    st.plotly_chart(fig, width="stretch", theme=None)


st.divider()


# ---------- Insight utama ----------
st.subheader("Wawasan utama")

top_prod = prod.iloc[-1]
share_prod = (
    top_prod["sales"] / total_sales * 100
    if total_sales > 0 else 0
)

top_neg = neg.iloc[0]
share_neg = (
    top_neg["sales"] / total_sales * 100
    if total_sales > 0 else 0
)

bulan_puncak = tren.loc[tren["sales"].idxmax()]

share_uk = (
    uk.set_index("dealsize")["sales"] / total_sales * 100
    if total_sales > 0
    else uk.set_index("dealsize")["sales"] * 0
)

uk_top = share_uk.idxmax()

i1, i2 = st.columns(2)

with i1:
    st.info(
        f"**Lini produk andalan:** {top_prod['productline']} "
        f"menyumbang {share_prod:.0f}% dari total penjualan "
        "pada filter ini."
    )

    st.info(
        f"**Pasar terbesar:** {top_neg['country']} "
        f"memberi {share_neg:.0f}% dari total penjualan."
    )

with i2:
    st.info(
        f"**Bulan puncak:** "
        f"{bulan_puncak['year_month']:%B %Y} "
        f"dengan penjualan ${bulan_puncak['sales']:,.0f}."
    )

    st.info(
        f"**Ukuran transaksi dominan:** {uk_top} "
        f"({share_uk[uk_top]:.0f}% dari penjualan)."
    )


# ---------- Catatan ----------
st.caption(
    "Catatan: data tahun 2005 hanya sampai Mei, sehingga "
    "total penjualan tahun 2005 tidak bisa dibandingkan "
    "langsung dengan tahun 2003 dan 2004."
)


# ---------- Tabel data ----------
with st.expander("Lihat data (500 baris pertama)"):
    st.dataframe(
        data.head(500),
        width="stretch"
    )
