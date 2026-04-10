import streamlit as st

st.set_page_config(
    page_title="NutriMahasiswa - Sistem Rekomendasi Pola Makan Sehat",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a7f4b 0%, #2d9e6b 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: #f8fffe;
        border: 1px solid #c3e6d4;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .recommendation-card {
        background: #ffffff;
        border-left: 4px solid #1a7f4b;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .status-good { color: #1a7f4b; font-weight: bold; }
    .status-warn { color: #e6a817; font-weight: bold; }
    .status-bad  { color: #d9534f; font-weight: bold; }
    .sidebar .sidebar-content { background: #f0faf5; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigasi
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/1a7f4b/ffffff?text=NutriMahasiswa", use_column_width=True)
    st.markdown("---")
    page = st.selectbox(
        "📌 Navigasi Menu",
        [
            "🏠 Beranda",
            "👤 Profil & Kebutuhan Gizi",
            "🍽️ Log Makanan Harian",
            "🎯 Rekomendasi Menu",
            "📊 Dashboard Progress",
            "📋 Evaluasi TAM"
        ]
    )
    st.markdown("---")
    st.markdown("**ℹ️ Tentang Aplikasi**")
    st.caption("Sistem Rekomendasi Pola Makan Sehat untuk Mahasiswa berdasarkan analisis kandungan nutrisi menggunakan Machine Learning.")

# Routing halaman
if page == "🏠 Beranda":
    from pages import beranda
    beranda.show()
elif page == "👤 Profil & Kebutuhan Gizi":
    from pages import profil
    profil.show()
elif page == "🍽️ Log Makanan Harian":
    from pages import log_makanan
    log_makanan.show()
elif page == "🎯 Rekomendasi Menu":
    from pages import rekomendasi
    rekomendasi.show()
elif page == "📊 Dashboard Progress":
    from pages import dashboard
    dashboard.show()
elif page == "📋 Evaluasi TAM":
    from pages import evaluasi_tam
    evaluasi_tam.show()
