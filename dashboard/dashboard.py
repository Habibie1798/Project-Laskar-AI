import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Bike Sharing",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚲 Dashboard Peminjaman Sepeda")
st.markdown("Analisis Data Bike Sharing di Washington DC (2011–2012)")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {
        1: 'Clear',
        2: 'Cloudy',
        3: 'Light Rain/Snow',
        4: 'Heavy Rain/Snow'
    }

    df['season'] = df['season'].map(season_map)
    df['weathersit'] = df['weathersit'].map(weather_map)

    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🔎 Filter Data")

min_date = df['dteday'].min()
max_date = df['dteday'].max()

start_date = st.sidebar.date_input("Mulai Tanggal", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("Sampai Tanggal", min_value=min_date, max_value=max_date, value=max_date)

seasons = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())
weathers = st.sidebar.multiselect("Pilih Cuaca", df['weathersit'].unique(), default=df['weathersit'].unique())

# Apply filter
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date)) &
    (df['season'].isin(seasons)) &
    (df['weathersit'].isin(weathers))
]

# Statistik Ringkas
st.subheader("📊 Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Hari", len(filtered_df))
col2.metric("Total Peminjaman", int(filtered_df['cnt'].sum()))
col3.metric("Rata-rata Peminjaman", round(filtered_df['cnt'].mean(), 2))

st.markdown("---")

# Visualisasi 1 - Peminjaman per Musim
st.subheader("🌤️ Total Peminjaman per Musim")
fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_df, x='season', y='cnt', estimator=sum, ax=ax1)
ax1.set_title("Total Peminjaman per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Peminjaman")
st.pyplot(fig1)

# Visualisasi 2 - Pengaruh Cuaca
st.subheader("🌦️ Pengaruh Cuaca terhadap Peminjaman")
fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_df, x='weathersit', y='cnt', ax=ax2)
ax2.set_title("Distribusi Jumlah Peminjaman berdasarkan Cuaca")
ax2.set_xlabel("Cuaca")
ax2.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig2)

# Visualisasi 3 - Tren Bulanan
st.subheader("📈 Tren Peminjaman Sepeda Bulanan")
monthly_df = filtered_df.resample('M', on='dteday').agg({'cnt': 'sum'}).reset_index()
monthly_df['label'] = monthly_df['dteday'].dt.strftime('%Y-%b')

fig3, ax3 = plt.subplots(figsize=(10,5))
sns.lineplot(data=monthly_df, x='label', y='cnt', marker='o', ax=ax3)
ax3.set_title("Total Peminjaman per Bulan")
ax3.set_ylabel("Jumlah Peminjaman")
ax3.set_xlabel("Bulan")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Visualisasi 4 - Hari Libur vs Hari Kerja
st.subheader("📅 Perbandingan Peminjaman: Hari Libur vs Hari Kerja")

# Mapping label hari
working_map = {0: 'Libur', 1: 'Hari Kerja'}
filtered_df['workingday_label'] = filtered_df['workingday'].map(working_map)

fig4, ax4 = plt.subplots()
sns.boxplot(data=filtered_df, x='workingday_label', y='cnt', palette='Set2', ax=ax4)
ax4.set_title("Distribusi Jumlah Peminjaman: Hari Kerja vs Libur")
ax4.set_xlabel("Jenis Hari")
ax4.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig4)

# Tambahan Insight Otomatis
avg_working = filtered_df.groupby('workingday_label')['cnt'].mean().to_dict()
st.markdown(f"""
**💡 Insight Tambahan:**  
- Rata-rata peminjaman pada **hari kerja**: `{avg_working.get('Hari Kerja', 0):,.0f}`  
- Rata-rata peminjaman pada **hari libur**: `{avg_working.get('Libur', 0):,.0f}`
""")

st.markdown("---")
st.info("Gunakan filter di sebelah kiri untuk mengeksplorasi data secara interaktif 🎯")
