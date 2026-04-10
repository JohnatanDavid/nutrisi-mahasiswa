"""
models/recommendation_model.py
Model Rekomendasi Berbasis Konten (Content-Based Filtering)
menggunakan Cosine Similarity pada fitur nutrisi.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


class NutritionRecommender:
    """
    Merekomendasikan makanan berdasarkan kemiripan profil nutrisi
    dengan kebutuhan target pengguna (content-based filtering).
    """

    FITUR_NUTRISI = ["Calories", "Protein", "Carbs", "Fat", "Fiber"]

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.df = None
        self.fitur_scaled = None
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        """Latih model dengan dataset nutrisi."""
        self.df = df.copy()

        # Ambil fitur numerik
        X = self.df[self.FITUR_NUTRISI].fillna(0).values

        # Normalisasi 0-1 agar semua fitur setara
        self.fitur_scaled = self.scaler.fit_transform(X)
        self.is_fitted = True
        return self

    def rekomendasikan(
        self,
        kebutuhan: dict,
        n_rekomendasi: int = 5,
        exclude_categories: list = None,
        filter_kategori: str = None,
    ) -> pd.DataFrame:
        """
        Rekomendasikan makanan paling cocok berdasarkan target nutrisi.

        Parameters
        ----------
        kebutuhan : dict  — {kalori, protein, karbo, lemak, serat}
        n_rekomendasi : int — jumlah rekomendasi yang dikembalikan
        exclude_categories : list — kategori yang diabaikan
        filter_kategori : str — hanya tampilkan kategori ini (opsional)

        Returns
        -------
        pd.DataFrame dengan kolom tambahan Skor_Kemiripan dan Skor_Pct
        """
        if not self.is_fitted:
            raise RuntimeError("Model belum dilatih. Panggil fit() terlebih dahulu.")

        # Buat vektor target dari kebutuhan per-makan (bagi 3 untuk 3x makan)
        target_vector = np.array([[
            kebutuhan.get("kalori", 600) / 3,
            kebutuhan.get("protein", 50)  / 3,
            kebutuhan.get("karbo",   150) / 3,
            kebutuhan.get("lemak",   45)  / 3,
            kebutuhan.get("serat",   25)  / 3,
        ]])

        # Normalisasi vektor target menggunakan scaler yang sudah di-fit
        target_scaled = self.scaler.transform(target_vector)

        # Hitung cosine similarity antara target dan semua makanan
        skor = cosine_similarity(target_scaled, self.fitur_scaled)[0]

        df_hasil = self.df.copy()
        df_hasil["Skor_Kemiripan"] = skor
        df_hasil["Skor_Pct"] = (skor * 100).round(1)

        # Filter kategori jika diminta
        if filter_kategori:
            df_hasil = df_hasil[df_hasil["Category"] == filter_kategori]

        # Abaikan kategori tertentu (misal minuman beralkohol)
        if exclude_categories:
            df_hasil = df_hasil[~df_hasil["Category"].isin(exclude_categories)]

        # Urutkan dan ambil top-N
        df_hasil = df_hasil.sort_values("Skor_Kemiripan", ascending=False)
        df_hasil = df_hasil.head(n_rekomendasi)

        # Kolom yang ditampilkan
        cols = ["Food", "Measure", "Calories", "Protein", "Carbs",
                "Fat", "Fiber", "Category", "Skor_Pct"]
        return df_hasil[cols].reset_index(drop=True)

    def rekomendasikan_per_waktu_makan(self, kebutuhan: dict) -> dict:
        """
        Buat rencana makan sehari: Sarapan, Makan Siang, Makan Malam.
        Masing-masing mengutamakan kategori yang berbeda.
        """
        EXCLUDE = ["Drinks,Alcohol, Beverages", "Jams, Jellies", "Desserts, sweets"]

        # Sarapan: prioritaskan karbohidrat & serat (sereal, buah, susu)
        sarapan_cat = ["Breads, cereals, fastfood,grains", "Fruits A-F",
                       "Fruits G-P", "Fruits R-Z", "Dairy products"]
        sarapan = self._rekomendasikan_dari_kategori(kebutuhan, sarapan_cat, EXCLUDE, n=3)

        # Makan siang: protein tinggi (daging, ikan, kacang)
        siang_cat = ["Meat, Poultry", "Fish, Seafood", "Seeds and Nuts",
                     "Vegetables F-P", "Vegetables A-E"]
        siang = self._rekomendasikan_dari_kategori(kebutuhan, siang_cat, EXCLUDE, n=4)

        # Makan malam: seimbang, lebih rendah kalori
        malam_cat = ["Vegetables A-E", "Vegetables F-P", "Vegetables R-Z",
                     "Fish, Seafood", "Soups"]
        malam = self._rekomendasikan_dari_kategori(kebutuhan, malam_cat, EXCLUDE, n=3)

        return {"Sarapan": sarapan, "Makan Siang": siang, "Makan Malam": malam}

    def _rekomendasikan_dari_kategori(
        self, kebutuhan, kategori_list, exclude, n
    ) -> pd.DataFrame:
        """Helper: rekomendasikan dari subset kategori tertentu."""
        df_sub = self.df[self.df["Category"].isin(kategori_list)].copy()
        if df_sub.empty:
            return self.rekomendasikan(kebutuhan, n_rekomendasi=n, exclude_categories=exclude)

        # Buat sub-scaler untuk subset ini
        sub_scaler = MinMaxScaler()
        X_sub = df_sub[self.FITUR_NUTRISI].fillna(0).values
        X_sub_scaled = sub_scaler.fit_transform(X_sub)

        target_vector = np.array([[
            kebutuhan.get("kalori", 600) / 3,
            kebutuhan.get("protein", 50)  / 3,
            kebutuhan.get("karbo",   150) / 3,
            kebutuhan.get("lemak",   45)  / 3,
            kebutuhan.get("serat",   25)  / 3,
        ]])
        target_scaled = sub_scaler.transform(target_vector)

        skor = cosine_similarity(target_scaled, X_sub_scaled)[0]
        df_sub = df_sub.copy()
        df_sub["Skor_Pct"] = (skor * 100).round(1)
        df_sub = df_sub.sort_values("Skor_Pct", ascending=False).head(n)

        cols = ["Food", "Measure", "Calories", "Protein", "Carbs",
                "Fat", "Fiber", "Category", "Skor_Pct"]
        return df_sub[cols].reset_index(drop=True)
