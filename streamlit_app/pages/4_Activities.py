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
    "id", "name", "day_of_week", "date_fr", "hour",
    "distance_km", "pace_min_km", "moving_time_minutes",
    "total_elevation_gain_m", "suffer_score"
]].copy()

st.title("🏃 Liste de mes sorties")
st.caption(f"{len(df_table)} sortie(s) affichée(s)")

st.dataframe(
    df_table.drop(columns=["id"]),
    use_container_width=True,
    hide_index=True,
    column_config={
        "name":                   st.column_config.TextColumn("Sortie"),
        "day_of_week":            st.column_config.TextColumn("Jour"),
        "date_fr":                st.column_config.TextColumn("Date"),
        "hour":                   st.column_config.NumberColumn("Heure", format="%dh00"),
        "distance_km":            st.column_config.NumberColumn("Distance (km)", format="%.2f km"),
        "pace_min_km":            st.column_config.NumberColumn("Allure (min/km)", format="%.2f"),
        "moving_time_minutes":    st.column_config.NumberColumn("Durée (min)", format="%.0f min"),
        "total_elevation_gain_m": st.column_config.NumberColumn("Dénivelé (m)", format="%.0f m"),
        "suffer_score":           st.column_config.NumberColumn("Suffer score", format="%.0f"),
    }
)