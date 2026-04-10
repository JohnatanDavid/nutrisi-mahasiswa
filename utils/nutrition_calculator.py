"""
utils/nutrition_calculator.py
Kalkulasi kebutuhan nutrisi harian berdasarkan profil mahasiswa.
Menggunakan rumus Harris-Benedict untuk BMR dan TDEE.
"""


def hitung_bmi(berat_kg: float, tinggi_cm: float) -> float:
    """Hitung Body Mass Index."""
    tinggi_m = tinggi_cm / 100
    return round(berat_kg / (tinggi_m ** 2), 1)


def kategori_bmi(bmi: float) -> dict:
    """Kategorikan BMI dan berikan pesan."""
    if bmi < 18.5:
        return {"status": "Kurus", "warna": "status-warn",
                "pesan": "Kamu perlu menambah asupan kalori dan protein."}
    elif bmi < 25.0:
        return {"status": "Normal", "warna": "status-good",
                "pesan": "BMI kamu ideal! Pertahankan pola makan sehat."}
    elif bmi < 30.0:
        return {"status": "Gemuk", "warna": "status-warn",
                "pesan": "Disarankan mengurangi asupan lemak dan gula."}
    else:
        return {"status": "Obesitas", "warna": "status-bad",
                "pesan": "Segera konsultasi dengan ahli gizi."}


def hitung_bmr(berat_kg: float, tinggi_cm: float, usia: int, jenis_kelamin: str) -> float:
    """
    Hitung Basal Metabolic Rate (BMR) dengan rumus Harris-Benedict.
    Laki-laki : 88.362 + (13.397 × berat) + (4.799 × tinggi) − (5.677 × usia)
    Perempuan : 447.593 + (9.247 × berat) + (3.098 × tinggi) − (4.330 × usia)
    """
    if jenis_kelamin == "Laki-laki":
        bmr = 88.362 + (13.397 * berat_kg) + (4.799 * tinggi_cm) - (5.677 * usia)
    else:
        bmr = 447.593 + (9.247 * berat_kg) + (3.098 * tinggi_cm) - (4.330 * usia)
    return round(bmr, 0)


FAKTOR_AKTIVITAS = {
    "Sangat Sedentary (jarang olahraga)": 1.2,
    "Ringan (olahraga 1-3x/minggu)": 1.375,
    "Sedang (olahraga 3-5x/minggu)": 1.55,
    "Aktif (olahraga 6-7x/minggu)": 1.725,
    "Sangat Aktif (atlet/kerja fisik berat)": 1.9,
}


def hitung_tdee(bmr: float, aktivitas: str) -> float:
    """Total Daily Energy Expenditure berdasarkan aktivitas."""
    faktor = FAKTOR_AKTIVITAS.get(aktivitas, 1.375)
    return round(bmr * faktor, 0)


def hitung_kebutuhan_nutrisi(tdee: float, tujuan: str) -> dict:
    """
    Hitung kebutuhan makro harian berdasarkan TDEE dan tujuan.
    Distribusi makro mengikuti panduan gizi seimbang Indonesia (Kemenkes).
    """
    if tujuan == "Turunkan Berat Badan":
        kalori_target = tdee - 300        # defisit 300 kcal
        protein_pct = 0.30
        karbo_pct   = 0.40
        lemak_pct   = 0.30
    elif tujuan == "Naikkan Berat Badan":
        kalori_target = tdee + 300        # surplus 300 kcal
        protein_pct = 0.25
        karbo_pct   = 0.50
        lemak_pct   = 0.25
    else:  # Maintain / Jaga Berat
        kalori_target = tdee
        protein_pct = 0.25
        karbo_pct   = 0.50
        lemak_pct   = 0.25

    # 1 gram protein = 4 kcal, karbo = 4 kcal, lemak = 9 kcal
    protein_g = round((kalori_target * protein_pct) / 4, 0)
    karbo_g   = round((kalori_target * karbo_pct)   / 4, 0)
    lemak_g   = round((kalori_target * lemak_pct)   / 9, 0)
    serat_g   = 25  # rekomendasi standar (AKG Indonesia)

    return {
        "kalori": int(kalori_target),
        "protein": int(protein_g),
        "karbo":   int(karbo_g),
        "lemak":   int(lemak_g),
        "serat":   serat_g,
    }


def evaluasi_asupan(asupan: dict, kebutuhan: dict) -> dict:
    """
    Bandingkan asupan aktual vs kebutuhan, berikan status tiap nutrisi.
    Returns dict dengan persen pemenuhan dan status.
    """
    hasil = {}
    for nutrisi in ["kalori", "protein", "karbo", "lemak", "serat"]:
        target = kebutuhan.get(nutrisi, 1)
        aktual = asupan.get(nutrisi, 0)
        persen = round((aktual / target * 100), 1) if target > 0 else 0

        if persen < 70:
            status = "Kurang"
        elif persen <= 120:
            status = "Cukup"
        else:
            status = "Berlebih"

        hasil[nutrisi] = {
            "aktual": round(aktual, 1),
            "target": target,
            "persen": persen,
            "status": status,
        }
    return hasil
