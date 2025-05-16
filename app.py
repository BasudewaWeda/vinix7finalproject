import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.preprocessing import MinMaxScaler

st.title('International Undergradute Program (IUP) Dalam Perguruan Tinggi Di Indonesia')

@st.cache_data
def load_data():
    df = pd.read_excel("miniteam_b_10.xlsx", sheet_name="dataset")
    df.set_index('No', inplace=True)

    return df

df = load_data()

st.markdown(""" 
             ## Kelompok 10 B:
            - Ida Ayu Made Putri Santiani
            - Ida Ayu Putri Widiasuari
            - Ida Ayu Tri Sabina Putri
            - Ida Bagus Gede Basudewa Weda
            """)

st.subheader('Data Mentah')
st.text('Dataset yang telah dikumpulkan memiliki ' +  str(df.shape[0]) + ' baris dan memiliki ' + str(df.shape[1]) + ' kolom')
st.dataframe(df)

st.divider()

tab1, tab2 = st.tabs(['Visualisasi Data', 'Rekomendasi Jurusan'])

with tab1:
    st.subheader('Universitas Dengan Jurusan IUP Terbanyak')
    sum_jurusan = df.groupby("PTN")['Jurusan'].count().sort_values(ascending=False).reset_index()[:10]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sum_jurusan, y="PTN", x='Jurusan', ax=ax)
    st.pyplot(fig)
    st.info('Universitas dengan **jurusan IUP terbanyak** adalah **Universitas Brawijaya** dan **Universitas Gajah Mada** dengan total **30 jurusan IUP**.')

    st.divider()

    st.subheader('Universitas Dengan Biaya UKT Dalam Negeri dan Luar Negeri Terendah')
    low_ukt_dalam = df.groupby("PTN")['UKT_Mahasiswa_Dalam_Negeri'].mean().sort_values().reset_index()[:8]
    low_ukt_luar = df.groupby("PTN")['UKT_Mahasiswa_Luar_Negeri'].mean().sort_values().reset_index()[:8]

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    sns.barplot(
        data=low_ukt_dalam,
        x='UKT_Mahasiswa_Dalam_Negeri',
        y='PTN',
        ax=axes[0],
        palette='Blues_r'
    )
    axes[0].set_title("Rata-rata UKT Dalam Negeri Termurah")
    axes[0].set_xlabel("UKT (Rp)")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    # axes[0].tick_params(axis='x', rotation=45)

    sns.barplot(
        data=low_ukt_luar,
        x='UKT_Mahasiswa_Luar_Negeri',
        y='PTN',
        ax=axes[1],
        palette='Greens_r'
    )
    axes[1].set_title("Rata-rata UKT Luar Negeri Termurah")
    axes[1].set_xlabel("UKT (Rp)")
    axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
    # axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)
    st.info("""
            **Universitas Negeri Surabaya** memiliki **rata-rata biaya UKT untuk mahasiswa dalam negeri dan mahasiswa luar negeri terendah** dengan rata-rata UKT untuk mahasiswa dalam negeri dan mahasiswa luar negeri sebesar **Rp. 12.731.250**.
            """)

    st.divider()

    st.subheader('Universitas Dengan Rata-Rata Kuota Terbesar')
    kuota_high = df.groupby("PTN")['Kuota'].mean().sort_values(ascending=False).reset_index()[:5]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=kuota_high, x="Kuota", y="PTN", ax=ax)
    st.pyplot(fig)
    st.info('Universitas dengan **rata-rata kuota terbesar** adalah **Universitas Padjajaran** dengan rata-rata kuota sebesar **42,8**.')

    st.divider()

    st.subheader('Proporsi Kuota Jurusan')
    kuota_jurusan = (df.groupby('Jurusan')['Kuota'].sum().sort_values(ascending=False))
    top_5 = kuota_jurusan.head(5)
    other_jurusan = kuota_jurusan[5:].sum()

    fig, ax = plt.subplots()
    ax.pie(top_5, labels=top_5.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)
    st.info('Jurusan **Manajemen** memiliki **proporsi kuota terbesar** yaitu **34% (440)** dari kuota keseluruhan.')

    st.divider()

    st.subheader('Jurusan Dengan Kuota Terbesar')
    top_kuota = df.copy()
    top_kuota['PTN_Jurusan'] = top_kuota['PTN'] + ' - ' + top_kuota['Jurusan']
    top_kuota = top_kuota.groupby('PTN_Jurusan')['Kuota'].sum().sort_values(ascending=False).reset_index()[:10]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_kuota, x="Kuota", y="PTN_Jurusan", ax=ax)
    ax.set_ylabel("PTN - Jurusan")
    st.pyplot(fig)
    st.info('Jurusan dengan **kuota terbesar** adalah **Jurusan Manajemen** pada **Institut Teknologi Bandung** dengan kuota sebesar **180**.')

    st.divider()

    st.subheader('Jurusan Dengan Biaya UKT Terendah')
    low_ukt = df.copy()
    low_ukt['PTN_Jurusan'] = low_ukt['PTN'] + ' - ' + low_ukt['Jurusan']

    ukt_dalam = (
        low_ukt.groupby('PTN_Jurusan')['UKT_Mahasiswa_Dalam_Negeri']
        .mean()
        .sort_values()
        .reset_index()
        .rename(columns={'UKT_Mahasiswa_Dalam_Negeri': 'UKT_Dalam'})
        .head(8)
    )

    ukt_luar = (
        low_ukt.groupby('PTN_Jurusan')['UKT_Mahasiswa_Luar_Negeri']
        .mean()
        .sort_values()
        .reset_index()
        .rename(columns={'UKT_Mahasiswa_Luar_Negeri': 'UKT_Luar'})
        .head(8)
    )

    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    sns.barplot(
        data=ukt_dalam,
        x='UKT_Dalam',
        y='PTN_Jurusan',
        ax=axes[0],
        palette='Blues_r'
    )
    axes[0].set_title("UKT Dalam Negeri")
    axes[0].set_xlabel("UKT (Rp)")
    axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"Rp {int(x):,}".replace(",", ".")))

    sns.barplot(
        data=ukt_luar,
        x='UKT_Luar',
        y='PTN_Jurusan',
        ax=axes[1],
        palette='Greens_r'
    )
    axes[1].set_title("UKT Luar Negeri")
    axes[1].set_xlabel("UKT (Rp)")
    axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"Rp {int(x):,}".replace(",", ".")))

    plt.tight_layout()
    st.pyplot(fig)
    st.info('Jurusan dengan **biaya UKT dalam negeri terendah** adalah **Sastra Jepang**, **Sastra Inggris**, **Ilmu Gizi**, dan **Ilmu Keperawatan** pada **Universitas Brawijaya** dengan biaya UKT sebesar **Rp. 9.533.550**. Jurusan dengan **biaya UKT luar negeri terendah** adalah **Pendidikan Bahasa Mandarin** pada **Universitas Negeri Surabaya** dengan biaya UKT sebesar **Rp. 11.000.000.**')


    st.divider()

    st.subheader('Korelasi Kuota Dengan Biaya UKT')
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    sns.regplot(data=df, x='UKT_Mahasiswa_Dalam_Negeri', y='Kuota', scatter_kws={"alpha": 0.6}, line_kws={"color": "red"}, ax=axes[0])
    sns.regplot(data=df, x='UKT_Mahasiswa_Luar_Negeri', y='Kuota', scatter_kws={"alpha": 0.6}, line_kws={"color": "red"}, ax=axes[1])

    plt.tight_layout()
    st.pyplot(fig)
    st.info('Banyaknya **kuota** dan besarnya **biaya UKT tidak memiliki korelasi**.')

