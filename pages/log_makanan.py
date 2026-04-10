"""pages/log_makanan.py — Halaman pencatatan makanan harian."""

import streamlit as st
import pandas as pd
from datetime import date
from utils.data_loader import load_and_clean_data, search_food
from utils.nutrition_calculator import evaluasi_asupan


@st.cache_data
def get_data():
    return load_and_clean_data("data/nutrients.csv")


def show():
    st.title("🍽️ Log Makanan Harian")
    st.markdown("Catat makananmu hari ini. Sistem akan menghitung total nutrisi secara otomatis.")

    df = get_data()

    # Inisialisasi log di session state
    if "log_makanan" not in st.session_state:
        st.session_state["log_makanan"] = []

    # === FORM TAMBAH MAKANAN ===
    with st.expander("➕ Tambah Makanan", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            keyword = st.text_input("🔍 Cari makanan", placeholder="Contoh: chicken, rice, milk...")
        with col2:
            waktu_makan = st.selectbox("Waktu Makan", ["Sarapan", "Makan Siang", "Makan Malam", "Snack"])

        if keyword:
            hasil_cari = search_food(df, keyword)
            if hasil_cari.empty:
                st.warning("Makanan tidak ditemukan. Coba kata kunci lain.")
            else:
                cols_tampil = ["Food", "Measure", "Calories", "Protein", "Carbs", "Fat", "Fiber", "Category"]
                st.dataframe(hasil_cari[cols_tampil].head(10), use_container_width=True, hide_index=True)

                food_options = hasil_cari["Food"].tolist()
                pilihan = st.selectbox("Pilih makanan:", food_options)
                porsi = st.slider("Jumlah porsi", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

                if st.button("✅ Tambahkan ke Log", type="primary"):
                    row = hasil_cari[hasil_cari["Food"] == pilihan].iloc[0]
                    entry = {
                        "tanggal": str(date.today()),
                        "waktu": waktu_makan,
                        "makanan": row["Food"],
                        "porsi": porsi,
                        "kalori": round(row["Calories"] * porsi, 1),
                        "protein": round(row["Protein"] * porsi, 1),
                        "karbo": round(row["Carbs"] * porsi, 1),
                        "lemak": round(row["Fat"] * porsi, 1),
                        "serat": round(row["Fiber"] * porsi, 1),
                        "kategori": row["Category"],
                    }
                    st.session_state["log_makanan"].append(entry)
                    st.success(f"✅ {pilihan} ({porsi} porsi) ditambahkan!")
                    st.rerun()

    st.markdown("---")

    # === LOG HARI INI ===
    log = st.session_state["log_makanan"]
    log_hari_ini = [x for x in log if x["tanggal"] == str(date.today())]

    st.markdown(f"### 📋 Log Hari Ini — {date.today().strftime('%A, %d %B %Y')}")

    if not log_hari_ini:
        st.info("Belum ada makanan yang dicatat hari ini. Tambahkan makanan di atas!")
        return

    # Tampilkan per waktu makan
    for waktu in ["Sarapan", "Makan Siang", "Makan Malam", "Snack"]:
        items = [x for x in log_hari_ini if x["waktu"] == waktu]
        if not items:
            continue

        with st.expander(f"🕐 {waktu} ({len(items)} item)", expanded=True):
            df_items = pd.DataFrame(items)
            cols_tampil = ["makanan", "porsi", "kalori", "protein", "karbo", "lemak", "serat"]
            st.dataframe(df_items[cols_tampil].rename(columns={
                "makanan": "Makanan", "porsi": "Porsi", "kalori": "Kalori (kcal)",
                "protein": "Protein (g)", "karbo": "Karbo (g)",
                "lemak": "Lemak (g)", "serat": "Serat (g)"
            }), use_container_width=True, hide_index=True)

    # === TOTAL NUTRISI HARI INI ===
    st.markdown("---")
    st.markdown("### 📊 Total Nutrisi Hari Ini")

    total = {
        "kalori": sum(x["kalori"] for x in log_hari_ini),
        "protein": sum(x["protein"] for x in log_hari_ini),
        "karbo": sum(x["karbo"] for x in log_hari_ini),
        "lemak": sum(x["lemak"] for x in log_hari_ini),
        "serat": sum(x["serat"] for x in log_hari_ini),
    }

    c1, c2, c3, c4, c5 = st.columns(5)
    metrik = [
        (c1, "🔥 Kalori", total["kalori"], "kcal"),
        (c2, "💪 Protein", total["protein"], "g"),
        (c3, "🌾 Karbo", total["karbo"], "g"),
        (c4, "🫒 Lemak", total["lemak"], "g"),
        (c5, "🌿 Serat", total["serat"], "g"),
    ]
    for col, label, val, unit in metrik:
        with col:
            st.metric(label, f"{val:.1f} {unit}")

    # Evaluasi vs kebutuhan
    if "kebutuhan" in st.session_state:
        kebutuhan = st.session_state["kebutuhan"]
        evaluasi = evaluasi_asupan(total, kebutuhan)

        st.markdown("#### 🎯 vs Kebutuhan Harian")
        for nutrisi, data in evaluasi.items():
            pct = min(data["persen"], 100)
            warna = "🟢" if data["status"] == "Cukup" else ("🟡" if data["status"] == "Kurang" else "🔴")
            st.markdown(f"{warna} **{nutrisi.capitalize()}**: {data['aktual']} / {data['target']} ({data['persen']}%) — _{data['status']}_")
            st.progress(pct / 100)
    else:
        st.info("💡 Isi profil terlebih dahulu untuk melihat evaluasi vs kebutuhan gizimu.")

    # Hapus semua log
    st.markdown("---")
    if st.button("🗑️ Hapus Semua Log Hari Ini", type="secondary"):
        st.session_state["log_makanan"] = [
            x for x in log if x["tanggal"] != str(date.today())
        ]
        st.rerun()
