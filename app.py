import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul App
st.set_page_config(page_title="Dashboard Buah", layout="wide")
st.title("🍎 Dashboard Populasi Tanaman Buah")

# Baca file langsung dari lokal (pastikan file ini ada di folder yang sama)
df = pd.read_csv("databasebuah.csv")

# Debug: tampilkan nama kolom yang tersedia
st.write("Kolom yang tersedia:", df.columns.tolist())

# Tampilkan tabel asli
st.subheader("📄 Data Asli")
st.dataframe(df)

# Gabungkan buah per responden (sesuaikan nama kolom dengan yang ada di CSV)
# Ganti nama kolom sesuai dengan yang sebenarnya ada di file CSV
df_grouped = df.groupby(df.columns[0])[df.columns[1]]\
    .apply(lambda x: ", ".join(sorted(set(x)))).reset_index()

# Tampilkan tabel gabungan
st.subheader("👨‍🌾 Buah yang Ditanam per Responden")
st.dataframe(df_grouped)

# Buat grafik populasi buah
st.subheader("📊 Grafik Populasi Tanaman per Jenis Buah")

# Set style grafik
plt.style.use('default')
sns.set_palette("husl")

# Data populasi per buah (sesuaikan nama kolom)
populasi_per_buah = df.groupby(df.columns[1])[df.columns[2]].sum().sort_values(ascending=False)

# Grafik
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(
    populasi_per_buah.index,
    populasi_per_buah.values,
    color=plt.cm.Set3(range(len(populasi_per_buah))),
    edgecolor='black',
    linewidth=0.7,
    alpha=0.8
)

# Tambahkan label jumlah di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2.,
        height + max(populasi_per_buah.values)*0.01,
        f'{int(height):,}',
        ha='center',
        va='bottom',
        fontweight='bold',
        fontsize=10
    )

# Styling
ax.set_title("Jumlah Populasi Tanaman per Jenis Buah", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Jenis Buah", fontsize=12, fontweight='bold')
ax.set_ylabel("Jumlah Populasi", fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Format angka y pakai koma
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Tampilkan di Streamlit
st.pyplot(fig)