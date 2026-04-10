"""pages/evaluasi_tam.py — Evaluasi sistem menggunakan Technology Acceptance Model (TAM)."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Instrumen kuesioner TAM
PERTANYAAN_PU = {
    "PU1": "Menggunakan sistem ini membantu saya memilih makanan yang lebih sehat.",
    "PU2": "Sistem ini meningkatkan kesadaran saya tentang kandungan nutrisi makanan.",
    "PU3": "Rekomendasi yang diberikan sesuai dengan kebutuhan gizi saya.",
    "PU4": "Sistem ini membantu saya merencanakan pola makan harian dengan lebih baik.",
    "PU5": "Secara keseluruhan, sistem ini berguna untuk mendukung kesehatan saya.",
}

PERTANYAAN_PEOU = {
    "PEOU1": "Tampilan antarmuka sistem ini mudah dipahami.",
    "PEOU2": "Saya tidak memerlukan bantuan orang lain untuk menggunakan sistem ini.",
    "PEOU3": "Proses memasukkan data makanan terasa mudah dan tidak membingungkan.",
    "PEOU4": "Fitur pencarian makanan dalam sistem ini mudah digunakan.",
    "PEOU5": "Secara keseluruhan, sistem ini mudah dioperasikan.",
}

SKALA = {1: "1 - Sangat Tidak Setuju", 2: "2 - Tidak Setuju", 3: "3 - Netral",
         4: "4 - Setuju", 5: "5 - Sangat Setuju"}


def show():
    st.title("📋 Evaluasi TAM — Technology Acceptance Model")
    st.markdown("""
    Evaluasi ini mengukur penerimaan sistem menggunakan kerangka **TAM (Davis, 1989)**
    yang terdiri dari dua konstruk utama:
    - **Perceived Usefulness (PU)** — Seberapa bermanfaat sistem ini?
    - **Perceived Ease of Use (PEOU)** — Seberapa mudah sistem ini digunakan?
    """)

    st.markdown("---")

    # Informasi responden
    st.markdown("### 👤 Informasi Responden")
    c1, c2, c3 = st.columns(3)
    with c1:
        nama_resp = st.text_input("Nama (opsional)", placeholder="Bisa dikosongkan")
    with c2:
        prodi = st.selectbox("Program Studi", [
            "Sistem Informasi", "Informatika", "Teknik Komputer",
            "Teknik Elektro", "Manajemen", "Lainnya"
        ])
    with c3:
        semester = st.selectbox("Semester", list(range(1, 9)))

    st.markdown("---")

    with st.form("form_tam"):
        # ===== PERCEIVED USEFULNESS =====
        st.markdown("### 🎯 A. Perceived Usefulness (Kegunaan yang Dirasakan)")
        st.caption("Seberapa setuju Anda dengan pernyataan berikut? (1=Sangat Tidak Setuju, 5=Sangat Setuju)")

        nilai_pu = {}
        for kode, pertanyaan in PERTANYAAN_PU.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{kode}.** {pertanyaan}")
            with col2:
                nilai_pu[kode] = st.select_slider(
                    f"_{kode}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: SKALA[x],
                    value=4, label_visibility="collapsed"
                )

        st.markdown("---")

        # ===== PERCEIVED EASE OF USE =====
        st.markdown("### ⚙️ B. Perceived Ease of Use (Kemudahan Penggunaan)")
        st.caption("Seberapa setuju Anda dengan pernyataan berikut?")

        nilai_peou = {}
        for kode, pertanyaan in PERTANYAAN_PEOU.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{kode}.** {pertanyaan}")
            with col2:
                nilai_peou[kode] = st.select_slider(
                    f"_{kode}", options=[1, 2, 3, 4, 5],
                    format_func=lambda x: SKALA[x],
                    value=4, label_visibility="collapsed"
                )

        submitted = st.form_submit_button("📊 Lihat Hasil Evaluasi TAM", type="primary", use_container_width=True)

    # ===== HASIL =====
    if submitted:
        rata_pu = sum(nilai_pu.values()) / len(nilai_pu)
        rata_peou = sum(nilai_peou.values()) / len(nilai_peou)

        # Simpan hasil ke session state (simulasi database)
        if "hasil_tam" not in st.session_state:
            st.session_state["hasil_tam"] = []
        st.session_state["hasil_tam"].append({
            "responden": nama_resp or "Anonim",
            "prodi": prodi,
            "semester": semester,
            "PU": round(rata_pu, 2),
            "PEOU": round(rata_peou, 2),
        })

        st.markdown("---")
        st.markdown("### 📊 Hasil Evaluasi TAM Kamu")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Perceived Usefulness", f"{rata_pu:.2f} / 5.00",
                      help="Rata-rata skor kegunaan sistem (skala 1-5)")
        with c2:
            st.metric("Perceived Ease of Use", f"{rata_peou:.2f} / 5.00",
                      help="Rata-rata skor kemudahan penggunaan (skala 1-5)")
        with c3:
            rata_total = (rata_pu + rata_peou) / 2
            st.metric("Skor TAM Total", f"{rata_total:.2f} / 5.00")

        # Interpretasi
        def interpretasi(skor):
            if skor >= 4.2:
                return "✅ Sangat Baik — Diterima dengan baik oleh pengguna"
            elif skor >= 3.4:
                return "🟡 Baik — Dapat diterima pengguna"
            elif skor >= 2.6:
                return "🟠 Cukup — Perlu peningkatan"
            else:
                return "🔴 Kurang — Perlu evaluasi menyeluruh"

        st.info(f"**PU**: {interpretasi(rata_pu)}")
        st.info(f"**PEOU**: {interpretasi(rata_peou)}")

        # Spider chart
        categories = list(PERTANYAAN_PU.keys()) + list(PERTANYAAN_PEOU.keys())
        values_pu = list(nilai_pu.values()) + [None] * 5
        values_peou = [None] * 5 + list(nilai_peou.values())

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=list(nilai_pu.values()) + [list(nilai_pu.values())[0]],
            theta=list(PERTANYAAN_PU.keys()) + [list(PERTANYAAN_PU.keys())[0]],
            fill="toself", name="Perceived Usefulness", line_color="#1a7f4b",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=list(nilai_peou.values()) + [list(nilai_peou.values())[0]],
            theta=list(PERTANYAAN_PEOU.keys()) + [list(PERTANYAAN_PEOU.keys())[0]],
            fill="toself", name="Perceived Ease of Use", line_color="#2196f3",
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True, title="Profil TAM per Indikator", height=400,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Tabel detail
        st.markdown("#### 📋 Detail Skor per Indikator")
        rows = []
        for kode, pert in PERTANYAAN_PU.items():
            rows.append({"Kode": kode, "Konstruk": "PU", "Pertanyaan": pert, "Skor": nilai_pu[kode]})
        for kode, pert in PERTANYAAN_PEOU.items():
            rows.append({"Kode": kode, "Konstruk": "PEOU", "Pertanyaan": pert, "Skor": nilai_peou[kode]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ===== REKAP SEMUA RESPONDEN =====
    if "hasil_tam" in st.session_state and len(st.session_state["hasil_tam"]) > 1:
        st.markdown("---")
        st.markdown("### 👥 Rekap Semua Responden")
        df_rekap = pd.DataFrame(st.session_state["hasil_tam"])
        st.dataframe(df_rekap, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rata-rata PU (semua)", f"{df_rekap['PU'].mean():.2f}")
        with col2:
            st.metric("Rata-rata PEOU (semua)", f"{df_rekap['PEOU'].mean():.2f}")

    st.markdown("---")
    st.caption("📚 Referensi: Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319-340.")
