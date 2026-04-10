"""pages/beranda.py — Halaman utama aplikasi."""

import streamlit as st


def show():
    st.markdown("""
    <div class="main-header">
        <h1>🥗 NutriMahasiswa</h1>
        <p style="font-size:1.1rem; margin:0;">Sistem Rekomendasi Pola Makan Sehat berbasis Analisis Nutrisi</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistik singkat
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total Makanan", "337", help="Jumlah item makanan dalam database")
    with col2:
        st.metric("🗂️ Kategori", "14", help="Kategori makanan tersedia")
    with col3:
        st.metric("🧬 Parameter Nutrisi", "7", help="Kalori, Protein, Karbo, Lemak, Serat, dll")
    with col4:
        st.metric("🤖 Algoritma", "Cosine Similarity", help="Content-based filtering ML")

    st.markdown("---")

    # Panduan penggunaan
    st.markdown("### 📖 Cara Menggunakan Aplikasi")

    steps = [
        ("1️⃣ Isi Profil", "👤 Profil & Kebutuhan Gizi",
         "Masukkan data diri (usia, berat, tinggi, aktivitas) untuk menghitung kebutuhan gizi harian otomatis."),
        ("2️⃣ Log Makanan", "🍽️ Log Makanan Harian",
         "Catat apa yang kamu makan hari ini. Sistem akan menghitung total nutrisi secara real-time."),
        ("3️⃣ Lihat Rekomendasi", "🎯 Rekomendasi Menu",
         "Dapatkan rekomendasi menu makan sehat yang dipersonalisasi menggunakan Machine Learning."),
        ("4️⃣ Pantau Progress", "📊 Dashboard Progress",
         "Lihat grafik perkembangan nutrisi mingguan dan evaluasi pola makanmu."),
    ]

    for title, nav, desc in steps:
        with st.container():
            c1, c2 = st.columns([1, 4])
            with c1:
                st.markdown(f"### {title}")
            with c2:
                st.info(f"**{nav}** — {desc}")

    st.markdown("---")

    # Fitur unggulan
    st.markdown("### ✨ Fitur Unggulan")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        **🤖 Machine Learning**  
        Model Content-Based Filtering menggunakan Cosine Similarity untuk merekomendasikan
        makanan yang paling sesuai kebutuhan nutrisimu.
        """)
    with f2:
        st.markdown("""
        **📊 Dashboard Real-time**  
        Visualisasi interaktif kandungan nutrisi harian dan mingguan dengan grafik
        yang mudah dipahami.
        """)
    with f3:
        st.markdown("""
        **🎯 Personal & Akurat**  
        Rekomendasi disesuaikan dengan BMI, aktivitas fisik, dan tujuan kesehatanmu
        berdasarkan rumus ilmiah (Harris-Benedict).
        """)

    st.markdown("---")
    st.caption("📚 Dataset: Nutrition Details for Most Common Foods (Kaggle) | "
               "🏫 Proyek Sistem Informasi — Universitas Brawijaya Malang")
