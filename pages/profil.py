"""pages/profil.py — Halaman profil dan kalkulasi kebutuhan gizi."""

import streamlit as st
from utils.nutrition_calculator import (
    hitung_bmi, kategori_bmi, hitung_bmr, hitung_tdee, hitung_kebutuhan_nutrisi,
    FAKTOR_AKTIVITAS,
)


def show():
    st.title("👤 Profil & Kebutuhan Gizi")
    st.markdown("Isi data dirimu untuk mendapatkan kalkulasi kebutuhan nutrisi yang akurat.")

    with st.form("form_profil"):
        st.markdown("#### 📝 Data Diri")
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama", value=st.session_state.get("nama", ""))
            usia = st.number_input("Usia (tahun)", min_value=17, max_value=35, value=st.session_state.get("usia", 20))
            jenis_kelamin = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"],
                                     index=0 if st.session_state.get("jenis_kelamin", "Laki-laki") == "Laki-laki" else 1,
                                     horizontal=True)
        with c2:
            berat = st.number_input("Berat Badan (kg)", min_value=30.0, max_value=150.0,
                                    value=st.session_state.get("berat", 60.0), step=0.5)
            tinggi = st.number_input("Tinggi Badan (cm)", min_value=140.0, max_value=220.0,
                                     value=st.session_state.get("tinggi", 165.0), step=0.5)

        st.markdown("#### 🏃 Aktivitas & Tujuan")
        c3, c4 = st.columns(2)
        with c3:
            aktivitas = st.selectbox("Tingkat Aktivitas Fisik",
                                     list(FAKTOR_AKTIVITAS.keys()),
                                     index=1)
        with c4:
            tujuan = st.selectbox("Tujuan Kesehatan",
                                  ["Jaga Berat Badan", "Turunkan Berat Badan", "Naikkan Berat Badan"])

        submitted = st.form_submit_button("💾 Simpan & Hitung Kebutuhan Gizi", type="primary", use_container_width=True)

    if submitted:
        # Simpan ke session state
        st.session_state["nama"] = nama
        st.session_state["usia"] = usia
        st.session_state["jenis_kelamin"] = jenis_kelamin
        st.session_state["berat"] = berat
        st.session_state["tinggi"] = tinggi
        st.session_state["aktivitas"] = aktivitas
        st.session_state["tujuan"] = tujuan

        # Kalkulasi
        bmi = hitung_bmi(berat, tinggi)
        info_bmi = kategori_bmi(bmi)
        bmr = hitung_bmr(berat, tinggi, usia, jenis_kelamin)
        tdee = hitung_tdee(bmr, aktivitas)
        kebutuhan = hitung_kebutuhan_nutrisi(tdee, tujuan)

        st.session_state["kebutuhan"] = kebutuhan
        st.session_state["bmi"] = bmi
        st.session_state["tdee"] = tdee
        st.success("✅ Profil berhasil disimpan!")

    # Tampilkan hasil jika sudah ada data
    if "kebutuhan" in st.session_state:
        kebutuhan = st.session_state["kebutuhan"]
        bmi = st.session_state["bmi"]
        info_bmi = kategori_bmi(bmi)

        st.markdown("---")
        st.markdown("### 📊 Hasil Kalkulasi")

        # BMI
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("BMI", bmi)
        with c2:
            st.metric("Status", info_bmi["status"])
        with c3:
            st.metric("TDEE (kcal/hari)", int(st.session_state["tdee"]))

        st.info(f"💡 {info_bmi['pesan']}")

        st.markdown("#### 🎯 Kebutuhan Nutrisi Harian")
        cols = st.columns(5)
        nutrients = [
            ("🔥 Kalori", kebutuhan["kalori"], "kcal"),
            ("💪 Protein", kebutuhan["protein"], "gram"),
            ("🌾 Karbohidrat", kebutuhan["karbo"], "gram"),
            ("🫒 Lemak", kebutuhan["lemak"], "gram"),
            ("🌿 Serat", kebutuhan["serat"], "gram"),
        ]
        for col, (label, val, unit) in zip(cols, nutrients):
            with col:
                st.metric(label, f"{val} {unit}")

        # Panduan makro
        st.markdown("---")
        st.markdown("#### 📐 Distribusi Makro")
        st.markdown(f"""
        | Makronutrien | Target Harian | Per Makan (÷3) |
        |---|---|---|
        | 🔥 Kalori | {kebutuhan['kalori']} kcal | {kebutuhan['kalori']//3} kcal |
        | 💪 Protein | {kebutuhan['protein']} g | {kebutuhan['protein']//3} g |
        | 🌾 Karbohidrat | {kebutuhan['karbo']} g | {kebutuhan['karbo']//3} g |
        | 🫒 Lemak | {kebutuhan['lemak']} g | {kebutuhan['lemak']//3} g |
        | 🌿 Serat | {kebutuhan['serat']} g | {kebutuhan['serat']//3} g |
        """)
    else:
        st.info("👆 Isi formulir di atas dan klik **Simpan & Hitung** untuk melihat hasil.")
