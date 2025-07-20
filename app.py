import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid, GridOptionsBuilder

# pe
st.set_page_config(page_title="Dashboard Komoditas Buah", layout="wide")
st.title("Dashboard Komoditas Buah di Desa Kalisidi")

df = pd.read_csv("databasebuah.csv")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(cellStyle={"textAlign": "center"})
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, height=400)

st.subheader("📄 Data Komoditas Buah")
st.dataframe(df)

# Convert DataFrame ke HTML dengan style center
# html_table = df.to_html(index=False, classes="center-table", border=0)

# CSS untuk styling
# st.markdown("""
#     <style>
#         .center-table {
#             margin-left: auto;
#             margin-right: auto;
#             border-collapse: collapse;
#             width: 90%;
#         }
#         .center-table th, .center-table td {
#             text-align: center;
#             padding: 8px;
#             border: 1px solid #ddd;
#         }
#         .center-table tr:nth-child(even) {
#             background-color: #f9f9f9;
#         }
#         .center-table th {
#             background-color: #f0f2f6;
#             font-weight: bold;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown("### 📄 Data Asli (Rata Tengah & Rapi)")
# st.markdown(html_table, unsafe_allow_html=True)

df_grouped = df.groupby("Nama Pemilik Lahan")["Nama Buah"]\
    .apply(lambda x: ", ".join(sorted(set(x)))).reset_index()

st.subheader("👨‍🌾 Buah yang Ditanam per Responden")
st.dataframe(df_grouped)
st.subheader("📊 Grafik Populasi Tanaman per Jenis Buah")
plt.style.use('default')
sns.set_palette("husl")

df["Jumlah Populasi"] = pd.to_numeric(df["Jumlah Populasi"], errors='coerce')
populasi_per_buah = df.groupby("Nama Buah")["Jumlah Populasi"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(
    populasi_per_buah.index,
    populasi_per_buah.values,
    color=plt.cm.Set3(range(len(populasi_per_buah))),
    edgecolor='black',
    linewidth=0.7,
    alpha=0.8
)

max_value = populasi_per_buah.max()
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2.,
        height + max_value*0.01,
        f'{int(height):,}',
        ha='center',
        va='bottom',
        fontweight='bold',
        fontsize=10
    )

ax.set_title("Jumlah Populasi Tanaman per Jenis Buah", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Jenis Buah", fontsize=12, fontweight='bold')
ax.set_ylabel("Jumlah Populasi", fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)