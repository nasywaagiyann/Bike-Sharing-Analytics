import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Memuat dataset
day_df = pd.read_csv(r"pd.read_csv("day_data.csv") 

#Mengonversi tanggal
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
day_df.sort_values(by="dteday", inplace=True)

min_date, max_date = day_df["dteday"].min(), day_df["dteday"].max()

# ======================== STYLE DAN CSS ========================
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        h1 {text-align: center; font-size: 40px; font-weight: bold; color: #333;}
        h3 {text-align: center; font-size: 20px; font-weight: bold; color: #444;}
        .metric-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .metric-label {
            font-size: 16px;
            font-weight: bold;
            color: #555;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #222;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ======================== SIDEBAR ========================
with st.sidebar:
    st.title("Bike Sharings")
    st.image("C:\\Users\\Nasywa Agiyan Nisa\\OneDrive\\Python Test\\minimalist bicycle logo on a white background.jpg")
    st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        h1 {text-align: center; font-size: 40px; font-weight: bold; color: #333;}
        h3 {text-align: center; font-size: 20px; font-weight: bold; color: #444;}
        .stSidebar {
            background-color: #cce7ff !important;  /* Warna biru muda */
            padding: 10px;
            border-radius: 10px;
        }
        .metric-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .metric-label {
            font-size: 16px;
            font-weight: bold;
            color: #555;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #222;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
filtered_df = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]

# ======================== DASHBOARD TITLE ========================
st.markdown("<h1>Dashboard Bike Sharing</h1>", unsafe_allow_html=True)

total_rentals = filtered_df["count_cr"].sum()
avg_rentals = round(filtered_df["count_cr"].mean(), 2)

colA, colB = st.columns(2)

with colA:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Total Penyewaan</div>
            <div class="metric-value">{total_rentals:,} 🚲</div>
        </div>
    """, unsafe_allow_html=True)
    
with colB:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Rata-rata Penyewaan Harian</div>
            <div class="metric-value">{avg_rentals:,} 🚴‍♂️</div>
        </div>
    """, unsafe_allow_html=True)

# ======================== TREN PENYEWAAN SEPEDA ========================
st.markdown("<h3>Tren Penyewaan Sepeda</h3>", unsafe_allow_html=True)
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="dteday", y="count_cr", hue="year", marker="o", palette=["lightskyblue", "lightsalmon"], ax=ax1)

ax1.set_title("", fontsize=12, fontweight="bold")
ax1.set_xlabel("Tanggal", fontsize=10)
ax1.set_ylabel("Jumlah Penyewa Sepeda", fontsize=10)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.5)

st.pyplot(fig1)

# ======================== BAGIAN BAWAH: 2 GRAFIK SEJAJAR ========================
col1, col2 = st.columns(2)

# ---- GRAFIK 1: TOTAL PENYEWAAN BERDASARKAN MUSIM (KIRI) ----
with col1:
    st.markdown("<h3>Total Penyewaan Berdasarkan Musim</h3>", unsafe_allow_html=True)
    season_rentals = day_df.groupby("season")["count_cr"].sum().reset_index()

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    sns.barplot(data=season_rentals, x="season", y="count_cr", 
                palette = ["#ADD8E6", "#FFD580", "#90EE90", "#FF9999", "#D8BFD8"], ax=ax2)

    ax2.set_xlabel("Musim", fontsize=10)
    ax2.set_ylabel("Total Penyewaan Sepeda", fontsize=10)
    ax2.set_title("", fontsize=12, fontweight="bold")
    ax2.grid(axis="y", linestyle="", alpha=0.5)

    st.pyplot(fig2)


# ---- GRAFIK 2: POLA PENYEWAAN BERDASARKAN CASUAL & REGISTERED (KANAN) ----
with col2:
    st.markdown("<h3>Casual vs Registered per Hari</h3>", unsafe_allow_html=True)

    weekly_rentals = day_df.groupby("one_of_week")[["casual", "registered"]].sum().reset_index()

    # Ubah angka 0-6 menjadi nama hari
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    weekly_rentals["one_of_week"] = days

    fig3, ax3 = plt.subplots(figsize=(6, 5))

    ax3.bar(weekly_rentals["one_of_week"], weekly_rentals["casual"], 
        color="#ADD8E6", label="Casual") 

    ax3.bar(weekly_rentals["one_of_week"], weekly_rentals["registered"], 
        bottom=weekly_rentals["casual"], color="#FFD580", label="Registered") 


    ax3.set_xlabel("Hari dalam Seminggu", fontsize=10)
    ax3.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=10)
    ax3.set_title("", fontsize=12, fontweight="bold")
    ax3.legend()
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis="y", linestyle="", alpha=0.7)

    st.pyplot(fig3)

# ======================== PIE CHART & HUBUNGAN SUHU ========================
col3, col4 = st.columns(2)

with col3:
    st.markdown("<h3>Perbandingan Berdasarkan Casual vs Registered</h3>", unsafe_allow_html=True)
    rental_counts = day_df[["casual", "registered"]].sum()
    
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(rental_counts, labels=["Casual", "Registered"], autopct="%1.1f%%",
            colors=["#ADD8E6", "#FFD580"], startangle=90, wedgeprops={"edgecolor": "white"})

    ax4.set_title("", fontsize=12, fontweight="bold")
    st.pyplot(fig4)

with col4:
    st.markdown("<h3>Hubungan Suhu terhadap Penyewaan Sepeda</h3>", unsafe_allow_html=True)
    fig5, ax5 = plt.subplots(figsize=(6, 6))
    sns.scatterplot(data=day_df, x="temp", y="count_cr", alpha=0.6, ax=ax5, color="#ADD8E6")
    ax5.set_xlabel("Suhu")
    ax5.set_ylabel("Jumlah Penyewaan Sepeda")
    ax5.set_title("")
    st.pyplot(fig5)


# ======================== HUBUNGAN KECEPATAN ANGIN  ========================
col5, col6 = st.columns(2)

with col5:
    st.markdown("<h3 style='text-align:center;'>Pengaruh Kecepatan Angin</h3>", unsafe_allow_html=True)
    fig6, ax6 = plt.subplots(figsize=(3, 2))  
    sns.scatterplot(data=day_df, x="wind_speed", y="count_cr", alpha=0.6, color="#ADD8E6", ax=ax6)

    ax6.set_xlabel("Kecepatan Angin", fontsize=8)
    ax6.set_ylabel("Jumlah Penyewa", fontsize=8)
    ax6.set_title("")
    ax6.tick_params(axis='x', labelsize=7)
    ax6.tick_params(axis='y', labelsize=7)

    st.pyplot(fig6)

# ======================== JUMLAH PENYEWAAN BERDASARKAN KATEGORI ========================
with col6:
    st.markdown("<h3 style='text-align:center;'>Kategori Penyewaan Sepeda</h3>", unsafe_allow_html=True)

    if 'count_cr' in day_df.columns:
        bins = [0, 1800, 3600, 5400, 7200, 9000]
        labels = ["Sangat Rendah", "Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
        day_df['rental_category'] = pd.cut(day_df['count_cr'], bins=bins, labels=labels, right=True)

        light_palette = ["#ADD8E6", "#FFD580", "#90EE90", "#FF9999", "#D8BFD8"]

        fig7, ax7 = plt.subplots(figsize=(4, 2.5))  
        sns.countplot(data=day_df, x='rental_category', palette=light_palette, ax=ax7)

        ax7.set_xlabel("Kategori", fontsize=8)
        ax7.set_ylabel("Jumlah", fontsize=8)
        ax7.set_title("")
        ax7.tick_params(axis='x', labelsize=7)
        ax7.tick_params(axis='y', labelsize=7)

        st.pyplot(fig7)

st.caption('Copyright Nasywa Agiyan Nisa 2025')
