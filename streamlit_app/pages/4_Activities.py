import streamlit as st
import pandas as pd
from utils import format_pace, load_data, STRAVA_ORANGE, STRAVA_BLUE, PLOT_BG, PAPER_BG

df = load_data()

# ── Colonnes calculées ──
df["moving_time_minutes"] = (df["moving_time_seconds"] / 60).round(1)

# ── Sidebar filtres ──
st.sidebar.header("Filtres")

dist_range = st.sidebar.slider(
    "Distance (km)",
    0.0, float(df["distance_km"].max()),
    (0.0, float(df["distance_km"].max()))
)
pace_range = st.sidebar.slider(
    "Allure (min/km)",
    float(df["pace_min_km"].min()), float(df["pace_min_km"].max()),
    (float(df["pace_min_km"].min()), float(df["pace_min_km"].max()))
)
st.sidebar.caption(f"Allure : {format_pace(pace_range[0])} → {format_pace(pace_range[1])}")

duration_range = st.sidebar.slider(
    "Durée (min)",
    0, int(df["moving_time_minutes"].max()) + 1,
    (0, int(df["moving_time_minutes"].max()) + 1)
)

# ── Filtrage ──
df_filtered = df[
    (df["distance_km"]         >= dist_range[0])      &
    (df["distance_km"]         <= dist_range[1])      &
    (df["pace_min_km"]         >= pace_range[0])      &
    (df["pace_min_km"]         <= pace_range[1])      &
    (df["moving_time_minutes"] >= duration_range[0])  &
    (df["moving_time_minutes"] <= duration_range[1])
].copy()

# ── Tableau affiché ──
df_table = df_filtered[[
    "id", "name", "day_of_week", "date_fr", "hour_fr", "hour",
    "distance_km", "pace_min_km", "moving_time_minutes",
    "total_elevation_gain_m", "suffer_score"
]].copy()

# Appliquer format_pace et fillna APRÈS avoir gardé les colonnes numériques
df_table["pace_min_km"] = df_table["pace_min_km"].apply(format_pace)
df_table["suffer_score"] = df_table["suffer_score"].fillna("N/A")

df_table = df_table.rename(columns={
    "name":                   "Sortie",
    "day_of_week":            "Jour",
    "date_fr":                "Date",
    "hour_fr":                "Heure",
    "distance_km":            "Distance (km)",
    "pace_min_km":            "Allure (min/km)",
    "moving_time_minutes":    "Durée (min)",
    "total_elevation_gain_m": "Dénivelé (m)",
    "suffer_score":           "Suffer score",
})

st.title("🏃 Liste de mes sorties")
st.caption(f"{len(df_table)} sortie(s) affichée(s)")

# Afficher sans id et sans hour (gardés pour navigation et tri)
st.dataframe(
    df_table.drop(columns=["id", "hour"]),
    use_container_width=True,
    hide_index=True
)