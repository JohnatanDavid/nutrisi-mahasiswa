# 🥗 NutriMahasiswa — Sistem Rekomendasi Pola Makan Sehat

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4%2B-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

> Sistem rekomendasi pola makan berbasis **Machine Learning (Content-Based Filtering)** yang dirancang khusus untuk mahasiswa. Menganalisis kandungan nutrisi dari 337 item makanan dan merekomendasikan menu harian yang sesuai dengan kebutuhan gizi personal.

---

## 📋 Daftar Isi
- [Demo](#-demo)
- [Fitur](#-fitur)
- [Teknologi](#-teknologi)
- [Struktur Proyek](#-struktur-proyek)
- [Cara Install & Jalankan](#-cara-install--jalankan)
- [Cara Pakai Aplikasi](#-cara-pakai-aplikasi)
- [Dataset](#-dataset)
- [Model Machine Learning](#-model-machine-learning)
- [Evaluasi TAM](#-evaluasi-tam)
- [Tim](#-tim)

---

## 🚀 Demo

> **Link Aplikasi**: [https://nutrimahasiswa.streamlit.app](https://nutrimahasiswa.streamlit.app)  
> *(Akan aktif setelah deploy ke Streamlit Cloud)*

---

## ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| 👤 Profil Gizi | Kalkulasi BMI, BMR, dan TDEE otomatis menggunakan rumus Harris-Benedict |
| 🍽️ Log Makanan | Pencatatan makanan harian dengan pencarian dari 337 item makanan |
| 🤖 Rekomendasi ML | Content-Based Filtering dengan Cosine Similarity |
| 📊 Dashboard | Visualisasi progress nutrisi harian dan mingguan (Plotly) |
| 📋 Evaluasi TAM | Kuesioner Technology Acceptance Model (PU & PEOU) |

---

## 🛠 Teknologi

- **Frontend/UI**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (MinMaxScaler, Cosine Similarity)
- **Visualisasi**: Plotly
- **Dataset**: [Nutrition Details for Most Common Foods (Kaggle)](https://www.kaggle.com/datasets/niharika41298/nutrition-details-for-most-common-foods)

---

## 📁 Struktur Proyek

```
nutrisi-mahasiswa/
│
├── app.py                    # Entry point aplikasi Streamlit
├── requirements.txt          # Daftar library Python
├── README.md
├── .gitignore
│
├── data/
│   └── nutrients.csv         # Dataset nutrisi (337 makanan)
│
├── models/
│   ├── __init__.py
│   └── recommendation_model.py  # Model ML Content-Based Filtering
│
├── pages/
│   ├── __init__.py
│   ├── beranda.py            # Halaman utama
│   ├── profil.py             # Profil & kalkulasi gizi
│   ├── log_makanan.py        # Pencatatan makanan harian
│   ├── rekomendasi.py        # Halaman rekomendasi menu
│   ├── dashboard.py          # Dashboard progress mingguan
│   └── evaluasi_tam.py       # Kuesioner & hasil TAM
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # Preprocessing dataset
│   └── nutrition_calculator.py  # Kalkulasi BMI/BMR/TDEE/kebutuhan gizi
│
└── .streamlit/
    └── config.toml           # Konfigurasi tema Streamlit
```

---

## 💻 Cara Install & Jalankan

### Prasyarat
- Python 3.10 atau lebih baru
- Git

### Langkah 1 — Clone repository
```bash
git clone https://github.com/USERNAME/nutrisi-mahasiswa.git
cd nutrisi-mahasiswa
```

### Langkah 2 — Buat virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Langkah 4 — Jalankan aplikasi
```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser: `http://localhost:8501`

---

## 📖 Cara Pakai Aplikasi

1. **Isi Profil** → Masukkan data diri (usia, berat, tinggi, aktivitas, tujuan)
2. **Log Makanan** → Cari dan tambahkan makanan yang dikonsumsi hari ini
3. **Lihat Rekomendasi** → Dapatkan menu makan sehari yang direkomendasikan AI
4. **Pantau Dashboard** → Analisis tren nutrisi 7 hari terakhir
5. **Isi Kuesioner TAM** → Berikan penilaian kemudahan dan kegunaan sistem

---

## 📊 Dataset

- **Sumber**: [Kaggle — Nutrition Details for Most Common Foods](https://www.kaggle.com/datasets/niharika41298/nutrition-details-for-most-common-foods)
- **Jumlah item**: 337 makanan
- **Kategori**: 14 kategori (Dairy, Meat, Seafood, Vegetables, Fruits, Grains, dll.)
- **Fitur nutrisi**: Kalori, Protein, Lemak, Lemak Jenuh, Serat, Karbohidrat

---

## 🤖 Model Machine Learning

Sistem menggunakan **Content-Based Filtering** dengan algoritma **Cosine Similarity**:

```
Skor Kemiripan = cos(θ) = (A · B) / (||A|| × ||B||)
```

Di mana:
- **A** = vektor kebutuhan nutrisi pengguna (target per makan)
- **B** = vektor profil nutrisi setiap makanan dalam database
- Semua fitur dinormalisasi menggunakan **MinMaxScaler** sebelum perhitungan

Makanan dengan skor kemiripan tertinggi → direkomendasikan

---

## 📋 Evaluasi TAM

Evaluasi dilakukan menggunakan kerangka **Technology Acceptance Model (Davis, 1989)**:

| Konstruk | Kode | Jumlah Indikator | Skala |
|---|---|---|---|
| Perceived Usefulness | PU1–PU5 | 5 | Likert 1–5 |
| Perceived Ease of Use | PEOU1–PEOU5 | 5 | Likert 1–5 |

**Interpretasi Skor:**
- ≥ 4.2 → Sangat Baik
- 3.4–4.1 → Baik
- 2.6–3.3 → Cukup
- < 2.6 → Kurang

---

## 👥 Tim

| Nama | NIM | Peran |
|---|---|---|
| [Nama Kamu] | [NIM] | Developer, Data Analyst |
| [Nama Anggota] | [NIM] | UI Design, Dokumentasi |

**Universitas Brawijaya — Malang**  
Program Studi: [Nama Prodi]  
Mata Kuliah: Sistem Informasi / Rekayasa Perangkat Lunak  
Tahun: 2024/2025

---

## 📄 Lisensi

Proyek ini menggunakan lisensi [MIT](LICENSE).

---

> 💡 *"Makan sehat bukan soal diet ketat, tapi soal pilihan yang tepat setiap hari."*
