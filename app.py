import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul app
st.title("📊 Dashboard Tanaman Buah")

# Upload file CSV
uploaded_file = st.file_uploader("Upload file CSV kamu", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Asli")
    st.dataframe(df)

    # Hitung populasi tanaman per jenis buah
    populasi_per_buah = (
        df.groupby("Nama buah")["Jumlah Populasi Tanaman"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.subheader("🍎 Jumlah Populasi per Jenis Buah")

    # Plot cantik
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    barplot = sns.barplot(
        x="Jumlah Populasi Tanaman",
        y="Nama buah",
        data=populasi_per_buah,
        palette="viridis",
        ax=ax
    )

    for i, v in enumerate(populasi_per_buah["Jumlah Populasi Tanaman"]):
        ax.text(v + 1, i, str(v), color='black', va='center')

    ax.set_title("Jumlah Populasi Tanaman per Jenis Buah", fontsize=16, weight='bold')
    ax.set_xlabel("Jumlah Populasi")
    ax.set_ylabel("Jenis Buah")

    st.pyplot(fig)
