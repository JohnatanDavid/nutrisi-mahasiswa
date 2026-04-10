"""pages/dashboard.py — Dashboard progress kesehatan mingguan."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
import random


def show():
    st.title("📊 Dashboard Progress Kesehatan")
    st.markdown("Pantau perkembangan pola makanmu secara visual.")

    if "kebutuhan" not in st.session_state:
        st.warning("⚠️ Isi profil terlebih dahulu di **👤 Profil & Kebutuhan Gizi**.")
        return

    kebutuhan = st.session_state["kebutuhan"]
    log = st.session_state.get("log_makanan", [])

    # Tabs dashboard
    tab1, tab2, tab3 = st.tabs(["📅 Harian", "📈 Mingguan", "🍰 Distribusi Nutrisi"])

    # ========== TAB 1: HARIAN ==========
    with tab1:
        st.markdown("### ⚡ Status Nutrisi Hari Ini")

        hari_ini = str(date.today())
        log_hari = [x for x in log if x.get("tanggal") == hari_ini]

        total_hari = {
            "kalori": sum(x["kalori"] for x in log_hari),
            "protein": sum(x["protein"] for x in log_hari),
            "karbo": sum(x["karbo"] for x in log_hari),
            "lemak": sum(x["lemak"] for x in log_hari),
            "serat": sum(x["serat"] for x in log_hari),
        }

        # Gauge charts
        fig = go.Figure()
        nutrisi_list = [
            ("Kalori", total_hari["kalori"], kebutuhan["kalori"], "kcal"),
            ("Protein", total_hari["protein"], kebutuhan["protein"], "g"),
            ("Karbo", total_hari["karbo"], kebutuhan["karbo"], "g"),
            ("Lemak", total_hari["lemak"], kebutuhan["lemak"], "g"),
            ("Serat", total_hari["serat"], kebutuhan["serat"], "g"),
        ]

        cols = st.columns(5)
        for col, (nama, aktual, target, unit) in zip(cols, nutrisi_list):
            pct = min(round(aktual / target * 100, 0), 100) if target > 0 else 0
            with col:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pct,
                    title={"text": nama, "font": {"size": 13}},
                    number={"suffix": "%", "font": {"size": 18}},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#1a7f4b"},
                        "steps": [
                            {"range": [0, 70], "color": "#fef3cd"},
                            {"range": [70, 100], "color": "#d4edda"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 2},
                            "thickness": 0.75,
                            "value": 100,
                        },
                    },
                ))
                fig_gauge.update_layout(height=180, margin=dict(t=30, b=10, l=10, r=10))
                col.plotly_chart(fig_gauge, use_container_width=True)

        # Tabel detail
        if log_hari:
            df_log = pd.DataFrame(log_hari)
            st.dataframe(
                df_log[["waktu", "makanan", "porsi", "kalori", "protein", "karbo", "lemak", "serat"]].rename(
                    columns={"waktu": "Waktu", "makanan": "Makanan", "porsi": "Porsi",
                             "kalori": "Kalori", "protein": "Protein", "karbo": "Karbo",
                             "lemak": "Lemak", "serat": "Serat"}
                ),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Belum ada makanan dicatat hari ini.")

    # ========== TAB 2: MINGGUAN ==========
    with tab2:
        st.markdown("### 📈 Tren Nutrisi 7 Hari Terakhir")

        # Buat data mingguan (dari log + dummy jika kurang)
        df_minggu = _buat_data_mingguan(log, kebutuhan)

        fig_line = px.line(
            df_minggu, x="tanggal", y=["kalori", "protein", "karbo", "lemak"],
            title="Asupan Nutrisi Harian (7 Hari)",
            labels={"value": "Jumlah", "variable": "Nutrisi", "tanggal": "Tanggal"},
            color_discrete_map={
                "kalori": "#1a7f4b",
                "protein": "#2196f3",
                "karbo": "#ff9800",
                "lemak": "#f44336",
            },
        )
        fig_line.add_hline(y=kebutuhan["kalori"], line_dash="dash", line_color="#1a7f4b",
                           annotation_text=f"Target Kalori ({kebutuhan['kalori']} kcal)")
        fig_line.update_layout(height=380)
        st.plotly_chart(fig_line, use_container_width=True)

        # Bar chart pemenuhan
        df_minggu["pemenuhan_pct"] = (df_minggu["kalori"] / kebutuhan["kalori"] * 100).round(1)
        fig_bar = px.bar(
            df_minggu, x="tanggal", y="pemenuhan_pct",
            title="Pemenuhan Target Kalori Harian (%)",
            color="pemenuhan_pct",
            color_continuous_scale=["#f44336", "#ff9800", "#4caf50"],
            range_color=[0, 130],
        )
        fig_bar.add_hline(y=100, line_dash="dash", line_color="gray",
                          annotation_text="100% Target")
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ========== TAB 3: DISTRIBUSI ==========
    with tab3:
        st.markdown("### 🍰 Distribusi Nutrisi Hari Ini")

        log_hari2 = [x for x in log if x.get("tanggal") == str(date.today())]

        if not log_hari2:
            st.info("Belum ada data makanan hari ini. Log makananmu dulu!")
            return

        df_log2 = pd.DataFrame(log_hari2)

        col1, col2 = st.columns(2)

        with col1:
            # Pie chart makro
            total_p = df_log2["protein"].sum() * 4   # kcal
            total_k = df_log2["karbo"].sum() * 4
            total_l = df_log2["lemak"].sum() * 9

            fig_pie = go.Figure(go.Pie(
                labels=["Protein", "Karbohidrat", "Lemak"],
                values=[total_p, total_k, total_l],
                hole=0.4,
                marker_colors=["#2196f3", "#ff9800", "#f44336"],
            ))
            fig_pie.update_layout(title="Distribusi Kalori dari Makro", height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Bar chart per kategori
            kat_summary = df_log2.groupby("kategori")["kalori"].sum().reset_index()
            kat_summary.columns = ["Kategori", "Kalori"]
            fig_kat = px.bar(
                kat_summary.sort_values("Kalori", ascending=True),
                x="Kalori", y="Kategori", orientation="h",
                title="Kalori per Kategori Makanan",
                color="Kalori",
                color_continuous_scale="Greens",
            )
            fig_kat.update_layout(height=350)
            st.plotly_chart(fig_kat, use_container_width=True)


def _buat_data_mingguan(log: list, kebutuhan: dict) -> pd.DataFrame:
    """Agregasi log per hari + isi hari kosong dengan data random realistis."""
    hari_ini = date.today()
    tanggal_list = [(hari_ini - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    rows = []
    for tgl in tanggal_list:
        log_tgl = [x for x in log if x.get("tanggal") == tgl]
        if log_tgl:
            rows.append({
                "tanggal": tgl,
                "kalori": sum(x["kalori"] for x in log_tgl),
                "protein": sum(x["protein"] for x in log_tgl),
                "karbo": sum(x["karbo"] for x in log_tgl),
                "lemak": sum(x["lemak"] for x in log_tgl),
            })
        else:
            # Data dummy untuk demo (realistis: 70-110% kebutuhan)
            faktor = random.uniform(0.70, 1.10)
            rows.append({
                "tanggal": tgl,
                "kalori": round(kebutuhan["kalori"] * faktor),
                "protein": round(kebutuhan["protein"] * faktor),
                "karbo": round(kebutuhan["karbo"] * faktor),
                "lemak": round(kebutuhan["lemak"] * faktor),
            })

    df = pd.DataFrame(rows)
    df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.strftime("%d/%m")
    return df
