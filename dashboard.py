import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("main_data.csv")

# Debugging: Pastikan data tidak kosong
if df.empty:
    st.error("Dataset kosong! Pastikan main_data.csv memiliki data yang valid.")
    st.stop()

# Mapping Tahun: Ubah 0 → 2011 dan 1 → 2012
df['year'] = df['yr'].map({0: 2011, 1: 2012})

# Mapping Hari dalam Seminggu
weekday_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
df["weekday_label"] = df["weekday"].map(weekday_mapping)

# Streamlit dashboard
st.set_page_config(page_title="Dashboard Peminjaman Sepeda", layout="wide")
st.title("🚲 **Dashboard Analisis Peminjaman Sepeda**")

# Sidebar filter
st.sidebar.header("📊 **Filter Data**")
selected_year = st.sidebar.radio("Pilih Tahun", df["year"].unique())  # Menampilkan 2011 & 2012
selected_season = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())
selected_weather = st.sidebar.multiselect("Pilih Cuaca", df['weathersit'].unique(), default=df['weathersit'].unique())
selected_month = st.sidebar.slider("Pilih Bulan", min_value=1, max_value=12, value=(1, 12))
selected_weekday = st.sidebar.multiselect("Pilih Hari", df['weekday_label'].unique(), default=df['weekday_label'].unique())
selected_holiday = st.sidebar.radio("Pilih Hari Libur", [0, 1], format_func=lambda x: "Bukan Hari Libur" if x == 0 else "Hari Libur")
selected_workingday = st.sidebar.radio("Pilih Hari Kerja", [0, 1], format_func=lambda x: "Bukan Hari Kerja" if x == 0 else "Hari Kerja")

# Terapkan filter
filtered_df = df[
    (df['year'] == selected_year) &
    (df['season'].isin(selected_season)) &
    (df['weathersit'].isin(selected_weather)) &
    (df['mnth'].between(selected_month[0], selected_month[1])) &
    (df['weekday_label'].isin(selected_weekday)) &
    (df['holiday'] == selected_holiday) &
    (df['workingday'] == selected_workingday)
]

# Tampilkan dataset yang sudah difilter
st.write(f"📌 **Menampilkan Data untuk Tahun {selected_year}, Musim: {', '.join(selected_season)}, Cuaca: {', '.join(selected_weather)}, Bulan: {selected_month[0]} - {selected_month[1]}, Hari: {', '.join(selected_weekday)}**")

if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih. Silakan ubah filter.")
    st.stop()

st.dataframe(filtered_df)

# ======================== STATISTIK RINGKASAN (UPDATE BERDASARKAN FILTER) ========================
st.subheader("📌 **Statistik Ringkasan**")
col1, col2, col3 = st.columns(3)

with col1:
    total_peminjaman = filtered_df['cnt'].sum()
    st.metric("Total Peminjaman Sepeda", f"{total_peminjaman:,}")

with col2:
    rata_rata_harian = filtered_df['cnt'].mean()
    st.metric("Rata-rata Peminjaman Harian", f"{rata_rata_harian:.0f}")

with col3:
    if not filtered_df.empty:
        musim_terbanyak = filtered_df.groupby("season")["cnt"].sum().idxmax()
    else:
        musim_terbanyak = "Tidak ada data"
    st.metric("Musim dengan Peminjaman Terbanyak", musim_terbanyak)

# ======================== VISUALISASI GRAFIK (INTERAKTIF) ========================

# 🔍 Grafik 1: Total Peminjaman per Musim
st.subheader("🔍 **Total Peminjaman Sepeda per Musim**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_df, x="season", y="cnt", estimator=sum, palette="viridis")
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Total Peminjaman", fontsize=12)
plt.title("Total Peminjaman Sepeda per Musim", fontsize=14)
st.pyplot(fig)

st.info("📌 **Insight:** Musim **Fall** memiliki jumlah peminjaman tertinggi, sedangkan **Spring** memiliki jumlah terendah.")

# 🌦 Grafik 2: Pengaruh Cuaca terhadap Peminjaman
st.subheader("🌦 **Pengaruh Cuaca terhadap Peminjaman**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x="weathersit", y="cnt", palette="coolwarm")
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
plt.title("Pengaruh Cuaca terhadap Peminjaman Sepeda", fontsize=14)
st.pyplot(fig)

st.info("📌 **Insight:** Peminjaman sepeda paling tinggi saat cuaca **cerah (Clear)**, sedangkan hujan/salju mengurangi jumlah peminjaman secara drastis.")

# 📅 Grafik 3: Tren Peminjaman Sepeda per Bulan
st.subheader("📅 **Tren Peminjaman Sepeda per Bulan**")

df["mnth"] = pd.Categorical(df["mnth"], categories=range(1, 13), ordered=True)
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="mnth", y="cnt", estimator="sum", ci=None, marker="o", linewidth=2.5, color="dodgerblue")
plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Total Peminjaman", fontsize=12)
plt.title("Tren Peminjaman Sepeda per Bulan", fontsize=14)
st.pyplot(fig)

st.info("📌 **Insight:** Tren peminjaman meningkat saat pertengahan tahun (Mei - Sep) dan menurun saat musim dingin.")

# ======================== KESIMPULAN ========================
st.subheader("📌 **Kesimpulan**")
st.markdown("""
- **Musim Fall memiliki jumlah peminjaman tertinggi**, diikuti oleh Summer.
- **Musim Spring memiliki jumlah peminjaman terendah** karena cuaca yang tidak stabil.
- **Cuaca cerah meningkatkan jumlah peminjaman sepeda**.
- **Hujan atau salju menyebabkan penurunan jumlah peminjaman sepeda** secara drastis.
- **Tren peminjaman per bulan menunjukkan kenaikan saat pertengahan tahun dan penurunan di musim dingin.**
""")
