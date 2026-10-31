import pandas as pd

# 1. Baca data mentah
# keep_default_na=False supaya "NA" (North America) tidak dianggap data kosong
df = pd.read_csv(
    "data/raw/sales_data_sample.csv",
    encoding="latin-1",
    keep_default_na=False,
)
print("Baris awal      :", len(df))

# 2. Rapikan nama kolom dan nilai kosong
df.columns = df.columns.str.lower()
df = df.replace("", pd.NA)

# 3. NA = North America, tulis lengkap
df["territory"] = df["territory"].replace({"NA": "North America"})

# 4. Ubah teks tanggal jadi tipe tanggal
df["orderdate"] = pd.to_datetime(df["orderdate"], format="%m/%d/%Y %H:%M")

# 5. Buang kolom yang tidak dipakai
kolom_buang = [
    "phone", "addressline1", "addressline2",
    "contactlastname", "contactfirstname",
    "postalcode", "state", "orderlinenumber",
]
df = df.drop(columns=kolom_buang)

# 6. Tambah kolom bantu untuk grafik
df["year"] = df["orderdate"].dt.year
df["month"] = df["orderdate"].dt.month
df["year_month"] = df["orderdate"].dt.to_period("M").dt.to_timestamp()
df["price_vs_msrp_pct"] = ((df["priceeach"] - df["msrp"]) / df["msrp"] * 100).round(1)

# 7. Validasi
print("Baris akhir     :", len(df))
print("Kolom           :", len(df.columns))
print("Duplikat        :", int(df.duplicated().sum()))
print("Nilai kosong    :", int(df.isna().sum().sum()))
print("Rentang tanggal :", df["orderdate"].min().date(), "s/d", df["orderdate"].max().date())
print()
print(df["territory"].value_counts())

# 8. Simpan
df.to_csv("data/clean/sales_clean.csv", index=False)
print()
print("Tersimpan di data/clean/sales_clean.csv")