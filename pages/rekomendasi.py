"""pages/rekomendasi.py — Halaman rekomendasi menu sehat."""

import streamlit as st
import pandas as pd
from utils.data_loader import load_and_clean_data
from models.recommendation_model import NutritionRecommender


@st.cache_data
def get_data():
    return load_and_clean_data("data/nutrients.csv")


@st.cache_resource
def get_model():
    df = get_data()
    model = NutritionRecommender()
    model.fit(df)
    return model


def show():
    st.title("🎯 Rekomendasi Menu Sehat")
    st.markdown("Sistem akan merekomendasikan makanan terbaik berdasarkan kebutuhan nutrisimu menggunakan **Machine Learning (Content-Based Filtering)**.")

    df = get_data()
    model = get_model()

    # Cek apakah profil sudah diisi
    if "kebutuhan" not in st.session_state:
        st.warning("⚠️ Kamu belum mengisi profil! Silakan ke menu **👤 Profil & Kebutuhan Gizi** terlebih dahulu.")
        return

    kebutuhan = st.session_state["kebutuhan"]
    nama = st.session_state.get("nama", "Mahasiswa")

    st.success(f"👋 Halo, **{nama}**! Target kalori harianmu: **{kebutuhan['kalori']} kcal**")

    # Tabs: Rencana Harian vs Eksplorasi
    tab1, tab2 = st.tabs(["📅 Rencana Makan Sehari", "🔍 Eksplorasi per Kategori"])

    # ===================== TAB 1: RENCANA HARIAN =====================
    with tab1:
        st.markdown("### 🍽️ Rencana Makan Sehari yang Direkomendasikan")
        st.caption("Rekomendasi dihasilkan menggunakan Cosine Similarity — makanan dengan profil nutrisi paling mirip dengan kebutuhanmu.")

        if st.button("🔄 Generate Rekomendasi", type="primary", use_container_width=True):
            with st.spinner("🤖 Model sedang menganalisis nutrisi..."):
                rencana = model.rekomendasikan_per_waktu_makan(kebutuhan)

            _tampilkan_rencana(rencana, kebutuhan)
            st.session_state["rencana_makan"] = rencana

        elif "rencana_makan" in st.session_state:
            _tampilkan_rencana(st.session_state["rencana_makan"], kebutuhan)
        else:
            st.info("👆 Klik tombol di atas untuk mendapatkan rekomendasi menu harianmu!")

    # ===================== TAB 2: EKSPLORASI =====================
    with tab2:
        st.markdown("### 🔍 Eksplorasi Rekomendasi per Kategori")

        kategori_list = sorted(df["Category"].unique().tolist())
        col1, col2 = st.columns(2)
        with col1:
            kat_pilihan = st.selectbox("Pilih Kategori Makanan:", kategori_list)
        with col2:
            n_hasil = st.slider("Jumlah Rekomendasi:", min_value=3, max_value=15, value=5)

        if st.button("🔍 Cari Rekomendasi", type="primary"):
            hasil = model.rekomendasikan(
                kebutuhan,
                n_rekomendasi=n_hasil,
                filter_kategori=kat_pilihan,
                exclude_categories=["Drinks,Alcohol, Beverages"],
            )
            _tampilkan_tabel(hasil, f"Rekomendasi dari kategori: {kat_pilihan}")


def _tampilkan_rencana(rencana: dict, kebutuhan: dict):
    """Tampilkan rencana makan per waktu."""
    IKON = {"Sarapan": "☀️", "Makan Siang": "🌤️", "Makan Malam": "🌙"}
    total_kal = 0

    for waktu, df_rec in rencana.items():
        if df_rec is None or df_rec.empty:
            continue
        ikon = IKON.get(waktu, "🍽️")
        kal_waktu = df_rec["Calories"].sum()
        total_kal += kal_waktu

        st.markdown(f"#### {ikon} {waktu} (~{kal_waktu:.0f} kcal)")
        _tampilkan_tabel(df_rec, "")

    # Ringkasan
    st.markdown("---")
    st.markdown("#### 📊 Ringkasan Total Rencana")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Kalori", f"{total_kal:.0f} kcal",
                  delta=f"{total_kal - kebutuhan['kalori']:.0f} dari target",
                  delta_color="inverse")
    with c2:
        st.metric("Target Kalori", f"{kebutuhan['kalori']} kcal")
    with c3:
        pct = round(total_kal / kebutuhan["kalori"] * 100, 1)
        st.metric("Pemenuhan", f"{pct}%")


def _tampilkan_tabel(df_rec: pd.DataFrame, judul: str):
    """Tampilkan tabel rekomendasi dengan formatting."""
    if judul:
        st.markdown(f"**{judul}**")

    if df_rec.empty:
        st.info("Tidak ada rekomendasi untuk kriteria ini.")
        return

    # Format tabel
    df_show = df_rec[["Food", "Measure", "Calories", "Protein", "Carbs",
                       "Fat", "Fiber", "Category", "Skor_Pct"]].copy()
    df_show.columns = ["Makanan", "Porsi", "Kalori", "Protein (g)",
                       "Karbo (g)", "Lemak (g)", "Serat (g)", "Kategori", "Skor (%)"]
    df_show["Skor (%)"] = df_show["Skor (%)"].apply(lambda x: f"{x:.1f}%")

    st.dataframe(df_show, use_container_width=True, hide_index=True)
    st.caption(f"💡 Skor (%) = tingkat kesesuaian nutrisi dengan kebutuhanmu (algoritma Cosine Similarity)")