with tab2:
    rekom_df = df.copy()
    rekom_df['Jurusan_PTN'] = rekom_df['Jurusan'] + " - " + rekom_df['PTN']

    rekom_df = (
        rekom_df.groupby('Jurusan_PTN')
        .agg({
            'Kuota': 'mean',
            'UKT_Mahasiswa_Dalam_Negeri': 'mean'
        })
        .reset_index()
    )

    scaler = MinMaxScaler()
    rekom_df[['Kuota_norm', 'UKT_norm']] = scaler.fit_transform(
        rekom_df[['Kuota', 'UKT_Mahasiswa_Dalam_Negeri']]
    )

    rekom_df['UKT_norm_inv'] = 1 - rekom_df['UKT_norm']

    st.markdown("**Preferensi Rekomendasi:**")
    st.markdown("⬅️ **Kuota Besar** — **UKT Rendah** ➡️")
    preferensi = st.slider(
        label='',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )

    kuota_weight = (100 - preferensi) / 100
    ukt_weight = preferensi / 100

    rekom_df['Skor'] = (
        kuota_weight * rekom_df['Kuota_norm'] +
        ukt_weight * rekom_df['UKT_norm_inv']
    )

    rekomendasi = rekom_df.sort_values('Skor', ascending=False).head(10)

    st.subheader("Rekomendasi Jurusan - PTN:")
    st.dataframe(
        rekomendasi[['Jurusan_PTN', 'Kuota', 'UKT_Mahasiswa_Dalam_Negeri', 'Skor']].round(2)
    )

