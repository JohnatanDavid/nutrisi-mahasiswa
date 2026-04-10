"""
utils/data_loader.py
Modul untuk memuat dan membersihkan dataset nutrisi.
"""

import pandas as pd
import numpy as np
import re


def load_and_clean_data(filepath: str = "data/nutrients.csv") -> pd.DataFrame:
    """
    Memuat dataset nutrisi, membersihkan nilai-nilai tidak valid,
    dan mengembalikan DataFrame yang siap dipakai.
    """
    df = pd.read_csv(filepath)

    # Hapus spasi di nama kolom
    df.columns = df.columns.str.strip()

    # Kolom numerik yang akan dibersihkan
    numeric_cols = ["Grams", "Calories", "Protein", "Fat", "Sat.Fat", "Fiber", "Carbs"]

    for col in numeric_cols:
        # Hapus karakter non-numerik seperti koma, huruf, tanda 't', 'a'
        df[col] = df[col].astype(str).apply(_clean_numeric)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Hapus baris dengan terlalu banyak nilai kosong
    df = df.dropna(subset=["Food", "Calories"])

    # Isi nilai kosong dengan 0 untuk kolom nutrisi
    for col in numeric_cols:
        df[col] = df[col].fillna(0)

    # Pastikan tidak ada nilai negatif
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: max(x, 0))

    # Standarisasi nama kategori
    df["Category"] = df["Category"].str.strip()

    # Tambah kolom: protein per kalori (kualitas protein)
    df["Protein_per_Cal"] = np.where(
        df["Calories"] > 0,
        df["Protein"] / df["Calories"],
        0
    )

    # Reset index
    df = df.reset_index(drop=True)

    return df


def _clean_numeric(val: str) -> str:
    """Bersihkan string menjadi angka yang valid."""
    if pd.isna(val) or val in ["t", "a", "T", "A", "trace", "-", ""]:
        return "0"
    # Hapus koma sebagai pemisah ribuan
    val = val.replace(",", "")
    # Ambil hanya bagian numerik pertama (misal "8-44" → "8")
    match = re.search(r"[\d.]+", val)
    return match.group(0) if match else "0"


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Ringkasan rata-rata nutrisi per kategori makanan."""
    summary = df.groupby("Category").agg(
        Jumlah_Item=("Food", "count"),
        Rata_Kalori=("Calories", "mean"),
        Rata_Protein=("Protein", "mean"),
        Rata_Karbo=("Carbs", "mean"),
        Rata_Lemak=("Fat", "mean"),
        Rata_Serat=("Fiber", "mean"),
    ).round(1).reset_index()
    return summary


def get_food_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Filter makanan berdasarkan kategori."""
    return df[df["Category"] == category].copy()


def search_food(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """Cari makanan berdasarkan kata kunci (case-insensitive)."""
    mask = df["Food"].str.contains(keyword, case=False, na=False)
    return df[mask].copy()
